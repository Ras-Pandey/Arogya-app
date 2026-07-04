<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div class="flex h-screen bg-gray-50 font-sans text-gray-800 overflow-hidden">
    
    <Sidebar />

    <div class="flex-1 flex flex-col overflow-hidden relative">
      <header class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8 shadow-sm z-10">
        <h2 class="text-lg font-bold text-gray-700 tracking-tight">Dashboard</h2>
        <div class="flex items-center space-x-5">
          <span class="text-sm font-semibold text-gray-500 bg-gray-100 px-3 py-1 rounded-full border border-gray-200">FY: 2026-2027</span>
          <div class="h-9 w-9 rounded-full bg-emerald-100 border border-emerald-200 text-emerald-700 flex items-center justify-center font-bold shadow-sm cursor-pointer hover:bg-emerald-200">
            S
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-y-auto p-8">
         <router-view></router-view> 
      </main>

      <footer class="bg-white border-t border-gray-200 px-6 py-3 flex justify-between items-center shadow-[0_-4px_15px_rgba(0,0,0,0.02)] z-10">
  <div class="flex space-x-6 text-sm">
    <span class="flex items-center text-gray-600 font-medium">
      <kbd class="bg-white border border-gray-300 shadow-sm rounded px-2 py-0.5 text-xs font-bold text-gray-800 mr-2">F2</kbd> Add
    </span>
    <span class="flex items-center text-gray-600 font-medium">
      <kbd class="bg-white border border-gray-300 shadow-sm rounded px-2 py-0.5 text-xs font-bold text-gray-800 mr-2">F3</kbd> Edit
    </span>
    <span class="flex items-center text-gray-600 font-medium">
      <kbd class="bg-white border border-gray-300 shadow-sm rounded px-2 py-0.5 text-xs font-bold text-gray-800 mr-2">Del</kbd> Delete
    </span>
    <span class="flex items-center text-gray-600 font-medium">
      <kbd class="bg-white border border-gray-300 shadow-sm rounded px-2 py-0.5 text-xs font-bold text-gray-800 mr-2">F10</kbd> Save
    </span>
    <span class="flex items-center text-gray-600 font-medium">
      <kbd class="bg-white border border-gray-300 shadow-sm rounded px-2 py-0.5 text-xs font-bold text-gray-800 mr-2">Esc</kbd> Close / Cancel
    </span>
  </div>
  <div class="text-xs font-medium text-gray-400">Arogya-App v1.0 | Fast Billing Engine</div>
</footer>
    </div>
  </div>
</template>