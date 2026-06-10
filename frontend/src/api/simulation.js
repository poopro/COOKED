import service, { requestWithRetry } from './index'

/**
 * 建立模擬
 * @param {Object} data - { project_id, graph_id?, enable_twitter?, enable_reddit? }
 */
export const createSimulation = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/create', data), 3, 1000)
}

/**
 * 準備模擬環境（非同步任務）
 * @param {Object} data - { simulation_id, entity_types?, use_llm_for_profiles?, parallel_profile_count?, force_regenerate? }
 */
export const prepareSimulation = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/prepare', data), 3, 1000)
}

/**
 * 查詢準備任務進度
 * @param {Object} data - { task_id?, simulation_id? }
 */
export const getPrepareStatus = (data) => {
  return service.post('/api/simulation/prepare/status', data)
}

/**
 * 取得模擬狀態
 * @param {string} simulationId
 */
export const getSimulation = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}`)
}

/**
 * 取得模擬的 Agent Profiles
 * @param {string} simulationId
 * @param {string} platform - 'reddit' | 'twitter'
 */
export const getSimulationProfiles = (simulationId, platform = 'reddit') => {
  return service.get(`/api/simulation/${simulationId}/profiles`, { params: { platform } })
}

/**
 * 即時取得產生中的 Agent Profiles
 * @param {string} simulationId
 * @param {string} platform - 'reddit' | 'twitter'
 */
export const getSimulationProfilesRealtime = (simulationId, platform = 'reddit') => {
  return service.get(`/api/simulation/${simulationId}/profiles/realtime`, { params: { platform } })
}

/**
 * 取得模擬設定
 * @param {string} simulationId
 */
export const getSimulationConfig = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/config`)
}

/**
 * 即時取得產生中的模擬設定
 * @param {string} simulationId
 * @returns {Promise} 回傳設定資訊，包含中繼資料與設定內容
 */
export const getSimulationConfigRealtime = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/config/realtime`)
}

/**
 * 列出所有模擬
 * @param {string} projectId - 可選，依專案 ID 篩選
 */
export const listSimulations = (projectId) => {
  const params = projectId ? { project_id: projectId } : {}
  return service.get('/api/simulation/list', { params })
}

/**
 * 啟動模擬
 * @param {Object} data - { simulation_id, platform?, max_rounds?, enable_graph_memory_update? }
 */
export const startSimulation = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/start', data), 3, 1000)
}

/**
 * 粗估本次模擬 LLM 費用（依 .env 模型與 simulation_config）
 * @param {string} simulationId
 * @param {Object} [params] - { platform?, max_rounds?, graph_memory? }
 */
export const getCostEstimate = (simulationId, params = {}) => {
  return service.get('/api/simulation/cost-estimate', {
    params: { simulation_id: simulationId, ...params }
  })
}

/**
 * 停止模擬
 * @param {Object} data - { simulation_id }
 */
export const stopSimulation = (data) => {
  return service.post('/api/simulation/stop', data)
}

/**
 * 取得模擬執行即時狀態
 * @param {string} simulationId
 */
export const getRunStatus = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/run-status`)
}

/**
 * 取得模擬執行詳細狀態（含最近動作）
 * @param {string} simulationId
 */
export const getRunStatusDetail = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/run-status/detail`)
}

/**
 * 取得模擬中的貼文
 * @param {string} simulationId
 * @param {string} platform - 'reddit' | 'twitter'
 * @param {number} limit - 傳回筆數
 * @param {number} offset - 位移量
 */
export const getSimulationPosts = (simulationId, platform = 'reddit', limit = 50, offset = 0) => {
  return service.get(`/api/simulation/${simulationId}/posts`, {
    params: { platform, limit, offset }
  })
}

/**
 * 取得模擬時間軸（按輪次彙總）
 * @param {string} simulationId
 * @param {number} startRound - 起始輪次
 * @param {number} endRound - 結束輪次
 */
export const getSimulationTimeline = (simulationId, startRound = 0, endRound = null) => {
  const params = { start_round: startRound }
  if (endRound !== null) {
    params.end_round = endRound
  }
  return service.get(`/api/simulation/${simulationId}/timeline`, { params })
}

/**
 * 取得 Agent 統計資訊
 * @param {string} simulationId
 */
export const getAgentStats = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/agent-stats`)
}

/**
 * 取得模擬動作歷史
 * @param {string} simulationId
 * @param {Object} params - { limit, offset, platform, agent_id, round_num }
 */
export const getSimulationActions = (simulationId, params = {}) => {
  return service.get(`/api/simulation/${simulationId}/actions`, { params })
}

/**
 * 關閉模擬環境（優雅退出）
 * @param {Object} data - { simulation_id, timeout? }
 */
export const closeSimulationEnv = (data) => {
  return service.post('/api/simulation/close-env', data)
}

/**
 * 取得模擬環境狀態
 * @param {Object} data - { simulation_id }
 */
export const getEnvStatus = (data) => {
  return service.post('/api/simulation/env-status', data)
}

/**
 * 批次採訪 Agent
 * @param {Object} data - { simulation_id, interviews: [{ agent_id, prompt }] }
 */
export const interviewAgents = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/interview/batch', data), 3, 1000)
}

/**
 * 取得歷史模擬列表（附專案詳情）
 * 用於首頁歷史專案展示
 * @param {number} limit - 傳回筆數上限
 */
export const getSimulationHistory = (limit = 20) => {
  return service.get('/api/simulation/history', { params: { limit } })
}

/**
 * 對某次模擬跑「購買意願評估」（後端會逐位 agent 跑 LLM）
 * @param {string} simulationId
 * @param {Object} data - { product_desc, ad_copy, target_audience_criteria, sample_size? }
 */
export const runPurchaseIntent = (simulationId, data) => {
  return service.post(`/api/simulation/${simulationId}/purchase-intent`, data, {
    timeout: 5 * 60 * 1000  // 評估可能跑數分鐘，放長一點
  })
}

/**
 * 讀取最近一次的購買意願評估結果（沒有則回 null）
 */
export const getPurchaseIntent = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/purchase-intent`)
}

