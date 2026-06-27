<template>
  <div class="home-container">
    <!-- 頂部導覽列 -->
    <nav class="navbar">
      <div class="nav-brand">COOKED?</div>
      <div class="nav-links">
        <a href="https://github.com/666ghj/MiroFish" target="_blank" class="github-link">
          造訪我們的 Github 首頁 <span class="arrow">↗</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- 上半部：Hero 區 -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="orange-tag">一人公司創業點子驗證沙盒</span>
            <span class="version-text">/ v0.2-Founder Edition</span>
          </div>
          
          <h1 class="main-title">
            上傳你的點子<br>
            <span class="gradient-text">預演真實市場反應</span>
          </h1>
          
          <div class="hero-desc">
            <p>
              不用先燒錢、不用先辭職、不用先做產品。把你的<span class="highlight-bold">商業點子、產品企劃、廣告文案</span>丟進 <span class="highlight-bold">COOKED?</span>，我們會自動生成一個由<span class="highlight-orange">百萬級 AI 消費者</span>構成的虛擬市場，讓他們替你試用、討論、按讚或開酸。最後告訴你一件事 ——
            </p>
            <p class="slogan-text">
              這個點子會紅嗎？為什麼會？為什麼不會？<span class="blinking-cursor">_</span>
            </p>
            <p style="margin-top:1.5rem;font-size:0.95rem;">
              COOKED? 是為<span class="highlight-bold">一人公司、獨立開發者、小型新創團隊</span>打造的「上線前測試場」。配合本公司即將啟用的<span class="highlight-code">實體消費者沙盒基地</span>，我們讓創業不再是賭博，而是<span class="highlight-orange">可驗證、可迭代、可投資</span>的科學。
            </p>
          </div>
           
          <div class="decoration-square"></div>
        </div>
        
        <div class="hero-right">
          <!-- Logo 區 -->
          <div class="logo-container">
            <img src="../assets/logo/MiroFish_logo_left.jpeg" alt="COOKED? Logo" class="hero-logo" />
          </div>
          
          <button class="scroll-down-btn" @click="scrollToBottom">
            ↓
          </button>
        </div>
      </section>

      <!-- 下半部：雙欄版面 -->
      <section class="dashboard-section">
        <!-- 左欄：狀態與步驟 -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> 系統狀態
          </div>
          
          <h2 class="section-title">沙盒就緒</h2>
          <p class="section-desc">
            創業點子驗證場域待命。上傳你的商業計劃、產品介紹或廣告腳本，5 分鐘內生成虛擬市場反應報告
          </p>
          
          <!-- 資料指標卡片 -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">$5/次</div>
              <div class="metric-label">比焦點訪談便宜 1000 倍</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">5 分鐘</div>
              <div class="metric-label">從點子到市場反應報告</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">百萬級</div>
              <div class="metric-label">虛擬消費者並行測試</div>
            </div>
          </div>

          <!-- 專案模擬步驟說明 -->
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">◇</span> 創業驗證流程
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">理解你的點子</div>
                  <div class="step-desc">從你上傳的企劃／產品介紹／文案中，自動萃取核心賣點、目標客群與潛在風險</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">生成虛擬市場</div>
                  <div class="step-desc">自動建立目標族群的 AI 消費者群體（含人設、興趣、消費習慣、社群行為）</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">市場反應模擬</div>
                  <div class="step-desc">虛擬消費者會自動討論、轉發、按讚、開酸，重現真實社群發酵過程</div>
                </div>
             </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">會紅／不會紅？</div>
                  <div class="step-desc">產出「成敗預測報告」：成功機率、關鍵賣點、致命風險、改進建議</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">深度訪談虛擬用戶</div>
                  <div class="step-desc">想問「為什麼不買」？直接跟任何一位虛擬消費者對話，挖出真實拒絕理由</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右欄：互動主控台 -->
        <div class="right-panel">
          <div class="console-box">
            <!-- 上傳區 -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">01 / 你的點子</span>
                <span class="console-meta">商業計劃／產品介紹／文案 (PDF, MD, TXT)</span>
              </div>
              
              <div 
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />
                
                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">把你的點子丟進來</div>
                  <div class="upload-hint">商業計劃 · 產品介紹 · 廣告文案 · 任何想驗證的內容</div>
                </div>
                
                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 分割線 -->
            <div class="console-divider">
              <span>輸入參數</span>
            </div>

            <!-- 輸入區 -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">>_ 02 / 你想驗證什麼？</span>
                <span class="console-meta">越具體，預測越準</span>
              </div>

              <!-- AI 自動生成提示詞按鈕列 -->
              <div class="ai-gen-row">
                <span class="ai-gen-label">腦袋空白？讓 AI 幫你寫：</span>
                <button
                  class="ai-gen-btn"
                  type="button"
                  @click="generatePrompt('brief')"
                  :disabled="loading || !!generating"
                >
                  <span class="ai-gen-icon">✨</span>
                  <span>{{ generating === 'brief' ? '生成中...' : '簡短版' }}</span>
                </button>
                <button
                  class="ai-gen-btn extended"
                  type="button"
                  @click="generatePrompt('extended')"
                  :disabled="loading || !!generating"
                >
                  <span class="ai-gen-icon">📋</span>
                  <span>{{ generating === 'extended' ? '生成中...' : '詳細版' }}</span>
                </button>
                <button
                  v-if="formData.simulationRequirement"
                  class="ai-gen-btn ghost"
                  type="button"
                  @click="formData.simulationRequirement = ''"
                  :disabled="loading || !!generating"
                  title="清空"
                >
                  <span>清空</span>
                </button>
              </div>

              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  placeholder="// 例 1：我想推一款給獨立工作者的 AI 筆記 App，月費 199 元，目標是 25–35 歲自由接案者，會紅嗎？為什麼？&#10;&#10;// 例 2：這則 IG 廣告文案丟出去，會被消費者怎麼解讀？哪些族群會買單、哪些會反感？&#10;&#10;// 例 3：我打算在台北東區開一家『只賣一種飯』的快閃店，價格 280 元，會成功嗎？最大風險是什麼？"
                  rows="8"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">引擎: COOKED? DoomTest v0.2</div>
              </div>
            </div>

            <!-- 啟動按鈕 -->

            <!-- Local API key settings -->
            <div class="console-section api-key-section">
              <div class="console-header">
                <span class="console-label">03 / API Key &#35373;&#23450;</span>
                <span class="console-meta">&#21482;&#23384;&#22312;&#26412;&#27231;&#28687;&#35261;&#22120;&#65292;&#19981;&#26371;&#23531;&#36914; GitHub</span>
              </div>
              <div class="api-key-grid">
                <label class="api-key-field">
                  <span>OpenRouter API Key</span>
                  <input v-model="demoKeys.llmApiKey" type="password" autocomplete="off" placeholder="sk-or-v1-..." :disabled="loading" @change="saveDemoKeys" />
                </label>
                <label class="api-key-field">
                  <span>LLM Base URL</span>
                  <input v-model="demoKeys.llmBaseUrl" type="text" autocomplete="off" placeholder="https://openrouter.ai/api/v1" :disabled="loading" @change="saveDemoKeys" />
                </label>
                <label class="api-key-field">
                  <span>&#27169;&#22411;</span>
                  <input v-model="demoKeys.llmModel" type="text" autocomplete="off" placeholder="openai/gpt-4o-mini" :disabled="loading" @change="saveDemoKeys" />
                </label>
                <label class="api-key-field">
                  <span>Zep API Key&#65288;&#21487;&#36984;&#65292;&#30693;&#35672;&#22294;&#35676;&#29992;&#65289;</span>
                  <input v-model="demoKeys.zepApiKey" type="password" autocomplete="off" placeholder="&#21487;&#20808;&#30041;&#31354;&#65307;&#27794;&#26377;&#23427;&#23601;&#36339;&#36942;&#30693;&#35672;&#22294;&#35676; API" :disabled="loading" @change="saveDemoKeys" />
                </label>
              </div>
              <div class="api-key-actions">
                <button class="ai-gen-btn" type="button" @click="saveDemoKeys" :disabled="loading">&#20786;&#23384;&#26412;&#27231; API Key</button>
                <span v-if="apiKeySaved" class="api-key-saved">&#24050;&#20786;&#23384;</span>
                <span v-if="!hasDemoLLMKey" class="api-key-warning">&#35531;&#20808;&#36664;&#20837; OpenRouter API Key &#25165;&#33021;&#38283;&#22987;&#27169;&#25836;&#12290;</span>
              </div>
            </div>

            <div class="console-section btn-section">
              <button 
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!hasDemoLLMKey">&#35531;&#20808;&#36664;&#20837; API Key</span>
                <span v-else-if="!loading">&#38283;&#22987;&#39511;&#35657;&#25105;&#30340;&#40670;&#23376;</span>
                <span v-else>正在召集虛擬消費者...</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 一人公司加速器：虛擬＋實體雙沙盒 -->
      <section class="founder-section">
        <div class="founder-header">
          <span class="founder-tag">FOUNDER PROGRAM</span>
          <h2 class="founder-title">
            為什麼一人公司選 COOKED?？<br>
            <span class="founder-subtitle">業界唯一「虛擬＋實體」雙沙盒驗證</span>
          </h2>
        </div>

        <div class="founder-cards">
          <div class="founder-card">
            <div class="founder-num">01</div>
            <div class="founder-card-title">虛擬市場預演</div>
            <div class="founder-card-desc">
              百萬級 AI 消費者立即測試。$5 一次模擬，5 分鐘出報告，告訴你點子會不會紅、為什麼、為什麼不。
            </div>
            <div class="founder-card-meta">線上・立即可用</div>
          </div>

          <div class="founder-card highlight">
            <div class="founder-num">02</div>
            <div class="founder-card-title">實體沙盒場域</div>
            <div class="founder-card-desc">
              通過虛擬測試的點子，本公司提供<strong>實體快閃店面＋真實消費者</strong>測試場。把驗證過的概念直接放進真實市場，蒐集第一手資料。
            </div>
            <div class="founder-card-meta">即將啟用・限量開放</div>
          </div>

          <div class="founder-card">
            <div class="founder-num">03</div>
            <div class="founder-card-title">創投對接通路</div>
            <div class="founder-card-desc">
              通過兩階段驗證的專案，自動進入合作創投評估池。從「想法」到「可投資專案」一站到底。
            </div>
            <div class="founder-card-meta">合作中・後續推出</div>
          </div>
        </div>

        <div class="founder-flow">
          <div class="flow-step">
            <div class="flow-icon">💡</div>
            <div class="flow-label">你的點子</div>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-step">
            <div class="flow-icon">🤖</div>
            <div class="flow-label">虛擬市場預演</div>
            <div class="flow-meta">5 分鐘 · $5</div>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-step">
            <div class="flow-icon">🏪</div>
            <div class="flow-label">實體沙盒測試</div>
            <div class="flow-meta">真實消費者</div>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-step">
            <div class="flow-icon">🚀</div>
            <div class="flow-label">上市／募資</div>
          </div>
        </div>
      </section>

      <!-- 歷史專案資料庫 -->
      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'

