import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // Router import kiya

import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import 'primeicons/primeicons.css' // Yeh line hona mandatory hai!

const app = createApp(App)

app.use(router) // Router activate kiya
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: { darkModeSelector: 'none' }
  }
})

app.mount('#app')