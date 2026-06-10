# MiroFish

> **燒錢前，先讓大量 AI 消費者在虛擬社群裡預演一輪。**  
> 上傳 PDF / Markdown / 文字 → 看誰會買、誰會酸、為什麼。

[![Status](https://img.shields.io/badge/status-v0.3%20Founder%20Edition-purple)]()
[![Stack](https://img.shields.io/badge/stack-Vue3%20%2B%20Flask%20%2B%20OASIS-blue)]()
[![License](https://img.shields.io/badge/license-TBD-lightgrey)]()

---

## 這是什麼？（一句話）

**文件 → GraphRAG（Zep）→ 大量有差異的 Agent → [OASIS](https://github.com/camel-ai/oasis) 雙平台社群模擬（類 Twitter + 類 Reddit）→ 報告、訪談、問卷、購買意願評估。**

和「叫 ChatGPT 扮演一百種人」不同：這裡的 Agent **會互相看貼文、按讚、留言、被風向影響**，並有 **時序記憶**（不會每輪人格亂跳）。

---

## 五步驟流程

1. **上傳** 你的點子（例：`examples/business_idea_popup_restaurant.md`）
2. **建圖譜** 本體論 + GraphRAG，從文件抽出「會出現在你市場週遭」的角色
3. **生成 Agent** 完整人設（年齡、職業、興趣等）
4. **跑模擬** Info Plaza + Topic Community，多輪、多 Agent 並行互動
5. **看結果** 左側深度報告；右側 **Interactive Tools**：跟任意 Agent 對話、發問卷、**評估購買意願**

---

## 購買意願評估（Interactive Tools →「評估購買意願」）

模擬跑完後，在報告頁右側工具列點紫色按鈕。輸入 **產品描述、目標客群定義、廣告文案** 後，系統會：

- 每位 Agent：**隱藏 5 維心理敏感度**（主畫面不強調，可於人設卡展開查看）+ **模擬中的真實社群行為** → 綜合判斷 **BUY / REJECT**
- 分 **目標客群（TA）** 與 **路人**，分開算購買率
- 輸出 **「為什麼會買 / 為什麼不買」** 的百分比歸因（含社群聲量等僅模擬才拿得到的因子）

結果會寫入該次模擬目錄下的 `purchase_intent.json`，下次可從面板載入不必重跑。

---

## 快速啟動

**環境**：Python 3.10+（3.12 可裝，見下方 pip）、Node 18+、OpenRouter Key、Zep Cloud Key。

### Windows（推薦）

雙擊 **`run.bat`**：檢查依賴、啟動後端 `5001`、前端 `5173`、可開瀏覽器。關閉用 **`stop.bat`**。  
※ 第一次安裝可能需 **5–10 分鐘**（含較大 Python 套件）。

### `.env`

複製 `.env.example` 為 `.env`，至少填入：

```bash
LLM_API_KEY=sk-or-v1-...
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=google/gemini-2.5-flash-lite
ZEP_API_KEY=z_...
```

Step 2 介面會顯示 **LLM 費用粗估與模型建議**；要換模型改 `LLM_MODEL_NAME` 後重啟即可。

### macOS / Linux（手動）

```bash
cd backend && python -m venv .venv && source .venv/bin/activate
pip install --ignore-requires-python flask flask-cors python-dotenv zep-cloud httpx pypdf camel-oasis
export FLASK_APP=app && flask run --port 5001

# 另開終端
cd frontend && npm install && npm run dev
```

---

## 技術棧（精簡）

| 層 | 技術 |
|---|---|
| 前端 | Vue 3、Vite |
| 後端 | Flask |
| 模擬 | camel-oasis（OASIS） |
| 記憶 / 圖譜 | Zep Cloud |
| LLM | OpenRouter（OpenAI 相容 API） |

主要 API 範例：`/api/graph/build`、`/api/simulation/start`、`/api/simulation/<id>/run-status`、`/api/simulation/<id>/purchase-intent`（POST/GET）。

---

## 長版說明

完整行銷敘事、案例、路線圖、Pitch Q&A 見 **[README.long.md](./README.long.md)**。

---

## 連結與授權

- **GitHub**：[github.com/666ghj/MiroFish](https://github.com/666ghj/MiroFish)
- **License**：待補