const router = useRouter()


const DEMO_KEYS_STORAGE_KEY = 'cooked_demo_keys'

const demoKeys = ref({
  llmApiKey: '',
  llmBaseUrl: 'https://openrouter.ai/api/v1',
  llmModel: 'openai/gpt-4o-mini',
  zepApiKey: ''
})
const apiKeySaved = ref(false)

const loadDemoKeys = () => {
  try {
    const saved = JSON.parse(localStorage.getItem(DEMO_KEYS_STORAGE_KEY) || '{}') || {}
    demoKeys.value = { ...demoKeys.value, ...saved }
  } catch (err) {
    console.warn('Failed to load local API key settings:', err)
  }
}

const saveDemoKeys = () => {
  const cleaned = {
    llmApiKey: demoKeys.value.llmApiKey.trim(),
    llmBaseUrl: demoKeys.value.llmBaseUrl.trim() || 'https://openrouter.ai/api/v1',
    llmModel: demoKeys.value.llmModel.trim() || 'openai/gpt-4o-mini',
    zepApiKey: demoKeys.value.zepApiKey.trim()
  }
  demoKeys.value = cleaned
  localStorage.setItem(DEMO_KEYS_STORAGE_KEY, JSON.stringify(cleaned))
  apiKeySaved.value = true
  window.setTimeout(() => {
    apiKeySaved.value = false
  }, 1800)
}

