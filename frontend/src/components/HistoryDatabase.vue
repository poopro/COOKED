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
      <article v-for="project in projects" :key="project.simulation_id" class="project-card">
        <div class="card-header">
          <span class="card-id">{{ formatSimulationId(project.simulation_id) }}</span>
          <span class="card-progress" :class="getProgressClass(project)">{{ formatRounds(project) }}</span>
        </div>
        <h3 class="card-title">{{ getSimulationTitle(project.simulation_requirement) }}</h3>
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
          <button class="action-btn danger" type="button" :disabled="deletingId === project.simulation_id" @click="deleteHistory(project)">{{ deletingId === project.simulation_id ? t('deleting') : t('delete') }}</button>
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
  history: '\u6b77\u53f2\u6a21\u64ec', loading: '\u8f09\u5165\u6b77\u53f2\u7d00\u9304...', empty_title: '\u9084\u6c92\u6709\u6a21\u64ec\u7d00\u9304', empty_body: '\u4e0a\u50b3\u4e00\u500b\u9ede\u5b50\uff0cCOOKED? \u6703\u5728\u9019\u88e1\u4fdd\u5b58\u6bcf\u6b21\u5e02\u5834\u63a8\u6f14\u3002', reload: '\u91cd\u65b0\u8f09\u5165', no_requirement: '\u672a\u63d0\u4f9b\u6a21\u64ec\u9700\u6c42', open_run: '\u958b\u555f\u63a8\u6f14', open_report: '\u67e5\u770b\u6700\u7d42\u5831\u544a', no_report: '\u5c1a\u672a\u751f\u6210\u5831\u544a', replay: '\u91cd\u64ad', deleting: '\u522a\u9664\u4e2d', delete: '\u522a\u9664', close: '\u95dc\u9589', stage: '\u968e\u6bb5', prev: '\u4e0a\u4e00\u9801', next: '\u4e0b\u4e00\u9801', restart: '\u91cd\u65b0\u64ad\u653e', unnamed: '\u672a\u547d\u540d\u6a21\u64ec', not_started: '\u672a\u958b\u59cb', ready: '\u5c31\u7dd2', running: '\u63a8\u6f14\u4e2d', stopped: '\u5df2\u505c\u6b62', completed: '\u5df2\u5b8c\u6210', failed: '\u5931\u6557', idle: '\u5f85\u547d', preparing: '\u6e96\u5099\u4e2d', cooked: '\u5df2\u7d93\u70e4\u7126', not_cooked: '\u9084\u6c92\u70e4\u7126', partial: '\u534a\u719f\u8b66\u6212', reason_role: '\u4f9d\u89d2\u8272\u6c60\u58d3\u529b\u4f30\u7b97', reason_risk: '\u4f9d\u5831\u544a\u98a8\u96aa\u5206\u6578\u4f30\u7b97', reason_status: '\u4f9d\u63a8\u6f14\u72c0\u614b\u8207\u5831\u544a\u4f30\u7b97', reason_wait: '\u7b49\u5f85\u66f4\u591a\u7d50\u679c', input_idea: '\u8f38\u5165\u9ede\u5b50', saved_none: '\u9019\u6b21\u6a21\u64ec\u6c92\u6709\u4fdd\u5b58\u6587\u5b57\u9700\u6c42\u3002', sim_id: '\u6a21\u64ec\u7de8\u865f', created: '\u5efa\u7acb\u6642\u9593', graph_build: '\u77e5\u8b58\u5716\u8b5c\u5efa\u7acb', graph_body: '\u7cfb\u7d71\u628a pitch\u3001\u6587\u4ef6\u8207\u8a2d\u5b9a\u6574\u7406\u6210\u53ef\u88ab\u4ee3\u7406\u89d2\u8272\u5f15\u7528\u7684\u5e02\u5834\u80cc\u666f\u3002', project: '\u5c08\u6848', graph: '\u77e5\u8b58\u5716\u8b5c', agents: '\u4ee3\u7406\u89d2\u8272\u751f\u6210', agents_body: '\u516c\u5171\u89d2\u8272\u88ab\u8f49\u6210 plaza \u88e1\u7684\u4e0d\u540c\u8072\u97f3\u3002', agent_count: '\u89d2\u8272\u6578', run: '\u5e02\u5834\u63a8\u6f14', run_body: '\u6a21\u64ec\u4ee5\u52a0\u901f\u6642\u9593\u524d\u9032\uff0c\u89c0\u5bdf\u8a0e\u8ad6\u3001\u885d\u7a81\u8207\u8206\u8ad6\u64f4\u6563\u3002', progress: '\u9032\u5ea6', status: '\u72c0\u614b', platform: '\u5e73\u53f0', outcome: '\u7d50\u679c\u8207\u4e0b\u4e00\u6b65', outcome_done: '\u9019\u6b21\u6a21\u64ec\u5df2\u6709\u6700\u7d42\u5831\u544a\uff0c\u53ef\u4ee5\u76f4\u63a5\u67e5\u770b\u98a8\u96aa\u8207\u6539\u7248\u65b9\u5411\u3002', outcome_wait: '\u9019\u6b21\u6a21\u64ec\u9084\u6c92\u6709\u5831\u544a\uff0c\u5efa\u8b70\u5148\u8dd1\u5b8c\u63a8\u6f14\u518d\u751f\u6210\u7e3d\u7d50\u3002', final_report: '\u6700\u7d42\u5831\u544a', generated: '\u5df2\u751f\u6210', not_generated: '\u5c1a\u672a\u751f\u6210', score: 'Cooked \u5206\u6578', version: '\u7248\u672c'
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
  const xhr = new XMLHttpRequest(); xhr.open('GET', `http://localhost:5001/api/simulation/history?limit=${limit}`, true); xhr.timeout = 15000
  xhr.onload = () => { try { if (xhr.status < 200 || xhr.status >= 300) throw new Error(`HTTP ${xhr.status}`); const payload = JSON.parse(xhr.responseText || '{}'); resolve(Array.isArray(payload.data) ? payload.data : []) } catch (error) { reject(error) } }
  xhr.onerror = () => reject(new Error('history connection failed')); xhr.ontimeout = () => reject(new Error('history timeout')); xhr.send()
})
const loadHistory = async () => { loading.value = true; try { const response = await Promise.race([getSimulationHistory(30), new Promise((_, reject) => setTimeout(() => reject(new Error('history timeout')), 8000))]); projects.value = normalizeHistoryResponse(response) } catch { try { projects.value = await fetchHistoryFallback(30) } catch { projects.value = [] } } finally { loading.value = false } }

