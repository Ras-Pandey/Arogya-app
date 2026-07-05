import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Existing Imports
import CompanyMaster from '../views/CompanyMaster.vue'
import MedicineMaster from '../views/MedicineMaster.vue'
import SaltMaster from '../views/SaltMaster.vue'
import SupplierMaster from '../views/SupplierMaster.vue'
import PurchaseEntry from '../views/PurchaseEntry.vue'
import StockRegister from '../views/StockRegister.vue'
import PurchaseList from '../views/PurchaseList.vue'
import LoginView from '../views/LoginView.vue'
// Naya Import: Billing View
import BillingView from '../views/BillingView.vue'

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
  { path: '/billing', name: 'billing', component: BillingView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Updated Navigation Guard
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