const hasDemoLLMKey = computed(() => demoKeys.value.llmApiKey.trim().length > 0)

onMounted(loadDemoKeys)

// 表單資料
const formData = ref({
  simulationRequirement: ''
})

// 檔案列表
const files = ref([])

// 狀態
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)
const generating = ref('')  // '' | 'brief' | 'extended'

// 檔案輸入 ref
const fileInput = ref(null)

// 計算屬性：是否可提交
const canSubmit = computed(() => {
  return hasDemoLLMKey.value && formData.value.simulationRequirement.trim() !== '' && files.value.length > 0
})

// 觸發檔案選擇
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// 處理檔案選擇
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// 處理拖曳相關
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// 新增檔案
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// 移除檔案
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// 捲動到底部
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// === AI 提示詞自動生成 ===
// 簡短版模板池（每次隨機選一條，讓 demo 看起來更聰明）
const briefTemplates = [
  topic => `我想驗證「${topic}」這個點子，會紅嗎？為什麼會？為什麼不會？最大的致命風險是什麼？`,
  topic => `「${topic}」如果現在上市，目標客群會買單嗎？哪些族群會強力支持，哪些族群會反感開酸？`,
  topic => `驗證點子：${topic}。請告訴我（1）成功機率多少？（2）我有哪些沒想到的盲點？（3）三個具體改進建議`,
  topic => `「${topic}」這個點子在台灣市場會走出怎樣的路？最大的競品威脅是什麼？預算有限的情況下要先做什麼？`,
  topic => `想知道「${topic}」的市場反應：消費者會怎麼看？社群會發酵成什麼樣？我應該擔心被酸的哪些點？`
]

