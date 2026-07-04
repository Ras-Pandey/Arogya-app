import { createRouter, createWebHistory } from 'vue-router'
import CompanyMaster from '../views/CompanyMaster.vue'
import MedicineMaster from '../views/MedicineMaster.vue'
import SaltMaster from '../views/SaltMaster.vue'
import SupplierMaster from '../views/SupplierMaster.vue'
import PurchaseEntry from '../views/PurchaseEntry.vue'
import StockRegister from '../views/StockRegister.vue'

const routes = [
  { path: '/', redirect: '/company' },
  { path: '/company', component: CompanyMaster },
  { path: '/salt', component: SaltMaster },
  { path: '/medicine', component: MedicineMaster },
  { path: '/supplier', component: SupplierMaster },
  { path: '/purchase', component: PurchaseEntry },
  { path: '/stock', component: StockRegister },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router