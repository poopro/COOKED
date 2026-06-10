<template>
  <div class="pi-overlay" @click.self="handleClose">
    <div class="pi-panel">
      <!-- ===== Header ===== -->
      <div class="pi-header">
        <div class="pi-title-block">
          <div class="pi-eyebrow">PURCHASE INTENT EVALUATION</div>
          <h2 class="pi-title">買單意願模擬</h2>
          <p class="pi-sub">
            結合每位 Agent 的隱藏心理 meter（5 維敏感度）+ 在 Info Plaza / Topic Community 的真實行為，
            預測「會不會買」並把人群拆成<b>目標客群</b>與<b>路人</b>對比。
          </p>
        </div>
        <button class="pi-close" @click="handleClose" title="關閉">×</button>
      </div>

      <div class="pi-body">
        <!-- ===== Phase 1: Inputs ===== -->
        <section v-if="phase === 'input'" class="pi-input-section">
          <div class="pi-form">
            <div class="pi-field">
              <label>產品 / 服務描述</label>
              <textarea
                v-model="form.product_desc"
                rows="3"
                placeholder="例：QuantumSleep 智能溫控枕，內建溫控晶片自動恆溫於 21°C，幫助高壓上班族改善淺眠。"
              ></textarea>
            </div>

            <div class="pi-field">
              <label>
                目標客群定義 (Target Audience)
                <span class="pi-hint">用一句話描述「誰才是你想賣給的人」</span>
              </label>
              <input
                v-model="form.target_audience_criteria"
                placeholder="例：30–50 歲、有淺眠困擾、月薪 5 萬以上的雙薪上班族"
              />
            </div>

            <div class="pi-field">
              <label>廣告文案</label>
              <textarea
                v-model="form.ad_copy"
                rows="6"
                placeholder="把要評估的廣告文案完整貼進來，包含標題、訴求點、優惠資訊等..."
              ></textarea>
            </div>

            <div class="pi-row">
              <div class="pi-field-mini">
                <label>取樣人數</label>
                <select v-model.number="form.sample_size">
                  <option :value="6">6（最快，~ 1 分鐘）</option>
                  <option :value="12">12（標準）</option>
                  <option :value="20">20（深度）</option>
                  <option :value="0">全部</option>
                </select>
              </div>
              <button
                class="pi-run-btn"
                :disabled="!canRun || running"
                @click="runEvaluation"
              >
                <span v-if="running" class="pi-spinner"></span>
                {{ running ? '評估中...' : '開始評估' }}
              </button>
            </div>

            <div v-if="errorMsg" class="pi-error">
              <strong>失敗</strong>
              {{ errorMsg }}
            </div>
          </div>

          <!-- Existing result hint -->
          <div v-if="hasSavedResult && !running" class="pi-existing">
            <div>
              已找到上次的評估結果（{{ formatDate(savedAt) }}），
              <button class="pi-link-btn" @click="loadSaved">直接載入查看</button>
            </div>
          </div>
        </section>

        <!-- ===== Phase 2: Running ===== -->
        <section v-if="phase === 'running'" class="pi-running-section">
          <div class="pi-running-card">
            <div class="pi-spinner-large"></div>
            <div class="pi-running-msg">{{ runningMsg }}</div>
            <div class="pi-running-hint">
              每位 agent 需要呼叫 2 次 LLM（畫像 + 決策），請耐心等候。
              評估完成後結果會自動存到此模擬，下次開啟就不用重跑。
            </div>
          </div>
        </section>

        <!-- ===== Phase 3: Results ===== -->
        <section v-if="phase === 'result' && result" class="pi-result-section">
          <!-- KPI Cards -->
          <div class="pi-kpi-grid">
            <div class="pi-kpi-card pi-kpi-total" :class="kpiClass(result.summary.buy_rate)">
              <div class="pi-kpi-label">總體購買率</div>
              <div class="pi-kpi-value">{{ result.summary.buy_rate }}%</div>
              <div class="pi-kpi-foot">
                {{ result.summary.buyers }} / {{ result.summary.total }} 人會買
              </div>
            </div>
            <div class="pi-kpi-card pi-kpi-target">
              <div class="pi-kpi-label">目標客群購買率</div>
              <div class="pi-kpi-value">{{ result.summary.target.buy_rate }}%</div>
              <div class="pi-kpi-foot">
                {{ result.summary.target.buyers }} / {{ result.summary.target.count }} 位 TA
              </div>
            </div>
            <div class="pi-kpi-card pi-kpi-non-target">
              <div class="pi-kpi-label">路人購買率</div>
              <div class="pi-kpi-value">{{ result.summary.non_target.buy_rate }}%</div>
              <div class="pi-kpi-foot">
                {{ result.summary.non_target.buyers }} / {{ result.summary.non_target.count }} 位路人
              </div>
            </div>
            <div class="pi-kpi-card pi-kpi-conf">
              <div class="pi-kpi-label">平均決策信心</div>
              <div class="pi-kpi-value">{{ result.summary.avg_confidence }}</div>
              <div class="pi-kpi-foot">越高代表 LLM 越篤定</div>
            </div>
          </div>

          <!-- Attribution: 為什麼買 vs 為什麼不買 -->
          <div class="pi-attr-grid">
            <div class="pi-attr-card pi-attr-pos">
              <div class="pi-attr-title">
                <span class="pi-attr-dot pi-attr-dot-pos"></span>
                為什麼會買（驅動因子歸因 %）
              </div>
              <div v-if="result.summary.drivers_attribution_pct.length === 0"
                   class="pi-attr-empty">沒人決定購買 — 也就沒有驅動因子</div>
              <div v-else class="pi-attr-list">
                <div
                  v-for="d in result.summary.drivers_attribution_pct.slice(0, 6)"
                  :key="d.key"
                  class="pi-attr-row"
                >
                  <div class="pi-attr-row-label">{{ factorLabel(d.key) }}</div>
                  <div class="pi-attr-row-bar-wrap">
                    <div class="pi-attr-row-bar pi-attr-row-bar-pos"
                         :style="{ width: d.pct + '%' }"></div>
                  </div>
                  <div class="pi-attr-row-pct">{{ d.pct }}%</div>
                </div>
              </div>
            </div>

            <div class="pi-attr-card pi-attr-neg">
              <div class="pi-attr-title">
                <span class="pi-attr-dot pi-attr-dot-neg"></span>
                為什麼不買（阻力因子歸因 %）
              </div>
              <div v-if="result.summary.barriers_attribution_pct.length === 0"
                   class="pi-attr-empty">沒人 reject — 沒有阻力因子</div>
              <div v-else class="pi-attr-list">
                <div
                  v-for="b in result.summary.barriers_attribution_pct.slice(0, 6)"
                  :key="b.key"
                  class="pi-attr-row"
                >
                  <div class="pi-attr-row-label">{{ factorLabel(b.key) }}</div>
                  <div class="pi-attr-row-bar-wrap">
                    <div class="pi-attr-row-bar pi-attr-row-bar-neg"
                         :style="{ width: b.pct + '%' }"></div>
                  </div>
                  <div class="pi-attr-row-pct">{{ b.pct }}%</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tabs: TA vs Non-TA -->
          <div class="pi-tabs">
            <button
              :class="['pi-tab', { active: activeGroup === 'target' }]"
              @click="activeGroup = 'target'"
            >
              目標客群 <span class="pi-tab-count">{{ targetGroup.length }}</span>
            </button>
            <button
              :class="['pi-tab', { active: activeGroup === 'non_target' }]"
              @click="activeGroup = 'non_target'"
            >
              路人 <span class="pi-tab-count">{{ nonTargetGroup.length }}</span>
            </button>
            <div class="pi-tabs-spacer"></div>
            <button class="pi-rerun-btn" @click="resetForm">
              <span class="pi-icon-refresh">↻</span> 重新評估
            </button>
          </div>

          <!-- Persona Cards Grid -->
          <div class="pi-persona-grid">
            <div
              v-for="p in currentGroup"
              :key="p.user_id"
              :class="['pi-persona-card', p.decision === 'BUY' ? 'pi-card-buy' : 'pi-card-reject']"
            >
              <div class="pi-card-head">
                <div class="pi-card-avatar">{{ (p.name || 'A')[0] }}</div>
                <div class="pi-card-id">
                  <div class="pi-card-name">{{ p.name }}</div>
                  <div class="pi-card-meta">
                    {{ p.age || '?' }}歲 · {{ p.profession || '—' }}
                  </div>
                </div>
                <div :class="['pi-card-badge', p.decision === 'BUY' ? 'badge-buy' : 'badge-reject']">
                  {{ p.decision }}
                  <span class="pi-card-conf">{{ p.confidence }}%</span>
                </div>
              </div>

              <p class="pi-card-reason">{{ p.one_line_reason }}</p>

              <div class="pi-card-tags">
                <span v-if="p.is_target_audience" class="pi-card-tag tag-ta">
                  TA · {{ p.target_match_reason }}
                </span>
                <span v-else class="pi-card-tag tag-non-ta">
                  非 TA
                </span>
              </div>

              <!-- Toggle hidden internal meter -->
              <div class="pi-card-expand">
                <button class="pi-expand-btn" @click="togglePersona(p.user_id)">
                  {{ expandedPersona === p.user_id ? '收起' : '查看內部 meter ↓' }}
                </button>
                <div v-if="expandedPersona === p.user_id" class="pi-card-internal">
                  <div class="pi-internal-block">
                    <div class="pi-internal-title">隱藏 5 維敏感度（0–10）</div>
                    <div class="pi-meter-list">
                      <div v-for="dim in PSYCH_DIMS" :key="dim.key" class="pi-meter-row">
                        <div class="pi-meter-label">{{ dim.label }}</div>
                        <div class="pi-meter-bar-wrap">
                          <div class="pi-meter-bar"
                               :style="{ width: ((p.hidden_profile[dim.key] || 0) * 10) + '%' }"></div>
                        </div>
                        <div class="pi-meter-val">{{ p.hidden_profile[dim.key] }}</div>
                      </div>
                    </div>
                    <div class="pi-meter-summary">
                      “{{ p.hidden_profile.summary || '—' }}”
                    </div>
                  </div>

                  <div class="pi-internal-block">
                    <div class="pi-internal-title">在社群上做了什麼</div>
                    <div class="pi-sig-summary">{{ p.sim_signals.text_summary }}</div>
                  </div>

                  <div v-if="p.suggestion" class="pi-internal-block">
                    <div class="pi-internal-title">給品牌方的改進建議</div>
                    <div class="pi-suggestion">💡 {{ p.suggestion }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="currentGroup.length === 0" class="pi-empty">
              這群人是空的（沒有 agent 落在這個分類）
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { runPurchaseIntent, getPurchaseIntent } from '../api/simulation'

const props = defineProps({
  simulationId: { type: String, required: true },
  productHint: { type: String, default: '' },     // 如有，從外部帶入產品描述
  taHint: { type: String, default: '' }           // 如有，從外部帶入 TA 描述
})
const emit = defineEmits(['close'])

const PSYCH_DIMS = [
  { key: 'persuasiveness',      label: '說服力（理性訴求）' },
  { key: 'trust',               label: '信任偏好' },
  { key: 'emotional_resonance', label: '情感共鳴' },
  { key: 'social_proof',        label: '社群從眾性' },
  { key: 'urgency',             label: '急迫感反應' }
]

const FACTOR_LABEL_MAP = {
  persuasiveness: '理性說服力',
  trust: '品牌信任',
  emotional_resonance: '情感共鳴',
  social_proof: '社會認同',
  urgency: '限時急迫感',
  price_sensitivity: '價格敏感',
  social_buzz_positive: '社群正向聲量',
  social_buzz_negative: '社群負評',
  own_engagement: '自身已有正向互動',
  no_engagement: '社群上幾乎沒接觸過',
  skepticism: '對廣告的懷疑',
  brand_familiarity: '品牌熟悉度',
  evaluation_error: '評估系統錯誤'
}
const factorLabel = (k) => FACTOR_LABEL_MAP[k] || k

// ---- State ----
const phase = ref('input')   // input / running / result
const running = ref(false)
const runningMsg = ref('準備中...')
const errorMsg = ref('')
const result = ref(null)
const savedAt = ref(null)
const hasSavedResult = ref(false)
const expandedPersona = ref(null)
const activeGroup = ref('target')

const form = ref({
  product_desc: props.productHint || '',
  ad_copy: '',
  target_audience_criteria: props.taHint || '',
  sample_size: 12
})

const canRun = computed(() => {
  return form.value.product_desc.trim().length > 0
      && form.value.ad_copy.trim().length > 0
      && form.value.target_audience_criteria.trim().length > 0
})

const targetGroup = computed(() =>
  (result.value?.personas || []).filter(p => p.is_target_audience)
)
const nonTargetGroup = computed(() =>
  (result.value?.personas || []).filter(p => !p.is_target_audience)
)
const currentGroup = computed(() =>
  activeGroup.value === 'target' ? targetGroup.value : nonTargetGroup.value
)

// ---- Lifecycle ----
onMounted(async () => {
  // Check for saved result
  try {
    const res = await getPurchaseIntent(props.simulationId)
    if (res.success && res.data) {
      hasSavedResult.value = true
      savedAt.value = res.data.evaluated_at
    }
  } catch (e) {
    // Ignore — saved result may simply not exist
  }
})

// ---- Methods ----
const handleClose = () => emit('close')

const togglePersona = (uid) => {
  expandedPersona.value = expandedPersona.value === uid ? null : uid
}

const kpiClass = (rate) => {
  if (rate >= 60) return 'kpi-green'
  if (rate >= 35) return 'kpi-amber'
  return 'kpi-red'
}

const formatDate = (iso) => {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}

const loadSaved = async () => {
  try {
    const res = await getPurchaseIntent(props.simulationId)
    if (res.success && res.data) {
      result.value = res.data
      // Populate form from saved input so user sees what was evaluated
      if (res.data.input) {
        form.value.product_desc = res.data.input.product_desc || form.value.product_desc
        form.value.ad_copy = res.data.input.ad_copy || form.value.ad_copy
        form.value.target_audience_criteria =
          res.data.input.target_audience_criteria || form.value.target_audience_criteria
      }
      activeGroup.value = targetGroup.value.length > 0 ? 'target' : 'non_target'
      phase.value = 'result'
    }
  } catch (e) {
    errorMsg.value = '讀取既有評估失敗：' + (e.message || e)
  }
}

const runEvaluation = async () => {
  if (!canRun.value || running.value) return
  errorMsg.value = ''
  running.value = true
  phase.value = 'running'
  runningMsg.value = '送出評估請求...'

  try {
    const payload = {
      product_desc: form.value.product_desc.trim(),
      ad_copy: form.value.ad_copy.trim(),
      target_audience_criteria: form.value.target_audience_criteria.trim(),
    }
    if (form.value.sample_size && form.value.sample_size > 0) {
      payload.sample_size = form.value.sample_size
    }
    runningMsg.value = '逐位 agent 跑 LLM 評估中（每位約 5–10 秒）...'

    const res = await runPurchaseIntent(props.simulationId, payload)
    if (!res.success) {
      throw new Error(res.error || '後端回傳失敗')
    }
    result.value = res.data
    activeGroup.value = targetGroup.value.length > 0 ? 'target' : 'non_target'
    phase.value = 'result'
  } catch (e) {
    errorMsg.value = e?.response?.data?.error || e.message || String(e)
    phase.value = 'input'
  } finally {
    running.value = false
  }
}

const resetForm = () => {
  expandedPersona.value = null
  result.value = null
  phase.value = 'input'
}
</script>

<style scoped>
.pi-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: stretch;
  justify-content: center;
  padding: 24px;
}
.pi-panel {
  width: 100%;
  max-width: 1180px;
  background: #ffffff;
  border-radius: 14px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.25);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Header */
