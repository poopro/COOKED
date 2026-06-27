
<template>
  <div class="env-setup-panel cooked-step2">
    <div class="scroll-container">
      <section class="step-card hero-card">
        <div class="step-header">
          <div>
            <span class="step-index">STEP 02</span>
            <h2>&#x6A21;&#x64EC;&#x74B0;&#x5883;&#x8A2D;&#x5B9A;</h2>
          </div>
          <span class="badge" :class="phase >= 4 ? 'success' : 'processing'">{{ phase >= 4 ? '\u8a2d\u5b9a\u5b8c\u6210' : '\u6e96\u5099\u4e2d' }}</span>
        </div>
        <p class="description">COOKED? &#x6703;&#x6839;&#x64DA;&#x4F60;&#x7684;&#x9EDE;&#x5B50;&#x3001;&#x77E5;&#x8B58;&#x5716;&#x8B5C;&#x8207;&#x6587;&#x4EF6;&#x5167;&#x5BB9;&#xFF0C;&#x751F;&#x6210;&#x516C;&#x5171;&#x89D2;&#x8272;&#x3001;&#x8A0E;&#x8AD6;&#x7BC0;&#x594F;&#x8207;&#x63A8;&#x6F14;&#x53C3;&#x6578;&#x3002;</p>
        <div class="info-grid">
          <div class="info-item"><span>&#x5C08;&#x6848; ID</span><strong>{{ projectData?.project_id || '\u5c1a\u672a\u8f09\u5165' }}</strong></div>
          <div class="info-item"><span>&#x5716;&#x8B5C; ID</span><strong>{{ projectData?.graph_id || '\u5c1a\u672a\u8f09\u5165' }}</strong></div>
          <div class="info-item"><span>&#x4EFB;&#x52D9; ID</span><strong>{{ taskId || '\u7b49\u5f85\u5efa\u7acb' }}</strong></div>
        </div>
      </section>

      <section class="step-card character-card">
        <div class="step-header compact">
          <div><span class="step-index">CAST</span><h3>&#x89D2;&#x8272;&#x6C60;&#x914D;&#x7F6E;</h3></div>
          <span class="badge processing">{{ totalCharacterCount }} ???</span>
        </div>
        <p class="description">&#x5148;&#x8A2D;&#x5B9A;&#x5BA2;&#x6236;&#x3001;&#x7AF6;&#x54C1;&#x8207;&#x5176;&#x4ED6;&#x516C;&#x5171;&#x89D2;&#x8272;&#x7684;&#x6578;&#x91CF;&#xFF1B;&#x793E;&#x7FA4;&#x5E73;&#x53F0;&#x53EA;&#x662F;&#x767C;&#x8A00;&#x6A19;&#x7C64;&#xFF0C;&#x4E0D;&#x6703;&#x88AB;&#x7576;&#x6210;&#x5716;&#x8B5C;&#x5BE6;&#x9AD4;&#x3002;</p>
        <div class="character-controls">
          <label><span>&#x6F5B;&#x5728;&#x5BA2;&#x6236;</span><input type="number" min="0" max="200" v-model.number="characterSettings.customer_count" /></label>
          <label><span>&#x7AF6;&#x54C1; / Vendor</span><input type="number" min="0" max="80" v-model.number="characterSettings.vendor_count" /></label>
          <label><span>&#x5176;&#x4ED6;&#x516C;&#x5171;&#x89D2;&#x8272;</span><input type="number" min="0" max="120" v-model.number="characterSettings.other_count" /></label>
        </div>
        <div class="platform-block">
          <span class="mini-label">&#x5E73;&#x53F0;&#x767C;&#x8A00;&#x6A19;&#x7C64;</span>
          <div class="platform-tags">
            <button v-for="tag in platformOptions" :key="tag" type="button" class="tag-pill" :class="{ active: characterSettings.platform_tags.includes(tag) }" @click="togglePlatformTag(tag)">{{ tag }}</button>
          </div>
        </div>
        <button class="start-btn secondary" type="button" :disabled="phase > 0 && phase < 4" @click="startPrepareSimulation">{{ phase > 0 && phase < 4 ? '\u6b63\u5728\u751f\u6210\u89d2\u8272\u6c60' : '\u5957\u7528\u8a2d\u5b9a\u4e26\u751f\u6210\u6a21\u64ec\u74b0\u5883' }}</button>
      </section>

      <section class="step-card">
        <div class="step-header compact">
          <div><span class="step-index">??</span><h3>&#x516C;&#x5171;&#x89D2;&#x8272;&#x751F;&#x6210;</h3></div>
          <span class="badge" :class="phase > 1 ? 'success' : 'pending'">{{ phase > 1 ? '\u5df2\u751f\u6210' : '\u7b49\u5f85\u4e2d' }}</span>
        </div>
        <p class="description">&#x89D2;&#x8272;&#x4EE3;&#x8868;&#x4E0D;&#x540C;&#x516C;&#x5171;&#x8072;&#x97F3;&#xFF1A;&#x6F5B;&#x5728;&#x4F7F;&#x7528;&#x8005;&#x3001;&#x6295;&#x8CC7;&#x4EBA;&#x3001;&#x7AF6;&#x54C1;&#x3001;&#x65C1;&#x89C0;&#x8005;&#x8207;&#x65E9;&#x671F;&#x652F;&#x6301;&#x8005;&#x3002;</p>
        <div class="stats-grid">
          <div><strong>{{ profiles.length }}</strong><span>&#x5DF2;&#x751F;&#x6210;&#x89D2;&#x8272;</span></div>
          <div><strong>{{ expectedTotal || '-' }}</strong><span>&#x9810;&#x8A08;&#x89D2;&#x8272;</span></div>
          <div><strong>{{ entityTypes.length || '-' }}</strong><span>&#x89D2;&#x8272;&#x985E;&#x578B;</span></div>
        </div>
        <div v-if="profiles.length" class="profile-grid">
          <article v-for="profile in profiles.slice(0, 6)" :key="profile.user_id || profile.name || profile.username" class="profile-card">
            <strong>{{ profile.name || profile.username || '\u533f\u540d\u89d2\u8272' }}</strong>
            <span>{{ profile.profession || '\u516c\u5171\u89d2\u8272' }}</span>
            <p>{{ profile.bio || '\u6b64\u89d2\u8272\u6703\u5728\u6a21\u64ec\u4e2d\u6839\u64da\u81ea\u8eab\u80cc\u666f\u505a\u51fa\u53cd\u61c9\u3002' }}</p>
          </article>
        </div>
        <div v-else class="empty-state">&#x89D2;&#x8272;&#x751F;&#x6210;&#x5F8C;&#x6703;&#x5728;&#x9019;&#x88E1;&#x5373;&#x6642;&#x51FA;&#x73FE;&#x3002;</div>
      </section>

      <section class="step-card">
        <div class="step-header compact">
          <div><span class="step-index">CONFIG</span><h3>&#x6A21;&#x64EC;&#x8A2D;&#x5B9A;</h3></div>
          <span class="badge" :class="simulationConfig ? 'success' : 'pending'">{{ simulationConfig ? '\u5df2\u8f09\u5165' : '\u7b49\u5f85\u4e2d' }}</span>
        </div>
        <template v-if="simulationConfig">
          <div class="config-grid">
            <div><span>&#x6A21;&#x64EC;&#x6642;&#x9577;</span><strong>{{ simulationConfig.time_config?.total_simulation_hours || '-' }} &#x5C0F;&#x6642;</strong></div>
            <div><span>&#x6BCF;&#x8F2A;&#x6642;&#x9593;</span><strong>{{ simulationConfig.time_config?.minutes_per_round || '-' }} &#x5206;&#x9418;</strong></div>
            <div><span>&#x81EA;&#x52D5;&#x8F2A;&#x6578;</span><strong>{{ autoGeneratedRounds || '-' }} &#x8F2A;</strong></div>
            <div><span>&#x89D2;&#x8272;&#x8A2D;&#x5B9A;</span><strong>{{ simulationConfig.agent_configs?.length || 0 }} &#x7D44;</strong></div>
          </div>
          <div v-if="simulationConfig.event_config?.narrative_direction" class="narrative-box">
            <span>&#x6558;&#x4E8B;&#x65B9;&#x5411;</span>
            <p>{{ simulationConfig.event_config.narrative_direction }}</p>
          </div>
        </template>
        <div v-else class="empty-state">&#x7B49;&#x5F85; LLM &#x751F;&#x6210;&#x6A21;&#x64EC;&#x53C3;&#x6578;&#x3002;</div>
      </section>

      <section class="step-card cost-card">
        <div class="step-header compact">
          <div><span class="step-index">COST</span><h3>LLM &#x8CBB;&#x7528;&#x4F30;&#x7B97;</h3></div>
          <span v-if="costLoading" class="badge processing">&#x66F4;&#x65B0;&#x4E2D;</span>
        </div>
        <p v-if="costError" class="cost-error">{{ costError }}</p>
        <template v-else-if="costEstimate">
          <div class="cost-summary">
            <span>&#x76EE;&#x524D;&#x6A21;&#x578B;&#xFF1A;<code>{{ costEstimate.resolved_model_id }}</code></span>
            <strong>${{ costEstimate.usd_low }} - ${{ costEstimate.usd_high }} USD</strong>
            <small>&#x4E2D;&#x4F4D;&#x4F30;&#x7B97; ${{ costEstimate.usd_mid }}&#xFF0C;&#x4F86;&#x6E90;&#xFF1A;{{ pricingSourceLabel(costEstimate.pricing_source) }}</small>
          </div>
          <p class="description">{{ costEstimate.disclaimer_zh }}</p>
          <div v-if="costEstimate.recommend_cheaper?.length" class="model-list">
            <h4>&#x514D;&#x8CBB; / &#x8D85;&#x7701;&#x6A21;&#x578B;</h4>
            <button v-for="m in costEstimate.recommend_cheaper" :key="m.id" class="model-pill" :class="{ active: m.id === costEstimate.resolved_model_id }" @click="trialModelOverride = m.id"><span>{{ m.name || m.id }}</span><small>{{ m.tier }} ? ${{ m.estimated_usd_mid }}</small></button>
          </div>
          <div v-if="costEstimate.recommend_premium?.length" class="model-list premium">
            <h4>&#x54C1;&#x8CEA;&#x8F03;&#x9AD8;&#x6A21;&#x578B;</h4>
            <button v-for="m in costEstimate.recommend_premium" :key="m.id" class="model-pill" :class="{ active: m.id === costEstimate.resolved_model_id }" @click="trialModelOverride = m.id"><span>{{ m.name || m.id }}</span><small>{{ m.tier }} ? ${{ m.estimated_usd_mid }}</small></button>
          </div>
        </template>
        <div v-else class="empty-state">&#x8A2D;&#x5B9A;&#x751F;&#x6210;&#x5F8C;&#x6703;&#x81EA;&#x52D5;&#x4F30;&#x7B97;&#x8CBB;&#x7528;&#x3002;</div>
      </section>

      <section class="step-card launch-card">
        <div class="step-header compact"><div><span class="step-index">ROUNDS</span><h3>&#x63A8;&#x6F14;&#x8F2A;&#x6578;</h3></div></div>
        <label class="round-toggle"><input type="checkbox" v-model="useCustomRounds" /><span>&#x4F7F;&#x7528;&#x81EA;&#x8A02;&#x8F2A;&#x6578;</span></label>
        <div v-if="useCustomRounds" class="round-control"><input type="range" min="5" max="120" step="5" v-model.number="customMaxRounds" /><strong>{{ customMaxRounds }} &#x8F2A;</strong></div>
        <p v-else class="description">&#x76EE;&#x524D;&#x4F7F;&#x7528;&#x81EA;&#x52D5;&#x8A2D;&#x5B9A;&#xFF1A;{{ autoGeneratedRounds || '-' }} &#x8F2A;&#x3002;</p>
        <button class="start-btn" type="button" :disabled="phase < 4" @click="handleStartSimulation">{{ phase < 4 ? '\u7b49\u5f85\u8a2d\u5b9a\u5b8c\u6210' : '\u958b\u59cb\u5e02\u5834\u63a8\u6f14' }}</button>
      </section>

      <section class="step-card log-card">
        <div class="step-header compact"><div><span class="step-index">LOG</span><h3>&#x7CFB;&#x7D71;&#x8F38;&#x51FA;</h3></div></div>
        <div ref="logContent" class="log-content">
          <div v-for="(log, idx) in systemLogs" :key="idx" class="log-row"><span>{{ log.time }}</span><p>{{ log.msg }}</p></div>
          <div v-if="!systemLogs?.length" class="empty-state">&#x7B49;&#x5F85;&#x7CFB;&#x7D71;&#x8F38;&#x51FA;&#x3002;</div>
        </div>
      </section>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { 
  prepareSimulation, 
  getPrepareStatus, 
  getSimulationProfilesRealtime,
  getSimulationConfig,
  getSimulationConfigRealtime,
  getCostEstimate
} from '../api/simulation'

