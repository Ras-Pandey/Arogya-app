<script setup>
import { computed, onMounted, ref } from 'vue'
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'
import { useAuthStore } from './stores/auth'
import { useRoute } from 'vue-router'

// Variable ko ref ke roop mein rakhein
const authStore = ref(null)
const isReady = ref(false)

onMounted(() => {
  // Mount hone ke baad store initialize karein
  authStore.value = useAuthStore()
  isReady.value = true
})

const route = useRoute()
const showLayout = computed(() => route.path !== '/login')
</script>

<template>
  <div v-if="isReady" class="flex h-screen bg-gray-50 font-sans text-gray-800 overflow-hidden">
    <Sidebar v-if="showLayout && authStore.isAuthenticated" />

    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar v-if="showLayout && authStore.isAuthenticated" />

      <main class="flex-1 overflow-y-auto p-8">
         <router-view></router-view> 
      </main>
    </div>
  </div>
</template>