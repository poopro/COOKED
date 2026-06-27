const appTitle = 'COOKED? - 創業輿論模擬沙盒'

const exactText = new Map([
  ['MIROFISH', 'COOKED?'],
  ['MiroFish', 'COOKED?'],
  ['MirrorFish', 'COOKED?'],
  ['Graph Relationship Visualization', '知識圖譜關係視覺化'],
  ['Refresh', '重新整理'],
  ['Node Details', '節點詳情'],
  ['Relationship', '關係'],
  ['Entity Types', '實體類型'],
  ['Show Edge Labels', '顯示關係標籤'],
  ['Simulation ID', '模擬 ID'],
  ['Prediction Report', '預測報告'],
  ['Waiting for Report Agent...', '等待報告代理生成...'],
  ['Report Generation Complete', '報告生成完成'],
  ['Report Started', '報告已開始'],
  ['Content Ready', '內容已就緒'],
  ['Report Agent', '報告代理'],
  ['Simulation', '模擬'],
  ['You', '你'],
  ['Home', '首頁'],
  ['Start', '開始'],
  ['Stop', '停止'],
  ['Reset', '重設'],
  ['Report', '報告'],
  ['Graph', '圖譜'],
  ['Split', '雙欄'],
  ['Workbench', '工作台'],
  ['Ready', '就緒'],
  ['Running', '執行中'],
  ['Completed', '已完成'],
  ['Generating', '生成中'],
  ['Preparing', '準備中'],
  ['Error', '錯誤'],
  ['Loading...', '載入中...'],
  ['No data', '沒有資料'],
  ['Back', '返回'],
  ['Next', '下一步'],
  ['Generate', '生成'],
  ['Submit', '送出'],
  ['Save', '儲存'],
  ['Cancel', '取消'],
  ['Delete', '刪除'],
  ['Replay', '重播'],
  ['Open', '開啟'],
  ['Close', '關閉'],
  ['Name:', '名稱：'],
  ['Created:', '建立時間：'],
  ['Properties:', '屬性：'],
  ['Summary:', '摘要：'],
  ['Labels:', '標籤：'],
  ['Episodes:', '事件片段：'],
  ['Fact:', '事實：'],
  ['Type:', '類型：'],
  ['Label:', '標籤：'],
  ['Valid From:', '有效起始：'],
  ['None', '無'],
  ['Unknown', '未知'],
  ['items', '項'],
  ['RELATED', '相關'],
  ['RELATED_TO', '相關於'],
  ['Self Relations', '自我關係'],
  ['PROJECT ID', '專案 ID'],
  ['Project ID', '專案 ID'],
  ['Graph ID', '圖譜 ID'],
  ['TASK ID', '任務 ID'],
  ['Task ID', '任務 ID'],
  ['AGENT', '代理'],
  ['SYSTEM DASHBOARD', '系統儀表板'],
  ['NO_PROJECT', '沒有專案'],
])

const phraseText = [
  [/MiroFish-Founder v0\.2/g, 'COOKED? DoomTest v0.2'],
  [/MIROFISH/g, 'COOKED?'],
  [/MiroFish/g, 'COOKED?'],
  [/MirrorFish/g, 'COOKED?'],
  [/Github/g, 'GitHub'],
  [/Graph Relationship Visualization/g, '知識圖譜關係視覺化'],
  [/Prediction Report/g, '預測報告'],
  [/Report Agent/g, '報告代理'],
  [/Simulation ID/g, '模擬 ID'],
  [/Node Details/g, '節點詳情'],
  [/Entity Types/g, '實體類型'],
  [/Show Edge Labels/g, '顯示關係標籤'],
  [/Waiting for Report Agent\.\.\./g, '等待報告代理生成...'],
  [/Report Generation Complete/g, '報告生成完成'],
  [/Report Started/g, '報告已開始'],
  [/Content Ready/g, '內容已就緒'],
  [/Step\s*(\d+)\s*\/\s*(\d+)/g, '第 $1 / $2 步'],
  [/Graph/g, '圖譜'],
  [/Report/g, '報告'],
  [/Simulation/g, '模擬'],
  [/Project/g, '專案'],
  [/Agent/g, '代理'],
  [/Upload/g, '上傳'],
  [/Start/g, '開始'],
  [/Stop/g, '停止'],
  [/Error/g, '錯誤'],
  [/Loading\.\.\./g, '載入中...'],
  [/No upload payload found\. Waiting for user to start from home page\./g, '尚未找到上傳資料，請從首頁重新開始。'],
  [/No pending files found for new project\./g, '尚未找到待上傳檔案，請回首頁重新操作。'],
]