const props = defineProps({
  simulationId: String,  // 敺蝏辣隡
  projectData: Object,
  graphData: Object,
  systemLogs: Array
})

const emit = defineEmits(['go-back', 'next-step', 'add-log', 'update-status'])

// State
const phase = ref(0) // 0: ???? 1: ?Ｙ?鈭箄身, 2: ?Ｙ?閮剖?, 3: 摰?
const taskId = ref(null)
const prepareProgress = ref(0)
const currentStage = ref('')
const progressMessage = ref('')
const profiles = ref([])
const entityTypes = ref([])
const expectedTotal = ref(null)
const simulationConfig = ref(null)
const selectedProfile = ref(null)
const showProfilesDetail = ref(true)

// ?亥??駁?嚗???銝甈∟撓?箇??鞈?
let lastLoggedMessage = ''
let lastLoggedProfileCount = 0
let lastLoggedConfigStage = ''

// 璅⊥頛芣閮剖?
const useCustomRounds = ref(false) // ?身雿輻?芸?閮剖?頛芣
const customMaxRounds = ref(40)   // ?身?刻 40 頛?
// Watch stage to update phase
watch(currentStage, (newStage) => {
  if (newStage === 'generating_profiles') {
    phase.value = 1
  } else if (newStage === 'generating_config') {
    phase.value = 2
    if (!configTimer) {
      addLog('開始生成模擬設定...')
      startConfigPolling()
    }
  } else if (newStage === 'copying_scripts') {
    phase.value = 2
  }
})

