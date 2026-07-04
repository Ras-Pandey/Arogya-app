<script setup>
</script>

<template>
  <aside class="w-64 bg-slate-900 text-white flex flex-col shadow-xl z-20 transition-all duration-300">
    <div class="h-16 flex items-center justify-center border-b border-slate-800">
      <h1 class="text-2xl font-bold text-emerald-400 tracking-wide">
        Arogya<span class="text-white">App</span>
      </h1>
    </div>
    
    <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
      <p class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-3 mt-2">Masters</p>
      
      <router-link to="/company" class="flex items-center px-4 py-2.5 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors" active-class="bg-emerald-500/15 text-emerald-400 border border-emerald-500/20 shadow-sm">
        <i class="pi pi-building mr-3"></i> Company Master
      </router-link>
      <router-link to="/salt" class="flex items-center px-4 py-2.5 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors" active-class="bg-emerald-500/15 text-emerald-400 border border-emerald-500/20 shadow-sm">
        <i class="pi pi-receipt mr-3"></i> Salt / Formula Master
      </router-link>
      
      <router-link to="/medicine" class="flex items-center px-4 py-2.5 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors" active-class="bg-emerald-500/15 text-emerald-400 border border-emerald-500/20 shadow-sm">
        <i class="pi pi-box mr-3"></i> Medicine Master
      </router-link>
      
      <p class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-3 mt-6">Transactions</p>
      <a href="#" class="flex items-center px-4 py-2.5 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
        <i class="pi pi-shopping-cart mr-3"></i> Purchase (In)
      </a>
      <a href="#" class="flex items-center px-4 py-2.5 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
        <i class="pi pi-receipt mr-3"></i> Billing (POS)
      </a>
    </nav>
  </aside>
</template>