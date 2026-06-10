# MiroFish

> **精簡版說明請看 [README.md](./README.md)；本檔為完整長版（創新敘事、案例、路線圖、Pitch 等）。**

> ## **燒錢前，先讓 1,000 個 AI 消費者幫你跑一輪。**
>
> 把你的點子（PDF / Markdown / 一段文字）丟進來，5 分鐘後告訴你：
> **會不會紅？哪群人會買？哪群人會酸？為什麼？怎麼修？**

[![Status](https://img.shields.io/badge/status-v0.3%20Founder%20Edition-purple)]()
[![Stack](https://img.shields.io/badge/stack-Vue3%20%2B%20Flask%20%2B%20OASIS-blue)]()
[![License](https://img.shields.io/badge/license-TBD-lightgrey)]()

---

## TL;DR — 30 秒看懂

| | 傳統做法 | MiroFish |
|---|---|---|
| **想知道點子會不會紅** | 直接做 MVP 燒幾十萬 | 5 分鐘虛擬模擬，~$0.50 美金 |
| **想知道 TA 怎麼想** | 焦點訪談（1 場 5–20 萬） | 直接跟任何一位 AI 消費者對話 |
| **想知道廣告會不會被酸** | 上線投廣再看數據 | 上線前 1,000 個 AI 在虛擬 Twitter / Reddit 先吵一輪 |
| **想知道誰會買** | 等付款數據 | 「目標客群 80% 會買、路人只有 20% 會買」直接告訴你 |
| **想知道為什麼不買** | 看評論 / 退貨單 | 「33% 因為價格、22% 因為不信任」可行動歸因 % |

> 你不用先燒錢、不用先辭職、不用先做產品。

---

## 一、這個產品的「創新點」是什麼？

市面上講「AI 模擬市場」的工具一抓一大把，但它們大多是：
**「給 LLM 一段文案 → LLM 用一個平均人格給你打 80 分」**。

這不是市場，這只是 ChatGPT。

MiroFish 不一樣。我們做的是 **「會互相影響的虛擬社群」**：

### 🎯 創新優勢 ① — 不是「一個 AI 給平均答案」，是「一千個有差異的 AI 互相吵」

我們用 [OASIS](https://github.com/camel-ai/oasis)（Camel-AI 開源的多 Agent 社群模擬框架）模擬一個迷你版 Twitter + Reddit：
- 每個 AI 都有自己的年齡、職業、MBTI、興趣、口頭禪、偏見
- 每個 AI 看得到別人的貼文、會按讚、會酸、會轉發、會被影響
- 整個系統會出現**真實社群才有的「群眾效應」**：意見領袖、酸民、跟風、輿情翻車

這跟「叫一個 ChatGPT 扮演 100 種人」**完全不是同一件事**。
ChatGPT 給你的是「平均的中庸答案」，MiroFish 給你的是「會互相點火、會吵起來的真實社群動態」。

### 🎯 創新優勢 ② — Agent 不是憑空生的，是從你的文件抽出來的

別人的工具是隨機抽 50 個 persona。我們的方法叫 **「文件 → 知識圖譜 → 真實人物畫像」**：

```
你上傳的 PDF / Markdown
        ↓
LLM 萃取裡面提到的人、組織、品牌、地點、事件
        ↓
建成 GraphRAG 知識圖譜（用 Zep Cloud）
        ↓
每個圖譜節點 → 一個有真實背景的 AI Agent
```

舉例：你上傳「一碗 — 台北東區單品快閃飯店」的計劃書，MiroFish 會抽出
**「東區上班族」、「鬍鬚張」、「八方雲集」、「美食 KOL」、「IG 用戶」、「外送平台」**…
然後用這些「真的會出現在你產品周遭」的角色當 Agent，**而不是隨機抽 50 個美國中年男子**。

### 🎯 創新優勢 ③ — Agent 有「時序記憶」，不會講話前後矛盾

每個 AI Agent 都掛在 [Zep](https://www.getzep.com/) 的時序記憶系統上。
意思是這位 Agent **會記得**：
- 上一輪自己發過什麼貼文
- 上一輪誰反駁過他
- 自己對這個品牌過去抱怨過幾次

所以行為連貫、會「黑掉」、會「真愛粉」，就跟真人一樣。
傳統 LLM 模擬是每次重新生成，今天說愛你明天說恨你 — MiroFish 不會。

### 🎯 創新優勢 ④ — 雙平台並行：Info Plaza 〈Twitter-like〉 + Topic Community 〈Reddit-like〉

同一群 Agent 同時在兩個社群文化下發酵：
- **Info Plaza**：短訊息、轉發、按讚、追蹤 — 看你的點子能不能病毒擴散
- **Topic Community**：長文討論、評論、上下投票 — 看你的點子能不能撐住理性討論

很多東西在 Twitter 紅、在 Reddit 被酸（反之亦然），雙平台同時跑你才知道真相。

### 🎯 創新優勢 ⑤ — 購買意願評估：不是測廣告，是測「真實情境下會不會掏錢」

> 這是 v0.3 新加的旗艦功能，請特別看一下。

市面上的廣告 AI 評估系統（例如 GAP_MK1）只做一件事：
**給 LLM 一份廣告文案 → 跑 5 維度心理分數 → 80 分通過。**

問題是：**真實消費者掏錢前，看的不只是廣告，還看「我朋友怎麼說」、「網路風向」、「有沒有人翻車」。**

MiroFish 的購買意願評估**直接接到模擬出來的社群行為**：

```
最終 BUY / REJECT 決策
        ↑
┌───────┴───────┐
│               │
內部隱藏 5 維 meter        Info Plaza / Topic Community
（這位 agent 對什麼最買單）   實際模擬出的社群行為
（5 維度藏起來不顯眼）         （這位 agent 在社群上看過/做過什麼）
```

而且我們會幫你把人切兩半看：
- **目標客群（TA）購買率**
- **路人購買率**
- 還有「為什麼會買 / 為什麼不買」的**百分比歸因**（12 個因子細拆）

詳細看 [§ 五、購買意願評估](#五購買意願評估purchase-intent-旗艦功能)。

---

## 二、為什麼一人公司、新創團隊、行銷人會需要這個？

### 創業者最常踩的 5 個坑：

| 坑 | 傳統做法 | 為什麼會死 |
|---|---|---|
| 不知道點子會不會紅 | 直接做 MVP 上線 | 燒掉幾十萬，失敗了還要刪 IG 貼文 |
| 想知道 TA 想法 | 找朋友問 | 朋友會講客套話，沒人敢說「你這想法很爛」 |
| 想做焦點訪談 | 找市調公司 | **一場 5–20 萬**，獨立創業者根本付不起 |
| 想測廣告會不會翻車 | 直接投廣告 | 真的翻車後，社群會永遠記得 |
| 想跟創投談 | 沒數據 | 被打槍 / 被砍估值 |

### MiroFish 把這 5 個坑全部變成「上線前的虛擬演習」

**「點 5 次滑鼠、付 0.5 美金、5 分鐘後拿到一份比 5 萬市調報告還具體的洞察。」**

---

## 三、它怎麼運作？（5 步驟流程）

```
┌──────────────────────────────────────────────────────────────────┐
│  Step 01    Step 02    Step 03    Step 04         Step 05        │
│  ─────     ─────      ─────      ─────           ─────           │
│  上傳   →  AI 理解  →  建虛擬市場  →  跑模擬     →    報告 + 對話  │
│  點子      你的點子   1k+ AI Agent  雙平台社群     會不會紅 +     │
│                       從文件而來    會互相影響     可問任何 Agent │
└──────────────────────────────────────────────────────────────────┘
```

### Step 1｜上傳你的點子
PDF / Markdown / TXT 都行。可以是商業計劃書、產品介紹、廣告文案、IG 貼文、募資簡報。
**範例**：上傳 `examples/business_idea_popup_restaurant.md`（一家台北東區的快閃飯店計劃）。

### Step 2｜AI 理解你的點子
系統會做三件事：

1. **文件解析 + 切塊**：把長文件拆成有意義的段落
2. **本體論生成**（Ontology）：自動定義「這個產業會出現的角色類型」
   - 餐飲業 → 上班族、外送員、美食 KOL、競品店家、平台代表…
   - SaaS 業 → 工程師、產品經理、CTO、技術評論家…
3. **GraphRAG 圖譜建構**：用 Zep 把所有實體和關係存成知識圖譜

**這一步同時會跑「LLM 費用粗估」**，告訴你這次模擬大概要花多少美金，並推薦你便宜或更高品質的模型（看 §[六之一](#六之一模型費用粗估與模型推薦)）。

### Step 3｜建立虛擬市場
從圖譜抽出實體，用 LLM 把每個實體擴寫成一個有完整人設的 AI Agent：

```json
{
  "user_id": 17,
  "name": "Lin Yi-Hsuan",
  "age": 31, "gender": "female", "mbti": "ENFJ",
  "profession": "信義區外商上班族",
  "bio": "白天忙得跟狗一樣，午餐預算 NT$300，重 IG 美學",
  "persona": "ENFJ + 注重效率 + 對排隊容忍度低 + 會 Threads 發文抱怨",
  "interested_topics": ["美食", "快時尚", "Threads"],
  "follower_count": 432
}
```

### Step 4｜雙平台社群模擬
**這一步是 MiroFish 的核心引擎。** 每位 Agent 同時被丟進兩個虛擬社群：

| 平台 | 對應現實 | 可用動作 |
|---|---|---|
| **Info Plaza** | Twitter / Threads | 發文、按讚、轉發、引用、追蹤、IDLE |
| **Topic Community** | Reddit / Dcard | 發文、留言、上/下投票、搜尋、追蹤、靜音、刷新、IDLE |

每一輪（=模擬世界 30 分鐘）：
- 系統挑出「現在會上線」的 Agent（看時段是高峰還是低谷）
- 每位上線的 Agent 都會跟 LLM 對話一次，自主決定：「我這輪要做什麼？」
- 看到別人的貼文、按讚、回應 → 寫進記憶 → 下輪繼續
- 整個社群有意見領袖、有酸民、有跟風、會發酵 → 跟真實社群長一樣

模擬可以跑 10–100 輪，視你的需求。

### Step 5｜報告 + Interactive Tools（互動工具列）
模擬完成後，你進入報告頁，右側的 **Interactive Tools** 工具列幫你深挖結果：

1. **ReportAgent 自動寫的深度報告**（左側）
   用 ReACT 模式（Reason + Act + Reflect 循環），分章節撰寫，會自己跑去模擬資料庫查資料佐證每個結論
2. **跟任何虛擬消費者直接對話**（Interactive Tools → 與世界中任意個體對話）
   點任一位 Agent 開啟 Interview 模式，問「你為什麼不買？」、「你看到那則廣告什麼感覺？」
3. **發送問卷調查到世界中**（Interactive Tools → 問卷）
   挑選樣本 → 設計題目 → 並行讓多位 Agent 回答 → 拿結構化結果
4. **評估購買意願**（Interactive Tools → ★ 旗艦功能，§[五](#五購買意願評估purchase-intent-旗艦功能)）
   結合每位 Agent 的隱藏 5 維 meter + 模擬出的社群行為，預測 BUY / REJECT 並做歸因

---

## 四、跟市面上其他工具的差異化

| 工具 | 訪談一個 AI | 像 MiroFish 嗎？ |
|---|---|---|
| **ChatGPT「角色扮演」** | 一個 AI 假裝是 100 種人 | ❌ 沒有 Agent 之間互相影響、沒有時序記憶、沒有社群動態 |
| **問卷網站** | 真人但樣本小，1,000 份要 1 週 + 幾萬塊 | ❌ 沒辦法看「他們互相討論後會變成什麼」 |
| **焦點訪談公司** | 真人，深度好但成本爆炸 | ❌ 一場 5–20 萬、人少（5–8 人）、有人說客套話 |
| **A/B 測試平台** | 真實流量 | ❌ 已經要燒廣告費了，這是「上線後測」不是「上線前測」 |
| **GAP_MK1 / 廣告 AI 評估器** | 文案 → 5 維分數 | ⚠️ 只有單張文案、沒有社群行為、沒有 TA / 路人分群 |
| **MiroFish** | ✅ 1,000 個有差異 Agent + GraphRAG 來自你文件 + 雙平台社群動態 + 時序記憶 + 購買意願歸因 + 對話訪談 | — |

**MiroFish 是目前唯一同時做到「會互相影響的社群 + 從你文件來的角色 + 真實情境下的購買意願歸因」的工具。**

---

## 五、購買意願評估（Purchase Intent，旗艦功能）

### 它在問什麼？

模擬跑完後，AI 們在 Info Plaza 發文討論完了。
**老闆現在最想問**：「OK，這群人到底會不會掏錢買我的東西？為什麼？」

這就是購買意願評估要回答的事。

### 跟一般廣告 AI 評估有什麼不一樣？

| 維度 | 一般工具（GAP_MK1 純文案測） | MiroFish 購買意願評估 |
|------|---|---|
| **資料來源** | 只有廣告文案 | 廣告文案 **+** Info Plaza 模擬出來的真實社群行為 |
| **5 維心理 meter** | 直接秀（讓人看分數爽爽） | **藏在 agent 內部當「敏感度權重」**，主畫面只顯示最終 BUY/REJECT |
| **受眾分群** | 隨機 persona | LLM 把 agent 分成「目標客群 (TA)」與「路人」，**兩群分開算購買率** |
| **個體決策** | 5 維度加總平均 | 5 維度敏感度 × 這位 agent 在社群上看過/做過什麼 → 綜合判斷 |
| **歸因輸出** | 「最高分維度」 | 「為什麼會買 / 為什麼不買」的**百分比歸因**（12 個因子） |

### 它怎麼決定 BUY / REJECT？

每位 agent 跑兩次 LLM：

**第 1 次（畫像 + 分類）**：
- 推導隱藏的 5 維敏感度（說服力 / 信任 / 情感共鳴 / 社群從眾 / 急迫感）
- 加 2 個輔助維度（價格敏感度 / 懷疑基礎值）
- 判斷是否屬於目標客群（TA / 非 TA）

**第 2 次（決策）**：把以下全部丟給 LLM 判斷：
1. agent 公開人設
2. agent 的隱藏 5 維敏感度（**內部 meter**）
3. agent 在 Info Plaza / Topic Community 上的真實行為摘要
   （自己發過什麼、留過什麼言、按過幾個讚、追蹤幾個人）
4. 你的產品描述 + 廣告文案

→ LLM 站在這位 agent 的立場給出：
```json
{
  "decision": "BUY",
  "confidence": 78,
  "one_line_reason": "她朋友圈最近都在討論這家店，加上溏心蛋切開的 IG 美照戳中她",
  "main_drivers": ["social_buzz_positive", "emotional_resonance", "own_engagement"],
  "main_barriers": [],
  "suggestion": "可以多放幾張溏心蛋的特寫"
}
```

### 12 個歸因因子（會出現在「為什麼買 / 不買」的歸因條）

```
理性說服力 │ 品牌信任 │ 情感共鳴 │ 社會認同 │ 限時急迫感
價格敏感   │ 社群正向聲量 │ 社群負評 │ 自身已有正向互動
社群上沒接觸過 │ 對廣告的懷疑 │ 品牌熟悉度
```

**特別注意**：`social_buzz_positive` / `social_buzz_negative` / `own_engagement` 這幾個是純 MiroFish 才有的因子 — 它們直接來自模擬出的社群行為，純廣告測根本拿不到這些訊號。

### 主畫面（5 維度藏起來，BUY/REJECT 上桌）

打開「評估購買意願」面板會看到：

| 區塊 | 內容 |
|---|---|
| **KPI 卡 ×4** | 總體購買率、TA 購買率、路人購買率、平均決策信心 |
| **歸因條 ×2** | 為什麼會買 % vs 為什麼不買 %（橫條圖） |
| **Tabs** | 目標客群 / 路人 兩個分頁 |
| **Persona 卡** | BUY/REJECT 徽章 + 一句話原因 + 信心度 + TA tag |
| **「展開查看內部 meter ↓」** | 點開才看到 5 維度敏感度、心理摘要、社群行為摘要、給品牌建議 |

**為什麼 5 維度要藏起來？** 因為老闆最想看的是「會不會買、為什麼、要不要修」，
不是一堆雷達圖。雷達圖留給細看單一 agent 的時候。

### 怎麼用？

1. **先把模擬跑完一輪**（Step 3 顯示「已完成」）
2. 進入 Step 5（報告頁）後，看到右側的 **Interactive Tools** 工具列
3. 點工具列裡的紫色 pill「**評估購買意愿**」 → 開啟全螢幕評估面板
4. 填三件事：產品描述 / 目標客群定義 / 廣告文案
5. 選取樣 6 / 12 / 20 / 全部 agents
6. 按開始 → 12 位約 1–2 分鐘
7. 看結果，**結果會自動存到 `purchase_intent.json`，下次再打開面板會有「直接載入」捷徑不用重跑**

> 💡 為什麼放在 Interactive Tools？因為它跟「跟 agent 對話」、「發問卷」一樣，
> 都是**模擬完成後拿來深挖結果**的工具，邏輯上同一群 → 收進同一條工具列最直觀。

---

## 六、安裝與啟動

### 環境需求
- **Python 3.10+**（Python 3.12 也能跑，camel-oasis 會用 `--ignore-requires-python` 強裝）
- **Node.js 18+**
- **8GB+ RAM**（推薦 16GB）
- **OpenRouter API Key**（OpenAI 介面相容，最便宜的選項）
- **Zep Cloud API Key**（記憶系統，免費額度夠玩）

### 🚀 一鍵啟動（Windows 推薦）

雙擊專案根目錄的 **`run.bat`** — 它會自動：
1. 檢查 Python venv 完整性（缺套件會自動裝）
2. 啟動後端 Flask（port `5001`）
3. 啟動前端 Vite（port `5173`）
4. 自動打開瀏覽器到 `http://localhost:5173`

要關掉時，雙擊 **`stop.bat`**。

> 第一次跑會花 5–10 分鐘下載 torch / transformers / camel-oasis 等大套件。
> 之後每次都是秒開。

### 環境變數（`.env`）

複製 `.env.example` 為 `.env`，填入：

```bash
LLM_API_KEY=sk-or-v1-...                       # OpenRouter Key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=google/gemini-2.5-flash-lite    # 推薦：又快又便宜

ZEP_API_KEY=z_...                              # 從 https://www.getzep.com/ 拿
```

### macOS / Linux 手動啟動

```bash
# 後端
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --ignore-requires-python flask flask-cors python-dotenv \
            zep-cloud httpx pypdf camel-oasis
export FLASK_APP=app
flask run --port 5001

# 另開終端 — 前端
cd frontend
npm install
npm run dev
```

---

## 六之一、模型費用粗估與模型推薦

> 你不用懂什麼是 token，先記一句話：**模擬會做幾百到幾千次 LLM 呼叫，每次都會被收錢。**

### Step 2 會看到「LLM 費用粗估」面板

它會：
1. 抓你 `.env` 裡的 `LLM_MODEL_NAME`
2. 看你模擬的時數、每輪分鐘數、Agent 數量、有沒有開圖譜回寫
3. 推估這次跑大概花多少美金（**低 / 中 / 高區間**，不是固定值）
4. 列出更便宜 / 更高品質的模型，每個都用同樣參數試算費用

### 換模型超快

- **想看別的模型多少錢**：直接點推薦清單卡片，面板立刻重算
- **真的想換**：把 `provider/model-name` 貼到 `.env` 的 `LLM_MODEL_NAME=`，重啟服務

### 推薦清單（內建備援單價，OpenRouter 即時報價會自動覆蓋）

| 等級 | 模型 ID | 適合場景 |
|---|---|---|
| 💸 便宜 | `google/gemini-2.5-flash-lite` | **預設值**，超便宜超快 |
| 💸 便宜 | `meta-llama/llama-3.1-8b-instruct` | 大量並發、成本最低 |
| 💸 便宜 | `deepseek/deepseek-chat` | 中文好、CP 值高 |
| ⚖️ 平衡 | `openai/gpt-4o-mini` | 穩定、業界標竿 |
| ⚖️ 平衡 | `anthropic/claude-3.5-haiku` | Anthropic 入門 |
| 💎 高品質 | `openai/gpt-4o` | 報告品質明顯升級 |
| 💎 高品質 | `anthropic/claude-3.5-sonnet` | 推理 / 文案最強之一 |
| 💎 高品質 | `deepseek/deepseek-r1` | 強推理、相對便宜 |

完整清單：[openrouter.ai/models](https://openrouter.ai/models)

---

## 七、技術架構（給工程師看）

```
┌──────────────────────────────────────────────────────────────────┐
│  Frontend (Vue 3 + Vite + D3.js)                                 │
│  ├── Home.vue                  落地頁 / 上傳介面                  │
│  ├── Process.vue               5 步驟主流程                       │
│  ├── Step1GraphBuild.vue       上傳 → 圖譜建構                    │
│  ├── Step2EnvSetup.vue         Agent 生成 + 費用粗估              │
│  ├── Step3Simulation.vue       模擬執行 + 雙平台時間軸            │
│  ├── Step4Report.vue           報告生成（左 outline / 右 timeline）│
│  ├── Step5Interaction.vue      Interactive Tools 工具列           │
│  │                              （訪談 / 問卷 / 購買意願評估）     │
│  └── PurchaseIntentPanel.vue   ★ 購買意願評估面板（被 Step5 觸發） │
└──────────────────────────────────────────────────────────────────┘
                              ↓ REST API
┌──────────────────────────────────────────────────────────────────┐
│  Backend (Flask + Python)                                        │
│  ├── api/                                                        │
│  │   ├── graph.py                       圖譜建構 / 重置 / 查詢    │
│  │   ├── simulation.py                  模擬 / 訪談 / 購買評估    │
│  │   └── report.py                      ReportAgent 對話         │
│  ├── services/                                                   │
│  │   ├── text_processor.py              文件解析（PDF / MD）     │
│  │   ├── ontology_generator.py          本體論生成（產業特化）   │
│  │   ├── graph_builder.py               GraphRAG 建構            │
│  │   ├── oasis_profile_generator.py     Zep 實體 → AI 人設       │
│  │   ├── simulation_runner.py           OASIS 子程序管理         │
│  │   ├── simulation_manager.py          模擬狀態 / 結果讀寫       │
│  │   ├── simulation_ipc.py              Runner ↔ Worker 通訊     │
│  │   ├── llm_cost_estimator.py          費用粗估服務             │
│  │   ├── purchase_intent_evaluator.py   ★ 購買意願評估服務        │
│  │   ├── report_agent.py                ReACT 報告生成 Agent     │
│  │   ├── zep_tools.py                   Zep 圖譜檢索工具         │
│  │   ├── zep_entity_reader.py           實體節點讀取             │
│  │   └── zep_graph_memory_updater.py    Agent 記憶動態更新       │
│  ├── scripts/                                                    │
│  │   ├── run_parallel_simulation.py     ★ 主模擬腳本（雙平台並行） │
│  │   ├── run_twitter_simulation.py                               │
│  │   └── run_reddit_simulation.py                                │
│  └── models/project.py                  專案管理                  │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  外部服務 / 框架                                                  │
│  ├── camel-oasis    社群模擬框架（Camel-AI 開源，主引擎）         │
│  ├── Zep Cloud      圖譜 + 時序記憶                               │
│  ├── OpenRouter     LLM 服務（OpenAI 介面相容，便宜）              │
│  └── PyTorch/Transformers  推薦系統 / 句子嵌入（OASIS 內部用）     │
└──────────────────────────────────────────────────────────────────┘
```

### 關鍵技術名詞（白話版）

| 名詞 | 一句話解釋 |
|---|---|
| **GraphRAG** | 把文件變成「知識圖譜」，AI 查資料比一般 RAG 精準很多 |
| **OASIS** | 開源的多 Agent 社群模擬框架，可模擬上百萬個 AI 用戶 |
| **Zep** | 時序記憶系統，讓每個 Agent「記得」自己的過去 |
| **ReACT** | 讓 AI 用「想 → 做 → 反思」循環產出深度報告 |
| **Hidden 5-dim meter** | 每個 agent 內部的 5 維敏感度，**藏起來不直接顯示** |

### 後端 API 重要端點

| Endpoint | 方法 | 功能 |
|---|---|---|
| `/api/graph/build` | POST | 上傳文件 → 建 GraphRAG |
| `/api/simulation/create` | POST | 建立模擬 |
| `/api/simulation/cost-estimate` | GET | 模擬前費用粗估 |
| `/api/simulation/start` | POST | 啟動雙平台並行模擬 |
| `/api/simulation/<id>/run-status` | GET | 模擬實時狀態 |
| `/api/simulation/<id>/profiles` | GET | Agent 人設清單 |
| `/api/simulation/<id>/actions` | GET | 全部社群動作 |
| `/api/simulation/<id>/purchase-intent` | POST/GET | ★ 購買意願評估 |
| `/api/simulation/interview/batch` | POST | 跟多位 Agent 對話 |
| `/api/report/generate` | POST | 啟動 ReportAgent 寫報告 |

---

## 八、真實使用案例 — 「一碗」快閃飯店驗證

讓我們用 `examples/business_idea_popup_restaurant.md` 跑一次完整流程。

### Step 1：創業者的點子

> **「一碗」是台北東區單品快閃飯店，菜單只賣「日式溏心蛋牛肉燴飯」，
> NT$280，鎖定東區辦公族午餐市場。**

老闆最想驗證的 5 個問題：
1. NT$280 對東區上班族是「划算」還是「貴」？
2. 「只賣一道菜」是「專注」還是「沒選擇 → 不去」？
3. 如果有人發負評，輿情會發酵到什麼程度？
4. 跟「鬍鬚張」、「八方雲集」的勝率多高？
5. 月後加推第二款飯，老客戶會買單還是覺得失焦？

### Step 2：MiroFish 自動建立的虛擬市場

從計劃書裡，系統會抽出這些角色當 Agent：
- **東區上班族**（25–40 歲、月薪 4–8 萬，分外商 / 本土兩派）
- **美食 KOL**（小資女 / 上班族男性食記 / 抖音食評）
- **競品店家粉絲**（鬍鬚張、八方雲集老顧客）
- **IG 美學重視者**（網美、Threads 重度使用者）
- **餐飲業同行**（會酸、會跟風）
- **路人**（午餐預算只有 NT$120，根本不會買）

### Step 3：模擬出來的真實社群動態

雙平台跑 30 輪後可能會看到：
- Info Plaza（Twitter-like）：開幕當天某美食 KOL po 出溏心蛋切開照，2 小時內被轉 50 次，#東區午餐革命 開始發酵
- Topic Community（Reddit-like）：有人開長文吐槽「NT$280 一碗飯太貴」，獲 80 個讚、200 條留言
- 一位東區外商上班族 Agent **連續 3 輪都在發負評**（因為他覺得 NT$280 應該包飲料）
- 一位餐飲同行 Agent 在嘲諷「這種模式撐不過 6 個月」，獲 30 個讚

### Step 4：購買意願評估的結果（虛擬例）

| 指標 | 數字 |
|---|---|
| 總體購買率 | **47%** |
| **目標客群（TA）購買率** | **78%** |
| **路人購買率** | **18%** |
| 平均決策信心 | 71 |

**為什麼會買 % 歸因**：
1. emotional_resonance（情感共鳴）— 31%
2. social_buzz_positive（社群正向聲量）— 24%
3. urgency（限時優惠）— 18%

**為什麼不買 % 歸因**：
1. price_sensitivity（價格敏感）— 38%
2. skepticism（對廣告懷疑）— 22%
3. social_buzz_negative（社群負評）— 15%

### 老闆從這份報告學到什麼？

✅ **TA 鎖定是對的**：78% 購買率代表你的 TA 定義精準
⚠️ **「只賣一道菜」沒問題，但「NT$280」是最大阻力**：38% 不買是因為價格 → 考慮加 NT$240 商業午餐選項
✅ **IG 美照真的有用**：情感共鳴貢獻 31% 的買單，繼續放大美照行銷
⚠️ **要小心輿情翻車**：15% 路人因為「社群負評」不買 → 開幕第一週要嚴密監控 Threads，第一條負評要回得快

**這份洞察，市調公司要花 5 萬，MiroFish 花 0.5 美金 + 5 分鐘。**

---

## 九、商業模式

| 方案 | 對象 | 價格 | 內容 |
|---|---|---|---|
| **Free** | 個人嘗鮮 | $0 | 每月 1 次模擬，最多 100 個 Agent |
| **Solo Founder** | 一人公司 | $29 / 月 | 每月 10 次模擬，最多 1,000 個 Agent，全部購買意願評估 |
| **Startup** | 小型團隊 | $199 / 月 | 不限次數，最多 10,000 Agent + 報告匯出 + 多人協作 |
| **Sandbox+** | 通過虛擬驗證者 | 報價制 | 實體沙盒場域 + 真實消費者測試 |
| **Enterprise** | 中大型客戶 | 客製 | 私有部署 + API + 客製人格資料庫 + SLA |

---

## 十、產品路線圖

### Phase 1｜v0.3 Founder Edition（現況）✅
- ✅ 文件 → GraphRAG 圖譜
- ✅ Agent 人設自動生成
- ✅ 雙平台並行模擬（Info Plaza + Topic Community）
- ✅ ReportAgent 寫報告
- ✅ Agent 訪談對話
- ✅ LLM 費用粗估 + 模型推薦
- ✅ **購買意願評估**（5 維 hidden meter + Info Plaza 訊號 + TA 分群 + 歸因 %）
- ✅ Windows 一鍵啟動 `run.bat` / `stop.bat`

### Phase 2｜短期（3 個月內）
- [ ] 一人公司專屬儀表板（多模擬比較）
- [ ] 產業模板（餐飲、3C、美妝、SaaS、服飾）
- [ ] A/B 雙策略對照模擬（同一群 agent 跑 2 套廣告）
- [ ] 競品反應模擬（「如果鬍鬚張看到一碗開幕，他會做什麼？」）
- [ ] 商業 KPI 圖表（觸及人數、轉換率、風險分數）

### Phase 3｜中期（6 個月）
- [ ] **實體沙盒場域上線**（公司核心競爭力）
- [ ] 廠商客戶授權人格資料庫
- [ ] 歷史事件回測，證明準確度
- [ ] Persona Marketplace（虛擬消費者群包）

### Phase 4｜長期（1 年）
- [ ] 百萬級 Agent 規模
- [ ] 跨平台模擬（IG、TikTok、Threads）
- [ ] 真實數據即時校準
- [ ] 創投對接平台

---

## 十一、合規與隱私

我們嚴格遵守：
- 🇹🇼 **台灣個人資料保護法**
- 🇪🇺 **歐盟 GDPR**
- **差分隱私（Differential Privacy）** 處理所有人格資料

所有虛擬消費者皆為：
- ✅ 統計合成（基於公開市調資料 + 學術資料集）
- ✅ 完全匿名，無法回推到任何真人
- ✅ 廠商上傳的客戶資料皆需明確授權同意書

---

## 十二、簡報快速對照（拿出去 pitch 用）

### 一句話版本
> **「給一人公司用的虛擬市場驗證器，5 分鐘告訴你點子會不會紅。」**

### 三句話版本
> 「創業最大的成本不是錢，是把錯的點子做出來。
> MiroFish 讓你在燒錢之前，先用 1,000 個會互相吵架的 AI 消費者預演一次。
> 配合公司的實體沙盒場域，我們提供完整的『虛擬 → 實體 → 募資』創業驗證鏈，
> 是亞洲第一個給一人公司用的科學化創業基礎設施。」

### 三大賣點
1. **虛擬市場預演**：$0.5、5 分鐘，比焦點訪談便宜 10,000 倍
2. **實體沙盒場域**：本公司獨家，把驗證過的點子放進真實市場
3. **創投對接通路**：從想法直通可投資項目，創業變成科學

### Demo 必講的 3 個亮點

1. **「上傳即生成」的爽感**
   隨便丟一份 PDF，10 秒內螢幕上爬出一張完整知識圖譜 + 50 個有頭有臉的 AI Agent
2. **「會吵起來的社群」殺手級展示**
   秀模擬時間軸給觀眾看：「Lin 說好吃 → Wang 反駁太貴 → KOL 加入戰局 → 30 輪後變成翻車事件」
3. **「我可以直接問 AI 為什麼不買」**
   點任一張 REJECT 卡，問 Agent「你為什麼覺得太貴？」、「如果降到 NT$240 你會買嗎？」
   AI 用她的人設+記憶回答你 — 這比任何問卷都直接

### 預期問題與回答

**Q: 預測準確度怎麼證明？**
A: 用「歷史事件回測」—— 把過去某產品上市前的資料餵進系統，預測結果跟真實市場反應比對。
這是金融業在用的證明方法。Phase 3 會公開回測報告。

**Q: AI 消費者真的夠真實嗎？**
A: 目前是 GraphRAG + LLM 推論生成 + Zep 時序記憶。
下一階段會建立「多源人格資料庫」，整合公開學術資料 + 市調報告 + 廠商授權資料，
並用差分隱私處理。

**Q: 為什麼一人公司會付錢？**
A: 因為他們最缺市場研究預算，也最怕踩雷。
$29/月換來「上線前的安全感」+ 「跟創投談判時的數據佐證」 = 最甘願花的錢。

**Q: 跟 ChatGPT 直接問有什麼不同？**
A: ChatGPT 給你「平均答案」。
MiroFish 模擬的是 1,000 個有不同背景、會互相影響、會發酵翻車的真實社群動態 ——
這是 ChatGPT 永遠做不到的事。

**Q: 為什麼是現在這個時間點？**
A: 三件事剛好對齊：
- LLM 推理成本一年降 10 倍（2024 跑一次要 $50，2026 只要 $0.5）
- OASIS 等開源模擬框架成熟（2024 才公開發布）
- 一人公司 / 獨立創業者爆發（YC 2025 Demo Day 80% 是 1–3 人團隊）

---

## 十三、團隊與聯絡

- **GitHub**：[github.com/666ghj/MiroFish](https://github.com/666ghj/MiroFish)
- **公司網站**：（待補）
- **商務合作**：（待補）

### 想參與的話

- 🐛 **找到 bug**：開 GitHub Issue
- 💡 **有功能建議**：發 PR 或 Discussion
- 💼 **想當 beta 用戶**：聯絡團隊（待補）
- 💰 **想投資 / 合作**：聯絡團隊（待補）

---

## License

待補（暫定 Apache 2.0 或 BSL）

---

> ## **「讓創業不再是賭博，而是可驗證、可迭代、可投資的科學。」**
>
> — MiroFish Founder Program · v0.3
