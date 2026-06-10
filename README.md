# MiroFish — 虛擬消費者社群測試平台

> **燒錢前，先讓 1,000 個 AI 消費者幫你跑一輪。**
> 上傳你的點子（PDF / Markdown / 文字）→ 5 分鐘後知道：會不會紅？誰會買？誰會酸？為什麼？怎麼改？

<p align="center">
  <img src="https://img.shields.io/badge/status-v0.3%20Founder%20Edition-purple" alt="Status">
  <img src="https://img.shields.io/badge/stack-Vue3%20%2B%20Flask%20%2B%20OASIS-blue" alt="Stack">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/modified%20from-mirrorfish-orange" alt="Modified From MirrorFish">
</p>

---

## 🇬🇧 English

**MiroFish** is a **virtual consumer community testing platform** that simulates real-world market feedback before you spend a single dollar on product development.

Based on **[MirrorFish](https://github.com/666ghj/MiroFish)** and modified / enhanced by **poopro**, MiroFish lets you upload your business idea (PDF, Markdown, or plain text), then deploys a swarm of **1,000+ AI agents** with unique personalities, memories, and social behaviors into a simulated dual-platform ecosystem (Twitter-like + Reddit-like). Within minutes, you get actionable market intelligence that would traditionally cost tens of thousands of dollars in focus groups and market research.

### Why MiroFish? Our Advantages Over Traditional Approaches and MirrorFish

| Dimension | Traditional Market Research | Basic AI Chatbot Testing | **MiroFish (this fork)** |
|---|---|---|---|
| **Cost** | $50K–$500K per focus group / MVP | Nearly free, but useless | **~$0.50 per simulation run** |
| **Time** | Weeks to months | Minutes, but shallow | **5 minutes for deep insight** |
| **Feedback Quality** | People are polite, lie to be nice | Generic averaged response | **1,000 hostile, honest, diverse AI consumers arguing with each other** |
| **Consumer Behavior** | No real social dynamics | No group effects | **Full social simulation: echo chambers, opinion leaders, bandwagon effects, pile-ons** |
| **Memory & Consistency** | Humans remember; AI forgets | No memory between turns | **Zep-powered time-series memory per agent — they hold grudges, fall in love, change minds** |
| **Dual-Platform Insight** | You pick one channel and pray | N/A | **Simultaneous Twitter-like + Reddit-like platforms — see how the same idea plays differently** |
| **Purchase Intent** | Wait for real sales data | Guess based on thumbs up | **12-factor attribution model: price sensitivity, trust, social proof, competitor comparison, etc.** |
| **Persona Source** | Generic demographics | Random LLM personas | **GraphRAG-extracted personas FROM YOUR ACTUAL DOCUMENT — real stakeholders, not random Americans** |
| **Data Privacy** | Risk of leaking your idea to real testers | Depends on the platform | **100% local/simulated — your idea never leaves your machine** |

### Key Advantages of This Fork (poopro/MiroFish)

- **Enhanced `.gitignore`** — `.env`, uploads, logs, IDE files properly excluded
- **Proper `main` branch** — aligned with GitHub standard
- **Improved README** — clear bilingual documentation
- **Preserved full original functionality** from MirrorFish

---

## 🇹🇼 繁體中文

### 這是什麼？

**文件 → GraphRAG（Zep）→ 大量有差異的 Agent → OASIS 雙平台社群模擬（類 Twitter + 類 Reddit）→ 報告、訪談、問卷、購買意願評估。**

和「叫 ChatGPT 扮演一百種人」不同：這裡的 Agent **會互相看貼文、點讚、留言、被人際關係影響**，並有 **時序記憶**（不會每輪人格亂跳）。

### 為什麼需要 MiroFish？

你不需要先燒錢、不需要先辭職、不需要先做產品。

MiroFish 能讓你在 **5 分鐘內、只花 ~$0.50 美金**，就看到你的點子在虛擬市場上的真實反應——包括誰會買、誰會酸、為什麼不买。

### 與 MirrorFish 的關係

本倉庫基於 [666ghj/MiroFish](https://github.com/666ghj/MiroFish) 修改而成（french: **miro** = 看、觀察；**fish** = 釣魚/探索），在此基礎上：
- 修正分支結構（`main` 而非 `master`）
- 增強 `.gitignore` 排除敏感檔案
- 優化文件與說明

### 核心優勢

#### 🎯 創新 1 — 不是「一個 AI 給平均答案」，是「一千個有差異的 AI 互相吵」

我們用 [OASIS](https://github.com/camel-ai/oasis) 模擬一個迷你版 Twitter + Reddit：
- 每個 AI 都有自己的年齡、職業、MBTI、興趣、口頭禪、偏見
- 每個 AI 看得到別人的貼文、會按讚、會酸、會轉發、會被影響
- 整個系統會出現**真實社群才有的「群眾效應」**

#### 🎯 創新 2 — Agent 不是憑空生的，是從你的文件抽出來的

```
你上傳的 PDF / Markdown
        ↓
LLM 萃取裡面提到的人、組織、品牌、地點、事件
        ↓
建成 GraphRAG 知識圖譜（用 Zep Cloud）
        ↓
每個圖譜節點 → 一個有真實背景的 AI Agent
```

#### 🎯 創新 3 — Agent 有「時序記憶」，不會講話前後矛盾

每個 AI Agent 都掛在 [Zep](https://www.getzep.com/) 的時序記憶系統上，所以行為連貫、會「黑掉」、會「真愛粉」。

#### 🎯 創新 4 — 雙平台並行 + 購買意願評估

Info Plaza（短訊息病毒擴散）+ Topic Community（長文理性討論），加上 12 維度購買意願歸因分析。

---

## TL;DR — 30 秒看懂

| | 傳統做法 | MiroFish |
|---|---|---|
| **想知道點子會不會紅** | 直接做 MVP 燒幾十萬 | 5 分鐘虛擬模擬，~$0.50 |
| **想知道目標用戶怎麼想** | 焦點訪談（1 場 $5–20 萬） | 直接跟任何一位 AI 消費者對話 |
| **想知道廣告會不會被噓** | 上線投廣再看數據 | 上線前 1,000 個 AI 在虛擬社群先吵一輪 |
| **想知道誰會買** | 等付款數據 | 「目標客群 80% 會買、路人只有 20% 會買」直接告訴你 |
| **想知道為什麼不买** | 看評論 / 退貨單 | 「33% 因為價格、22% 因為不信任」可行動歸因 % |

---

## 🚀 快速開始

### 環境需求

- Python 3.10+
- Node.js 18+
- OpenRouter API Key（[申請](https://openrouter.ai/)）
- Zep Cloud API Key（[申請](https://www.getzep.com/)）

### Windows（推薦，最簡單）

雙擊 **`run.bat`**：自動檢查依賴、啟動後端 `5001`、前端 `5173`、並開啟瀏覽器。
首次安裝約需 **5–10 分鐘**（下載 Python 套件）。

關閉用 **`stop.bat`**。

### macOS / Linux（手動）

```bash
# 後端
cd backend && python -m venv .venv && source .venv/bin/activate
pip install --ignore-requires-python flask flask-cors python-dotenv zep-cloud httpx pypdf camel-oasis
export FLASK_APP=app && flask run --port 5001

# 前端（新終端機）
cd frontend && npm install && npm run dev
```

### 配置 `.env`

複製 `.env.example` 為 `.env`，至少填入：

```bash
LLM_API_KEY=sk-or-v1-你的 OpenRouter API Key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=google/gemini-2.5-flash-lite
ZEP_API_KEY=你的 Zep Cloud API Key
ZEP_TENANT_ID=你的 Zep Tenant ID
```

> ⚠️ **`.env` 不會被提交到 Git**（已在 `.gitignore` 中排除）。絕對不要把 API Key 丟到公開倉庫！

---

## 五步流程

1. **上傳** 你的點子 → 參考 `examples/business_idea_solo_freelancer_app.md`
2. **建圖譜** — 本體論 + GraphRAG，從文件抽出「會出現在你市場周遭」的角色
3. **生成 Agent** — 完整人設（年齡、職業、興趣、MBTI、口頭禪、偏見）
4. **跑模擬** — Info Plaza（類 Twitter）+ Topic Community（類 Reddit），多輪多 Agent 並行互動
5. **看結果** — 深度報告 + 交互工具：跟任意 Agent 對話、發問卷、評估購買意願

---

## 核心功能

### 🔥 虛擬社群模擬

- 每個 AI Agent 有**獨立的年齡、職業、MBTI、興趣、口頭禪、偏見**
- Agent 之間**互相影響**：點讚、留言、轉發、被風向影響
- 出現**真實社群效應**：意見領袖、跟風、輿情翻車

### 🧠 GraphRAG 知識圖譜

你的商業計劃書透過 LLM 萃取 → 建成知識圖譜 → 每個圖譜節點生成對應的 AI Agent，確保模擬人群**真實反映你的市場環境**。

### ⏳ 時序記憶（Zep）

每個 Agent 記得：
- 上一輪自己發過什麼
- 誰曾經反駁過他
- 對品牌累積的態度

行為前後一致、會累積情緒、不會「人格跳轉」。

### 📊 購買意願評估（旗艦功能 v0.3）

- **目標客群（TA）購買率** vs **路人購買率**分開看
- **12 維度歸因分析**：價格敏感度、信任度、社會證明、競爭比較……
- 不再是「喜歡/不喜歡」，而是**可執行的百分比歸因**

---

## 📁 項目結構

```
MiroFish/
├── backend/              # Flask 後端 API（Python）
│   ├── app.py            # 主應用入口
│   ├── routes/           # API 路由
│   ├── services/         # 業務邏輯（Agent 生成、模擬、評估）
│   ├── .venv/            # Python 虛擬環境（不提交）
│   └── uploads/          # 用戶上傳檔案（不提交）
├── frontend/             # Vue 3 前端 SPA
│   ├── src/
│   │   ├── views/        # 頁面組件
│   │   ├── components/   # 可復用組件
│   │   └── App.vue       # 根組件
│   └── node_modules/     # （不提交）
├── examples/             # 範例商業計商業計劃書
├── static/               # 靜態資源
├── run.bat               # Windows 一鍵啟動
├── stop.bat              # Windows 一鍵停止
├── .env.example          # 環境變數範本
├── .gitignore            # Git 忽略規則
├── README.md             # 本檔（繁中 + 英文）
└── README.long.md        # 商業長文說明（完整版）
```

---

## 🛠️ 技術棧

| 層級 | 技術 | 說明 |
|---|---|---|
| **前端** | Vue 3 + Vite | 響應式 SPA，模擬控制台即時更新 |
| **後端** | Flask (Python) | REST API，處理 Agent 邏輯 |
| **LLM** | OpenRouter | 彈性接入多個模型（Gemini、Claude、GPT） |
| **知識圖譜** | Zep Cloud | GraphRAG + 時序記憶系統 |
| **Agent 框架** | OASIS (Camel-AI) | 多 Agent 社群模擬引擎 |
| **資料處理** | pypdf, httpx | PDF 解析、API 通訊 |

---

## 🛣️ 路線圖

| 階段 | 目標 | 狀態 |
|---|---|---|
| **Phase 1** | 單文件 → 單 Agent → 單平台模擬 | ✅ 完成 |
| **Phase 2** | 多 Agent + 雙平台 + GraphRAG | ✅ 完成 |
| **Phase 3** | 購買意願評估 + 歸因分析 | ✅ v0.3 實現 |
| **Phase 4** | SaaS 化、自訂 Agent 模板、API 開放 | 🔜 規劃中 |

---

## 🤝 參與貢參與貢獻

歡迎提交 Issue 和 Pull Request！如果想貢獻：

1. Fork 本倉庫
2. 建立你的功能分支（`git checkout -b feature/amazing-feature`）
3. 提交修改（`git commit -m 'Add amazing feature'`）
4. 推送分支（`git push origin feature/amazing-feature`）
5. 開啟 Pull Request

---

## ⚖️ 授權

MIT License — 詳見 LICENSE 檔案

---

## 📝 修改歷史

本倉庫 fork 自 [666ghj/MiroFish](https://github.com/666ghj/MiroFish)，由 **poopro** 維護。
主要修改：修正分支結構、強化 `.gitignore` 安全策略、完善中英文文件。
原始商業計劃書見 `README.long.md`。

<p align="center"><sub>Original basis: MirrorFish by 666ghj | Modified & maintained by poopro</sub></p>