const cookedMeter = (project) => project?.cooked_meter || { score: 50, label: 'PARTIALLY COOKED', reason: 'fallback' }
const cookedLabel = (project) => cookedMeter(project).label === 'COOKED' ? t('cooked') : (cookedMeter(project).label === 'NOT COOKED YET' ? t('not_cooked') : t('partial'))
const cookedReason = (project) => { const reason = cookedMeter(project).reason || ''; if (reason.includes('\u89d2\u8272') || reason === 'role_mix_pressure') return t('reason_role'); if (reason.includes('\u98a8\u96aa') || reason === 'report_risk_score') return t('reason_risk'); if (reason.includes('\u63a8\u6f14') || reason === 'run_status_and_report') return t('reason_status'); return t('reason_wait') }
const replaySlides = computed(() => { const project = replayProject.value; if (!project) return []; const total = project.total_rounds || 0; const current = project.current_round || 0; return [
  { key:'idea', title:t('input_idea'), body:project.simulation_requirement || t('saved_none'), facts:[{label:t('sim_id'), value:formatSimulationId(project.simulation_id)}, {label:t('created'), value:`${formatDate(project.created_at)} ${formatTime(project.created_at)}`}] },
  { key:'knowledge', title:t('graph_build'), body:t('graph_body'), facts:[{label:t('project'), value:project.project_id || '-'}, {label:t('graph'), value:project.graph_id || '-'}] },
  { key:'agents', title:t('agents'), body:t('agents_body'), facts:[{label:t('agent_count'), value:project.profiles_count || project.entities_count || 0}] },
  { key:'run', title:t('run'), body:t('run_body'), facts:[{label:t('progress'), value: total ? `${current}/${total}` : t('not_started')}, {label:t('status'), value:statusLabel(project.runner_status || project.status || 'idle')}, {label:t('platform'), value:platformLabel(project)}] },
  { key:'outcome', title:t('outcome'), body: project.report_id ? t('outcome_done') : t('outcome_wait'), facts:[{label:t('final_report'), value: project.report_id ? t('generated') : t('not_generated')}, {label:t('score'), value:`${cookedMeter(project).score}% ? ${cookedLabel(project)}`}, {label:t('version'), value:project.version || 'local'}] }
]})
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
const formatSimulationId = (id) => !id ? 'SIM_UNKNOWN' : `SIM_${id.replace('sim_','').slice(0,6).toUpperCase()}`
const formatRounds = (s) => { const c=s.current_round||0, total=s.total_rounds||0; return total ? `${c}/${total}` : t('not_started') }
const platformLabel = (p) => Array.isArray(p.platform_tags)&&p.platform_tags.length ? p.platform_tags.join(' + ') : [p.enable_reddit?'Reddit':'', p.enable_twitter?'X/Twitter':''].filter(Boolean).join(' + ') || 'Plaza'
const statusLabel = (s) => ({ready:t('ready'), running:t('running'), stopped:t('stopped'), completed:t('completed'), failed:t('failed'), idle:t('idle'), preparing:t('preparing')}[s] || s)
onMounted(loadHistory)
</script>

