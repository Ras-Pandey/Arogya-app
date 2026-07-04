<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = ref(null)
const router = useRouter()

onMounted(() => {
  authStore.value = useAuthStore()
})

const handleLogout = () => {
  authStore.value.setLogout()
  router.push('/login')
}
</script>

<template>
  <header v-if="authStore" class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8 shadow-sm">
    <h2 class="text-lg font-bold text-gray-700">Dashboard</h2>
    <div class="flex items-center space-x-5">
      <span class="text-sm font-medium text-gray-700">User: {{ authStore.user }}</span>
      <button @click="handleLogout" class="text-red-600 font-bold hover:underline">Signout</button>
    </div>
  </header>
</template>