// 敺身摰葉閮??芸??Ｙ??憚?賂?銝蝙?函′蝺函Ⅳ?身?潘?
const autoGeneratedRounds = computed(() => {
  if (!simulationConfig.value?.time_config) {
    return null // 閮剖??芰??餈? null
  }
  const totalHours = simulationConfig.value.time_config.total_simulation_hours
  const minutesPerRound = simulationConfig.value.time_config.minutes_per_round
  if (!totalHours || !minutesPerRound) {
    return null // 閮剖?鞈?銝??湔?餈? null
  }
  const calculatedRounds = Math.floor((totalHours * 60) / minutesPerRound)
  // 蝣箔??憭扯憚?訾?撠 40嚗?血潘?嚗????蝭??啣虜
  return Math.max(calculatedRounds, 40)
})

// LLM cost estimate (OpenRouter)
const costEstimate = ref(null)
const costLoading = ref(false)
const costError = ref('')
const trialModelOverride = ref('')
const defaultModelId = ref('')
let costFetchTimer = null

const pricingSourceLabel = (src) => {
  const m = { openrouter: 'OpenRouter 即時報價', fallback_static: '內建參考單價', unknown: '未知' }
  return m[src] || src
}

const fetchCostEstimate = async () => {
  if (!props.simulationId || !simulationConfig.value || !autoGeneratedRounds.value) return
  costLoading.value = true
  costError.value = ''
  try {
    const rounds = useCustomRounds.value ? customMaxRounds.value : autoGeneratedRounds.value
    const params = {
      platform: 'parallel',
      max_rounds: rounds,
      graph_memory: true
    }
    if (trialModelOverride.value) {
      params.model = trialModelOverride.value
    }
    const res = await getCostEstimate(props.simulationId, params)
    costEstimate.value = res.data
    if (!trialModelOverride.value && res.data?.resolved_model_id) {
      defaultModelId.value = res.data.resolved_model_id
    }
  } catch (e) {
    costError.value = e.message || '無法取得費用估算'
    costEstimate.value = null
  } finally {
    costLoading.value = false
  }
}

const scheduleCostFetch = () => {
  if (costFetchTimer) clearTimeout(costFetchTimer)
  costFetchTimer = setTimeout(fetchCostEstimate, 450)
}

const selectTrialModel = (modelId) => {
  trialModelOverride.value = modelId || ''
  scheduleCostFetch()
}

const resetTrialModel = () => {
  if (!trialModelOverride.value) return
  trialModelOverride.value = ''
  scheduleCostFetch()
}

watch(
  () => [
    props.simulationId,
    simulationConfig.value,
    useCustomRounds.value,
    customMaxRounds.value,
    autoGeneratedRounds.value,
    trialModelOverride.value
  ],
  () => scheduleCostFetch(),
  { deep: true }
)

// Polling timer
let pollTimer = null
let profilesTimer = null
let configTimer = null

// Computed
const displayProfiles = computed(() => {
  if (showProfilesDetail.value) {
    return profiles.value
  }
  return profiles.value.slice(0, 6)
})

// ?寞?agent_id??撖孵??sername
const getAgentUsername = (agentId) => {
  if (profiles.value && profiles.value.length > agentId && agentId >= 0) {
    const profile = profiles.value[agentId]
    return profile?.username || `agent_${agentId}`
  }
  return `agent_${agentId}`
}

// 閮???犖閮剔??閰梢??餅
const totalTopicsCount = computed(() => {
  return profiles.value.reduce((sum, p) => {
    return sum + (p.interested_topics?.length || 0)
  }, 0)
})

// Methods
const addLog = (msg) => {
  emit('add-log', msg)
}

// 憭???璅⊥??孵
const handleStartSimulation = () => {
  const params = {}

  if (useCustomRounds.value) {
    params.maxRounds = customMaxRounds.value
    addLog(`開始模擬：使用自訂 ${customMaxRounds.value} 輪`)
  } else {
    addLog(`開始模擬：使用自動設定 ${autoGeneratedRounds.value} 輪`)
  }

  emit('next-step', params)
}

const truncateBio = (bio) => {
  if (bio.length > 80) {
    return bio.substring(0, 80) + '...'
  }
  return bio
}

const selectProfile = (profile) => {
  selectedProfile.value = profile
}