<style scoped>
.history-database{position:relative;width:100%;margin-top:40px;padding:38px 0 44px}.section-header{display:flex;align-items:center;gap:14px;margin-bottom:22px}.section-line{flex:1;height:1px;background:#111;opacity:.28}.section-title,.card-id,.card-progress,.card-meta,.replay-kicker,.slide-label{font-family:'JetBrains Mono','Courier New',monospace;font-size:11px;font-weight:800;letter-spacing:.04em;text-transform:uppercase}.cards-container{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px}.project-card{min-height:280px;display:flex;flex-direction:column;gap:14px;padding:18px;border:2px solid #111;background:rgba(250,248,242,.96);box-shadow:8px 8px 0 rgba(17,17,17,.12)}.card-header,.card-meta,.card-actions,.replay-footer{display:flex;align-items:center;gap:10px}.card-header{justify-content:space-between}.card-progress{border:1px solid #111;padding:5px 8px}.card-progress.completed{background:#111;color:#f7f1df}.card-progress.in-progress{background:#d9ff66}.card-title{margin:0;font-size:22px;line-height:1.08;font-weight:900}.card-desc{margin:0;color:#363636;line-height:1.55;font-size:14px}.card-meta{margin-top:auto;color:#555;flex-wrap:wrap}.cooked-meter{display:grid;gap:7px;padding:10px;border:1px solid rgba(17,17,17,.28);background:rgba(255,255,255,.42)}.meter-head{display:flex;justify-content:space-between;font-family:'JetBrains Mono','Courier New',monospace;font-size:11px;font-weight:900}.meter-head strong{font-size:18px}.meter-track{height:8px;border:1px solid #111;background:#f7f1df;overflow:hidden}.meter-track span{display:block;height:100%;background:linear-gradient(90deg,#d9ff66,#ff6a3d)}.card-actions{border-top:1px solid rgba(17,17,17,.18);padding-top:12px;flex-wrap:wrap}.action-btn{min-height:34px;padding:0 12px;border:1px solid #111;background:transparent;color:#111;font-weight:800;cursor:pointer}.action-btn.primary{background:#111;color:#f7f1df}.action-btn.success{background:#d9ff66}.action-btn.muted{opacity:.58;cursor:not-allowed}.action-btn.danger{margin-left:auto;border-color:#a32929;color:#a32929}.loading-state,.empty-state{display:grid;place-items:center;gap:10px;min-height:180px;text-align:center}.loading-spinner{width:24px;height:24px;border:2px solid rgba(17,17,17,.22);border-top-color:#111;border-radius:50%;animation:spin .8s linear infinite}.empty-title{font-size:24px;font-weight:900}.replay-overlay{position:fixed;inset:0;z-index:3000;display:grid;place-items:center;padding:28px;background:rgba(17,17,17,.5);backdrop-filter:blur(8px)}.replay-modal{width:min(1040px,100%);max-height:min(760px,92vh);display:flex;flex-direction:column;border:2px solid #111;background:#f7f1df;box-shadow:18px 18px 0 rgba(17,17,17,.32);overflow:hidden}.replay-header{display:flex;justify-content:space-between;gap:16px;padding:22px 24px;border-bottom:2px solid #111}.icon-close{width:38px;height:38px;border:1px solid #111;background:transparent;font-size:22px}.replay-body{min-height:420px;display:grid;grid-template-columns:240px 1fr}.replay-stage-list{display:flex;flex-direction:column;gap:8px;padding:18px;border-right:2px solid #111;overflow:auto}.stage-dot{text-align:left;border:1px solid rgba(17,17,17,.3);background:transparent;padding:10px;font-weight:800}.stage-dot.active,.stage-dot.done{background:#111;color:#f7f1df}.replay-slide{padding:34px;display:flex;flex-direction:column;justify-content:center}.replay-slide h3{margin:8px 0 12px;font-size:clamp(28px,5vw,58px);line-height:.95}.slide-facts{display:grid;gap:8px;margin-top:22px;max-width:620px}.fact-row{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid rgba(17,17,17,.2);padding-bottom:8px}.replay-footer{justify-content:space-between;padding:16px 20px;border-top:2px solid #111}.replay-progress{display:flex;gap:5px}.replay-progress span{width:28px;height:4px;background:rgba(17,17,17,.2)}.replay-progress span.active{background:#111}@keyframes spin{to{transform:rotate(360deg)}}@media(max-width:760px){.replay-body{grid-template-columns:1fr}.replay-stage-list{border-right:0;border-bottom:2px solid #111}.action-btn.danger{margin-left:0}}
</style>