// 詳細版模板（結構化、專業、長）
const extendedTemplate = (topic) => `我想驗證以下創業點子：「${topic}」

【希望模擬告訴我】
1. 這個點子整體的「成功機率」（0-100%），並給出具體理由
2. 哪些族群會強力支持這個點子？為什麼？（請列出 2-3 種典型用戶畫像）
3. 哪些族群會反對甚至開酸？為什麼？（請列出他們最可能的攻擊點）
4. 跟現有競品比，我的核心優勢與劣勢分別是什麼？
5. 如果這個點子最終失敗，最有可能的「失敗模式」是什麼？（例如：市場太小？定價錯？時機不對？）
6. 三個我可能沒想到的「潛在風險」
7. 三個具體可執行的「改進建議」

【特別在意的事】
- 社群輿論的發酵速度與情緒分布
- 早期種子用戶最在意的功能或體驗是什麼
- 價格敏感度：現行定價是「划算」、「合理」還是「太貴」？
- 如果在 IG／Threads／Dcard 被討論，會是正面還是負面話題？

【模擬規模建議】
請生成多元化的虛擬消費者群體，涵蓋不同年齡、職業、消費習慣，模擬約 100~300 人的真實社群討論。`

// 從已上傳的檔名萃取「主題」
const extractTopic = () => {
  if (files.value.length === 0) {
    return '我的創業點子'
  }
  // 取第一份檔案，去掉副檔名與編號前綴
  const fileName = files.value[0].name
  const cleaned = fileName
    .replace(/\.[^.]+$/, '')
    .replace(/^business[_-]?idea[_-]?/i, '')
    .replace(/[_-]/g, ' ')
    .trim()
  return cleaned || '我的創業點子'
}

// 模擬「AI 思考」延遲（讓按鈕看起來真的在跑模型）
const simulateThinking = (ms = 800) => new Promise(resolve => setTimeout(resolve, ms))

// 主產生函式
const generatePrompt = async (mode) => {
  if (generating.value) return
  generating.value = mode

  try {
    await simulateThinking(mode === 'extended' ? 1200 : 700)

    const topic = extractTopic()

    if (mode === 'brief') {
      const tpl = briefTemplates[Math.floor(Math.random() * briefTemplates.length)]
      formData.value.simulationRequirement = tpl(topic)
    } else {
      formData.value.simulationRequirement = extendedTemplate(topic)
    }
  } finally {
    generating.value = ''
  }
}

// 開始模擬－立即跳轉，API 呼叫在 Process 頁面進行
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  
  // 儲存待上傳資料
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(files.value, formData.value.simulationRequirement)
    
    // 立即跳轉到 Process 頁面（使用特殊標識表示新建專案）
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>
/* 全域變數與重置 */
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-light: #F5F5F5;
  --gray-text: #666666;
  --border: #E5E5E5;
  /* 
    使用 Space Grotesk 作為主要標題字體，JetBrains Mono 作為程式碼／標籤字體
    請確定已在 index.html 引入上述 Google Fonts 
  */
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans TC', system-ui, sans-serif;
  --font-cn: 'Noto Sans TC', system-ui, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: var(--white);
  font-family: var(--font-sans);
  color: var(--black);
}

