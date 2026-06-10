# MiroFish

> **烧钱前，先让 1,000 个 AI 消费者帮你跑一轮。**
> 上传 PDF / Markdown / 文字 → 看谁会买、谁会酸、为什么。

[![Status](https://img.shields.io/badge/status-v0.3%20Founder%20Edition-purple)]()
[![Stack](https://img.shields.io/badge/stack-Vue3%20%2B%20Flask%20%2B%20OASIS-blue)]()
[![License](https://img.shields.io/badge/license-TBD-lightgrey)]()

---

## 这是什么？

**文件 → GraphRAG（Zep）→ 大量有差异的 Agent → OASIS 双平台社群模拟（类 Twitter + 类 Reddit）→ 报告、访谈、问卷、购买意愿评估。**

和「叫 ChatGPT 扮演一百种人」不同：这里的 Agent **会互相看帖子、点赞、留言、被风向影响**，并有 **时序记忆**（不会每轮人格乱跳）。

## TL;DR — 30 秒看懂

| | 传统做法 | MiroFish |
|---|---|---|
| **想知道点子会不会红** | 直接做 MVP 烧几十万 | 5 分钟虚拟模拟，~$0.50 |
| **想知道目标用户怎么想** | 焦点访谈（1 场 5–20 万） | 直接跟任何一位 AI 消费者对话 |
| **想知道广告会不会被喷** | 上线投广告再看数据 | 上线前 1,000 个 AI 在虚拟 Twitter / Reddit 先吵一轮 |
| **想知道谁会买** | 等付款数据 | 「目标客群 80% 会买、路人只有 20% 会买」直接告诉你 |
| **想知道为什么不买** | 看评论 / 退货单 | 「33% 因为价格、22% 因为不信任」可行动归因 % |

---

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- OpenRouter API Key
- Zep Cloud API Key

### Windows（推荐）

双击 **`run.bat`**：自动检查依赖、启动后端 `5001`、前端 `5173`、并打开浏览器。
第一次安装可能需要 **5–10 分钟**（含较大的 Python 套件）。

关闭用 **`stop.bat`**。

### macOS / Linux（手动）

```bash
# 后端
cd backend && python -m venv .venv && source .venv/bin/activate
pip install --ignore-requires-python flask flask-cors python-dotenv zep-cloud httpx pypdf camel-oasis
export FLASK_APP=app && flask run --port 5001

# 前端（新终端）
cd frontend && npm install && npm run dev
```

### 配置 `.env`

复制 `.env.example` 为 `.env`，至少填入：

```bash
LLM_API_KEY=sk-***...
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=google/gemini-2.5-flash-lite
ZEP_API_KEY=***
```

> ⚠️ **`.env` 不会被提交到 Git**（已在 `.gitignore` 中排除）。

---

## 五步流程

1. **上传** 你的点子 → `examples/business_idea_solo_freelancer_app.md`
2. **建图谱** 本本体论 + GraphRAG，从文件抽出「会出现在你市场周遭」的角色
3. **生成 Agent** 完整人设（年龄、职业、兴趣、MBTI、口头禅、偏见）
4. **跑模拟** Info Plaza（类 Twitter）+ Topic Community（类 Reddit），多轮多 Agent 并行互动
5. **看结果** 深度报告 + 交互工具：跟任意 Agent 对话、发问卷、评估购买意愿

---

## 核心功能

### 🔥 虚拟社群模拟

- 每个 AI Agent 有**独立的年龄、职业、MBTI、兴趣、口头禅、偏见**
- Agent 之间**会互相看帖子、点赞、反驳、转发、被影响**
- 系统会出现**真实社群才有的「群体效应」**：意见领袖、酸民、跟风、舆情翻车
- 基于 [OASIS](https://github.com/camel-ai/oasis) 框架（类 Twitter + 类 Reddit 双平台）

### 🔥 从你的文件生成 Agent

```
你上传的 PDF / Markdown
        ↓
LLM 萃取里面提到的人、组织、品牌、地点、事件
        ↓
建成 GraphRAG 知识图谱（用 Zep Cloud）
        ↓
每个图谱节点 → 一个有真实背景的 AI Agent
```

### 🔥 时序记忆

每个 Agent 挂在 Zep 的时序记忆系统上，会记住：
- 上一轮自己发过什么帖子
- 上一轮谁反驳过自己
- 自己对这个品牌过去抱怨过几次

行为连贯、会「黑掉」、会「真爱粉」，跟真人一样。

### 🔥 购买意愿评估（v0.3 旗舰功能）

直接接入模拟出来的社群行为，不是单独测广告：

- 每位 Agent：**隐藏 5 维心理敏感度** + **真实社群行为** → 综合判断 BUY / REJECT
- 分**目标客群（TA）**与**路人**，分开算购买率
- 输出「为什么买 / 为什么不买」的**百分比归因**（12 个因子细拆）
- 结果写入 `purchase_intent.json`，下次可从面板载入不必重跑

---

## 项目结构

```
MiroFish/
├── backend/
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 核心服务
│   │   ├── utils/         # 工具
│   │   └── config.py      # 配置
│   ├── scripts/           # 独立脚本
│   └── .venv/             # Python 虚拟环境（不纳入 Git）
├── frontend/
│   ├── src/
│   │   ├── views/         # 页面
│   │   ├── components/    # 组件
│   │   ├── api/           # API 客户端
│   │   ├── assets/        # 静态资源
│   │   ├── router/        # 路由
│   │   └── store/         # 状态管理
│   ├── index.html
│   └── package.json
├── examples/              # 示例商业计划
├── static/                # 图片资源
├── .env.example           # 环境变量模板
├── .gitignore
├── run.bat                # Windows 一键启动
├── stop.bat               # Windows 一键关闭
└── README.md
```

---

## 技术栈

| 层级 | 技术 |
|---|---|
| 前端 | Vue 3 + Vite |
| 后端 | Flask + Flask-CORS |
| 模拟框架 | [OASIS](https://github.com/camel-ai/oasis) (Camel-AI) |
| 记忆 / 图谱 | Zep Cloud (GraphRAG + 时序记忆) |
| LLM | OpenRouter（OpenAI 兼容 API） |

主要 API：`/api/graph/build`、`/api/simulation/start`、`/api/simulation/<id>/run-status`、`/api/simulation/<id>/purchase-intent`

---

## 路线图

| 阶段 | 时间 | 目标 |
|---|---|---|
| Phase 1 | 已完成 | 五步流程跑通，v0.3 发布 |
| Phase 2 | 近期 | 压力测试 + 一人公司内测 |
| Phase 3 | 中期（6 个月） | 实体沙盒场域 + 历史事件回测 |
| Phase 4 | 长期（1 年） | 百万级 Agent 规模 + 跨平台模拟 |

---

## 参与贡献

- 🐛 **发现 Bug**：开 GitHub Issue
- 💡 **功能建议**：发 PR 或 Discussion
- 📝 **改进文档**：直接编辑 README

---

## License

待定（暂定 Apache 2.0 或 BSL）

---

> **「让创业不再是赌博，而是可验证、可迭代、可投资的科学。」**
>
> — MiroFish Founder Program · v0.3
