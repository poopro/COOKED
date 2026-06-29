<template>
  <section class="history-database">
    <header class="section-header">
      <div class="section-line"></div><span class="section-title">{{ t('history') }}</span><div class="section-line"></div>
    </header>

    <div v-if="loading" class="loading-state">
      <span class="loading-spinner"></span><span class="loading-text">{{ t('loading') }}</span>
    </div>

    <div v-else-if="projects.length === 0" class="empty-state">
      <div class="empty-title">{{ t('empty_title') }}</div>
      <p>{{ t('empty_body') }}</p>
      <button class="action-btn" type="button" @click="loadHistory">{{ t('reload') }}</button>
    </div>

    <div v-else class="cards-container">
      <article v-for="project in projects" :key="`${project.history_type || 'simulation'}-${project.simulation_id}`" class="project-card">
        <div class="card-header">
          <span class="card-id">{{ formatSimulationId(project.simulation_id) }}</span>
          <span class="card-progress" :class="getProgressClass(project)">{{ formatRounds(project) }}</span>
        </div>
        <h3 class="card-title">{{ getHistoryTitle(project) }}</h3>
        <p class="card-desc">{{ truncateText(project.simulation_requirement || t('no_requirement'), 96) }}</p>
        <div class="card-meta"><span>{{ formatDate(project.created_at) }}</span><span>{{ formatTime(project.created_at) }}</span><span>{{ statusLabel(project.runner_status || project.status || 'idle') }}</span></div>
        <div class="cooked-meter">
          <div class="meter-head"><span>COOKED METER</span><strong>{{ cookedMeter(project).score }}%</strong></div>
          <div class="meter-track"><span :style="{ width: cookedMeter(project).score + '%' }"></span></div>
          <small>{{ cookedLabel(project) }} ? {{ cookedReason(project) }}</small>
        </div>
        <div class="card-actions">
          <button class="action-btn primary" type="button" @click="goToProject(project)">{{ t('open_run') }}</button>
          <button v-if="project.report_id" class="action-btn success" type="button" @click="openReport(project)">{{ t('open_report') }}</button>
          <button v-else class="action-btn muted" type="button" disabled>{{ t('no_report') }}</button>
          <button class="action-btn" type="button" @click="openReplay(project)">{{ t('replay') }}</button>
          <button v-if="project.history_type !== 'project'" class="action-btn danger" type="button" :disabled="deletingId === project.simulation_id" @click="deleteHistory(project)">{{ deletingId === project.simulation_id ? t('deleting') : t('delete') }}</button>
        </div>
      </article>
    </div>

    <Teleport to="body">
      <Transition name="modal">
        <div v-if="replayProject" class="replay-overlay" @click.self="closeReplay">
          <div class="replay-modal">
            <header class="replay-header"><div><span class="replay-kicker">COOKED? {{ t('replay') }}</span><h2>{{ getSimulationTitle(replayProject.simulation_requirement) }}</h2></div><button class="icon-close" type="button" @click="closeReplay" :aria-label="t('close')">x</button></header>
            <div class="replay-body">
              <aside class="replay-stage-list"><button v-for="(slide, idx) in replaySlides" :key="slide.key" type="button" class="stage-dot" :class="{ active: idx === replayIndex, done: idx < replayIndex }" @click="replayIndex = idx"><span>{{ String(idx + 1).padStart(2, '0') }}</span>{{ slide.title }}</button></aside>
              <Transition name="slide-pop" mode="out-in"><section :key="currentSlide.key" class="replay-slide"><div class="slide-label">{{ t('stage') }} {{ replayIndex + 1 }} / {{ replaySlides.length }}</div><h3>{{ currentSlide.title }}</h3><p>{{ currentSlide.body }}</p><div class="slide-facts"><div v-for="fact in currentSlide.facts" :key="fact.label" class="fact-row"><span>{{ fact.label }}</span><strong>{{ fact.value }}</strong></div></div></section></Transition>
            </div>
            <footer class="replay-footer"><button class="action-btn" type="button" :disabled="replayIndex === 0" @click="prevSlide">{{ t('prev') }}</button><div class="replay-progress"><span v-for="(_, idx) in replaySlides" :key="idx" :class="{ active: idx <= replayIndex }"></span></div><button class="action-btn primary" type="button" @click="nextSlide">{{ replayIndex === replaySlides.length - 1 ? t('restart') : t('next') }}</button></footer>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSimulationHistory, deleteSimulation } from '../api/simulation'

