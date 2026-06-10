"""
LLM 費用粗估服務（OpenRouter 為主，OpenAI 介面相容）

功能：
1. 讀取 simulation_config.json 中的 time_config / agent_configs
2. 模擬 run_parallel_simulation.py 主迴圈會發生的「決策呼叫」次數
3. 結合每次呼叫的 token 量級（範圍）與模型單價，給出 USD 區間
4. 推薦更便宜 / 更高品質的模型清單，並用相同參數試算費用

設計重點：
- 主要面向 OpenRouter 上的 OpenAI 相容模型 ID（如 openai/gpt-4o-mini）
- 若使用者只填 "gpt-4o-mini" 也能找到對應價格
- 即時報價失敗時自動退回內建參考單價（fallback_static）
- 回傳結構與 frontend/src/components/Step2EnvSetup.vue 中的 cost-estimate-panel 對齊
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import httpx

from ..config import Config
from ..utils.logger import get_logger

logger = get_logger("mirofish.cost.estimator")


# ----------------------------------------------------------------------------
# 模型推薦清單與內建參考單價（USD per 1M tokens）
# 內建為 fallback，OpenRouter 即時報價成功時會優先使用
# ----------------------------------------------------------------------------

# 結構：id -> {"name": str, "input": float, "output": float, "tier": "cheap"|"premium"|"balanced"}
# input/output：每 1,000,000 tokens 的美金價格
KNOWN_MODELS: Dict[str, Dict[str, Any]] = {
    # ===== 便宜（推薦給 demo / 大量並發）=====
    "google/gemini-flash-1.5": {
        "name": "Gemini Flash 1.5",
        "input": 0.075,
        "output": 0.30,
        "tier": "cheap",
    },
    "google/gemini-2.0-flash-001": {
        "name": "Gemini 2.0 Flash",
        "input": 0.10,
        "output": 0.40,
        "tier": "cheap",
    },
    "google/gemini-2.5-flash-lite": {
        "name": "Gemini 2.5 Flash Lite",
        "input": 0.10,
        "output": 0.40,
        "tier": "cheap",
    },
    "google/gemini-2.5-flash": {
        "name": "Gemini 2.5 Flash",
        "input": 0.30,
        "output": 2.50,
        "tier": "balanced",
    },
    "meta-llama/llama-3.1-8b-instruct": {
        "name": "Llama 3.1 8B Instruct",
        "input": 0.06,
        "output": 0.06,
        "tier": "cheap",
    },
    "mistralai/mistral-nemo": {
        "name": "Mistral Nemo",
        "input": 0.13,
        "output": 0.13,
        "tier": "cheap",
    },
    "deepseek/deepseek-chat": {
        "name": "DeepSeek V3 Chat",
        "input": 0.27,
        "output": 1.10,
        "tier": "cheap",
    },
    "openai/gpt-4o-mini": {
        "name": "GPT-4o mini",
        "input": 0.15,
        "output": 0.60,
        "tier": "cheap",
    },
    "anthropic/claude-3-haiku": {
        "name": "Claude 3 Haiku",
        "input": 0.25,
        "output": 1.25,
        "tier": "cheap",
    },
    # ===== 平衡 =====
    "openai/gpt-4.1-mini": {
        "name": "GPT-4.1 mini",
        "input": 0.40,
        "output": 1.60,
        "tier": "balanced",
    },
    "anthropic/claude-3.5-haiku": {
        "name": "Claude 3.5 Haiku",
        "input": 0.80,
        "output": 4.00,
        "tier": "balanced",
    },
    "qwen/qwen-2.5-72b-instruct": {
        "name": "Qwen 2.5 72B Instruct",
        "input": 0.35,
        "output": 0.40,
        "tier": "balanced",
    },
    "meta-llama/llama-3.3-70b-instruct": {
        "name": "Llama 3.3 70B Instruct",
        "input": 0.59,
        "output": 0.79,
        "tier": "balanced",
    },
    # ===== 高品質（適合做小規模、嚴肅報告）=====
    "openai/gpt-4o": {
        "name": "GPT-4o",
        "input": 2.50,
        "output": 10.00,
        "tier": "premium",
    },
    "openai/gpt-4.1": {
        "name": "GPT-4.1",
        "input": 2.00,
        "output": 8.00,
        "tier": "premium",
    },
    "anthropic/claude-3.5-sonnet": {
        "name": "Claude 3.5 Sonnet",
        "input": 3.00,
        "output": 15.00,
        "tier": "premium",
    },
    "google/gemini-pro-1.5": {
        "name": "Gemini Pro 1.5",
        "input": 1.25,
        "output": 5.00,
        "tier": "premium",
    },
    "deepseek/deepseek-r1": {
        "name": "DeepSeek R1（推理模型）",
        "input": 0.55,
        "output": 2.19,
        "tier": "premium",
    },
    "x-ai/grok-2-1212": {
        "name": "Grok 2",
        "input": 2.00,
        "output": 10.00,
        "tier": "premium",
    },
}

# 嘗試把使用者的縮寫對應到完整 OpenRouter id
ALIASES: Dict[str, str] = {
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "gpt-4o": "openai/gpt-4o",
    "gpt-4.1-mini": "openai/gpt-4.1-mini",
    "gpt-4.1": "openai/gpt-4.1",
    "claude-3-haiku": "anthropic/claude-3-haiku",
    "claude-3.5-haiku": "anthropic/claude-3.5-haiku",
    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "gemini-flash-1.5": "google/gemini-flash-1.5",
    "gemini-pro-1.5": "google/gemini-pro-1.5",
    "deepseek-chat": "deepseek/deepseek-chat",
    "deepseek-r1": "deepseek/deepseek-r1",
}


# ----------------------------------------------------------------------------
# 每次 LLM 呼叫的 token 估計值（input/output 各自的低/中/高 區間）
# ----------------------------------------------------------------------------

# 經驗值：OASIS 每個 agent 的決策 prompt（含 system、profile、最近貼文/評論、可用動作）
# 大致落在 1200~3500 input tokens；輸出（CREATE_POST 內容或工具呼叫參數）約 80~400
PER_CALL_TOKENS = {
    "input_low": 1200,
    "input_mid": 2200,
    "input_high": 3500,
    "output_low": 80,
    "output_mid": 200,
    "output_high": 400,
}

# 工具呼叫額外開銷：camel-ai 在多步工具呼叫時可能會多打 LLM
# 例如先決定動作、再產生內容，平均係數 1.0 ~ 1.6
TOOL_CALL_FACTOR_LOW = 1.0
TOOL_CALL_FACTOR_MID = 1.3
TOOL_CALL_FACTOR_HIGH = 1.6

# 啟用 Zep 圖譜記憶回寫時的額外負擔（額外 input tokens 用於彙整）
GRAPH_MEMORY_INPUT_BUMP = 0.20  # +20% input tokens
GRAPH_MEMORY_OUTPUT_BUMP = 0.10


# ----------------------------------------------------------------------------
# OpenRouter 即時報價（30 分鐘快取）
# ----------------------------------------------------------------------------

_OPENROUTER_CACHE: Dict[str, Any] = {
    "fetched_at": 0.0,
    "by_id": {},
}
_OPENROUTER_TTL_SEC = 30 * 60


def _fetch_openrouter_models() -> Dict[str, Dict[str, float]]:
    """
    從 OpenRouter 抓取目前公開的模型價格表。
    回傳：{model_id: {"input": usd_per_mtok, "output": usd_per_mtok}}
    若失敗則回傳空字典。
    """
    now = time.time()
    if (
        _OPENROUTER_CACHE["by_id"]
        and now - _OPENROUTER_CACHE["fetched_at"] < _OPENROUTER_TTL_SEC
    ):
        return _OPENROUTER_CACHE["by_id"]

    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.get("https://openrouter.ai/api/v1/models")
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        logger.warning(f"OpenRouter 報價抓取失敗，將使用內建參考單價: {e}")
        return {}

    by_id: Dict[str, Dict[str, float]] = {}
    for item in data.get("data", []):
        model_id = item.get("id")
        pricing = item.get("pricing") or {}
        try:
            prompt_per_token = float(pricing.get("prompt", 0) or 0)
            completion_per_token = float(pricing.get("completion", 0) or 0)
        except (TypeError, ValueError):
            continue

        # OpenRouter 的價格欄位是「每 1 個 token 的 USD」
        input_per_mtok = prompt_per_token * 1_000_000
        output_per_mtok = completion_per_token * 1_000_000

        if model_id:
            by_id[model_id] = {
                "input": input_per_mtok,
                "output": output_per_mtok,
            }

    _OPENROUTER_CACHE["by_id"] = by_id
    _OPENROUTER_CACHE["fetched_at"] = now
    logger.info(f"OpenRouter 報價快取更新：{len(by_id)} 個模型")
    return by_id


def _normalize_model_id(raw: str) -> str:
    """把使用者輸入的縮寫對應成 OpenRouter 標準 id。"""
    if not raw:
        return ""
    raw = raw.strip()
    if raw in KNOWN_MODELS:
        return raw
    if raw in ALIASES:
        return ALIASES[raw]
    # 沒前綴但實際是 openai 系列
    if "/" not in raw and f"openai/{raw}" in KNOWN_MODELS:
        return f"openai/{raw}"
    return raw


def _resolve_pricing(model_id: str) -> Tuple[float, float, str]:
    """
    取得指定模型的 (input_per_mtok, output_per_mtok, source)
    source: "openrouter" | "fallback_static" | "unknown"
    """
    normalized = _normalize_model_id(model_id)

    live = _fetch_openrouter_models()
    if normalized in live:
        prc = live[normalized]
        return float(prc["input"]), float(prc["output"]), "openrouter"

    if normalized in KNOWN_MODELS:
        prc = KNOWN_MODELS[normalized]
        return float(prc["input"]), float(prc["output"]), "fallback_static"

    return 0.0, 0.0, "unknown"


# ----------------------------------------------------------------------------
# 主迴圈呼叫次數估算（與 run_parallel_simulation.py 的 get_active_agents_for_round 對齊）
# ----------------------------------------------------------------------------

@dataclass
class RoundsEstimate:
    total_rounds_config: int
    effective_rounds: int
    total_decisions_one_platform: float


def _avg_activity_filter(agent_configs: List[Dict[str, Any]]) -> float:
    """
    activity_level 過濾器在程式裡會「以該機率讓該 agent 進入候選池」，
    取所有 agent 的平均 activity_level 當期望通過率，若無資料退回 0.5。
    """
    if not agent_configs:
        return 0.5
    levels: List[float] = []
    for cfg in agent_configs:
        try:
            v = float(cfg.get("activity_level", 0.5))
            levels.append(max(0.0, min(1.0, v)))
        except (TypeError, ValueError):
            continue
    if not levels:
        return 0.5
    return sum(levels) / len(levels)


def _estimate_decisions_per_platform(
    config: Dict[str, Any],
    max_rounds: Optional[int],
) -> RoundsEstimate:
    """
    估算單一平台主迴圈內，所有輪總共會發生多少次「agent 決策」。
    每次決策 ≈ 一次 LLM 呼叫（不含工具回合放大）。
    """
    time_config = config.get("time_config", {})
    agent_configs = config.get("agent_configs", [])

    total_hours = int(time_config.get("total_simulation_hours", 72) or 72)
    minutes_per_round = max(int(time_config.get("minutes_per_round", 60) or 60), 1)
    config_total_rounds = max((total_hours * 60) // minutes_per_round, 0)

    if max_rounds is not None and max_rounds > 0:
        effective_rounds = min(config_total_rounds, max_rounds)
    else:
        effective_rounds = config_total_rounds

    base_min = float(time_config.get("agents_per_hour_min", 5) or 5)
    base_max = float(time_config.get("agents_per_hour_max", 20) or 20)
    avg_target = (base_min + base_max) / 2.0

    peak_hours = set(time_config.get("peak_hours") or [19, 20, 21, 22])
    off_peak_hours = set(time_config.get("off_peak_hours") or [0, 1, 2, 3, 4, 5])
    peak_mult = float(time_config.get("peak_activity_multiplier", 1.5) or 1.5)
    off_peak_mult = float(time_config.get("off_peak_activity_multiplier", 0.3) or 0.3)

    activity_pass_rate = _avg_activity_filter(agent_configs)
    candidate_count = len(agent_configs)

    total_decisions = 0.0
    for round_idx in range(effective_rounds):
        simulated_minutes = round_idx * minutes_per_round
        simulated_hour = (simulated_minutes // 60) % 24
        if simulated_hour in peak_hours:
            mult = peak_mult
        elif simulated_hour in off_peak_hours:
            mult = off_peak_mult
        else:
            mult = 1.0

        # 期望候選池大小（受 activity_level 過濾）
        expected_candidates = candidate_count * activity_pass_rate
        # 期望這輪實際選出多少 agent（受 min/max * mult 與候選池上限約束）
        target_count = avg_target * mult
        actual_active = min(expected_candidates, target_count)
        total_decisions += max(actual_active, 0.0)

    return RoundsEstimate(
        total_rounds_config=config_total_rounds,
        effective_rounds=effective_rounds,
        total_decisions_one_platform=total_decisions,
    )


# ----------------------------------------------------------------------------
# 由「決策次數」+「每次 token 區間」+「單價」計算 USD 區間
# ----------------------------------------------------------------------------

def _compute_usd_for_pricing(
    decisions_total: float,
    input_per_mtok: float,
    output_per_mtok: float,
    graph_memory: bool,
) -> Tuple[float, float, float, Dict[str, Any]]:
    """
    回傳 (usd_low, usd_mid, usd_high, token_breakdown)
    """
    in_bump = (1 + GRAPH_MEMORY_INPUT_BUMP) if graph_memory else 1.0
    out_bump = (1 + GRAPH_MEMORY_OUTPUT_BUMP) if graph_memory else 1.0

    calls_low = decisions_total * TOOL_CALL_FACTOR_LOW
    calls_mid = decisions_total * TOOL_CALL_FACTOR_MID
    calls_high = decisions_total * TOOL_CALL_FACTOR_HIGH

    in_low = calls_low * PER_CALL_TOKENS["input_low"] * in_bump
    in_mid = calls_mid * PER_CALL_TOKENS["input_mid"] * in_bump
    in_high = calls_high * PER_CALL_TOKENS["input_high"] * in_bump

    out_low = calls_low * PER_CALL_TOKENS["output_low"] * out_bump
    out_mid = calls_mid * PER_CALL_TOKENS["output_mid"] * out_bump
    out_high = calls_high * PER_CALL_TOKENS["output_high"] * out_bump

    usd_low = (in_low / 1_000_000) * input_per_mtok + (out_low / 1_000_000) * output_per_mtok
    usd_mid = (in_mid / 1_000_000) * input_per_mtok + (out_mid / 1_000_000) * output_per_mtok
    usd_high = (in_high / 1_000_000) * input_per_mtok + (out_high / 1_000_000) * output_per_mtok

    breakdown = {
        "input_tokens_low": int(in_low),
        "input_tokens_mid": int(in_mid),
        "input_tokens_high": int(in_high),
        "output_tokens_low": int(out_low),
        "output_tokens_mid": int(out_mid),
        "output_tokens_high": int(out_high),
        "estimated_llm_calls_low": int(calls_low),
        "estimated_llm_calls": int(calls_mid),
        "estimated_llm_calls_high": int(calls_high),
    }
    return usd_low, usd_mid, usd_high, breakdown


# ----------------------------------------------------------------------------
# 對外 API
# ----------------------------------------------------------------------------

def load_simulation_config_from_disk(simulation_id: str) -> Dict[str, Any]:
    """讀取已生成的 simulation_config.json，找不到則拋 FileNotFoundError。"""
    sim_dir = os.path.join(Config.OASIS_SIMULATION_DATA_DIR, simulation_id)
    config_path = os.path.join(sim_dir, "simulation_config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"找不到 simulation_config.json，請先呼叫 /api/simulation/prepare 生成設定: {simulation_id}"
        )
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _platforms_count(platform: str) -> int:
    return 2 if platform == "parallel" else 1


def _build_recommendations(
    selected_id: str,
    decisions_per_platform: float,
    platforms_count: int,
    graph_memory: bool,
    live_pricing: Dict[str, Dict[str, float]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """根據「同樣參數」試算各候選模型費用，分成便宜 / 高品質兩組。"""
    decisions_total = decisions_per_platform * platforms_count

    rows: List[Dict[str, Any]] = []
    for model_id, info in KNOWN_MODELS.items():
        if model_id == selected_id:
            continue

        pricing_src = "fallback_static"
        input_p = info["input"]
        output_p = info["output"]
        if model_id in live_pricing:
            input_p = live_pricing[model_id]["input"]
            output_p = live_pricing[model_id]["output"]
            pricing_src = "openrouter"

        _, usd_mid, _, _ = _compute_usd_for_pricing(
            decisions_total=decisions_total,
            input_per_mtok=input_p,
            output_per_mtok=output_p,
            graph_memory=graph_memory,
        )
        rows.append(
            {
                "id": model_id,
                "name": info["name"],
                "tier": info["tier"],
                "pricing_source": pricing_src,
                "input_per_mtok": round(input_p, 4),
                "output_per_mtok": round(output_p, 4),
                "estimated_usd_mid": round(usd_mid, 3),
            }
        )

    cheaper = [r for r in rows if r["tier"] == "cheap"]
    cheaper.sort(key=lambda r: r["estimated_usd_mid"])
    cheaper = cheaper[:6]

    premium = [r for r in rows if r["tier"] == "premium"]
    premium.sort(key=lambda r: r["estimated_usd_mid"])
    premium = premium[:5]

    return cheaper, premium


def build_cost_estimate_payload(
    config: Dict[str, Any],
    resolved_model_id: str,
    platform: str,
    max_rounds: Optional[int],
    graph_memory: bool,
) -> Dict[str, Any]:
    """組合給前端的完整估算 payload。"""
    rounds_est = _estimate_decisions_per_platform(config, max_rounds)
    plats = _platforms_count(platform)
    decisions_total = rounds_est.total_decisions_one_platform * plats

    in_p, out_p, pricing_source = _resolve_pricing(resolved_model_id)

    if pricing_source == "unknown":
        usd_low = usd_mid = usd_high = 0.0
        breakdown = {
            "estimated_llm_calls_low": int(decisions_total * TOOL_CALL_FACTOR_LOW),
            "estimated_llm_calls": int(decisions_total * TOOL_CALL_FACTOR_MID),
            "estimated_llm_calls_high": int(decisions_total * TOOL_CALL_FACTOR_HIGH),
        }
        disclaimer = (
            "目前模型不在內建價格表，且無法從 OpenRouter 抓到即時報價，"
            "因此只計算決策次數而沒有金額。請改用清單中推薦的 OpenRouter 模型 id。"
        )
    else:
        usd_low, usd_mid, usd_high, breakdown = _compute_usd_for_pricing(
            decisions_total=decisions_total,
            input_per_mtok=in_p,
            output_per_mtok=out_p,
            graph_memory=graph_memory,
        )
        gm_note = "（已加上 Zep 圖譜回寫的額外開銷）" if graph_memory else ""
        src_note = "OpenRouter 即時報價" if pricing_source == "openrouter" else "內建參考單價"
        disclaimer = (
            f"以上為粗估區間，依 {src_note} 計算{gm_note}，"
            "實際費用會因每篇貼文長度、工具呼叫次數、prompt 命中率而上下浮動。"
            "建議跑一輪短時間試水（例如 max_rounds=20）後再決定是否放大。"
        )

    live_pricing = _fetch_openrouter_models() if pricing_source != "unknown" else {}
    cheaper, premium = _build_recommendations(
        selected_id=_normalize_model_id(resolved_model_id),
        decisions_per_platform=rounds_est.total_decisions_one_platform,
        platforms_count=plats,
        graph_memory=graph_memory,
        live_pricing=live_pricing,
    )

    payload: Dict[str, Any] = {
        "resolved_model_id": _normalize_model_id(resolved_model_id) or resolved_model_id,
        "input_per_mtok": round(in_p, 4),
        "output_per_mtok": round(out_p, 4),
        "pricing_source": pricing_source,
        "platform": platform,
        "platforms_count": plats,
        "graph_memory": graph_memory,
        "usd_low": round(usd_low, 3),
        "usd_mid": round(usd_mid, 3),
        "usd_high": round(usd_high, 3),
        "token_estimate": {
            "total_rounds_config": rounds_est.total_rounds_config,
            "effective_rounds": rounds_est.effective_rounds,
            "decisions_per_platform": int(rounds_est.total_decisions_one_platform),
            "platforms_count": plats,
            **breakdown,
        },
        "recommend_cheaper": cheaper,
        "recommend_premium": premium,
        "openrouter_models_url": "https://openrouter.ai/models",
        "disclaimer_zh": disclaimer,
    }
    return payload
