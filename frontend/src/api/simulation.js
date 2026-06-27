import service, { requestWithRetry } from './index'

/**
 * 撱箇?璅⊥
 * @param {Object} data - { project_id, graph_id?, enable_twitter?, enable_reddit? }
 */
export const createSimulation = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/create', data), 3, 1000)
}

/**
 * 皞?璅⊥?啣?嚗??郊隞餃?嚗? * @param {Object} data - { simulation_id, entity_types?, use_llm_for_profiles?, parallel_profile_count?, force_regenerate? }
 */
export const prepareSimulation = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/prepare', data), 3, 1000)
}

/**
 * ?亥岷皞?隞餃??脣漲
 * @param {Object} data - { task_id?, simulation_id? }
 */
export const getPrepareStatus = (data) => {
  return service.post('/api/simulation/prepare/status', data)
}

/**
 * ??璅⊥??? * @param {string} simulationId
 */
export const getSimulation = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}`)
}

/**
 * ??璅⊥??Agent Profiles
 * @param {string} simulationId
 * @param {string} platform - 'reddit' | 'twitter'
 */
export const getSimulationProfiles = (simulationId, platform = 'reddit') => {
  return service.get(`/api/simulation/${simulationId}/profiles`, { params: { platform } })
}

/**
 * ?單????Ｙ?銝剔? Agent Profiles
 * @param {string} simulationId
 * @param {string} platform - 'reddit' | 'twitter'
 */
export const getSimulationProfilesRealtime = (simulationId, platform = 'reddit') => {
  return service.get(`/api/simulation/${simulationId}/profiles/realtime`, { params: { platform } })
}

/**
 * ??璅⊥閮剖?
 * @param {string} simulationId
 */
export const getSimulationConfig = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/config`)
}

/**
 * ?單????Ｙ?銝剔?璅⊥閮剖?
 * @param {string} simulationId
 * @returns {Promise} ?閮剖?鞈?嚗??思葉蝜潸???閮剖??批捆
 */
export const getSimulationConfigRealtime = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/config/realtime`)
}

/**
 * ???芋?? * @param {string} projectId - ?舫嚗?撠? ID 蝭拚
 */
export const listSimulations = (projectId) => {
  const params = projectId ? { project_id: projectId } : {}
  return service.get('/api/simulation/list', { params })
}

/**
 * ??璅⊥
 * @param {Object} data - { simulation_id, platform?, max_rounds?, enable_graph_memory_update? }
 */
export const startSimulation = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/start', data), 3, 1000)
}

/**
 * 蝎摯?祆活璅⊥ LLM 鞎餌嚗? .env 璅∪???simulation_config嚗? * @param {string} simulationId
 * @param {Object} [params] - { platform?, max_rounds?, graph_memory? }
 */
export const getCostEstimate = (simulationId, params = {}) => {
  return service.get('/api/simulation/cost-estimate', {
    params: { simulation_id: simulationId, ...params }
  })
}

/**
 * ?迫璅⊥
 * @param {Object} data - { simulation_id }
 */
export const stopSimulation = (data) => {
  return service.post('/api/simulation/stop', data)
}

/**
 * ??璅⊥?瑁??單???? * @param {string} simulationId
 */
export const getRunStatus = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/run-status`)
}

/**
 * ??璅⊥?瑁?閰喟敦????急?餈?雿?
 * @param {string} simulationId
 */
export const getRunStatusDetail = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/run-status/detail`)
}

/**
 * ??璅⊥銝剔?鞎潭?
 * @param {string} simulationId
 * @param {string} platform - 'reddit' | 'twitter'
 * @param {number} limit - ?喳?蝑
 * @param {number} offset - 雿宏?? */
export const getSimulationPosts = (simulationId, platform = 'reddit', limit = 50, offset = 0) => {
  return service.get(`/api/simulation/${simulationId}/posts`, {
    params: { platform, limit, offset }
  })
}

/**
 * ??璅⊥??頠賂??憚甈∪?蝮踝?
 * @param {string} simulationId
 * @param {number} startRound - 韏瑕?頛芣活
 * @param {number} endRound - 蝯?頛芣活
 */
export const getSimulationTimeline = (simulationId, startRound = 0, endRound = null) => {
  const params = { start_round: startRound }
  if (endRound !== null) {
    params.end_round = endRound
  }
  return service.get(`/api/simulation/${simulationId}/timeline`, { params })
}

/**
 * ?? Agent 蝯梯?鞈?
 * @param {string} simulationId
 */
export const getAgentStats = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/agent-stats`)
}

/**
 * ??璅⊥??甇瑕
 * @param {string} simulationId
 * @param {Object} params - { limit, offset, platform, agent_id, round_num }
 */
export const getSimulationActions = (simulationId, params = {}) => {
  return service.get(`/api/simulation/${simulationId}/actions`, { params })
}

/**
 * ??璅⊥?啣?嚗??綽?
 * @param {Object} data - { simulation_id, timeout? }
 */
export const closeSimulationEnv = (data) => {
  return service.post('/api/simulation/close-env', data)
}

/**
 * ??璅⊥?啣???? * @param {Object} data - { simulation_id }
 */
export const getEnvStatus = (data) => {
  return service.post('/api/simulation/env-status', data)
}

/**
 * ?寞活?∟赤 Agent
 * @param {Object} data - { simulation_id, interviews: [{ agent_id, prompt }] }
 */
export const interviewAgents = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/interview/batch', data), 3, 1000)
}

/**
 * ??甇瑕璅⊥?”嚗?撠?閰單?嚗? * ?冽擐?甇瑕撠?撅內
 * @param {number} limit - ?喳?蝑銝?
 */
export const getSimulationHistory = (limit = 20) => {
  return service.get('/api/simulation/history', { params: { limit }, timeout: 15000 })
}

/**
 * Delete one simulation from local history.
 * @param {string} simulationId
 */
export const deleteSimulation = (simulationId) => {
  return service.delete(`/api/simulation/${simulationId}`)
}
/**
 * 撠?甈⊥芋?祈??頃鞎瑟?憿?隡啜?敺垢?? agent 頝?LLM嚗? * @param {string} simulationId
 * @param {Object} data - { product_desc, ad_copy, target_audience_criteria, sample_size? }
 */
export const runPurchaseIntent = (simulationId, data) => {
  return service.post(`/api/simulation/${simulationId}/purchase-intent`, data, {
    timeout: 5 * 60 * 1000
  })
}
/**
 * 霈??餈?甈∠?鞈潸眺??閰摯蝯?嚗?????null嚗? */
export const getPurchaseIntent = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/purchase-intent`)
}