const zh = {
  history: '歷史模擬', loading: '正在載入歷史紀錄...', empty_title: '還沒有任何模擬紀錄', empty_body: '上傳一個點子，COOKED? 會在這裡保存每次市場推演。', reload: '重新載入', no_requirement: '未提供模擬需求', open_run: '啟動推演', open_report: '查看最終報告', no_report: '尚未生成報告', replay: '重播', deleting: '刪除中', delete: '刪除', close: '關閉', stage: '階段', prev: '上一頁', next: '下一頁', restart: '重新播放', unnamed: '未命名模擬', not_started: '未開始', ready: '就緒', running: '推演中', stopped: '已停止', completed: '已完成', failed: '失敗', idle: '閒置', preparing: '準備中', cooked: '已烹飪', not_cooked: '尚未烹飪', partial: '部分烹飪警告', reason_role: '依角色配比計算', reason_risk: '依報告風險分數計算', reason_status: '依推演狀態與報告計算', reason_wait: '等待更多結果', input_idea: '輸入點子', saved_none: '此次模擬沒有保存任何文件需求', sim_id: '模擬編號', created: '建立時間', graph_build: '知識圖譜建立', graph_body: '系統將 pitch、文件與設定整理成可被代理角色引用的市場圖譜。', project: '專案', graph: '知識圖譜', agents: '代理角色生成', agents_body: '共同角色被饋食成廣場的不同聲音。', agent_count: '角色數量', run: '市場推演', run_body: '模擬以加速時間進行，見證辯論、批評與爭論的發酵。', progress: '進度', status: '狀態', platform: '平台', outcome: '結果與下一步', outcome_done: '此次模擬已有最終報告，可直接檢視報告與版本向導。', outcome_wait: '此次模擬尚未有最終報告，建議先完成推演再產生終極結果。', final_report: '最終報告', generated: '已生成', not_generated: '尚未生成', score: 'Cooked 分數', version: '版本'
}
const t = (key) => zh[key] || key
const router = useRouter()
const projects = ref([])
const loading = ref(false)
const deletingId = ref('')
const replayProject = ref(null)
const replayIndex = ref(0)

const normalizeHistoryResponse = (response) => Array.isArray(response?.data) ? response.data : (Array.isArray(response?.data?.data) ? response.data.data : [])
const fetchHistoryFallback = (limit = 30) => new Promise((resolve, reject) => {
  const xhr = new XMLHttpRequest()
  xhr.open('GET', `http://localhost:5001/api/simulation/history?limit=${limit}`, true)
  xhr.timeout = 15000
  xhr.onload = () => {
    try {
      if (xhr.status < 200 || xhr.status >= 300) throw new Error(`HTTP ${xhr.status}`)
      const payload = JSON.parse(xhr.responseText || '{}')
      resolve(Array.isArray(payload.data) ? payload.data : [])
    } catch (error) {
      reject(error)
    }
  }
  xhr.onerror = () => reject(new Error('history connection failed'))
  xhr.ontimeout = () => reject(new Error('history timeout'))
  xhr.send()
})
const loadHistory = async () => {
  loading.value = true
  try {
    const response = await Promise.race([
      getSimulationHistory(30),
      new Promise((_, reject) => setTimeout(() => reject(new Error('history timeout')), 8000))
    ])
    projects.value = normalizeHistoryResponse(response)
  } catch {
    try {
      projects.value = await fetchHistoryFallback(30)
    } catch {
      projects.value = []
    }
  } finally {
    loading.value = false
  }
}