.pi-header {
  padding: 20px 28px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}
.pi-eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #6366f1;
  margin-bottom: 4px;
}
.pi-title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
}
.pi-sub {
  margin: 6px 0 0;
  font-size: 13px;
  color: #475569;
  line-height: 1.55;
  max-width: 760px;
}
.pi-close {
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  width: 36px;
  height: 36px;
  font-size: 22px;
  color: #64748b;
  cursor: pointer;
  flex-shrink: 0;
}
.pi-close:hover { background: #f1f5f9; color: #0f172a; }

/* Body scroll */
.pi-body {
  overflow-y: auto;
  padding: 24px 28px 32px;
  flex-grow: 1;
}

/* ===== Phase: Inputs ===== */
.pi-form { display: flex; flex-direction: column; gap: 16px; max-width: 760px; }
.pi-field { display: flex; flex-direction: column; gap: 6px; }
.pi-field label {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
}
.pi-field label .pi-hint {
  font-size: 11px;
  font-weight: 400;
  color: #94a3b8;
  margin-left: 6px;
}
.pi-field textarea, .pi-field input {
  font-family: inherit;
  font-size: 13px;
  padding: 10px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  resize: vertical;
  background: #f8fafc;
  color: #0f172a;
}
.pi-field textarea:focus, .pi-field input:focus {
  outline: none;
  border-color: #6366f1;
  background: #ffffff;
}
.pi-row { display: flex; align-items: flex-end; gap: 16px; margin-top: 6px; }
.pi-field-mini { display: flex; flex-direction: column; gap: 6px; flex-shrink: 0; }
.pi-field-mini label { font-size: 12px; color: #475569; font-weight: 500; }
.pi-field-mini select {
  padding: 9px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 13px;
  background: #f8fafc;
}
.pi-run-btn {
  flex-grow: 1;
  padding: 11px 22px;
  background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: opacity .2s;
}
.pi-run-btn:hover { opacity: 0.92; }
.pi-run-btn:disabled { opacity: 0.45; cursor: not-allowed; }
.pi-error {
  margin-top: 8px;
  padding: 10px 14px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  border-radius: 8px;
  font-size: 13px;
}
.pi-error strong { margin-right: 6px; }
.pi-existing {
  margin-top: 16px;
  padding: 10px 14px;
  background: #eef2ff;
  border: 1px solid #c7d2fe;
  border-radius: 8px;
  font-size: 13px;
  color: #3730a3;
}
.pi-link-btn {
  background: transparent;
  border: none;
  color: #4f46e5;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}

/* Spinners */
.pi-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: pi-spin 0.8s linear infinite;
}
.pi-spinner-large {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: pi-spin 0.8s linear infinite;
  margin: 0 auto 18px;
}
@keyframes pi-spin {
  to { transform: rotate(360deg); }
}

/* ===== Phase: Running ===== */
.pi-running-section {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 320px;
}
.pi-running-card { text-align: center; max-width: 420px; }
.pi-running-msg {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}
.pi-running-hint {
  font-size: 12px;
  color: #64748b;
  line-height: 1.6;
}

/* ===== Phase: Results — KPI ===== */
.pi-kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 24px;
}
@media (max-width: 900px) {
  .pi-kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
.pi-kpi-card {
  border: 1px solid #e5e7eb;
  border-top: 3px solid #94a3b8;
  border-radius: 10px;
  padding: 16px 18px;
  background: #ffffff;
}
.pi-kpi-label {
  font-size: 11px;
  letter-spacing: 1px;
  color: #64748b;
  text-transform: uppercase;
  font-weight: 600;
}
.pi-kpi-value {
  font-size: 32px;
  font-weight: 800;
  margin-top: 6px;
  color: #0f172a;
  font-feature-settings: 'tnum';
}
.pi-kpi-foot { font-size: 11px; color: #94a3b8; margin-top: 4px; }
.pi-kpi-card.kpi-green { border-top-color: #10b981; }
.pi-kpi-card.kpi-green .pi-kpi-value { color: #059669; }
.pi-kpi-card.kpi-amber { border-top-color: #f59e0b; }
.pi-kpi-card.kpi-amber .pi-kpi-value { color: #d97706; }
.pi-kpi-card.kpi-red { border-top-color: #ef4444; }
.pi-kpi-card.kpi-red .pi-kpi-value { color: #dc2626; }
.pi-kpi-card.pi-kpi-target { border-top-color: #6366f1; }
.pi-kpi-card.pi-kpi-non-target { border-top-color: #94a3b8; }

/* ===== Attribution ===== */
.pi-attr-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}
@media (max-width: 900px) { .pi-attr-grid { grid-template-columns: 1fr; } }
.pi-attr-card {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 16px;
}
.pi-attr-title {
  font-weight: 600;
  font-size: 13px;
  color: #0f172a;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.pi-attr-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.pi-attr-dot-pos { background: #10b981; }
.pi-attr-dot-neg { background: #ef4444; }
.pi-attr-empty { font-size: 12px; color: #94a3b8; padding: 8px 0; }
.pi-attr-list { display: flex; flex-direction: column; gap: 8px; }
.pi-attr-row {
  display: grid;
  grid-template-columns: 130px 1fr 50px;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}
.pi-attr-row-label { color: #475569; }
.pi-attr-row-bar-wrap { background: #e5e7eb; height: 8px; border-radius: 4px; overflow: hidden; }
.pi-attr-row-bar { height: 100%; transition: width .4s; }
.pi-attr-row-bar-pos { background: linear-gradient(90deg, #10b981, #34d399); }
.pi-attr-row-bar-neg { background: linear-gradient(90deg, #ef4444, #f87171); }
.pi-attr-row-pct {
  text-align: right;
  font-weight: 700;
  color: #0f172a;
  font-feature-settings: 'tnum';
}

/* ===== Tabs ===== */
.pi-tabs {
  display: flex;
  align-items: center;
  border-bottom: 2px solid #e5e7eb;
  gap: 6px;
  margin-bottom: 16px;
}
.pi-tab {
  padding: 10px 18px;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}
.pi-tab.active { color: #4f46e5; border-bottom-color: #6366f1; }
.pi-tab-count {
  background: #e5e7eb;
  color: #475569;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 700;
}
.pi-tab.active .pi-tab-count { background: #c7d2fe; color: #4338ca; }
.pi-tabs-spacer { flex: 1; }
.pi-rerun-btn {
  background: transparent;
  border: 1px solid #cbd5e1;
  color: #64748b;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
}
.pi-rerun-btn:hover { background: #f1f5f9; color: #0f172a; }
.pi-icon-refresh { display: inline-block; margin-right: 2px; }

/* ===== Persona Cards ===== */
.pi-persona-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}
@media (max-width: 900px) { .pi-persona-grid { grid-template-columns: 1fr; } }
.pi-persona-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-left: 4px solid #94a3b8;
  border-radius: 10px;
  padding: 14px 16px;
  transition: box-shadow .2s;
}
.pi-persona-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
.pi-card-buy { border-left-color: #10b981; }
.pi-card-reject { border-left-color: #ef4444; }
.pi-card-head {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}
.pi-card-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e0e7ff;
  color: #4338ca;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}
.pi-card-id { flex-grow: 1; min-width: 0; }
.pi-card-name { font-weight: 600; font-size: 14px; color: #0f172a; }
.pi-card-meta { font-size: 11px; color: #94a3b8; }
.pi-card-badge {
  font-weight: 700;
  font-size: 12px;
  padding: 5px 10px;
  border-radius: 6px;
  border: 1px solid;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}
.badge-buy {
  background: #ecfdf5;
  border-color: #6ee7b7;
  color: #047857;
}
.badge-reject {
  background: #fef2f2;
  border-color: #fca5a5;
  color: #b91c1c;
}
.pi-card-conf {
  font-size: 10px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 3px;
  background: rgba(255,255,255,0.7);
}
.pi-card-reason {
  margin: 0;
  font-size: 13px;
  color: #334155;
  font-style: italic;
  background: #f8fafc;
  padding: 8px 10px;
  border-radius: 6px;
  line-height: 1.5;
}
.pi-card-tags { display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap; }
.pi-card-tag {
  font-size: 10px;
  padding: 3px 8px;
  border-radius: 999px;
  font-weight: 600;
}
.tag-ta { background: #ddd6fe; color: #5b21b6; }
.tag-non-ta { background: #f1f5f9; color: #64748b; }

/* Expand */
.pi-card-expand { margin-top: 10px; }
.pi-expand-btn {
  background: transparent;
  border: none;
  color: #6366f1;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
}
.pi-expand-btn:hover { color: #4338ca; }
.pi-card-internal {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.pi-internal-block {}
.pi-internal-title {
  font-size: 11px;
  font-weight: 700;
  color: #6366f1;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
  text-transform: uppercase;
}
.pi-meter-list { display: flex; flex-direction: column; gap: 5px; }
.pi-meter-row {
  display: grid;
  grid-template-columns: 130px 1fr 30px;
  align-items: center;
  gap: 8px;
  font-size: 11px;
}
.pi-meter-label { color: #475569; }
.pi-meter-bar-wrap { background: #e5e7eb; height: 6px; border-radius: 3px; overflow: hidden; }
.pi-meter-bar {
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  height: 100%;
  transition: width .4s;
}
.pi-meter-val {
  text-align: right;
  font-weight: 700;
  color: #0f172a;
  font-feature-settings: 'tnum';
}
.pi-meter-summary {
  margin-top: 6px;
  font-size: 11px;
  color: #64748b;
  font-style: italic;
}
.pi-sig-summary {
  font-size: 11px;
  color: #475569;
  background: #f8fafc;
  padding: 8px;
  border-radius: 6px;
  white-space: pre-wrap;
  line-height: 1.5;
}
.pi-suggestion {
  font-size: 12px;
  color: #92400e;
  background: #fef3c7;
  padding: 8px 10px;
  border-radius: 6px;
}
.pi-empty {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  color: #94a3b8;
  font-size: 13px;
  background: #f8fafc;
  border-radius: 8px;
}
</style>