// ?芸???皞?璅⊥
const startPrepareSimulation = async () => {
  if (!props.simulationId) {
    addLog('無法準備模擬：缺少 simulationId')
    emit('update-status', 'error')
    return
  }

  phase.value = 1
  addLog(`開始準備模擬：${props.simulationId}`)
  addLog('正在生成角色與情境設定...')
  emit('update-status', 'processing')

  try {
    const res = await prepareSimulation({
      simulation_id: props.simulationId,
      use_llm_for_profiles: true,
      parallel_profile_count: 5,
      force_regenerate: true,
      character_settings: { ...characterSettings.value, target_profile_count: totalCharacterCount.value },
      platform_tags: characterSettings.value.platform_tags,
      target_profile_count: totalCharacterCount.value
    })

    if (res.success && res.data) {
      if (res.data.already_prepared) {
        addLog('此模擬已經準備完成，正在載入既有設定...')
        await loadPreparedData()
        return
      }

      taskId.value = res.data.task_id
      addLog('模擬準備任務已建立')
      addLog(`  Task ID: ${res.data.task_id}`)

      if (res.data.expected_entities_count) {
        expectedTotal.value = res.data.expected_entities_count
        addLog(`預計生成 ${res.data.expected_entities_count} 個角色 / 場景節點`)
        if (res.data.entity_types && res.data.entity_types.length > 0) {
          addLog(`  類型：${res.data.entity_types.join(', ')}`)
        }
      }

      addLog('開始輪詢準備進度...')
      startPolling()
      startProfilesPolling()
    } else {
      addLog(`準備失敗：${res.error || '未知錯誤'}`)
      emit('update-status', 'error')
    }
  } catch (err) {
    addLog(`準備模擬時發生錯誤：${err.message}`)
    emit('update-status', 'error')
  }
}
const startPolling = () => {
  pollTimer = setInterval(pollPrepareStatus, 2000)
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

const startProfilesPolling = () => {
  profilesTimer = setInterval(fetchProfilesRealtime, 3000)
}

const stopProfilesPolling = () => {
  if (profilesTimer) {
    clearInterval(profilesTimer)
    profilesTimer = null
  }
}

const pollPrepareStatus = async () => {
  if (!taskId.value && !props.simulationId) return

  try {
    const res = await getPrepareStatus({
      task_id: taskId.value,
      simulation_id: props.simulationId
    })

    if (res.success && res.data) {
      const data = res.data
      prepareProgress.value = data.progress || 0
      progressMessage.value = data.message || ''

      if (data.progress_detail) {
        const detail = data.progress_detail
        currentStage.value = detail.current_stage || ''
        const logKey = `${detail.current_stage}-${detail.current_item}-${detail.total_items}`
        if (logKey !== lastLoggedMessage && detail.item_description) {
          lastLoggedMessage = logKey
          const stageInfo = `[${detail.stage_index}/${detail.total_stages}]`
          if (detail.total_items > 0) {
            addLog(`${stageInfo} ${detail.current_stage_name}: ${detail.current_item}/${detail.total_items} - ${detail.item_description}`)
          } else {
            addLog(`${stageInfo} ${detail.current_stage_name}: ${detail.item_description}`)
          }
        }
      } else if (data.message) {
        const match = data.message.match(/\[(\d+)\/(\d+)\]\s*([^:]+)/)
        if (match) {
          const label = match[3].trim()
          const stageByLabel = {
            '讀取資料': 'reading',
            '分析資料': 'reading',
            '生成 Agent': 'generating_profiles',
            '生成角色': 'generating_profiles',
            '生成設定': 'generating_config',
            '複製腳本': 'copying_scripts'
          }
          currentStage.value = stageByLabel[label] || label
        }
        if (data.message !== lastLoggedMessage) {
          lastLoggedMessage = data.message
          addLog(data.message)
        }
      }

      if (data.status === 'completed' || data.status === 'ready' || data.already_prepared) {
        addLog('模擬準備完成')
        stopPolling()
        stopProfilesPolling()
        await loadPreparedData()
      } else if (data.status === 'failed') {
        addLog(`準備失敗：${data.error || '未知錯誤'}`)
        stopPolling()
        stopProfilesPolling()
      }
    }
  } catch (err) {
    console.warn('輪詢準備狀態失敗:', err)
  }
}

const fetchProfilesRealtime = async () => {
  if (!props.simulationId) return

  try {
    const res = await getSimulationProfilesRealtime(props.simulationId, 'reddit')

    if (res.success && res.data) {
      profiles.value = res.data.profiles || []
      if (res.data.total_expected) {
        expectedTotal.value = res.data.total_expected
      }

      const types = new Set()
      profiles.value.forEach((p) => {
        if (p.entity_type) types.add(p.entity_type)
      })
      entityTypes.value = Array.from(types)

      const currentCount = profiles.value.length
      if (currentCount > 0 && currentCount !== lastLoggedProfileCount) {
        lastLoggedProfileCount = currentCount
        const total = expectedTotal.value || '?'
        const latestProfile = profiles.value[currentCount - 1]
        const profileName = latestProfile?.name || latestProfile?.username || `Agent_${currentCount}`
        if (currentCount === 1) {
          addLog('開始生成 Agent 角色...')
        }
        addLog(`Agent 角色 ${currentCount}/${total}: ${profileName} (${latestProfile?.profession || '未知職業'})`)

        if (expectedTotal.value && currentCount >= expectedTotal.value) {
          addLog(`已完成 ${currentCount} 個 Agent 角色`)
        }
      }
    }
  } catch (err) {
    console.warn('載入 Profiles 失敗:', err)
  }
}

const startConfigPolling = () => {
  configTimer = setInterval(fetchConfigRealtime, 2000)
}

const stopConfigPolling = () => {
  if (configTimer) {
    clearInterval(configTimer)
    configTimer = null
  }
}

const fetchConfigRealtime = async () => {
  if (!props.simulationId) return

  try {
    const res = await getSimulationConfigRealtime(props.simulationId)

    if (res.success && res.data) {
      const data = res.data

      if (data.generation_stage && data.generation_stage !== lastLoggedConfigStage) {
        lastLoggedConfigStage = data.generation_stage
        if (data.generation_stage === 'generating_profiles') {
          addLog('正在生成 Agent 角色設定...')
        } else if (data.generation_stage === 'generating_config') {
          addLog('正在生成模擬設定與參數...')
        }
      }

      if (data.config_generated && data.config) {
        simulationConfig.value = data.config
        addLog('模擬設定已生成')

        if (data.summary) {
          addLog(`  Agent 數量：${data.summary.total_agents}`)
          addLog(`  模擬時長：${data.summary.simulation_hours} 小時`)
          addLog(`  初始貼文：${data.summary.initial_posts_count}`)
          addLog(`  熱門話題：${data.summary.hot_topics_count}`)
          addLog(`  平台設定：Twitter ${data.summary.has_twitter_config ? '有' : '無'}，Reddit ${data.summary.has_reddit_config ? '有' : '無'}`)
        }

        if (data.config.time_config) {
          const tc = data.config.time_config
          const rounds = Math.floor((tc.total_simulation_hours * 60) / tc.minutes_per_round)
          addLog(`時間設定：每輪 ${tc.minutes_per_round} 分鐘，共 ${rounds} 輪`)
        }

        if (data.config.event_config?.narrative_direction) {
          const narrative = data.config.event_config.narrative_direction
          addLog(`敘事方向：${narrative.length > 50 ? narrative.substring(0, 50) + '...' : narrative}`)
        }

        stopConfigPolling()
        phase.value = 4
        addLog('所有設定完成，可以開始模擬')
        emit('update-status', 'completed')
      }
    }
  } catch (err) {
    console.warn('載入 Config 失敗:', err)
  }
}

const loadPreparedData = async () => {
  phase.value = 2
  addLog('正在載入已準備的模擬資料...')

  await fetchProfilesRealtime()
  addLog(`已載入 ${profiles.value.length} 個 Agent 角色`)

  try {
    const res = await getSimulationConfigRealtime(props.simulationId)
    if (res.success && res.data) {
      if (res.data.config_generated && res.data.config) {
        simulationConfig.value = res.data.config
        addLog('模擬設定已載入')

        if (res.data.summary) {
          addLog(`  Agent 數量：${res.data.summary.total_agents}`)
          addLog(`  模擬時長：${res.data.summary.simulation_hours} 小時`)
          addLog(`  初始貼文：${res.data.summary.initial_posts_count}`)
        }

        addLog('所有設定完成，可以開始模擬')
        phase.value = 4
        emit('update-status', 'completed')
      } else {
        addLog('設定尚未生成完成，繼續輪詢...')
        startConfigPolling()
      }
    }
  } catch (err) {
    addLog(`載入設定失敗：${err.message}`)
    emit('update-status', 'error')
  }
}
// Scroll log to bottom
const logContent = ref(null)
watch(() => props.systemLogs?.length, () => {
  nextTick(() => {
    if (logContent.value) {
      logContent.value.scrollTop = logContent.value.scrollHeight
    }
  })
})

onMounted(() => {
  // ?芸???皞?瘚?
  if (props.simulationId) {
    addLog('Step2 已載入，請先確認角色池設定，再生成模擬環境')
    startPrepareSimulation()
  }
})

onUnmounted(() => {
  stopPolling()
  stopProfilesPolling()
  stopConfigPolling()
  if (costFetchTimer) clearTimeout(costFetchTimer)
})
</script>

<style scoped>
.env-setup-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #FAFAFA;
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
}