const cookedMeter = (project) => project?.cooked_meter || { score: 50, label: 'PARTIALLY COOKED', reason: 'fallback' }
const cookedLabel = (project) => cookedMeter(project).label === 'COOKED' ? t('cooked') : (cookedMeter(project).label === 'NOT COOKED YET' ? t('not_cooked') : t('partial'))
const cookedReason = (project) => { const reason = cookedMeter(project).reason || ''; if (reason.includes('角色') || reason === 'role_mix_pressure') return t('reason_role'); if (reason.includes('風險') || reason === 'report_risk_score') return t('reason_risk'); if (reason.includes('推演') || reason === 'run_status_and_report') return t('reason_status'); return t('reason_wait') }
const replaySlides = computed(() => {
  const project = replayProject.value
  if (!project) return []
  const total = project.total_rounds || 0
  const current = project.current_round || 0
  return [
    { key:'idea', title:t('input_idea'), body:project.simulation_requirement || t('saved_none'), facts:[{label:t('sim_id'), value:formatSimulationId(project.simulation_id)}, {label:t('created'), value:`${formatDate(project.created_at)} ${formatTime(project.created_at)}`}] },
    { key:'knowledge', title:t('graph_build'), body:t('graph_body'), facts:[{label:t('project'), value:project.project_id || '-'}, {label:t('graph'), value:project.graph_id || '-'}] },
    { key:'agents', title:t('agents'), body:t('agents_body'), facts:[{label:t('agent_count'), value:project.profiles_count || project.entities_count || 0}] },
    { key:'run', title:t('run'), body:t('run_body'), facts:[{label:t('progress'), value: total ? `${current}/${total}` : t('not_started')}, {label:t('status'), value:statusLabel(project.runner_status || project.status || 'idle')}, {label:t('platform'), value:platformLabel(project)}] },
    { key:'outcome', title:t('outcome'), body: project.report_id ? t('outcome_done') : t('outcome_wait'), facts:[{label:t('final_report'), value: project.report_id ? t('generated') : t('not_generated')}, {label:t('score'), value:`${cookedMeter(project).score}% ? ${cookedLabel(project)}`}, {label:t('version'), value:project.version || 'local'}] }
  ]
})
const currentSlide = computed(() => replaySlides.value[replayIndex.value] || replaySlides.value[0] || { key:'empty', title:'', body:'', facts:[] })
const openReplay = (project) => { replayProject.value = project; replayIndex.value = 0 }
const closeReplay = () => { replayProject.value = null; replayIndex.value = 0 }
const nextSlide = () => { replayIndex.value = replayIndex.value >= replaySlides.value.length - 1 ? 0 : replayIndex.value + 1 }
const prevSlide = () => { if (replayIndex.value > 0) replayIndex.value -= 1 }
const openReport = (project) => { if (project?.report_id) router.push({ name:'Report', params:{ reportId: project.report_id } }) }
const goToProject = (project) => { if (project?.project_id) router.push({ name:'Process', params:{ projectId: project.project_id } }); else if (project?.simulation_id) router.push({ name:'Simulation', params:{ simulationId: project.simulation_id } }) }
const deleteHistory = async (project) => { const id = project?.simulation_id; if (!id || !window.confirm(`${t('delete')} ${formatSimulationId(id)}?`)) return; try { deletingId.value = id; await deleteSimulation(id); projects.value = projects.value.filter((item) => item.simulation_id !== id); if (replayProject.value?.simulation_id === id) closeReplay() } finally { deletingId.value = '' } }
const getProgressClass = (s) => { const c=s.current_round||0, total=s.total_rounds||0; if(!total||!c) return 'not-started'; return c>=total?'completed':'in-progress' }
const formatDate = (v) => { if(!v) return ''; const d=new Date(v); return Number.isNaN(d.getTime()) ? String(v).slice(0,10) : d.toISOString().slice(0,10) }
const formatTime = (v) => { if(!v) return ''; const d=new Date(v); return Number.isNaN(d.getTime()) ? '' : `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}` }
const truncateText = (text, n) => !text ? '' : (text.length > n ? `${text.slice(0,n)}...` : text)
const getSimulationTitle = (v) => { if(!v) return t('unnamed'); const clean=v.replace(/\s+/g,' ').trim(); return clean.length>24 ? `${clean.slice(0,24)}...` : clean }
const getHistoryTitle = (project) => getSimulationTitle(project?.simulation_requirement || project?.project_name || project?.name)
const formatSimulationId = (id) => !id ? 'SIM_UNKNOWN' : (id.startsWith('proj_') ? `PROJ_${id.replace('proj_','').slice(0,6).toUpperCase()}` : `SIM_${id.replace('sim_','').slice(0,6).toUpperCase()}`)
const formatRounds = (s) => { const c=s.current_round||0, total=s.total_rounds||0; return total ? `${c}/${total}` : t('not_started') }
const platformLabel = (p) => Array.isArray(p.platform_tags)&&p.platform_tags.length ? p.platform_tags.join(' + ') : [p.enable_reddit?'Reddit':'', p.enable_twitter?'X/Twitter':''].filter(Boolean).join(' + ') || 'Plaza'
const statusLabel = (s) => ({ready:t('ready'), running:t('running'), stopped:t('stopped'), completed:t('completed'), failed:t('failed'), idle:t('idle'), preparing:t('preparing')}[s] || s)
onMounted(loadHistory)
</script>

