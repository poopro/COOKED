# COOKED?

<p align="center">
  <img src="frontend/public/cooked-logo.svg" alt="COOKED? logo" width="420">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-v0.3%20Founder%20Edition-purple" alt="Status">
  <img src="https://img.shields.io/badge/frontend-Vue%203%20%2B%20Vite-42b883" alt="Frontend">
  <img src="https://img.shields.io/badge/backend-Flask%20%2B%20Python-3776ab" alt="Backend">
  <img src="https://img.shields.io/badge/license-AGPL--3.0-blue" alt="License">
  <img src="https://img.shields.io/badge/modified%20from-666ghj%2FMiroFish-orange" alt="Modified from 666ghj/MiroFish">
</p>

> English and Traditional Chinese documentation for COOKED?, a local-first virtual market testing lab.
>
> COOKED? 的英文與繁體中文說明文件：一個本機優先的虛擬市場測試沙盒。

- [English](#english)
- [繁體中文](#繁體中文)
- [License and Attribution](#license-and-attribution--授權與來源)

---

## English

COOKED? is a local-first virtual market testing lab for early product ideas, startup pitches, campaigns, and positioning experiments. Upload a PDF, Markdown file, or plain text idea, then let the system turn it into a simulated public conversation with AI agents, graph memory, social dynamics, and a final market-readiness report.

The short version: COOKED? helps you learn whether an idea is compelling before you spend real money building, launching, or pitching it.

This repository is a modified version of [666ghj/MiroFish](https://github.com/666ghj/MiroFish). The original project is licensed under the GNU Affero General Public License v3.0, and this modified version keeps that license. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

### What COOKED? Does

COOKED? simulates how a product idea might be received by different groups of people. It is not just a chatbot that says whether an idea is good. The app builds a miniature market environment, generates agent personas, runs conversations across social-style platforms, and turns the result into a report.

```text
Upload idea or document
        |
        v
Extract entities, claims, value props, risks, and target users
        |
        v
Build a graph-backed project memory
        |
        v
Generate simulated public roles and stakeholder agents
        |
        v
Run a dual-platform discussion
        |
        v
Score purchase intent, objections, risks, and next moves
        |
        v
Produce a report you can use for iteration
```

### Why It Exists

Most early-stage validation is slow, expensive, or too polite to be useful.

Focus groups can be expensive. Surveys often flatten nuance. A normal LLM chat can give a neat answer, but it usually does not create disagreement, social pressure, second-order reactions, or changing opinions over time.

COOKED? is built for the messy middle:

- Will people understand the idea?
- Who gets excited first?
- Who attacks it?
- What are the strongest objections?
- Does the pitch survive social discussion?
- Which features sound valuable, and which sound fake?
- Is the idea undercooked, overhyped, niche, or actually promising?

It is meant to be a fast pre-flight simulator for product judgment. It does not replace real users, but it can help you reach real users with sharper questions.

### Core Features

#### Document-Based Idea Intake

Upload an idea as PDF, Markdown, or text. COOKED? parses the content and extracts the market context it needs for simulation.

Useful inputs include startup one-pagers, product requirement drafts, landing page copy, pitch decks exported as PDF, campaign concepts, feature specs, research notes, and founder memos.

#### GraphRAG-Style Project Memory

COOKED? organizes your uploaded material into a graph-backed memory layer. Agents can refer back to the project context instead of responding from generic assumptions only.

This is useful when your idea has specific constraints, named competitors, stakeholders, pricing, user segments, or launch channels.

#### Simulated Public Agents

The system generates diverse agents representing customers, critics, vendors, observers, and other market voices. They are designed to disagree, react, question, and influence each other.

That makes the output more useful than a single averaged response.

#### Dual-Platform Social Simulation

COOKED? models two different social surfaces:

- A fast, short-form discussion environment
- A slower, thread-oriented community environment

The same idea can perform differently depending on the social context. A punchy consumer product might spread well in one environment and get torn apart in another.

#### Purchase Intent and Risk Evaluation

The report layer summarizes signals such as purchase motivation, trust, price sensitivity, social proof, differentiation, adoption friction, competitive pressure, confusing claims, messaging gaps, and critical objections.

The goal is not to produce a magic score. The goal is to show why the score happened.

#### History and Replay

The modified COOKED? build includes history-oriented UI work so previous runs can be reviewed. This is useful when comparing revisions of the same idea.

### Who It Is For

COOKED? is especially useful for:

- Solo founders testing an idea before building an MVP
- Indie hackers checking whether a landing page sounds believable
- Students preparing product or entrepreneurship projects
- Marketers stress-testing campaign angles
- Product managers comparing feature narratives
- Researchers exploring simulated public opinion workflows
- Builders who want a private local sandbox before exposing an idea

### What It Is Not

COOKED? is not a real market study. It does not replace real customer interviews, sales calls, paid acquisition tests, usability testing, legal review, financial review, medical review, or production-grade forecasting.

Treat the output as a structured simulation, not as truth. The best use is to find hypotheses, objections, and blind spots faster.

### Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3, Vite, D3 |
| Backend | Python, Flask |
| Memory and graph layer | Zep Cloud integration |
| LLM provider | OpenRouter-compatible API configuration |
| Simulation scripts | Python-based parallel social simulation |
| File parsing | PDF and text parsing utilities |
| Local launch | Windows batch scripts, manual Unix-style commands |

### Repository Structure

```text
COOKED/
├── backend/
│   ├── app/
│   │   ├── api/                  # Flask API routes
│   │   ├── models/               # Data models
│   │   ├── services/             # Graph, simulation, reports, LLM calls
│   │   └── utils/                # Logging, parsing, locale, retry helpers
│   ├── scripts/                  # Simulation runners
│   └── start-backend.bat         # Windows backend launcher
├── frontend/
│   ├── public/                   # Static browser assets
│   ├── src/
│   │   ├── api/                  # Frontend API clients
│   │   ├── assets/               # Logo and visual assets
│   │   ├── components/           # Vue components
│   │   ├── router/               # Vue Router setup
│   │   └── views/                # App screens
│   └── start-frontend.bat        # Windows frontend launcher
├── examples/                     # Demo startup ideas
├── locales/                      # UI language strings
├── static/                       # Static images
├── run.bat                       # Windows one-click launcher
├── stop.bat                      # Windows stopper
├── LICENSE                       # AGPL-3.0 license text
└── NOTICE                        # Upstream attribution and modification notice
```

### Requirements

Install these before running the app:

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- An OpenRouter-compatible API key
- A Zep Cloud API key and tenant ID

The project is designed for local development. Keep credentials in `.env`; do not commit real keys.

### Quick Start on Windows

The easiest path is:

```bat
run.bat
```

The launcher starts:

- Backend API on `http://localhost:5001`
- Frontend app on `http://localhost:5173`

To stop the local services:

```bat
stop.bat
```

There are also separate launchers if you want to run each side manually:

```bat
backend\start-backend.bat
frontend\start-frontend.bat
```

### Manual Setup

Backend:

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS or Linux
source .venv/bin/activate

pip install --ignore-requires-python flask flask-cors python-dotenv zep-cloud httpx pypdf camel-oasis
set FLASK_APP=app
flask run --port 5001
```

On macOS or Linux, use `export FLASK_APP=app` instead of `set FLASK_APP=app`.

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

### Environment Variables

Create a `.env` file in the project root or configure the equivalent environment variables for your shell.

```env
LLM_API_KEY=sk-or-v1-your-openrouter-key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=google/gemini-2.5-flash-lite

ZEP_API_KEY=your-zep-api-key
ZEP_TENANT_ID=your-zep-tenant-id
```

Optional acceleration variables may be supported by the simulation scripts:

```env
LLM_BOOST_API_KEY=sk-or-v1-your-second-key
LLM_BOOST_BASE_URL=https://openrouter.ai/api/v1
LLM_BOOST_MODEL_NAME=your-fast-model
```

Never commit `.env`, API keys, generated uploads, logs, or local virtual environments.

### Running a Demo

The `examples/` folder contains sample idea documents that can be uploaded directly into the app.

Good first tests:

- `examples/business_idea_solo_freelancer_app.md`
- `examples/business_idea_popup_restaurant.md`
- `examples/business_idea_risky_dating_app.md`

Suggested demo flow:

1. Start the app with `run.bat`.
2. Open the frontend.
3. Upload one of the example Markdown files.
4. Let COOKED? build the graph.
5. Generate the simulation environment.
6. Run the social simulation.
7. Generate the final report.
8. Change the original idea and run it again to compare outcomes.

### Product Workflow

1. Upload a rough product idea, memo, or plan.
2. Build a graph-oriented project memory from the upload.
3. Generate simulated roles and discussion settings.
4. Run the social simulation.
5. Review the final report and revise the idea.

### Example Questions COOKED? Can Help Answer

- Is the target user obvious from the pitch?
- Which segment reacts most positively?
- What part of the idea sounds fake or overclaimed?
- What would competitors attack?
- Does the product need a narrower wedge?
- Is the pricing believable?
- Which messaging angle creates the strongest interest?
- What needs to change before a landing page test?
- What should be asked in real customer interviews?

### Development Notes

Useful commands:

```bash
# Frontend production build
cd frontend
npm run build

# Backend syntax check
cd ..
python -m compileall backend/app
```

The current app is optimized for local experimentation, not hardened production deployment. Before hosting it publicly, review authentication, file upload limits, API key handling, CORS settings, rate limits, worker isolation, log retention, and Zep project separation.

### Security and Privacy

COOKED? is intended to run locally. Your uploaded ideas and generated simulation data should stay on your own machine unless you configure external services or deploy the app elsewhere.

Important reminders:

- Do not commit `.env`.
- Do not commit real uploaded customer documents.
- Do not commit generated logs or simulation output.
- Rotate any API key that was accidentally exposed.
- Review third-party service terms before uploading sensitive documents.

---

## 繁體中文

COOKED? 是一個本機優先的虛擬市場測試沙盒，適合用來測試早期產品點子、創業企劃、行銷活動、定位假設與簡報敘事。你可以上傳 PDF、Markdown 或純文字，系統會把你的想法轉成一場由 AI 代理人、圖譜記憶、社群互動與最終報告組成的市場模擬。

一句話說：COOKED? 讓你在真正花錢開發、投廣告、找客戶、找投資人之前，先看見一個點子可能會怎麼被理解、質疑、喜歡或打臉。

本倉庫修改自 [666ghj/MiroFish](https://github.com/666ghj/MiroFish)。原始專案採用 GNU Affero General Public License v3.0，本修改版也保留相同授權。請見 [LICENSE](LICENSE) 與 [NOTICE](NOTICE)。

### COOKED? 在做什麼

COOKED? 不是單純問聊天機器人「這個點子好不好」。它會建立一個迷你的市場環境，從你的文件中抽取脈絡，產生不同立場的代理人，讓他們在類社群平台中互動，最後整理成可讀的市場回饋報告。

```text
上傳點子或文件
        |
        v
萃取實體、主張、價值、風險與目標使用者
        |
        v
建立圖譜化專案記憶
        |
        v
生成不同角色與利害關係人代理人
        |
        v
執行雙平台社群討論
        |
        v
評估購買意願、反對理由、風險與下一步
        |
        v
產生可用來迭代的報告
```

### 為什麼需要它

早期驗證常常太慢、太貴，或太客氣。

焦點訪談很花錢，問卷容易把細節壓扁；一般 LLM 對話雖然很快，但通常只會給你一個整理過的平均答案，不會自然產生爭論、社群壓力、二次反應與時間序列上的態度變化。

COOKED? 主要用來處理這些問題：

- 使用者看得懂這個點子嗎？
- 誰會第一個感興趣？
- 誰會反對或吐槽？
- 最強的反對理由是什麼？
- 這個 pitch 放進社群討論後還站得住嗎？
- 哪些功能聽起來有價值，哪些聽起來很假？
- 這個點子是還沒煮熟、過度包裝、太小眾，還是真的有機會？

它不是用來取代真人使用者，而是幫你更快找到假設、盲點與下一輪真人訪談該問的問題。

### 核心功能

#### 文件式點子輸入

你可以上傳 PDF、Markdown 或純文字。COOKED? 會解析內容，抽取市場模擬需要的背景資訊。

適合上傳的內容包括：

- 創業 one-pager
- 產品需求草稿
- Landing page 文案
- Pitch deck 匯出的 PDF
- 行銷活動概念
- 功能規格
- 研究筆記
- 創辦人 memo

#### GraphRAG 式專案記憶

COOKED? 會把你的文件整理成圖譜化記憶，讓代理人可以根據你的實際內容反應，而不是只靠通用常識亂猜。

如果你的點子包含特定競品、定價、目標族群、利害關係人、使用情境或上市渠道，這一層會特別有用。

#### 模擬公眾代理人

系統會生成不同角色的代理人，例如潛在客戶、批評者、競品觀察者、供應商、一般旁觀者等。這些代理人會彼此影響、質疑、附和、反駁與改變立場。

這比單一平均答案更接近「點子被丟進市場後會發生什麼」。

#### 雙平台社群模擬

COOKED? 模擬兩種不同社群表面：

- 快速、短訊息、容易擴散的討論環境
- 較慢、較長文、偏社群討論串的環境

同一個點子在不同社群脈絡下可能會有完全不同的結果。短影音爆點型產品可能在一個環境很強，在另一個環境被問到破功。

#### 購買意願與風險評估

報告會整理多種訊號，例如：

- 購買動機
- 信任感
- 價格敏感度
- 社會證明
- 差異化
- 採用阻力
- 競爭壓力
- 模糊或誇大的主張
- 訊息缺口
- 關鍵反對理由

重點不是產生一個神奇分數，而是讓你看懂為什麼會得到這個結果。

#### 歷史與重播

此 COOKED? 修改版加入了歷史與重播相關的介面工作，方便回看過去的推演結果，也適合比較同一個點子不同版本之間的差異。

### 適合誰使用

COOKED? 特別適合：

- 想在做 MVP 前先測試點子的 solo founder
- 想知道 landing page 聽起來可不可信的 indie hacker
- 準備創業或產品專題的學生
- 想壓測行銷角度的 marketer
- 想比較功能敘事的 product manager
- 研究模擬公眾意見流程的人
- 想先在本機私密測試，再把點子拿出去問真人的 builder

### 它不是什麼

COOKED? 不是正式市場研究，也不能取代真人訪談、銷售電話、投放測試、可用性測試、法律審查、財務審查、醫療審查或真正的預測系統。

請把輸出視為結構化模擬，而不是真理。最好的用法是更快找到假設、反對理由與盲點。

### 技術棧

| 層級 | 技術 |
|---|---|
| 前端 | Vue 3, Vite, D3 |
| 後端 | Python, Flask |
| 記憶與圖譜 | Zep Cloud integration |
| LLM 供應商 | OpenRouter-compatible API configuration |
| 模擬腳本 | Python-based parallel social simulation |
| 檔案解析 | PDF and text parsing utilities |
| 本機啟動 | Windows batch scripts, manual Unix-style commands |

### 專案結構

```text
COOKED/
├── backend/
│   ├── app/
│   │   ├── api/                  # Flask API 路由
│   │   ├── models/               # 資料模型
│   │   ├── services/             # 圖譜、模擬、報告、LLM 呼叫
│   │   └── utils/                # logging、解析、locale、retry helper
│   ├── scripts/                  # 模擬 runner
│   └── start-backend.bat         # Windows 後端啟動器
├── frontend/
│   ├── public/                   # 前端靜態資源
│   ├── src/
│   │   ├── api/                  # 前端 API client
│   │   ├── assets/               # logo 與視覺資源
│   │   ├── components/           # Vue components
│   │   ├── router/               # Vue Router 設定
│   │   └── views/                # App 畫面
│   └── start-frontend.bat        # Windows 前端啟動器
├── examples/                     # demo 創業點子
├── locales/                      # UI 語系字串
├── static/                       # 靜態圖片
├── run.bat                       # Windows 一鍵啟動
├── stop.bat                      # Windows 停止腳本
├── LICENSE                       # AGPL-3.0 授權文字
└── NOTICE                        # 上游來源與修改聲明
```

### 系統需求

執行前請先安裝：

- Python 3.10 或更新版本
- Node.js 18 或更新版本
- npm
- OpenRouter-compatible API key
- Zep Cloud API key 與 tenant ID

此專案主要設計給本機開發與實驗使用。請把憑證放在 `.env`，不要把真實 key commit 進 Git。

### Windows 快速開始

最簡單的方式是執行：

```bat
run.bat
```

啟動後會開：

- 後端 API：`http://localhost:5001`
- 前端 App：`http://localhost:5173`

停止服務：

```bat
stop.bat
```

如果想分開啟動前後端：

```bat
backend\start-backend.bat
frontend\start-frontend.bat
```

### 手動設定

後端：

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS or Linux
source .venv/bin/activate

pip install --ignore-requires-python flask flask-cors python-dotenv zep-cloud httpx pypdf camel-oasis
set FLASK_APP=app
flask run --port 5001
```

在 macOS 或 Linux，請把 `set FLASK_APP=app` 改成：

```bash
export FLASK_APP=app
```

前端：

```bash
cd frontend
npm install
npm run dev
```

開啟：

```text
http://localhost:5173
```

### 環境變數

在專案根目錄建立 `.env`，或用 shell 設定對應環境變數。

```env
LLM_API_KEY=sk-or-v1-your-openrouter-key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=google/gemini-2.5-flash-lite

ZEP_API_KEY=your-zep-api-key
ZEP_TENANT_ID=your-zep-tenant-id
```

模擬腳本也可能支援可選的加速模型變數：

```env
LLM_BOOST_API_KEY=sk-or-v1-your-second-key
LLM_BOOST_BASE_URL=https://openrouter.ai/api/v1
LLM_BOOST_MODEL_NAME=your-fast-model
```

不要 commit `.env`、API keys、上傳資料、logs 或虛擬環境。

### 執行 Demo

`examples/` 資料夾中有可以直接上傳的範例點子文件。

建議先試：

- `examples/business_idea_solo_freelancer_app.md`
- `examples/business_idea_popup_restaurant.md`
- `examples/business_idea_risky_dating_app.md`

建議流程：

1. 用 `run.bat` 啟動 app。
2. 開啟前端。
3. 上傳其中一個 Markdown 範例。
4. 讓 COOKED? 建立圖譜。
5. 生成模擬環境。
6. 執行社群模擬。
7. 生成最終報告。
8. 修改原本點子後再跑一次，比較兩版差異。

### 產品流程

1. 上傳粗略產品點子、memo 或企劃。
2. 從上傳內容建立圖譜化專案記憶。
3. 生成模擬角色與討論設定。
4. 執行社群模擬。
5. 閱讀最終報告，修改點子再迭代。

### COOKED? 可以幫你回答的問題

- 目標使用者是否清楚？
- 哪個族群反應最好？
- 哪一段敘事聽起來最假或最誇大？
- 競品會攻擊哪裡？
- 產品是否需要更窄的切入點？
- 定價是否可信？
- 哪個訊息角度最能產生興趣？
- 在做 landing page 測試前應該改什麼？
- 下一輪真人訪談應該問哪些問題？

### 開發備忘

常用指令：

```bash
# 前端 production build
cd frontend
npm run build

# 後端語法檢查
cd ..
python -m compileall backend/app
```

目前此 app 比較適合本機實驗，還不是已強化的 production deployment。公開部署前請檢查 authentication、file upload limits、API key handling、CORS settings、rate limits、worker isolation、log retention 與 Zep project separation。

### 安全與隱私

COOKED? 預設是本機執行。除非你自行設定外部服務或部署到雲端，否則上傳的點子與模擬資料應該保留在你的機器上。

重要提醒：

- 不要 commit `.env`。
- 不要 commit 真實客戶文件。
- 不要 commit 生成的 logs 或 simulation output。
- 如果 API key 曾經外洩，請立刻 rotate。
- 上傳敏感文件到第三方服務前，請先確認服務條款與資料政策。

---

## License and Attribution / 授權與來源

This repository is licensed under the GNU Affero General Public License v3.0. See [LICENSE](LICENSE).

Because AGPL-3.0 has network-use obligations, if you modify this project and make it available over a network, you must provide the corresponding source code under the same license. This README is not legal advice; read the license text and consult counsel if you need certainty.

本倉庫採用 GNU Affero General Public License v3.0。請見 [LICENSE](LICENSE)。

AGPL-3.0 對網路服務使用情境有原始碼提供義務。如果你修改本專案並透過網路提供服務，通常需要以相同授權提供對應原始碼。本 README 不是法律意見；若你需要法律確定性，請直接閱讀授權條款並諮詢專業人士。

COOKED? is a modified version of [666ghj/MiroFish](https://github.com/666ghj/MiroFish).

COOKED? 修改自 [666ghj/MiroFish](https://github.com/666ghj/MiroFish)。

Original basis / 原始來源：

- Repository / 倉庫：[https://github.com/666ghj/MiroFish](https://github.com/666ghj/MiroFish)
- License / 授權：GNU Affero General Public License v3.0

This modified version is maintained by `poopro` and includes COOKED? branding, launcher updates, localization work, history/replay UI additions, demo materials, and repository hygiene changes.

此修改版由 `poopro` 維護，包含 COOKED? 品牌化、啟動腳本更新、語系與在地化、歷史與重播 UI、demo 材料，以及倉庫整理等修改。

---

<p align="center"><sub>COOKED? is modified from 666ghj/MiroFish and distributed under AGPL-3.0. / COOKED? 修改自 666ghj/MiroFish，並以 AGPL-3.0 散布。</sub></p>
