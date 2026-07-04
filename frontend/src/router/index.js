import { createRouter, createWebHistory } from 'vue-router'
import CompanyMaster from '../views/CompanyMaster.vue'
import MedicineMaster from '../views/MedicineMaster.vue'
import SaltMaster from '../views/SaltMaster.vue' // Naya Import

const routes = [
  { path: '/', redirect: '/company' },
  { path: '/company', component: CompanyMaster },
  { path: '/salt', component: SaltMaster }, // Naya Route
  { path: '/medicine', component: MedicineMaster },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router