<style scoped>
.history-database{position:relative;width:100%;margin-top:40px;padding:38px 0 44px}.section-header{display:flex;align-items:center;gap:14px;margin-bottom:22px}.section-line{flex:1;height:1px;background:#111;opacity:.28}.section-title,.card-id,.card-progress,.card-meta,.replay-kicker,.slide-label{font-family:'JetBrains Mono','Courier New',monospace;font-size:11px;font-weight:800;letter-spacing:.04em;text-transform:uppercase}.cards-container{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px}.project-card{min-height:280px;display:flex;flex-direction:column;gap:14px;padding:18px;border:2px solid #111;background:rgba(250,248,242,.96);box-shadow:8px 8px 0 rgba(17,17,17,.12)}.card-header,.card-meta,.card-actions,.replay-footer{display:flex;align-items:center;gap:10px}.card-header{justify-content:space-between}.card-progress{border:1px solid #111;padding:5px 8px}.card-progress.completed{background:#111;color:#f7f1df}.card-progress.in-progress{background:#d9ff66}.card-title{margin:0;font-size:22px;line-height:1.08;font-weight:900}.card-desc{margin:0;color:#363636;line-height:1.55;font-size:14px}.card-meta{margin-top:auto;color:#555;flex-wrap:wrap}.cooked-meter{display:grid;gap:7px;padding:10px;border:1px solid rgba(17,17,17,.28);background:rgba(255,255,255,.42)}.meter-head{display:flex;justify-content:space-between;font-family:'JetBrains Mono','Courier New',monospace;font-size:11px;font-weight:900}.meter-head strong{font-size:18px}.meter-track{height:8px;border:1px solid #111;background:#f7f1df;overflow:hidden}.meter-track span{display:block;height:100%;background:linear-gradient(90deg,#d9ff66,#ff6a3d)}.card-actions{border-top:1px solid rgba(17,17,17,.18);padding-top:12px;flex-wrap:wrap}.action-btn{min-height:34px;padding:0 12px;border:1px solid #111;background:transparent;color:#111;font-weight:800;cursor:pointer}.action-btn.primary{background:#111;color:#f7f1df}.action-btn.success{background:#d9ff66}.action-btn.muted{opacity:.58;cursor:not-allowed}.action-btn.danger{margin-left:auto;border-color:#a32929;color:#a32929}.loading-state,.empty-state{display:grid;place-items:center;gap:10px;min-height:180px;text-align:center}.loading-spinner{width:24px;height:24px;border:2px solid rgba(17,17,17,.22);border-top-color:#111;border-radius:50%;animation:spin .8s linear infinite}.empty-title{font-size:24px;font-weight:900}.replay-overlay{position:fixed;inset:0;z-index:3000;display:grid;place-items:center;padding:28px;background:rgba(17,17,17,.5);backdrop-filter:blur(8px)}.replay-modal{width:min(1040px,100%);max-height:min(760px,92vh);display:flex;flex-direction:column;border:2px solid #111;background:#f7f1df;box-shadow:18px 18px 0 rgba(17,17,17,.32);overflow:hidden}.replay-header{display:flex;justify-content:space-between;gap:16px;padding:22px 24px;border-bottom:2px solid #111}.icon-close{width:38px;height:38px;border:1px solid #111;background:transparent;font-size:22px}.replay-body{min-height:420px;display:grid;grid-template-columns:240px 1fr}.replay-stage-list{display:flex;flex-direction:column;gap:8px;padding:18px;border-right:2px solid #111;overflow:auto}.stage-dot{text-align:left;border:1px solid rgba(17,17,17,.3);background:transparent;padding:10px;font-weight:800}.stage-dot.active,.stage-dot.done{background:#111;color:#f7f1df}.replay-slide{padding:34px;display:flex;flex-direction:column;justify-content:center}.replay-slide h3{margin:8px 0 12px;font-size:clamp(28px,5vw,58px);line-height:.95}.slide-facts{display:grid;gap:8px;margin-top:22px;max-width:620px}.fact-row{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid rgba(17,17,17,.2);padding-bottom:8px}.replay-footer{justify-content:space-between;padding:16px 20px;border-top:2px solid #111}.replay-progress{display:flex;gap:5px}.replay-progress span{width:28px;height:4px;background:rgba(17,17,17,.2)}.replay-progress span.active{background:#111}@keyframes spin{to{transform:rotate(360deg)}}@media(max-width:760px){.replay-body{grid-template-columns:1fr}.replay-stage-list{border-right:0;border-bottom:2px solid #111}.action-btn.danger{margin-left:0}}
</style>