const simplifiedPairs = [
  ['图谱', '圖譜'], ['关系', '關係'], ['节点', '節點'], ['属性', '屬性'], ['实体', '實體'],
  ['显示', '顯示'], ['关闭', '關閉'], ['刷新', '重新整理'], ['还原', '還原'], ['最大化', '最大化'],
  ['创建', '建立'], ['加载', '載入'], ['失败', '失敗'], ['错误', '錯誤'], ['未知错误', '未知錯誤'],
  ['项目', '專案'], ['模拟', '模擬'], ['报告', '報告'], ['启动', '啟動'], ['停止失败', '停止失敗'],
  ['生成', '生成'], ['输入', '輸入'], ['输出', '輸出'], ['历史', '歷史'], ['记录', '紀錄'],
  ['数据', '資料'], ['文件', '檔案'], ['上传', '上傳'], ['查看', '查看'], ['选择', '選擇'],
  ['当前', '目前'], ['状态', '狀態'], ['准备', '準備'], ['完成', '完成'], ['运行', '執行'],
  ['用户', '使用者'], ['购买', '購買'], ['广告', '廣告'], ['产品', '產品'], ['服务', '服務'],
]

const attrNames = ['alt', 'title', 'aria-label', 'placeholder']
const mojibakePattern = /[\uE000-\uF8FF]|�|[\u0080-\u009F]/
const fallbackByClass = [
  ['panel-title', '知識圖譜關係視覺化'],
  ['section-title', '分析區塊'],
  ['step-name', '流程階段'],
  ['console-label', '輸入區'],
  ['console-meta', '支援 PDF、Markdown、文字檔'],
  ['model-badge', '引擎：COOKED? DoomTest v0.2'],
  ['empty-text', '等待資料生成...'],
  ['loading-text', '載入中...'],
]

function toTraditional(value) {
  return simplifiedPairs.reduce((current, [from, to]) => current.split(from).join(to), value)
}

function translateValue(value) {
  if (!value) return value
  const trimmed = value.trim()
  if (exactText.has(trimmed)) return value.replace(trimmed, exactText.get(trimmed))

  let translated = phraseText.reduce((current, [pattern, replacement]) => current.replace(pattern, replacement), value)
  translated = toTraditional(translated)
  return translated
}

function sanitizeMojibakeElement(element) {
  if (!element?.classList) return
  if (!mojibakePattern.test(element.textContent || '')) return
  for (const [className, fallback] of fallbackByClass) {
    if (element.classList.contains(className)) {
      element.textContent = fallback
      return
    }
  }
}

function translateTextNode(node) {
  const value = node.nodeValue
  const nextValue = translateValue(value)
  if (nextValue !== value) node.nodeValue = nextValue
}

function translateElement(element) {
  sanitizeMojibakeElement(element)
  attrNames.forEach((name) => {
    if (!element.hasAttribute?.(name)) return
    const value = element.getAttribute(name)
    const nextValue = translateValue(value)
    if (nextValue !== value) element.setAttribute(name, nextValue)
  })
}

function translateTree(root = document.body) {
  if (!root) return
  document.documentElement.lang = 'zh-Hant-TW'
  document.title = appTitle

  if (root.nodeType === Node.TEXT_NODE) {
    translateTextNode(root)
    return
  }

  if (root.nodeType === Node.ELEMENT_NODE) translateElement(root)

  const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT)
  while (walker.nextNode()) {
    const node = walker.currentNode
    if (node.nodeType === Node.TEXT_NODE) translateTextNode(node)
    else translateElement(node)
  }
}

function installBrandingLayer() {
  translateTree()
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => translateTree(node))
      if (mutation.type === 'characterData') translateTree(mutation.target)
      if (mutation.type === 'attributes') translateElement(mutation.target)
    })
  })

  observer.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: attrNames,
  })
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', installBrandingLayer, { once: true })
} else {
  installBrandingLayer()
}