/* 頂部導覽 */
.navbar {
  height: 60px;
  background: var(--black);
  color: var(--white);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1.2rem;
}

.nav-links {
  display: flex;
  align-items: center;
}

.github-link {
  color: var(--white);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.github-link:hover {
  opacity: 0.8;
}

.arrow {
  font-family: sans-serif;
}

/* 主要內容區 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Hero 区域 */
.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.orange-tag {
  background: var(--orange);
  color: var(--white);
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 0.75rem;
}

.version-text {
  color: #999;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.2;
  font-weight: 500;
  margin: 0 0 40px 0;
  letter-spacing: -2px;
  color: var(--black);
}

.gradient-text {
  background: linear-gradient(90deg, #000000 0%, #444444 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--gray-text);
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: var(--black);
  font-weight: 700;
}

.highlight-orange {
  color: var(--orange);
  font-weight: 700;
  font-family: var(--font-mono);
}

.highlight-code {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--black);
  font-weight: 600;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 520;
  color: var(--black);
  letter-spacing: 1px;
  border-left: 3px solid var(--orange);
  padding-left: 15px;
  margin-top: 20px;
}

.blinking-cursor {
  color: var(--orange);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: var(--orange);
}

.hero-right {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 40px;
}

.hero-logo {
  max-width: 500px; /* 调整logo大小 */
  width: 100%;
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--orange);
  font-size: 1.2rem;
  transition: all 0.2s;
}

.scroll-down-btn:hover {
  border-color: var(--orange);
}

/* Dashboard 双栏布局 */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

/* 左侧面板 */
.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: var(--orange);
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
}

.section-desc {
  color: var(--gray-text);
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 12px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.metric-card {
  flex: 1 1 0;
  border: 1px solid var(--border);
  padding: 18px 20px;
  min-width: 130px;
  transition: all 0.2s;
}

.metric-card:hover {
  border-color: var(--orange);
  transform: translateY(-2px);
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 520;
  margin-bottom: 5px;
  color: var(--orange);
}

.metric-label {
  font-size: 0.8rem;
  color: #777;
  line-height: 1.4;
}

/* 项目模拟步骤介绍 */
.steps-container {
  border: 1px solid var(--border);
  padding: 30px;
  position: relative;
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--black);
  opacity: 0.3;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-text);
}

/* 右侧交互控制台 */
.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid #CCC; /* 外部实线 */
  padding: 8px; /* 内边距形成双重边框感 */
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
}

.upload-zone {
  border: 1px dashed #CCC;
  height: 200px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #FAFAFA;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: #F0F0F0;
  border-color: #999;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid #DDD;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #999;
}

.upload-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #999;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: var(--white);
  padding: 8px 12px;
  border: 1px solid #EEE;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #EEE;
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #BBB;
  letter-spacing: 1px;
}

/* AI 自动生成提示词按钮 */
.ai-gen-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
  padding: 10px 12px;
  background: linear-gradient(90deg, rgba(255, 69, 0, 0.04), rgba(0, 0, 0, 0.02));
  border: 1px dashed rgba(255, 69, 0, 0.25);
}

.ai-gen-label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
  margin-right: 6px;
  letter-spacing: 0.5px;
}

.ai-gen-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: 1px solid var(--black);
  background: var(--white);
  color: var(--black);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.ai-gen-btn:hover:not(:disabled) {
  background: var(--black);
  color: var(--white);
  transform: translateY(-1px);
}

.ai-gen-btn.extended {
  border-color: var(--orange);
  color: var(--orange);
}

.ai-gen-btn.extended:hover:not(:disabled) {
  background: var(--orange);
  color: var(--white);
}

.ai-gen-btn.ghost {
  border-color: #ccc;
  color: #999;
  margin-left: auto;
}

.ai-gen-btn.ghost:hover:not(:disabled) {
  background: #f5f5f5;
  color: var(--black);
}

.ai-gen-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.ai-gen-icon {
  font-size: 0.9rem;
  animation: gen-pulse 2s ease-in-out infinite;
}

@keyframes gen-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.15); }
}