.scroll-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Step Card */
.step-card {
  background: #FFF;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #EAEAEA;
  transition: all 0.3s ease;
  position: relative;
}

.step-card.active {
  border-color: #FF5722;
  box-shadow: 0 4px 12px rgba(255, 87, 34, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.step-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 20px;
  font-weight: 700;
  color: #E0E0E0;
}

.step-card.active .step-num,
.step-card.completed .step-num {
  color: #000;
}

.step-title {
  font-weight: 600;
  font-size: 14px;
  letter-spacing: 0.5px;
}

.badge {
  font-size: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.success { background: #E8F5E9; color: #2E7D32; }
.badge.processing { background: #FF5722; color: #FFF; }
.badge.pending { background: #F5F5F5; color: #999; }
.badge.accent { background: #E3F2FD; color: #1565C0; }

.card-content {
  /* No extra padding - uses step-card's padding */
}

.api-note {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #999;
  margin-bottom: 8px;
}

.description {
  font-size: 12px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 16px;
}

/* Action Section */
.action-section {
  margin-top: 16px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn.primary {
  background: #000;
  color: #FFF;
}

.action-btn.primary:hover:not(:disabled) {
  opacity: 0.8;
}

.action-btn.secondary {
  background: #F5F5F5;
  color: #333;
}

.action-btn.secondary:hover:not(:disabled) {
  background: #E5E5E5;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-group {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.action-group.dual {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.action-group.dual .action-btn {
  width: 100%;
}

/* Info Card */
.info-card {
  background: #F5F5F5;
  border-radius: 6px;
  padding: 16px;
  margin-top: 16px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed #E0E0E0;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 12px;
  color: #666;
}

.info-value {
  font-size: 13px;
  font-weight: 500;
}

.info-value.mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
  background: #F9F9F9;
  padding: 16px;
  border-radius: 6px;
}

.stat-card {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: #000;
  font-family: 'JetBrains Mono', monospace;
}

.stat-label {
  font-size: 9px;
  color: #999;
  text-transform: uppercase;
  margin-top: 4px;
  display: block;
}

/* Profiles Preview */
.profiles-preview {
  margin-top: 20px;
  border-top: 1px solid #E5E5E5;
  padding-top: 16px;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.preview-title {
  font-size: 12px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.profiles-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  max-height: 320px;
  overflow-y: auto;
  padding-right: 4px;
}

.profiles-list::-webkit-scrollbar {
  width: 4px;
}

.profiles-list::-webkit-scrollbar-thumb {
  background: #DDD;
  border-radius: 2px;
}

.profiles-list::-webkit-scrollbar-thumb:hover {
  background: #CCC;
}

.profile-card {
  background: #FAFAFA;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
  padding: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.profile-card:hover {
  border-color: #999;
  background: #FFF;
}

.profile-header {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 6px;
}

.profile-realname {
  font-size: 14px;
  font-weight: 700;
  color: #000;
}

.profile-username {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #999;
}

.profile-meta {
  margin-bottom: 8px;
}

.profile-profession {
  font-size: 11px;
  color: #666;
  background: #F0F0F0;
  padding: 2px 8px;
  border-radius: 3px;
}

.profile-bio {
  font-size: 12px;
  color: #444;
  line-height: 1.6;
  margin: 0 0 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.profile-topics {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.topic-tag {
  font-size: 10px;
  color: #1565C0;
  background: #E3F2FD;
  padding: 2px 8px;
  border-radius: 10px;
}

.topic-more {
  font-size: 10px;
  color: #999;
  padding: 2px 6px;
}

/* Config Preview */
/* Config Detail Panel */
.config-detail-panel {
  margin-top: 16px;
}

.config-block {
  margin-top: 16px;
  border-top: 1px solid #E5E5E5;
  padding-top: 12px;
}

.config-block:first-child {
  margin-top: 0;
  border-top: none;
  padding-top: 0;
}

.config-block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.config-block-title {
  font-size: 12px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.config-block-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  background: #F1F5F9;
  color: #475569;
  padding: 2px 8px;
  border-radius: 10px;
}

/* Config Grid */
.config-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.config-item {
  background: #F9F9F9;
  padding: 12px 14px;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.config-item-label {
  font-size: 11px;
  color: #94A3B8;
}

.config-item-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 600;
  color: #1E293B;
}

/* Time Periods */
.time-periods {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.period-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: #F9F9F9;
  border-radius: 6px;
}

.period-label {
  font-size: 12px;
  font-weight: 500;
  color: #64748B;
  min-width: 70px;
}

.period-hours {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #475569;
  flex: 1;
}

.period-multiplier {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  color: #6366F1;
  background: #EEF2FF;
  padding: 2px 6px;
  border-radius: 4px;
}

/* Agents Cards */
.agents-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 4px;
}

.agents-cards::-webkit-scrollbar {
  width: 4px;
}

.agents-cards::-webkit-scrollbar-thumb {
  background: #DDD;
  border-radius: 2px;
}

.agents-cards::-webkit-scrollbar-thumb:hover {
  background: #CCC;
}

.agent-card {
  background: #F9F9F9;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
  padding: 14px;
  transition: all 0.2s ease;
}

.agent-card:hover {
  border-color: #999;
  background: #FFF;
}

/* Agent Card Header */
.agent-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid #F1F5F9;
}

.agent-identity {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.agent-id {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #94A3B8;
}

.agent-name {
  font-size: 14px;
  font-weight: 600;
  color: #1E293B;
}

.agent-tags {
  display: flex;
  gap: 6px;
}

.agent-type {
  font-size: 10px;
  color: #64748B;
  background: #F1F5F9;
  padding: 2px 8px;
  border-radius: 4px;
}

.agent-stance {
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 4px;
}

.stance-neutral {
  background: #F1F5F9;
  color: #64748B;
}

.stance-supportive {
  background: #DCFCE7;
  color: #16A34A;
}

.stance-opposing {
  background: #FEE2E2;
  color: #DC2626;
}

.stance-observer {
  background: #FEF3C7;
  color: #D97706;
}

/* Agent Timeline */
.agent-timeline {
  margin-bottom: 14px;
}

.timeline-label {
  display: block;
  font-size: 10px;
  color: #94A3B8;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.mini-timeline {
  display: flex;
  gap: 2px;
  height: 16px;
  background: #F8FAFC;
  border-radius: 4px;
  padding: 3px;
}

.timeline-hour {
  flex: 1;
  background: #E2E8F0;
  border-radius: 2px;
  transition: all 0.2s;
}

.timeline-hour.active {
  background: linear-gradient(180deg, #6366F1, #818CF8);
}

.timeline-marks {
  display: flex;
  justify-content: space-between;
  margin-top: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  color: #94A3B8;
}

/* Agent Params */
.agent-params {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.param-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.param-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.param-item .param-label {
  font-size: 10px;
  color: #94A3B8;
}

.param-item .param-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 600;
  color: #475569;
}

.param-value.with-bar {
  display: flex;
  align-items: center;
  gap: 6px;
}

.mini-bar {
  height: 4px;
  background: linear-gradient(90deg, #6366F1, #A855F7);
  border-radius: 2px;
  min-width: 4px;
  max-width: 40px;
}

.param-value.positive {
  color: #16A34A;
}

.param-value.negative {
  color: #DC2626;
}

.param-value.neutral {
  color: #64748B;
}

.param-value.highlight {
  color: #6366F1;
}

/* Platforms Grid */
.platforms-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.platform-card {
  background: #F9F9F9;
  padding: 14px;
  border-radius: 6px;
}

.platform-card-header {
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid #E5E5E5;
}

.platform-name {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.platform-params {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.param-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.param-label {
  font-size: 12px;
  color: #64748B;
}

.param-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 600;
  color: #1E293B;
}

/* Reasoning Content */
.reasoning-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.reasoning-item {
  padding: 12px 14px;
  background: #F9F9F9;
  border-radius: 6px;
}

.reasoning-text {
  font-size: 13px;
  color: #555;
  line-height: 1.7;
  margin: 0;
}

/* Profile Modal */
.profile-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.profile-modal {
  background: #FFF;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px;
  background: #FFF;
  border-bottom: 1px solid #F0F0F0;
}

.modal-header-info {
  flex: 1;
}

.modal-name-row {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 8px;
}

.modal-realname {
  font-size: 20px;
  font-weight: 700;
  color: #000;
}

.modal-username {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: #999;
}

.modal-profession {
  font-size: 12px;
  color: #666;
  background: #F5F5F5;
  padding: 4px 10px;
  border-radius: 4px;
  display: inline-block;
  font-weight: 500;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  color: #999;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  transition: color 0.2s;
  padding: 0;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

/* ?箸靽⊥蝵 */
.modal-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px 16px;
  margin-bottom: 32px;
  padding: 0;
  background: transparent;
  border-radius: 0;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 11px;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.info-value {
  font-size: 15px;
  font-weight: 600;
  color: #333;
}

.info-value.mbti {
  font-family: 'JetBrains Mono', monospace;
  color: #FF5722;
}

/* 璅∪??箏? */
.modal-section {
  margin-bottom: 28px;
}

.section-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.section-bio {
  font-size: 14px;
  color: #333;
  line-height: 1.6;
  margin: 0;
  padding: 16px;
  background: #F9F9F9;
  border-radius: 6px;
  border-left: 3px solid #E0E0E0;
}

/* 閰梢??倌 */
.topics-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.topic-item {
  font-size: 11px;
  color: #1565C0;
  background: #E3F2FD;
  padding: 4px 10px;
  border-radius: 12px;
  transition: all 0.2s;
  border: none;
}

.topic-item:hover {
  background: #BBDEFB;
  color: #0D47A1;
}

/* 閰喟敦鈭箄身 */
.persona-dimensions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.dimension-card {
  background: #F8F9FA;
  padding: 12px;
  border-radius: 6px;
  border-left: 3px solid #DDD;
  transition: all 0.2s;
}

.dimension-card:hover {
  background: #F0F0F0;
  border-left-color: #999;
}

.dim-title {
  display: block;
  font-size: 12px;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.dim-desc {
  display: block;
  font-size: 10px;
  color: #888;
  line-height: 1.4;
}

.persona-content {
  max-height: none;
  overflow: visible;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 0;
}

.persona-content::-webkit-scrollbar {
  width: 4px;
}

.persona-content::-webkit-scrollbar-thumb {
  background: #DDD;
  border-radius: 2px;
}

.section-persona {
  font-size: 13px;
  color: #555;
  line-height: 1.8;
  margin: 0;
  text-align: justify;
}

/* System Logs */
.system-logs {
  background: #000;
  color: #DDD;
  padding: 16px;
  font-family: 'JetBrains Mono', monospace;
  border-top: 1px solid #222;
  flex-shrink: 0;
}

.log-header {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #333;
  padding-bottom: 8px;
  margin-bottom: 8px;
  font-size: 10px;
  color: #888;
}

.log-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  height: 80px; /* Approx 4 lines visible */
  overflow-y: auto;
  padding-right: 4px;
}

.log-content::-webkit-scrollbar {
  width: 4px;
}

.log-content::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 2px;
}

.log-line {
  font-size: 11px;
  display: flex;
  gap: 12px;
  line-height: 1.5;
}

.log-time {
  color: #666;
  min-width: 75px;
}

.log-msg {
  color: #CCC;
  word-break: break-all;
}

/* Spinner */
.spinner-sm {
  width: 16px;
  height: 16px;
  border: 2px solid #E5E5E5;
  border-top-color: #FF5722;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
/* Orchestration Content */
.orchestration-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 16px;
}

.box-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.narrative-box {
  background: #FFFFFF;
  padding: 20px 24px;
  border-radius: 12px;
  border: 1px solid #EEF2F6;
  box-shadow: 0 4px 24px rgba(0,0,0,0.03);
  transition: all 0.3s ease;
}

.narrative-box .box-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 13px;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
  font-weight: 600;
}

.special-icon {
  filter: drop-shadow(0 2px 4px rgba(255, 87, 34, 0.2));
  transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.narrative-box:hover .special-icon {
  transform: rotate(180deg);
}

.narrative-text {
  font-family: 'Inter', 'Noto Sans SC', system-ui, sans-serif;
  font-size: 14px;
  color: #334155;
  line-height: 1.8;
  margin: 0;
  text-align: justify;
  letter-spacing: 0.01em;
}

.topics-section {
  background: #FFF;
}

.hot-topics-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.hot-topic-tag {
  font-size: 12px;
  color:rgba(255, 86, 34, 0.88);
  background: #FFF3E0;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: 500;
}

.hot-topic-more {
  font-size: 11px;
  color: #999;
  padding: 4px 6px;
}

.initial-posts-section {
  border-top: 1px solid #EAEAEA;
  padding-top: 16px;
}

.posts-timeline {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-left: 8px;
  border-left: 2px solid #F0F0F0;
  margin-top: 12px;
}

.timeline-item {
  position: relative;
  padding-left: 20px;
}

.timeline-marker {
  position: absolute;
  left: 0;
  top: 14px;
  width: 12px;
  height: 2px;
  background: #DDD;
}

.timeline-content {
  background: #F9F9F9;
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #EEE;
}

.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.post-role {
  font-size: 11px;
  font-weight: 700;
  color: #333;
  text-transform: uppercase;
}

.post-agent-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.post-id,
.post-username {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #666;
  line-height: 1;
  vertical-align: baseline;
}

.post-username {
  margin-right: 6px;
}

.post-text {
  font-size: 12px;
  color: #555;
  line-height: 1.5;
  margin: 0;
}

/* 璅⊥頛芣閮剖??瑕? */
.rounds-config-section {
  margin: 24px 0;
  padding-top: 24px;
  border-top: 1px solid #EAEAEA;
}

.rounds-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #1E293B;
}

.section-desc {
  font-size: 12px;
  color: #94A3B8;
}

.desc-highlight {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  color: #1E293B;
  background: #F1F5F9;
  padding: 1px 6px;
  border-radius: 4px;
  margin: 0 2px;
}

/* Switch Control */
.switch-control {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px 4px 4px;
  border-radius: 20px;
  transition: background 0.2s;
}

.switch-control:hover {
  background: #F8FAFC;
}

.switch-control input {
  display: none;
}

.switch-track {
  width: 36px;
  height: 20px;
  background: #E2E8F0;
  border-radius: 10px;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}

.switch-track::after {
  content: '';
  position: absolute;
  left: 2px;
  top: 2px;
  width: 16px;
  height: 16px;
  background: #FFF;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}

.switch-control input:checked + .switch-track {
  background: #000;
}

.switch-control input:checked + .switch-track::after {
  transform: translateX(16px);
}

.switch-label {
  font-size: 12px;
  font-weight: 500;
  color: #64748B;
}

.switch-control input:checked ~ .switch-label {
  color: #1E293B;
}

/* Slider Content */
.rounds-content {
  animation: fadeIn 0.3s ease;
}

.slider-display {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 16px;
}

.slider-main-value {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.val-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 700;
  color: #000;
}

.val-unit {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.slider-meta-info {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #64748B;
  background: #F1F5F9;
  padding: 4px 8px;
  border-radius: 4px;
}

.range-wrapper {
  position: relative;
  padding: 0 2px;
}

.minimal-slider {
  -webkit-appearance: none;
  width: 100%;
  height: 4px;
  background: #E2E8F0;
  border-radius: 2px;
  outline: none;
  background-image: linear-gradient(#000, #000);
  background-size: var(--percent, 0%) 100%;
  background-repeat: no-repeat;
  cursor: pointer;
}

.minimal-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #FFF;
  border: 2px solid #000;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  transition: transform 0.1s;
  margin-top: -6px; /* Center thumb */
}

.minimal-slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

.minimal-slider::-webkit-slider-runnable-track {
  height: 4px;
  border-radius: 2px;
}

.range-marks {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #94A3B8;
  position: relative;
}

.mark-recommend {
  cursor: pointer;
  transition: color 0.2s;
  position: relative;
}

.mark-recommend:hover {
  color: #000;
}

.mark-recommend.active {
  color: #000;
  font-weight: 600;
}

.mark-recommend::after {
  content: '';
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 1px;
  height: 4px;
  background: #CBD5E1;
}

/* Auto Info */
.auto-info-card {
  display: flex;
  align-items: center;
  gap: 24px;
  background: #F8FAFC;
  padding: 16px 20px;
  border-radius: 8px;
}

.auto-value {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  gap: 4px;
  padding-right: 24px;
  border-right: 1px solid #E2E8F0;
}

.auto-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  justify-content: center;
}

.auto-meta-row {
  display: flex;
  align-items: center;
}

.duration-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 500;
  color: #64748B;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  padding: 3px 8px;
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.auto-desc {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.auto-desc p {
  margin: 0;
  font-size: 13px;
  color: #64748B;
  line-height: 1.5;
}

.highlight-tip {
  margin-top: 4px !important;
  font-size: 12px !important;
  color: #000 !important;
  font-weight: 500;
  cursor: pointer;
}

.highlight-tip:hover {
  text-decoration: underline;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Modal Transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .profile-modal {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-leave-active .profile-modal {
  transition: all 0.3s ease-in;
}

.modal-enter-from .profile-modal,
.modal-leave-to .profile-modal {
  transform: scale(0.95) translateY(10px);
  opacity: 0;
}

/* LLM 鞎餌蝎摯 */
.cost-estimate-panel {
  margin-top: 20px;
  padding: 16px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 12px;
  color: #334155;
}

.cost-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.cost-title {
  font-weight: 600;
  font-size: 13px;
  color: #0F172A;
}

.cost-loading {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #64748B;
}

.cost-error {
  color: #B91C1C;
  margin: 0;
}

.cost-model-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 8px;
}

.cost-label {
  color: #64748B;
}

.cost-mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  background: #E2E8F0;
  padding: 2px 6px;
  border-radius: 4px;
}

.cost-pricing-src {
  font-size: 11px;
  color: #94A3B8;
}

.cost-range-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 8px;
}

.cost-usd {
  font-size: 13px;
}

.cost-usd strong {
  font-family: 'JetBrains Mono', monospace;
}

.cost-mid {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #64748B;
}

.cost-disclaimer {
  margin: 0 0 8px;
  line-height: 1.5;
  color: #64748B;
  font-size: 11px;
}

.cost-tokens {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #475569;
  margin-bottom: 12px;
}

.cost-rec-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #CBD5E1;
}

.cost-rec-section.premium .rec-title {
  color: #0F172A;
}

.rec-title {
  font-weight: 600;
  margin-bottom: 8px;
  color: #334155;
}

.rec-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rec-list li {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 8px;
}

.rec-list li.rec-item {
  cursor: pointer;
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid transparent;
  transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
}

.rec-list li.rec-item:hover {
  background: #FFF7ED;
  border-color: #FED7AA;
  transform: translateY(-1px);
}

.rec-list li.rec-item.active {
  background: #FFEDD5;
  border-color: #FB923C;
}

.rec-name {
  color: #64748B;
  flex: 1;
  min-width: 120px;
}

.rec-price {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #475569;
}

.rec-usd {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #059669;
  font-weight: 600;
}

.cost-unit-row {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #475569;
  margin: 4px 0 8px;
}

.cost-override-tag {
  display: inline-block;
  margin-left: 6px;
  padding: 2px 8px;
  font-size: 11px;
  background: #FFEDD5;
  color: #C2410C;
  border-radius: 999px;
}

.cost-reset-btn {
  margin-left: 8px;
  padding: 2px 8px;
  font-size: 11px;
  background: transparent;
  border: 1px solid #CBD5E1;
  color: #475569;
  border-radius: 6px;
  cursor: pointer;
}

.cost-reset-btn:hover {
  background: #F1F5F9;
}

.rec-help {
  margin: 10px 0 4px;
  font-size: 12px;
  color: #475569;
  line-height: 1.5;
}

.cost-link {
  display: inline-block;
  margin-top: 12px;
  font-size: 11px;
  color: #FF5722;
  text-decoration: none;
}

.cost-link:hover {
  text-decoration: underline;
}


.cooked-step2 .step-card {
  border: 2px solid #111;
  border-radius: 0;
  background: rgba(250, 248, 242, 0.96);
  box-shadow: 8px 8px 0 rgba(17, 17, 17, 0.1);
}

.cooked-step2 .step-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}

.cooked-step2 .step-header h2,
.cooked-step2 .step-header h3 {
  margin: 4px 0 0;
  color: #111;
  letter-spacing: 0;
}

.cooked-step2 .step-header h2 { font-size: clamp(28px, 4vw, 52px); line-height: 0.95; }
.cooked-step2 .step-header h3 { font-size: 24px; line-height: 1.05; }

.cooked-step2 .step-index,
.cooked-step2 .badge,
.cooked-step2 .info-item span,
.cooked-step2 .config-grid span,
.cooked-step2 .narrative-box span,
.cooked-step2 .model-pill small,
.cooked-step2 .log-row span {
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.cooked-step2 .badge {
  border: 1px solid #111;
  padding: 6px 9px;
  white-space: nowrap;
}

.cooked-step2 .badge.success { background: #111; color: #f7f1df; }
.cooked-step2 .badge.processing { background: #d9ff66; color: #111; }
.cooked-step2 .badge.pending { background: transparent; color: #555; }

.cooked-step2 .description {
  margin: 0 0 16px;
  color: #383838;
  line-height: 1.6;
}

.cooked-step2 .info-grid,
.cooked-step2 .stats-grid,
.cooked-step2 .config-grid,
.cooked-step2 .profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
}

.cooked-step2 .info-item,
.cooked-step2 .stats-grid > div,
.cooked-step2 .config-grid > div,
.cooked-step2 .profile-card,
.cooked-step2 .narrative-box,
.cooked-step2 .cost-summary {
  border: 1px solid rgba(17, 17, 17, 0.24);
  background: rgba(255, 255, 255, 0.5);
  padding: 12px;
}

.cooked-step2 .info-item strong,
.cooked-step2 .stats-grid strong,
.cooked-step2 .config-grid strong {
  display: block;
  margin-top: 6px;
  color: #111;
  word-break: break-word;
}

.cooked-step2 .profile-card p,
.cooked-step2 .narrative-box p,
.cooked-step2 .log-row p {
  margin: 6px 0 0;
  line-height: 1.5;
}

.cooked-step2 .model-list {
  display: grid;
  gap: 8px;
  margin-top: 16px;
}

.cooked-step2 .model-list h4 {
  margin: 0;
  font-size: 14px;
}

.cooked-step2 .model-pill {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-height: 40px;
  border: 1px solid #111;
  background: transparent;
  color: #111;
  padding: 8px 10px;
  text-align: left;
  cursor: pointer;
}

.cooked-step2 .model-pill.active,
.cooked-step2 .model-pill:hover {
  background: #111;
  color: #f7f1df;
}

.cooked-step2 .round-toggle,
.cooked-step2 .round-control {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 12px 0;
}

.cooked-step2 .round-control input { flex: 1; }

.cooked-step2 .start-btn {
  width: 100%;
  min-height: 48px;
  border: 2px solid #111;
  background: #111;
  color: #f7f1df;
  font-weight: 900;
  cursor: pointer;
}

.cooked-step2 .start-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.cooked-step2 .log-content {
  max-height: 260px;
  overflow: auto;
  display: grid;
  gap: 8px;
}

.cooked-step2 .log-row {
  border-top: 1px solid rgba(17, 17, 17, 0.16);
  padding-top: 8px;
}


.cooked-step2 .character-controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  margin-top: 14px;
}

.cooked-step2 .character-controls label {
  display: grid;
  gap: 8px;
  border: 1px solid rgba(17, 17, 17, 0.24);
  background: rgba(255, 255, 255, 0.5);
  padding: 12px;
  font-weight: 800;
}

.cooked-step2 .character-controls input {
  min-height: 38px;
  border: 1px solid #111;
  background: #f7f1df;
  color: #111;
  padding: 0 10px;
  font-weight: 900;
}

.cooked-step2 .platform-block {
  margin-top: 14px;
}

.cooked-step2 .mini-label {
  display: block;
  margin-bottom: 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 900;
  text-transform: uppercase;
}

.cooked-step2 .platform-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.cooked-step2 .tag-pill {
  min-height: 34px;
  border: 1px solid #111;
  background: transparent;
  color: #111;
  padding: 0 10px;
  font-weight: 800;
  cursor: pointer;
}

.cooked-step2 .tag-pill.active {
  background: #d9ff66;
}

.cooked-step2 .start-btn.secondary {
  margin-top: 16px;
  background: #d9ff66;
  color: #111;
}
</style>














