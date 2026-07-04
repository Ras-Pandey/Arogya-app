import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
// IMPORT KO GLOBAL SCOPE SE HATA RAHE HAIN TAKI ERROR NA AAYE
import CompanyMaster from '../views/CompanyMaster.vue'
import MedicineMaster from '../views/MedicineMaster.vue'
import SaltMaster from '../views/SaltMaster.vue'
import SupplierMaster from '../views/SupplierMaster.vue'
import PurchaseEntry from '../views/PurchaseEntry.vue'
import StockRegister from '../views/StockRegister.vue'
import PurchaseList from '../views/PurchaseList.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  { path: '/', redirect: '/company' },
  { path: '/login', component: LoginView },
  { path: '/company', component: CompanyMaster },
  { path: '/salt', component: SaltMaster },
  { path: '/medicine', component: MedicineMaster },
  { path: '/supplier', component: SupplierMaster },
  { path: '/purchase', component: PurchaseEntry },
  { path: '/stock', component: StockRegister },
  { path: '/purchase-list', component: PurchaseList },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation Guard (Logic yahan function ke andar hai)
// router.beforeEach((to, from, next) => {
//   // Yahan import karne se "Active Pinia" ka error nahi aayega
//   import('../stores/auth').then(({ useAuthStore }) => {
//     const authStore = useAuthStore()

//     if (to.path !== '/login' && !authStore.isAuthenticated) {
//       next('/login')
//     } else if (to.path === '/login' && authStore.isAuthenticated) {
//       next('/company')
//     } else {
//       next()
//     }
//   })
// })

// export default router


router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (!authStore.isAuthenticated && to.path !== '/login') {
    return '/login'
  }
  if (authStore.isAuthenticated && to.path === '/login') {
    return '/company'
  }
})

export default router