.input-wrapper {
  position: relative;
  border: 1px solid #DDD;
  background: #FAFAFA;
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #AAA;
}

.start-engine-btn {
  width: 100%;
  background: var(--black);
  color: var(--white);
  border: none;
  padding: 20px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

/* 可点击状态（非禁用） */
.start-engine-btn:not(:disabled) {
  background: var(--black);
  border: 1px solid var(--black);
  animation: pulse-border 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: var(--orange);
  border-color: var(--orange);
  transform: translateY(-2px);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: #E5E5E5;
  color: #999;
  cursor: not-allowed;
  transform: none;
  border: 1px solid #E5E5E5;
}

/* 引导动画：微妙的边框脉冲 */
@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2); }
  70% { box-shadow: 0 0 0 6px rgba(0, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
}


.api-key-section {
  border-top: 1px solid #eee;
}

.api-key-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.api-key-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 0.74rem;
  color: #666;
}

.api-key-field input {
  min-width: 0;
  border: 1px solid #ddd;
  background: #fafafa;
  color: var(--black);
  padding: 10px 12px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  outline: none;
}

.api-key-field input:focus {
  border-color: var(--orange);
  background: var(--white);
}

.api-key-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.api-key-saved,
.api-key-warning {
  font-family: var(--font-mono);
  font-size: 0.74rem;
}

.api-key-saved {
  color: #0a7a38;
}

.api-key-warning {
  color: var(--orange);
}

/* Founder Section（一人公司加速器） */
.founder-section {
  margin: 80px 0 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
}

.founder-header {
  margin-bottom: 50px;
}

.founder-tag {
  display: inline-block;
  background: var(--black);
  color: var(--white);
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 2px;
  padding: 4px 10px;
  margin-bottom: 20px;
}

.founder-title {
  font-size: 2.5rem;
  line-height: 1.3;
  font-weight: 520;
  letter-spacing: -1px;
  margin: 0;
}

.founder-subtitle {
  color: var(--orange);
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 500;
}

.founder-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 60px;
}

.founder-card {
  border: 1px solid var(--border);
  padding: 30px;
  position: relative;
  transition: all 0.3s;
  background: var(--white);
}

.founder-card:hover {
  border-color: var(--black);
  transform: translateY(-4px);
  box-shadow: 6px 6px 0 var(--black);
}

.founder-card.highlight {
  background: var(--black);
  color: var(--white);
  border-color: var(--black);
}

.founder-card.highlight:hover {
  box-shadow: 6px 6px 0 var(--orange);
}

.founder-card.highlight .founder-card-meta {
  color: var(--orange);
}

.founder-num {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 700;
  opacity: 0.4;
  margin-bottom: 15px;
  letter-spacing: 1px;
}

.founder-card-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 15px;
  letter-spacing: -0.5px;
}

.founder-card-desc {
  font-size: 0.95rem;
  line-height: 1.7;
  margin-bottom: 20px;
  opacity: 0.9;
}

.founder-card.highlight .founder-card-desc {
  opacity: 0.85;
}

.founder-card-desc strong {
  color: var(--orange);
  font-weight: 700;
}

.founder-card-meta {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #999;
  letter-spacing: 1px;
  border-top: 1px solid #eee;
  padding-top: 12px;
}

.founder-card.highlight .founder-card-meta {
  border-top-color: rgba(255, 255, 255, 0.2);
}

/* Flow 流程图 */
.founder-flow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 30px;
  border: 1px dashed var(--border);
  background: #FAFAFA;
}

.flow-step {
  flex: 1;
  text-align: center;
}

.flow-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.flow-label {
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 4px;
}

.flow-meta {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--orange);
  letter-spacing: 0.5px;
}

.flow-arrow {
  font-family: var(--font-mono);
  font-size: 1.5rem;
  color: var(--orange);
  font-weight: 700;
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  
  .hero-section {
    flex-direction: column;
  }
  
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }
  
  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }


  .api-key-grid {
    grid-template-columns: 1fr;
  }

  .founder-cards {
    grid-template-columns: 1fr;
  }

  .founder-flow {
    flex-direction: column;
    gap: 20px;
  }

  .flow-arrow {
    transform: rotate(90deg);
  }

  .founder-title {
    font-size: 1.8rem;
  }

  .founder-subtitle {
    font-size: 1.1rem;
  }
}
</style>

