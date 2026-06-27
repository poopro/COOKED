import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './nous-theme.css'
import './zh-tw-branding.js'

const app = createApp(App)

app.use(router)

app.mount('#app')


