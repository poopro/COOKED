"""
购买意愿评估服务（Purchase Intent Evaluator）

設計理念：
1. 5 維度敏感度（說服力 / 信任 / 情感共鳴 / 社會認同 / 急迫感）是
   每個 AI Agent 的「**內部隱藏屬性**」，不直接放在前台首屏。
2. 最終 BUY/REJECT 決策同時參考兩件事：
   - (a) 內部 5 維 meter（這個 agent 對哪些訴求最買單）
   - (b) Info Plaza / Topic Community 模擬結果
        （這個 agent 在社群上看過/做過/被影響過什麼）
3. 同時把所有 agent 切成「目標客群 (Target Audience)」與「路人 (Non-Target)」，
   讓使用者看到兩群人對廣告的反應差異。

輸出包含：
- 整體購買率 / TA 購買率 / 路人購買率
- 「為什麼會買 / 為什麼不買」的歸因 % 拆解
- 每個 persona 的 BUY/REJECT、一句話原因、隱藏 5 維度雷達

注意：本檔案只跟 LLM 對話，不跟 OASIS 沙盒互動。
從沙盒拿資料是透過 SimulationManager + SimulationRunner.get_all_actions()。
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from ..config import Config
from ..utils.llm_client import LLMClient
from ..utils.logger import get_logger
from .simulation_manager import SimulationManager
from .simulation_runner import SimulationRunner, AgentAction

logger = get_logger("mirofish.purchase_intent")


# ============================================================================
# 常數
# ============================================================================

# 5 個內部心理維度
PSYCH_DIMENSIONS = [
    "persuasiveness",       # 說服力（理性訴求）敏感度
    "trust",                # 信任度（品牌/權威）敏感度
    "emotional_resonance",  # 情感共鳴敏感度
    "social_proof",         # 社會認同 / 從眾性
    "urgency",              # 急迫感 / 限時優惠反應
]

DIMENSION_LABEL_ZH = {
    "persuasiveness":      "說服力",
    "trust":               "信任度",
    "emotional_resonance": "情感共鳴",
    "social_proof":        "社會認同",
    "urgency":             "急迫感",
}

# 結果儲存檔名
RESULT_FILENAME = "purchase_intent.json"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class HiddenPsychProfile:
    """每個 agent 的內部心理 meter（不顯眼於主畫面）"""
    persuasiveness: int = 5       # 0–10
    trust: int = 5
    emotional_resonance: int = 5
    social_proof: int = 5
    urgency: int = 5
    price_sensitivity: int = 5    # 0=不在乎價格, 10=極價格敏感
    skepticism_baseline: int = 5  # 0=很容易相信, 10=極度懷疑
    summary: str = ""             # 一句話描述「他最容易被什麼說服」

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SimSignals:
    """這位 agent 在 Info Plaza / Topic Community 的關鍵訊號"""
    total_actions: int = 0
    posts_created: int = 0
    comments_created: int = 0
    likes_given: int = 0
    follows: int = 0
    own_posts_excerpt: List[str] = field(default_factory=list)  # 自己寫的關鍵內容
    own_comments_excerpt: List[str] = field(default_factory=list)
    activity_level: str = "low"   # low / medium / high
    # 用於 LLM 輸入的純文字摘要
    text_summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PersonaPurchaseResult:
    """每個 persona 的最終評估結果"""
    user_id: int
    name: str
    user_name: str
    age: Optional[int]
    profession: Optional[str]
    is_target_audience: bool
    target_match_reason: str

    hidden_profile: Dict[str, Any]
    sim_signals: Dict[str, Any]

    decision: str           # BUY or REJECT
    confidence: int         # 0–100
    one_line_reason: str    # 為什麼會 / 不會買
    main_drivers: List[str] # 主要驅動因子（用維度名）
    main_barriers: List[str]
    suggestion: str         # 給品牌方的改進建議

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# 主類別
# ============================================================================

class PurchaseIntentEvaluator:
    """
    執行流程：
        1. 從 simulation 拿 personas 和 actions
        2. 對每個 persona 並行（實際上是序列+sleep 防 rate limit）跑：
           a. LLM 推導 hidden 5 維 + 2 輔助維（一次呼叫）
           b. LLM 判斷是否為 TA（一次呼叫）
           c. LLM 結合產品+廣告+ hidden meter + 社群訊號 → BUY/REJECT（一次呼叫）
        3. 聚合：總體買單率、TA 買單率、Non-TA 買單率、歸因 %
        4. 寫到 simulation_dir/purchase_intent.json
    """

    # 為了避免一個 agent 跑 3 次 LLM 太慢，把 (a)+(b) 合成一次 batched call
    LLM_CALL_DELAY_SEC = 1.2

    def __init__(self):
        self.llm = LLMClient()
        self.manager = SimulationManager()

    # ---------- 公開入口 ----------

    def run(
        self,
        simulation_id: str,
        product_desc: str,
        ad_copy: str,
        target_audience_criteria: str,
        sample_size: Optional[int] = None,
        progress_cb: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """
        Args:
            simulation_id: 模擬 ID
            product_desc: 產品描述
            ad_copy: 廣告文案（要評估的內容）
            target_audience_criteria: 目標客群描述
            sample_size: 評估幾位 personas（None=全部）。預設 12 個避免太慢。
            progress_cb: callback(percent, message) 用於回報進度
        """
        if not product_desc or not product_desc.strip():
            raise ValueError("product_desc 不可為空")
        if not ad_copy or not ad_copy.strip():
            raise ValueError("ad_copy 不可為空")

        def _progress(p: int, msg: str):
            if progress_cb:
                try:
                    progress_cb(p, msg)
                except Exception:
                    pass
            logger.info(f"[purchase_intent {simulation_id}] {p}% {msg}")

        # --- 1. 載入 personas ---
        personas = self._load_personas(simulation_id)
        if not personas:
            raise ValueError("此模擬尚未生成 agent profiles，無法評估購買意願。")

        # 控制樣本大小，避免每次都跑 30+ 次 LLM
        if sample_size is None:
            sample_size = min(12, len(personas))
        sample_size = max(1, min(sample_size, len(personas)))
        if sample_size < len(personas):
            personas = personas[:sample_size]
        _progress(5, f"載入 {len(personas)} 位 agent，準備分析")

        # --- 2. 載入 actions（給社群訊號用） ---
        all_actions = self._load_actions(simulation_id)
        action_index = self._index_actions_by_user(all_actions)
        _progress(10, f"取得 {len(all_actions)} 筆社群動作")

        # --- 3. 逐位 persona 跑評估 ---
        results: List[PersonaPurchaseResult] = []
        per_persona_pct = 80 / max(1, len(personas))

        for idx, persona in enumerate(personas):
            uid = persona.get("user_id")
            name = persona.get("name") or persona.get("user_name") or f"Agent{uid}"
            try:
                _progress(int(10 + idx * per_persona_pct),
                          f"分析 {name} ({idx+1}/{len(personas)})")

                # 3a. 一次性產生 hidden profile + TA 分類（batched）
                hidden, is_target, ta_reason = self._step_profile_and_ta(
                    persona, target_audience_criteria
                )
                time.sleep(self.LLM_CALL_DELAY_SEC)

                # 3b. 整理社群訊號
                sig = self._extract_sim_signals(uid, action_index.get(uid, []))

                # 3c. 整合決策
                decision_result = self._step_purchase_decision(
                    persona, hidden, sig, product_desc, ad_copy
                )
                time.sleep(self.LLM_CALL_DELAY_SEC)

                results.append(PersonaPurchaseResult(
                    user_id=uid,
                    name=name,
                    user_name=persona.get("user_name", ""),
                    age=persona.get("age"),
                    profession=persona.get("profession"),
                    is_target_audience=is_target,
                    target_match_reason=ta_reason,
                    hidden_profile=hidden.to_dict(),
                    sim_signals=sig.to_dict(),
                    decision=decision_result.get("decision", "REJECT"),
                    confidence=int(decision_result.get("confidence", 50)),
                    one_line_reason=decision_result.get("one_line_reason", ""),
                    main_drivers=decision_result.get("main_drivers", []),
                    main_barriers=decision_result.get("main_barriers", []),
                    suggestion=decision_result.get("suggestion", ""),
                ))
            except Exception as e:
                logger.warning(f"persona {name} 評估失敗: {e}")
                # 失敗也塞個 placeholder，免得整體塌掉
                results.append(PersonaPurchaseResult(
                    user_id=uid,
                    name=name,
                    user_name=persona.get("user_name", ""),
                    age=persona.get("age"),
                    profession=persona.get("profession"),
                    is_target_audience=False,
                    target_match_reason=f"評估失敗：{e}",
                    hidden_profile=HiddenPsychProfile().to_dict(),
                    sim_signals=SimSignals().to_dict(),
                    decision="REJECT",
                    confidence=0,
                    one_line_reason=f"評估失敗：{str(e)[:120]}",
                    main_drivers=[],
                    main_barriers=["evaluation_error"],
                    suggestion="",
                ))

        _progress(92, "聚合結果中...")

        # --- 4. 聚合 ---
        aggregated = self._aggregate(results)

        # --- 5. 持久化 ---
        payload = {
            "simulation_id": simulation_id,
            "evaluated_at": datetime.utcnow().isoformat() + "Z",
            "model": Config.LLM_MODEL_NAME,
            "input": {
                "product_desc": product_desc,
                "ad_copy": ad_copy,
                "target_audience_criteria": target_audience_criteria,
                "sample_size": len(results),
            },
            "summary": aggregated,
            "personas": [r.to_dict() for r in results],
        }
        self._save_result(simulation_id, payload)

        _progress(100, "完成")
        return payload

    # ---------- step (a)+(b)：hidden profile + TA 分類 ----------

    def _step_profile_and_ta(
        self, persona: Dict[str, Any], ta_criteria: str
    ) -> Tuple[HiddenPsychProfile, bool, str]:
        bio = persona.get("bio") or ""
        persona_text = persona.get("persona") or ""
        age = persona.get("age")
        gender = persona.get("gender")
        profession = persona.get("profession") or persona.get("source_entity_type") or ""
        topics = persona.get("interested_topics") or []

        sys_prompt = (
            "你是消費者心理畫像分析師。"
            "我會給你一位 agent 的人設與目標客群定義。請輸出 JSON："
            "1) 推估這位 agent 對 5 大廣告心理維度（說服力 persuasiveness、"
            "信任 trust、情感共鳴 emotional_resonance、社會認同 social_proof、"
            "急迫感 urgency）的敏感度分數（0–10，10=極敏感）。"
            "2) 額外輸出 price_sensitivity 與 skepticism_baseline（0–10）。"
            "3) 用一句話 summary 描述「他最容易被什麼說服」。"
            "4) 判斷他是否屬於目標客群 is_target（true/false），"
            "以及 target_match_reason（一句話）。"
            "嚴格只回 JSON。"
        )
        user_prompt = (
            f"## Agent 人設\n"
            f"姓名: {persona.get('name')}\n"
            f"年齡/性別: {age} / {gender}\n"
            f"職業: {profession}\n"
            f"興趣主題: {', '.join(topics) if topics else '無'}\n"
            f"Bio: {bio}\n"
            f"性格描述: {persona_text}\n"
            f"\n## 目標客群定義\n{ta_criteria}\n"
            "\n請輸出 JSON 結構：\n"
            "{\n"
            '  "hidden_profile": {"persuasiveness":int,"trust":int,'
            '"emotional_resonance":int,"social_proof":int,"urgency":int,'
            '"price_sensitivity":int,"skepticism_baseline":int,"summary":"..."},\n'
            '  "is_target": bool,\n'
            '  "target_match_reason": "..."\n'
            "}"
        )
        data = self.llm.chat_json(
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=600,
        )

        hp_raw = data.get("hidden_profile", {}) or {}
        hp = HiddenPsychProfile(
            persuasiveness=self._clip(hp_raw.get("persuasiveness", 5)),
            trust=self._clip(hp_raw.get("trust", 5)),
            emotional_resonance=self._clip(hp_raw.get("emotional_resonance", 5)),
            social_proof=self._clip(hp_raw.get("social_proof", 5)),
            urgency=self._clip(hp_raw.get("urgency", 5)),
            price_sensitivity=self._clip(hp_raw.get("price_sensitivity", 5)),
            skepticism_baseline=self._clip(hp_raw.get("skepticism_baseline", 5)),
            summary=str(hp_raw.get("summary", ""))[:200],
        )
        is_target = bool(data.get("is_target", False))
        ta_reason = str(data.get("target_match_reason", ""))[:200]
        return hp, is_target, ta_reason

    # ---------- step (c)：BUY/REJECT 決策 ----------

    def _step_purchase_decision(
        self,
        persona: Dict[str, Any],
        hidden: HiddenPsychProfile,
        signals: SimSignals,
        product_desc: str,
        ad_copy: str,
    ) -> Dict[str, Any]:
        sys_prompt = (
            "你是「購買決策模擬器」。給定一位消費者的：\n"
            "1) 公開人設\n"
            "2) 內部隱藏心理 meter（5 大維度 + 2 輔助）\n"
            "3) 在社群（Info Plaza / Topic Community）上的真實行為紀錄\n"
            "4) 一個產品 + 一份廣告文案\n"
            "請站在這位消費者的立場，綜合評估會不會購買。\n"
            "重點：BUY/REJECT 必須**同時參考內部 meter 與社群行為**。"
            "例如：說服力 meter 高 + 社群上他自己已經發過正面評價 = 強烈 BUY；"
            "信任 meter 低 + 社群上看過很多負評 = 強烈 REJECT。\n"
            "main_drivers / main_barriers 必須從以下選項挑（可多選 1–3 個）：\n"
            "['persuasiveness','trust','emotional_resonance','social_proof','urgency',"
            "'price_sensitivity','social_buzz_positive','social_buzz_negative',"
            "'own_engagement','no_engagement','skepticism','brand_familiarity']\n"
            "嚴格只回 JSON。"
        )
        bio = persona.get("bio") or ""
        user_prompt = (
            f"## 消費者公開人設\n"
            f"姓名: {persona.get('name')} ({persona.get('age')}歲, "
            f"{persona.get('profession') or '-'})\n"
            f"Bio: {bio}\n"
            f"\n## 內部心理 meter (0–10)\n"
            f"- 說服力敏感度: {hidden.persuasiveness}\n"
            f"- 信任偏好: {hidden.trust}\n"
            f"- 情感共鳴: {hidden.emotional_resonance}\n"
            f"- 社會認同（從眾性）: {hidden.social_proof}\n"
            f"- 急迫感反應: {hidden.urgency}\n"
            f"- 價格敏感度: {hidden.price_sensitivity}\n"
            f"- 懷疑基礎值: {hidden.skepticism_baseline}\n"
            f"- 心理摘要: {hidden.summary}\n"
            f"\n## 在社群上的行為（Info Plaza / Topic Community）\n"
            f"{signals.text_summary or '（這位 agent 在模擬中沒有明顯活動）'}\n"
            f"\n## 產品\n{product_desc}\n"
            f"\n## 廣告文案\n{ad_copy}\n"
            f"\n請輸出 JSON：\n"
            "{\n"
            '  "decision": "BUY" 或 "REJECT",\n'
            '  "confidence": 0–100,\n'
            '  "one_line_reason": "一句話從消費者第一人稱解釋理由（中文）",\n'
            '  "main_drivers": ["最多3個維度"],\n'
            '  "main_barriers": ["最多3個維度"],\n'
            '  "suggestion": "給品牌方一句改進建議"\n'
            "}"
        )
        data = self.llm.chat_json(
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.6,
            max_tokens=600,
        )
        # 正規化
        decision = str(data.get("decision", "REJECT")).upper()
        if decision not in ("BUY", "REJECT"):
            decision = "REJECT"
        data["decision"] = decision
        data["confidence"] = self._clip(data.get("confidence", 50), lo=0, hi=100)
        return data

    # ---------- 聚合 ----------

    def _aggregate(self, results: List[PersonaPurchaseResult]) -> Dict[str, Any]:
        n = len(results)
        if n == 0:
            return {
                "total": 0,
                "buy_rate": 0,
                "target": {"count": 0, "buyers": 0, "buy_rate": 0},
                "non_target": {"count": 0, "buyers": 0, "buy_rate": 0},
                "avg_confidence": 0,
                "drivers_attribution_pct": [],
                "barriers_attribution_pct": [],
                "hidden_meter_avg": {d: 0 for d in PSYCH_DIMENSIONS},
            }
        buyers = [r for r in results if r.decision == "BUY"]
        target = [r for r in results if r.is_target_audience]
        non_target = [r for r in results if not r.is_target_audience]

        def _rate(group):
            if not group:
                return 0
            return round(100.0 * sum(1 for r in group if r.decision == "BUY") / len(group), 1)

        # 歸因 %
        drv_count: Dict[str, int] = {}
        bar_count: Dict[str, int] = {}
        for r in results:
            for d in r.main_drivers:
                drv_count[d] = drv_count.get(d, 0) + 1
            for b in r.main_barriers:
                bar_count[b] = bar_count.get(b, 0) + 1
        drv_total = sum(drv_count.values()) or 1
        bar_total = sum(bar_count.values()) or 1
        drivers_pct = sorted(
            [{"key": k, "count": v, "pct": round(100.0 * v / drv_total, 1)}
             for k, v in drv_count.items()],
            key=lambda x: x["count"], reverse=True,
        )
        barriers_pct = sorted(
            [{"key": k, "count": v, "pct": round(100.0 * v / bar_total, 1)}
             for k, v in bar_count.items()],
            key=lambda x: x["count"], reverse=True,
        )

        # 隱藏 meter 平均（給雷達圖）
        meter_avg = {}
        for d in PSYCH_DIMENSIONS:
            meter_avg[d] = round(
                sum(r.hidden_profile.get(d, 0) for r in results) / n, 1
            )

        return {
            "total": n,
            "buyers": len(buyers),
            "buy_rate": _rate(results),
            "target": {
                "count": len(target),
                "buyers": sum(1 for r in target if r.decision == "BUY"),
                "buy_rate": _rate(target),
            },
            "non_target": {
                "count": len(non_target),
                "buyers": sum(1 for r in non_target if r.decision == "BUY"),
                "buy_rate": _rate(non_target),
            },
            "avg_confidence": round(sum(r.confidence for r in results) / n, 1),
            "drivers_attribution_pct": drivers_pct,
            "barriers_attribution_pct": barriers_pct,
            "hidden_meter_avg": meter_avg,
        }

    # ---------- 載入器 ----------

    def _load_personas(self, simulation_id: str) -> List[Dict[str, Any]]:
        # Reddit profiles 是 JSON list，最方便。Twitter 是 CSV。
        sim_dir = os.path.join(Config.OASIS_SIMULATION_DATA_DIR, simulation_id)
        for fname in ("reddit_profiles.json", "twitter_profiles.json"):
            p = os.path.join(sim_dir, fname)
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list) and data:
                            return data
                except Exception as e:
                    logger.warning(f"讀取 {fname} 失敗: {e}")
        # fallback: 透過 manager
        try:
            return self.manager.get_profiles(simulation_id, platform="reddit")
        except Exception:
            return []

    def _load_actions(self, simulation_id: str) -> List[AgentAction]:
        try:
            return SimulationRunner.get_all_actions(simulation_id=simulation_id)
        except Exception as e:
            logger.warning(f"讀取 actions 失敗（可能模擬還未跑）: {e}")
            return []

    def _index_actions_by_user(
        self, actions: List[AgentAction]
    ) -> Dict[int, List[AgentAction]]:
        idx: Dict[int, List[AgentAction]] = {}
        for a in actions:
            idx.setdefault(a.agent_id, []).append(a)
        return idx

    # ---------- 社群訊號摘要 ----------

    def _extract_sim_signals(
        self, user_id: int, actions: List[AgentAction]
    ) -> SimSignals:
        sig = SimSignals()
        sig.total_actions = len(actions)
        if not actions:
            sig.text_summary = "（此 agent 在本次模擬中沒有公開動作）"
            return sig

        for a in actions:
            t = a.action_type
            args = a.action_args or {}
            if t == "CREATE_POST":
                sig.posts_created += 1
                content = args.get("content") or args.get("text") or ""
                if content:
                    sig.own_posts_excerpt.append(content[:200])
            elif t == "CREATE_COMMENT":
                sig.comments_created += 1
                content = args.get("content") or args.get("text") or ""
                if content:
                    sig.own_comments_excerpt.append(content[:200])
            elif t in ("LIKE_POST", "UPVOTE_POST"):
                sig.likes_given += 1
            elif t == "FOLLOW":
                sig.follows += 1

        if sig.total_actions <= 2:
            sig.activity_level = "low"
        elif sig.total_actions <= 8:
            sig.activity_level = "medium"
        else:
            sig.activity_level = "high"

        # 限制文本長度，避免 LLM token 爆炸
        posts_block = "\n".join(f"- 「{p}」" for p in sig.own_posts_excerpt[:3])
        comments_block = "\n".join(f"- 「{c}」" for c in sig.own_comments_excerpt[:3])
        sig.text_summary = (
            f"活躍度: {sig.activity_level}（共 {sig.total_actions} 個動作）\n"
            f"自發貼文: {sig.posts_created} 則，自發評論: {sig.comments_created} 則，"
            f"按讚: {sig.likes_given} 次，追蹤: {sig.follows} 人。\n"
            + (f"自己最近寫的貼文：\n{posts_block}\n" if posts_block else "")
            + (f"自己最近的評論：\n{comments_block}" if comments_block else "")
        )
        return sig

    # ---------- 寫入 / 讀取結果 ----------

    def _save_result(self, simulation_id: str, payload: Dict[str, Any]) -> str:
        sim_dir = os.path.join(Config.OASIS_SIMULATION_DATA_DIR, simulation_id)
        os.makedirs(sim_dir, exist_ok=True)
        path = os.path.join(sim_dir, RESULT_FILENAME)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        logger.info(f"購買意願結果已寫入 {path}")
        return path

    @classmethod
    def load_saved_result(cls, simulation_id: str) -> Optional[Dict[str, Any]]:
        path = os.path.join(
            Config.OASIS_SIMULATION_DATA_DIR, simulation_id, RESULT_FILENAME
        )
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"讀取既有 purchase_intent.json 失敗: {e}")
            return None

    # ---------- 工具 ----------

    @staticmethod
    def _clip(val: Any, lo: int = 0, hi: int = 10) -> int:
        try:
            v = int(val)
        except Exception:
            return lo
        return max(lo, min(hi, v))
