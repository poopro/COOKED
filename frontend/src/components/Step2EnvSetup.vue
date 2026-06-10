<template>
  <div class="env-setup-panel">
    <div class="scroll-container">
      <!-- Step 01: 模擬實例 -->
      <div class="step-card" :class="{ 'active': phase === 0, 'completed': phase > 0 }">
        <div class="card-header">
          <div class="step-info">
            <span class="step-num">01</span>
            <span class="step-title">模擬實例初始化</span>
          </div>
          <div class="step-status">
            <span v-if="phase > 0" class="badge success">已完成</span>
            <span v-else class="badge processing">初始化</span>
          </div>
        </div>
        
        <div class="card-content">
          <p class="api-note">POST /api/simulation/create</p>
          <p class="description">
            新增simulation實例，拉取模擬世界參數範本
          </p>

          <div v-if="simulationId" class="info-card">
            <div class="info-row">
              <span class="info-label">Project ID</span>
              <span class="info-value mono">{{ projectData?.project_id }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Graph ID</span>
              <span class="info-value mono">{{ projectData?.graph_id }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Simulation ID</span>
              <span class="info-value mono">{{ simulationId }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Task ID</span>
              <span class="info-value mono">{{ taskId || '非同步任務已完成' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 02: 產生 Agent 人設 -->
      <div class="step-card" :class="{ 'active': phase === 1, 'completed': phase > 1 }">
        <div class="card-header">
          <div class="step-info">
            <span class="step-num">02</span>
            <span class="step-title">產生 Agent 人設</span>
          </div>
          <div class="step-status">
            <span v-if="phase > 1" class="badge success">已完成</span>
            <span v-else-if="phase === 1" class="badge processing">{{ prepareProgress }}%</span>
            <span v-else class="badge pending">等待</span>
          </div>
        </div>

        <div class="card-content">
          <p class="api-note">POST /api/simulation/prepare</p>
          <p class="description">
            結合上下文，自動呼叫工具從知識圖譜梳理實體與關係，初始化模擬個體，並基於現實种子賦予他們獨特的行為與記憶
          </p>

          <!-- Profiles Stats -->
          <div v-if="profiles.length > 0" class="stats-grid">
            <div class="stat-card">
              <span class="stat-value">{{ profiles.length }}</span>
              <span class="stat-label">當前Agent数</span>
            </div>
            <div class="stat-card">
              <span class="stat-value">{{ expectedTotal || '-' }}</span>
              <span class="stat-label">預期Agent总数</span>
            </div>
            <div class="stat-card">
              <span class="stat-value">{{ totalTopicsCount }}</span>
              <span class="stat-label">現實种子當前關聯話題数</span>
            </div>
          </div>

          <!-- Profiles List Preview -->
          <div v-if="profiles.length > 0" class="profiles-preview">
            <div class="preview-header">
              <span class="preview-title">已產生的 Agent 人設</span>
            </div>
            <div class="profiles-list">
              <div 
                v-for="(profile, idx) in profiles" 
                :key="idx" 
                class="profile-card"
                @click="selectProfile(profile)"
              >
                <div class="profile-header">
                  <span class="profile-realname">{{ profile.username || 'Unknown' }}</span>
                  <span class="profile-username">@{{ profile.name || `agent_${idx}` }}</span>
                </div>
                <div class="profile-meta">
                  <span class="profile-profession">{{ profile.profession || '未知職業' }}</span>
                </div>
                <p class="profile-bio">{{ profile.bio || '暫無簡介' }}</p>
                <div v-if="profile.interested_topics?.length" class="profile-topics">
                  <span 
                    v-for="topic in profile.interested_topics.slice(0, 3)" 
                    :key="topic" 
                    class="topic-tag"
                  >{{ topic }}</span>
                  <span v-if="profile.interested_topics.length > 3" class="topic-more">
                    +{{ profile.interested_topics.length - 3 }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 03: 產生雙平台模擬設定 -->
      <div class="step-card" :class="{ 'active': phase === 2, 'completed': phase > 2 }">
        <div class="card-header">
          <div class="step-info">
            <span class="step-num">03</span>
            <span class="step-title">產生雙平台模擬設定</span>
          </div>
          <div class="step-status">
            <span v-if="phase > 2" class="badge success">已完成</span>
            <span v-else-if="phase === 2" class="badge processing">產生中</span>
            <span v-else class="badge pending">等待</span>
          </div>
        </div>

        <div class="card-content">
          <p class="api-note">POST /api/simulation/prepare</p>
          <p class="description">
            LLM 根據模擬需求與現實种子，智慧設定世界時間流速、推薦演算法、每個個體的活躍時間段、發言频率、事件觸發等參數
          </p>
          
          <!-- Config Preview -->
          <div v-if="simulationConfig" class="config-detail-panel">
            <!-- 時間設定 -->
            <div class="config-block">
              <div class="config-grid">
                <div class="config-item">
                  <span class="config-item-label">模擬時長</span>
                  <span class="config-item-value">{{ simulationConfig.time_config?.total_simulation_hours || '-' }} 小時</span>
                </div>
                <div class="config-item">
                  <span class="config-item-label">每輪時長</span>
                  <span class="config-item-value">{{ simulationConfig.time_config?.minutes_per_round || '-' }} 分鐘</span>
                </div>
                <div class="config-item">
                  <span class="config-item-label">總輪次</span>
                  <span class="config-item-value">{{ Math.floor((simulationConfig.time_config?.total_simulation_hours * 60 / simulationConfig.time_config?.minutes_per_round)) || '-' }} 輪</span>
                </div>
                <div class="config-item">
                  <span class="config-item-label">每小時活躍</span>
                  <span class="config-item-value">{{ simulationConfig.time_config?.agents_per_hour_min }}-{{ simulationConfig.time_config?.agents_per_hour_max }}</span>
                </div>
              </div>
              <div class="time-periods">
                <div class="period-item">
                  <span class="period-label">高峰时段</span>
                  <span class="period-hours">{{ simulationConfig.time_config?.peak_hours?.join(':00, ') }}:00</span>
                  <span class="period-multiplier">×{{ simulationConfig.time_config?.peak_activity_multiplier }}</span>
                </div>
                <div class="period-item">
                  <span class="period-label">工作時段</span>
                  <span class="period-hours">{{ simulationConfig.time_config?.work_hours?.[0] }}:00-{{ simulationConfig.time_config?.work_hours?.slice(-1)[0] }}:00</span>
                  <span class="period-multiplier">×{{ simulationConfig.time_config?.work_activity_multiplier }}</span>
                </div>
                <div class="period-item">
                  <span class="period-label">早間时段</span>
                  <span class="period-hours">{{ simulationConfig.time_config?.morning_hours?.[0] }}:00-{{ simulationConfig.time_config?.morning_hours?.slice(-1)[0] }}:00</span>
                  <span class="period-multiplier">×{{ simulationConfig.time_config?.morning_activity_multiplier }}</span>
                </div>
                <div class="period-item">
                  <span class="period-label">低谷时段</span>
                  <span class="period-hours">{{ simulationConfig.time_config?.off_peak_hours?.[0] }}:00-{{ simulationConfig.time_config?.off_peak_hours?.slice(-1)[0] }}:00</span>
                  <span class="period-multiplier">×{{ simulationConfig.time_config?.off_peak_activity_multiplier }}</span>
                </div>
              </div>
            </div>

            <!-- Agent 設定 -->
            <div class="config-block">
              <div class="config-block-header">
                <span class="config-block-title">Agent 設定</span>
                <span class="config-block-badge">{{ simulationConfig.agent_configs?.length || 0 }} 個</span>
              </div>
              <div class="agents-cards">
                <div 
                  v-for="agent in simulationConfig.agent_configs" 
                  :key="agent.agent_id" 
                  class="agent-card"
                >
                  <!-- 卡片头部 -->
                  <div class="agent-card-header">
                    <div class="agent-identity">
                      <span class="agent-id">Agent {{ agent.agent_id }}</span>
                      <span class="agent-name">{{ agent.entity_name }}</span>
                    </div>
                    <div class="agent-tags">
                      <span class="agent-type">{{ agent.entity_type }}</span>
                      <span class="agent-stance" :class="'stance-' + agent.stance">{{ agent.stance }}</span>
                    </div>
                  </div>
                  
                  <!-- 活躍時間轴 -->
                  <div class="agent-timeline">
                    <span class="timeline-label">活躍时段</span>
                    <div class="mini-timeline">
                      <div 
                        v-for="hour in 24" 
                        :key="hour - 1" 
                        class="timeline-hour"
                        :class="{ 'active': agent.active_hours?.includes(hour - 1) }"
                        :title="`${hour - 1}:00`"
                      ></div>
                    </div>
                    <div class="timeline-marks">
                      <span>0</span>
                      <span>6</span>
                      <span>12</span>
                      <span>18</span>
                      <span>24</span>
                    </div>
                  </div>

                  <!-- 行為參數 -->
                  <div class="agent-params">
                    <div class="param-group">
                      <div class="param-item">
                        <span class="param-label">發文/时</span>
                        <span class="param-value">{{ agent.posts_per_hour }}</span>
                      </div>
                      <div class="param-item">
                        <span class="param-label">留言/时</span>
                        <span class="param-value">{{ agent.comments_per_hour }}</span>
                      </div>
                      <div class="param-item">
                        <span class="param-label">回應延遲</span>
                        <span class="param-value">{{ agent.response_delay_min }}-{{ agent.response_delay_max }}min</span>
                      </div>
                    </div>
                    <div class="param-group">
                      <div class="param-item">
                        <span class="param-label">活躍度</span>
                        <span class="param-value with-bar">
                          <span class="mini-bar" :style="{ width: (agent.activity_level * 100) + '%' }"></span>
                          {{ (agent.activity_level * 100).toFixed(0) }}%
                        </span>
                      </div>
                      <div class="param-item">
                        <span class="param-label">情感傾向</span>
                        <span class="param-value" :class="agent.sentiment_bias > 0 ? 'positive' : agent.sentiment_bias < 0 ? 'negative' : 'neutral'">
                          {{ agent.sentiment_bias > 0 ? '+' : '' }}{{ agent.sentiment_bias?.toFixed(1) }}
                        </span>
                      </div>
                      <div class="param-item">
                        <span class="param-label">影响力</span>
                        <span class="param-value highlight">{{ agent.influence_weight?.toFixed(1) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 平台設定 -->
            <div class="config-block">
              <div class="config-block-header">
                <span class="config-block-title">推薦演算法設定</span>
              </div>
              <div class="platforms-grid">
                <div v-if="simulationConfig.twitter_config" class="platform-card">
                  <div class="platform-card-header">
                    <span class="platform-name">平台 1：廣場 / 資訊流</span>
                  </div>
                  <div class="platform-params">
                    <div class="param-row">
                      <span class="param-label">時效权重</span>
                      <span class="param-value">{{ simulationConfig.twitter_config.recency_weight }}</span>
                    </div>
                    <div class="param-row">
                      <span class="param-label">熱度权重</span>
                      <span class="param-value">{{ simulationConfig.twitter_config.popularity_weight }}</span>
                    </div>
                    <div class="param-row">
                      <span class="param-label">相關性权重</span>
                      <span class="param-value">{{ simulationConfig.twitter_config.relevance_weight }}</span>
                    </div>
                    <div class="param-row">
                      <span class="param-label">病毒阈值</span>
                      <span class="param-value">{{ simulationConfig.twitter_config.viral_threshold }}</span>
                    </div>
                    <div class="param-row">
                      <span class="param-label">回音室强度</span>
                      <span class="param-value">{{ simulationConfig.twitter_config.echo_chamber_strength }}</span>
                    </div>
                  </div>
                </div>
                <div v-if="simulationConfig.reddit_config" class="platform-card">
                  <div class="platform-card-header">
                    <span class="platform-name">平台 2：話題 / 社群</span>
                  </div>
                  <div class="platform-params">
                    <div class="param-row">
                      <span class="param-label">時效权重</span>
                      <span class="param-value">{{ simulationConfig.reddit_config.recency_weight }}</span>
                    </div>
                    <div class="param-row">
                      <span class="param-label">熱度权重</span>
                      <span class="param-value">{{ simulationConfig.reddit_config.popularity_weight }}</span>
                    </div>
                    <div class="param-row">
                      <span class="param-label">相關性权重</span>
                      <span class="param-value">{{ simulationConfig.reddit_config.relevance_weight }}</span>
                    </div>
                    <div class="param-row">
                      <span class="param-label">病毒阈值</span>
                      <span class="param-value">{{ simulationConfig.reddit_config.viral_threshold }}</span>
                    </div>
                    <div class="param-row">
                      <span class="param-label">回音室强度</span>
                      <span class="param-value">{{ simulationConfig.reddit_config.echo_chamber_strength }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- LLM 設定推理 -->
            <div v-if="simulationConfig.generation_reasoning" class="config-block">
              <div class="config-block-header">
                <span class="config-block-title">LLM 設定推理</span>
              </div>
              <div class="reasoning-content">
                <div 
                  v-for="(reason, idx) in simulationConfig.generation_reasoning.split('|').slice(0, 2)" 
                  :key="idx" 
                  class="reasoning-item"
                >
                  <p class="reasoning-text">{{ reason.trim() }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 04: 初始啟用編排 -->
      <div class="step-card" :class="{ 'active': phase === 3, 'completed': phase > 3 }">
        <div class="card-header">
          <div class="step-info">
            <span class="step-num">04</span>
            <span class="step-title">初始啟用編排</span>
          </div>
          <div class="step-status">
            <span v-if="phase > 3" class="badge success">已完成</span>
            <span v-else-if="phase === 3" class="badge processing">編排中</span>
            <span v-else class="badge pending">等待</span>
          </div>
        </div>

        <div class="card-content">
          <p class="api-note">POST /api/simulation/prepare</p>
          <p class="description">
            基於敘事方向，自動產生初始啟用事件與熱點話題，引導模擬世界的初始狀態
          </p>

          <div v-if="simulationConfig?.event_config" class="orchestration-content">
            <!-- 敘事方向 -->
            <div class="narrative-box">
              <span class="box-label narrative-label">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="special-icon">
                  <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="url(#paint0_linear)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M16.24 7.76L14.12 14.12L7.76 16.24L9.88 9.88L16.24 7.76Z" fill="url(#paint0_linear)" stroke="url(#paint0_linear)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <defs>
                    <linearGradient id="paint0_linear" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
                      <stop stop-color="#FF5722"/>
                      <stop offset="1" stop-color="#FF9800"/>
                    </linearGradient>
                  </defs>
                </svg>
                敘事引導方向
              </span>
              <p class="narrative-text">{{ simulationConfig.event_config.narrative_direction }}</p>
            </div>

            <!-- 熱點話題 -->
            <div class="topics-section">
              <span class="box-label">初始熱點話題</span>
              <div class="hot-topics-grid">
                <span v-for="topic in simulationConfig.event_config.hot_topics" :key="topic" class="hot-topic-tag">
                  # {{ topic }}
                </span>
              </div>
            </div>

            <!-- 初始帖子流 -->
            <div class="initial-posts-section">
              <span class="box-label">初始啟用序列 ({{ simulationConfig.event_config.initial_posts.length }})</span>
              <div class="posts-timeline">
                <div v-for="(post, idx) in simulationConfig.event_config.initial_posts" :key="idx" class="timeline-item">
                  <div class="timeline-marker"></div>
                  <div class="timeline-content">
                    <div class="post-header">
                      <span class="post-role">{{ post.poster_type }}</span>
                      <span class="post-agent-info">
                        <span class="post-id">Agent {{ post.poster_agent_id }}</span>
                        <span class="post-username">@{{ getAgentUsername(post.poster_agent_id) }}</span>
                      </span>
                    </div>
                    <p class="post-text">{{ post.content }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 05: 準備完成 -->
      <div class="step-card" :class="{ 'active': phase === 4 }">
        <div class="card-header">
          <div class="step-info">
            <span class="step-num">05</span>
            <span class="step-title">準備完成</span>
          </div>
          <div class="step-status">
            <span v-if="phase >= 4" class="badge processing">進行中</span>
            <span v-else class="badge pending">等待</span>
          </div>
        </div>

        <div class="card-content">
          <p class="api-note">POST /api/simulation/start</p>
          <p class="description">模擬環境已準備完成，可以開始运行模擬</p>
          
          <!-- 模擬輪數設定 - 只有在設定產生完成且輪數計算出来后才顯示 -->
          <div v-if="simulationConfig && autoGeneratedRounds" class="rounds-config-section">
            <div class="rounds-header">
              <div class="header-left">
                <span class="section-title">模擬輪數设定</span>
                <span class="section-desc">MiroFish 自動规划推演現實 <span class="desc-highlight">{{ simulationConfig?.time_config?.total_simulation_hours || '-' }}</span> 小時，每輪代表現實 <span class="desc-highlight">{{ simulationConfig?.time_config?.minutes_per_round || '-' }}</span> 分鐘時間流逝</span>
              </div>
              <label class="switch-control">
                <input type="checkbox" v-model="useCustomRounds">
                <span class="switch-track"></span>
                <span class="switch-label">自訂</span>
              </label>
            </div>
            
            <Transition name="fade" mode="out-in">
              <div v-if="useCustomRounds" class="rounds-content custom" key="custom">
                <div class="slider-display">
                  <div class="slider-main-value">
                    <span class="val-num">{{ customMaxRounds }}</span>
                    <span class="val-unit">轮</span>
                  </div>
                  <div class="slider-meta-info">
                    <span>若Agent规模为100：预计耗时约 {{ Math.round(customMaxRounds * 0.6) }} 分鐘</span>
                  </div>
                </div>

                <div class="range-wrapper">
                  <input 
                    type="range" 
                    v-model.number="customMaxRounds" 
                    min="10" 
                    :max="autoGeneratedRounds"
                    step="5"
                    class="minimal-slider"
                    :style="{ '--percent': ((customMaxRounds - 10) / (autoGeneratedRounds - 10)) * 100 + '%' }"
                  />
                  <div class="range-marks">
                    <span>10</span>
                    <span 
                      class="mark-recommend" 
                      :class="{ active: customMaxRounds === 40 }"
                      @click="customMaxRounds = 40"
                      :style="{ position: 'absolute', left: `calc(${(40 - 10) / (autoGeneratedRounds - 10) * 100}% - 30px)` }"
                    >40 (推薦)</span>
                    <span>{{ autoGeneratedRounds }}</span>
                  </div>
                </div>
              </div>
              
              <div v-else class="rounds-content auto" key="auto">
                <div class="auto-info-card">
                  <div class="auto-value">
                    <span class="val-num">{{ autoGeneratedRounds }}</span>
                    <span class="val-unit">轮</span>
                  </div>
                  <div class="auto-content">
                    <div class="auto-meta-row">
                      <span class="duration-badge">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        若Agent规模为100：预计耗时 {{ Math.round(autoGeneratedRounds * 0.6) }} 分鐘
                      </span>
                    </div>
                    <div class="auto-desc">
                      <p class="highlight-tip" @click="useCustomRounds = true">若首次运行，强烈建议切换至‘自訂模式’减少模擬輪數，以便快速预览效果並降低报错风险 ➝</p>
                    </div>
                  </div>
                </div>
              </div>
            </Transition>

            <!-- LLM 費用粗估（依 .env 模型 + 本模擬設定） -->
            <div class="cost-estimate-panel">
              <div class="cost-header">
                <span class="cost-title">LLM 費用粗估（OpenRouter）</span>
                <span v-if="costLoading" class="cost-loading">更新中…</span>
              </div>
              <p v-if="costError" class="cost-error">{{ costError }}</p>
              <template v-else-if="costEstimate">
                <div class="cost-model-row">
                  <span class="cost-label">試算模型</span>
                  <code class="cost-mono">{{ costEstimate.resolved_model_id }}</code>
                  <span v-if="costEstimate.pricing_source" class="cost-pricing-src">（{{ pricingSourceLabel(costEstimate.pricing_source) }}）</span>
                  <span v-if="trialModelOverride" class="cost-override-tag">試算中</span>
                  <button
                    v-if="trialModelOverride"
                    type="button"
                    class="cost-reset-btn"
                    @click="resetTrialModel"
                  >還原 .env 預設</button>
                </div>
                <div v-if="costEstimate.input_per_mtok != null" class="cost-unit-row">
                  <span>單價：input ${{ costEstimate.input_per_mtok }} / 1M tok，output ${{ costEstimate.output_per_mtok }} / 1M tok</span>
                </div>
                <div class="cost-range-row">
                  <span class="cost-usd">約 <strong>${{ costEstimate.usd_low }}</strong> ～ <strong>${{ costEstimate.usd_high }}</strong> USD</span>
                  <span class="cost-mid">中位 ${{ costEstimate.usd_mid }}</span>
                </div>
                <p class="cost-disclaimer">{{ costEstimate.disclaimer_zh }}</p>
                <div v-if="costEstimate.token_estimate" class="cost-tokens">
                  <span>有效輪數 {{ costEstimate.token_estimate.effective_rounds }}（設定上限 {{ costEstimate.token_estimate.total_rounds_config }} 輪），</span>
                  <span>平台數 {{ costEstimate.token_estimate.platforms_count }}，粗估 {{ costEstimate.token_estimate.estimated_llm_calls }} 次決策向 LLM</span>
                </div>

                <p v-if="costEstimate.recommend_cheaper?.length || costEstimate.recommend_premium?.length" class="rec-help">
                  點下方任何一張卡片可立即試算該模型的費用。決定使用後，把 id 貼到專案根目錄 <code class="cost-mono">.env</code> 的 <code class="cost-mono">LLM_MODEL_NAME</code>。
                </p>

                <div v-if="costEstimate.recommend_cheaper?.length" class="cost-rec-section">
                  <div class="rec-title">想省錢可考慮（同樣參數試算）</div>
                  <ul class="rec-list">
                    <li
                      v-for="m in costEstimate.recommend_cheaper"
                      :key="m.id"
                      :class="['rec-item', { active: m.id === costEstimate.resolved_model_id }]"
                      @click="selectTrialModel(m.id)"
                    >
                      <code class="cost-mono">{{ m.id }}</code>
                      <span class="rec-name">{{ m.name }}</span>
                      <span class="rec-price">in ${{ m.input_per_mtok }} / out ${{ m.output_per_mtok }} per 1M</span>
                      <span class="rec-usd">約 ${{ m.estimated_usd_mid }}</span>
                    </li>
                  </ul>
                </div>
                <div v-if="costEstimate.recommend_premium?.length" class="cost-rec-section premium">
                  <div class="rec-title">要更強推理可試（通常較貴）</div>
                  <ul class="rec-list">
                    <li
                      v-for="m in costEstimate.recommend_premium"
                      :key="m.id"
                      :class="['rec-item', { active: m.id === costEstimate.resolved_model_id }]"
                      @click="selectTrialModel(m.id)"
                    >
                      <code class="cost-mono">{{ m.id }}</code>
                      <span class="rec-name">{{ m.name }}</span>
                      <span class="rec-price">in ${{ m.input_per_mtok }} / out ${{ m.output_per_mtok }} per 1M</span>
                      <span class="rec-usd">約 ${{ m.estimated_usd_mid }}</span>
                    </li>
                  </ul>
                </div>
                <a
                  :href="costEstimate.openrouter_models_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="cost-link"
                >OpenRouter 模型列表（即時單價）↗</a>
              </template>
            </div>
          </div>

          <div class="action-group dual">
            <button 
              class="action-btn secondary"
              @click="$emit('go-back')"
            >
              ← 返回圖譜建立
            </button>
            <button 
              class="action-btn primary"
              :disabled="phase < 4"
              @click="handleStartSimulation"
            >
              開始雙世界並行模擬 ➝
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Profile Detail Modal -->
    <Transition name="modal">
      <div v-if="selectedProfile" class="profile-modal-overlay" @click.self="selectedProfile = null">
        <div class="profile-modal">
          <div class="modal-header">
          <div class="modal-header-info">
            <div class="modal-name-row">
              <span class="modal-realname">{{ selectedProfile.username }}</span>
              <span class="modal-username">@{{ selectedProfile.name }}</span>
            </div>
            <span class="modal-profession">{{ selectedProfile.profession }}</span>
          </div>
          <button class="close-btn" @click="selectedProfile = null">×</button>
        </div>
        
        <div class="modal-body">
          <!-- 基本信息 -->
          <div class="modal-info-grid">
            <div class="info-item">
              <span class="info-label">事件外顯年龄</span>
              <span class="info-value">{{ selectedProfile.age || '-' }} 岁</span>
            </div>
            <div class="info-item">
              <span class="info-label">事件外顯性别</span>
              <span class="info-value">{{ { male: '男', female: '女', other: '其他' }[selectedProfile.gender] || selectedProfile.gender }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">国家/地区</span>
              <span class="info-value">{{ selectedProfile.country || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">事件外顯MBTI</span>
              <span class="info-value mbti">{{ selectedProfile.mbti || '-' }}</span>
            </div>
          </div>

          <!-- 简介 -->
          <div class="modal-section">
            <span class="section-label">人設简介</span>
            <p class="section-bio">{{ selectedProfile.bio || '暫無簡介' }}</p>
          </div>

          <!-- 关注話題 -->
          <div class="modal-section" v-if="selectedProfile.interested_topics?.length">
            <span class="section-label">現實种子關聯話題</span>
            <div class="topics-grid">
              <span 
                v-for="topic in selectedProfile.interested_topics" 
                :key="topic" 
                class="topic-item"
              >{{ topic }}</span>
            </div>
          </div>

          <!-- 詳細人設 -->
          <div class="modal-section" v-if="selectedProfile.persona">
            <span class="section-label">詳細人設背景</span>
            
            <!-- 人設维度概览 -->
            <div class="persona-dimensions">
              <div class="dimension-card">
                <span class="dim-title">事件全景經歷</span>
                <span class="dim-desc">在此事件中的完整行為軌跡</span>
              </div>
              <div class="dimension-card">
                <span class="dim-title">行為模式侧写</span>
                <span class="dim-desc">经验总结與行事风格偏好</span>
              </div>
              <div class="dimension-card">
                <span class="dim-title">獨特記憶印记</span>
                <span class="dim-desc">基於現實种子形成的記憶</span>
              </div>
              <div class="dimension-card">
                <span class="dim-title">社会關係网络</span>
                <span class="dim-desc">個體链接與交互圖譜</span>
              </div>
            </div>

            <div class="persona-content">
              <p class="section-persona">{{ selectedProfile.persona }}</p>
            </div>
          </div>
        </div>
      </div>
      </div>
    </Transition>

    <!-- Bottom Info / Logs -->
    <div class="system-logs">
      <div class="log-header">
        <span class="log-title">SYSTEM DASHBOARD</span>
        <span class="log-id">{{ simulationId || 'NO_SIMULATION' }}</span>
      </div>
      <div class="log-content" ref="logContent">
        <div class="log-line" v-for="(log, idx) in systemLogs" :key="idx">
          <span class="log-time">{{ log.time }}</span>
          <span class="log-msg">{{ log.msg }}</span>
        </div>
      </div>
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
  simulationId: String,  // 從父组件传入
  projectData: Object,
  graphData: Object,
  systemLogs: Array
})

const emit = defineEmits(['go-back', 'next-step', 'add-log', 'update-status'])

// State
const phase = ref(0) // 0: 初始化, 1: 產生人設, 2: 產生設定, 3: 完成
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

// 日誌去重：記錄上一次輸出的關鍵資訊
let lastLoggedMessage = ''
let lastLoggedProfileCount = 0
let lastLoggedConfigStage = ''

// 模擬輪數設定
const useCustomRounds = ref(false) // 預設使用自動設定輪數
const customMaxRounds = ref(40)   // 預設推薦 40 輪

// Watch stage to update phase
watch(currentStage, (newStage) => {
  if (newStage === 'generating_profiles') {
    phase.value = 1
  } else if (newStage === 'generating_config') {
    phase.value = 2
    // 進入設定產生階段，開始輪詢設定
    if (!configTimer) {
      addLog('開始產生雙平台模擬設定...')
      startConfigPolling()
    }
  } else if (newStage === 'copying_scripts') {
    phase.value = 2 // 仍屬於設定階段
  }
})

// 從設定中計算自動產生的輪數（不使用硬編碼預設值）
const autoGeneratedRounds = computed(() => {
  if (!simulationConfig.value?.time_config) {
    return null // 設定未產生時返回 null
  }
  const totalHours = simulationConfig.value.time_config.total_simulation_hours
  const minutesPerRound = simulationConfig.value.time_config.minutes_per_round
  if (!totalHours || !minutesPerRound) {
    return null // 設定資料不完整時返回 null
  }
  const calculatedRounds = Math.floor((totalHours * 60) / minutesPerRound)
  // 確保最大輪數不小於 40（推薦值），避免滑動條範圍異常
  return Math.max(calculatedRounds, 40)
})

// LLM 費用粗估（OpenRouter）
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
    costError.value = e.message || '無法估算費用'
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

// 根據agent_id取得对应的username
const getAgentUsername = (agentId) => {
  if (profiles.value && profiles.value.length > agentId && agentId >= 0) {
    const profile = profiles.value[agentId]
    return profile?.username || `agent_${agentId}`
  }
  return `agent_${agentId}`
}

// 計算所有人設的關聯話題总数
const totalTopicsCount = computed(() => {
  return profiles.value.reduce((sum, p) => {
    return sum + (p.interested_topics?.length || 0)
  }, 0)
})

// Methods
const addLog = (msg) => {
  emit('add-log', msg)
}

// 处理開始模擬按钮点击
const handleStartSimulation = () => {
  // 建立傳遞给父组件的參數
  const params = {}
  
  if (useCustomRounds.value) {
    // 用戶自訂輪數，傳遞 max_rounds 參數
    params.maxRounds = customMaxRounds.value
    addLog(`開始模擬，自訂輪數: ${customMaxRounds.value} 輪`)
  } else {
    // 用戶選擇保持自動產生的輪數，不傳遞 max_rounds 參數
    addLog(`開始模擬，使用自動設定輪數: ${autoGeneratedRounds.value} 輪`)
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

// 自動開始準備模擬
const startPrepareSimulation = async () => {
  if (!props.simulationId) {
    addLog('錯誤：缺少 simulationId')
    emit('update-status', 'error')
    return
  }
  
  // 标记第一步完成，開始第二步
  phase.value = 1
  addLog(`模擬實例已创建: ${props.simulationId}`)
  addLog('正在準備模擬環境...')
  emit('update-status', 'processing')
  
  try {
    const res = await prepareSimulation({
      simulation_id: props.simulationId,
      use_llm_for_profiles: true,
      parallel_profile_count: 5
    })
    
    if (res.success && res.data) {
      if (res.data.already_prepared) {
        addLog('偵測到已有完成的準備工作，直接使用')
        await loadPreparedData()
        return
      }
      
      taskId.value = res.data.task_id
      addLog(`準備任務已啟動`)
      addLog(`  └─ Task ID: ${res.data.task_id}`)
      
      // 立即設定預期Agent总数（從prepare接口返回值取得）
      if (res.data.expected_entities_count) {
        expectedTotal.value = res.data.expected_entities_count
        addLog(`從Zep圖譜读取到 ${res.data.expected_entities_count} 個實體`)
        if (res.data.entity_types && res.data.entity_types.length > 0) {
          addLog(`  └─ 實體类型: ${res.data.entity_types.join(', ')}`)
        }
      }
      
      addLog('開始輪詢準備进度...')
      // 開始輪詢进度
      startPolling()
      // 開始即時取得 Profiles
      startProfilesPolling()
    } else {
      addLog(`準備失敗: ${res.error || '未知錯誤'}`)
      emit('update-status', 'error')
    }
  } catch (err) {
    addLog(`準備異常: ${err.message}`)
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
      
      // 更新進度
      prepareProgress.value = data.progress || 0
      progressMessage.value = data.message || ''
      
      // 解析階段信息並輸出詳細日誌
      if (data.progress_detail) {
        // 優先使用後端英文 stage key，避免依賴簡體／繁體顯示名
        currentStage.value = data.progress_detail.current_stage || ''
        
        // 輸出詳細進度日誌（避免重複）
        const detail = data.progress_detail
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
        // 從訊息中提取階段
        const match = data.message.match(/\[(\d+)\/(\d+)\]\s*([^:]+)/)
        if (match) {
          const label = match[3].trim()
          const stageByLabel = {
            '读取图谱实体': 'reading',
            '讀取圖譜實體': 'reading',
            '生成Agent人设': 'generating_profiles',
            '產生 Agent 人設': 'generating_profiles',
            '生成模拟配置': 'generating_config',
            '產生模擬設定': 'generating_config',
            '准备模拟脚本': 'copying_scripts',
            '準備模擬腳本': 'copying_scripts'
          }
          currentStage.value = stageByLabel[label] || label
        }
        // 輸出訊息日誌（避免重複）
        if (data.message !== lastLoggedMessage) {
          lastLoggedMessage = data.message
          addLog(data.message)
        }
      }
      
      // 檢查是否完成
      if (data.status === 'completed' || data.status === 'ready' || data.already_prepared) {
        addLog('✓ 準備工作已完成')
        stopPolling()
        stopProfilesPolling()
        await loadPreparedData()
      } else if (data.status === 'failed') {
        addLog(`✗ 準備失敗: ${data.error || '未知錯誤'}`)
        stopPolling()
        stopProfilesPolling()
      }
    }
  } catch (err) {
    console.warn('輪詢狀態失敗:', err)
  }
}

const fetchProfilesRealtime = async () => {
  if (!props.simulationId) return
  
  try {
    const res = await getSimulationProfilesRealtime(props.simulationId, 'reddit')
    
    if (res.success && res.data) {
      const prevCount = profiles.value.length
      profiles.value = res.data.profiles || []
      // 只有当 API 返回有效值时才更新，避免覆盖已有的有效值
      if (res.data.total_expected) {
        expectedTotal.value = res.data.total_expected
      }
      
      // 提取實體类型
      const types = new Set()
      profiles.value.forEach(p => {
        if (p.entity_type) types.add(p.entity_type)
      })
      entityTypes.value = Array.from(types)
      
      // 輸出 Profile 產生进度日誌（仅当数量变化时）
      const currentCount = profiles.value.length
      if (currentCount > 0 && currentCount !== lastLoggedProfileCount) {
        lastLoggedProfileCount = currentCount
        const total = expectedTotal.value || '?'
        const latestProfile = profiles.value[currentCount - 1]
        const profileName = latestProfile?.name || latestProfile?.username || `Agent_${currentCount}`
        if (currentCount === 1) {
          addLog(`開始產生Agent人設...`)
        }
        addLog(`→ Agent人設 ${currentCount}/${total}: ${profileName} (${latestProfile?.profession || '未知職業'})`)
        
        // 如果全部產生完成
        if (expectedTotal.value && currentCount >= expectedTotal.value) {
          addLog(`✓ 全部 ${currentCount} 個Agent人設產生完成`)
        }
      }
    }
  } catch (err) {
    console.warn('取得 Profiles 失敗:', err)
  }
}

// 設定輪詢
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
      
      // 輸出設定產生階段日誌（避免重复）
      if (data.generation_stage && data.generation_stage !== lastLoggedConfigStage) {
        lastLoggedConfigStage = data.generation_stage
        if (data.generation_stage === 'generating_profiles') {
          addLog('正在產生Agent人設設定...')
        } else if (data.generation_stage === 'generating_config') {
          addLog('正在呼叫LLM產生模擬設定參數...')
        }
      }
      
      // 如果設定已產生
      if (data.config_generated && data.config) {
        simulationConfig.value = data.config
        addLog('✓ 模擬設定產生完成')
        
        // 顯示詳細設定摘要
        if (data.summary) {
          addLog(`  ├─ Agent数量: ${data.summary.total_agents}个`)
          addLog(`  ├─ 模擬時長: ${data.summary.simulation_hours}小時`)
          addLog(`  ├─ 初始帖子: ${data.summary.initial_posts_count}条`)
          addLog(`  ├─ 熱點話題: ${data.summary.hot_topics_count}个`)
          addLog(`  └─ 平台設定: Twitter ${data.summary.has_twitter_config ? '✓' : '✗'}, Reddit ${data.summary.has_reddit_config ? '✓' : '✗'}`)
        }
        
        // 顯示時間設定詳情
        if (data.config.time_config) {
          const tc = data.config.time_config
          addLog(`時間設定: 每輪${tc.minutes_per_round}分鐘, 共${Math.floor((tc.total_simulation_hours * 60) / tc.minutes_per_round)}轮`)
        }
        
        // 顯示事件設定
        if (data.config.event_config?.narrative_direction) {
          const narrative = data.config.event_config.narrative_direction
          addLog(`敘事方向: ${narrative.length > 50 ? narrative.substring(0, 50) + '...' : narrative}`)
        }
        
        stopConfigPolling()
        phase.value = 4
        addLog('✓ 環境搭建完成，可以開始模擬')
        emit('update-status', 'completed')
      }
    }
  } catch (err) {
    console.warn('取得 Config 失敗:', err)
  }
}

const loadPreparedData = async () => {
  phase.value = 2
  addLog('正在載入已有設定資料...')

  // 最后取得一次 Profiles
  await fetchProfilesRealtime()
  addLog(`已載入 ${profiles.value.length} 個Agent人設`)

  // 取得設定（使用即時接口）
  try {
    const res = await getSimulationConfigRealtime(props.simulationId)
    if (res.success && res.data) {
      if (res.data.config_generated && res.data.config) {
        simulationConfig.value = res.data.config
        addLog('✓ 模擬設定載入成功')
        
        // 顯示詳細設定摘要
        if (res.data.summary) {
          addLog(`  ├─ Agent数量: ${res.data.summary.total_agents}个`)
          addLog(`  ├─ 模擬時長: ${res.data.summary.simulation_hours}小時`)
          addLog(`  └─ 初始帖子: ${res.data.summary.initial_posts_count}条`)
        }
        
        addLog('✓ 環境搭建完成，可以開始模擬')
        phase.value = 4
        emit('update-status', 'completed')
      } else {
        // 設定尚未產生，開始輪詢
        addLog('設定產生中，開始輪詢等待...')
        startConfigPolling()
      }
    }
  } catch (err) {
    addLog(`載入設定失敗: ${err.message}`)
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
  // 自動開始準備流程
  if (props.simulationId) {
    addLog('Step2 環境搭建初始化')
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

/* 基本信息网格 */
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

/* 模块区域 */
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

/* 話題标签 */
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

/* 詳細人設 */
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

/* 模擬輪數設定样式 */
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

/* LLM 費用粗估 */
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
</style>
