import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios' // 1. Axios import kiya
import './style.css'
import App from './App.vue'
import router from './router'

import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import 'primeicons/primeicons.css'

// Global Components
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Select from 'primevue/select';
import Dialog from 'primevue/dialog';

const app = createApp(App)

// 2. Axios Global Base URL Setup
// Ab aapko har jagah https://raspandey... likhne ki zaroorat nahi hai
axios.defaults.baseURL = 'https://raspandey.pythonanywhere.com/api';
app.config.globalProperties.$axios = axios;

app.component('InputText', InputText);
app.component('Password', Password);
app.component('Button', Button);
app.component('Select', Select);
app.component('Dialog', Dialog);

const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: { darkModeSelector: 'none' }
  }
})

app.mount('#app')