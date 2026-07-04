<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const stocks = ref([])
const loading = ref(true)

const fetchStock = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/transactions/stocks/')
        stocks.value = response.data
    } catch (error) { console.error(error) } finally { loading.value = false }
}

onMounted(() => fetchStock())
</script>

<template>
  <div class="w-full max-w-7xl mx-auto p-8">
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
            <h2 class="text-lg font-bold text-slate-800">Current Live Stock</h2>
            <Button icon="pi pi-refresh" text @click="fetchStock" />
        </div>
        <DataTable :value="stocks" :loading="loading" stripedRows class="p-datatable-sm text-sm">
            <Column field="medicine_name" header="Medicine"></Column>
            <Column field="batch_no" header="Batch"></Column>
            <Column field="expiry_date" header="Expiry"></Column>
            <Column field="current_qty" header="Available Qty" class="font-bold text-emerald-600"></Column>
            <Column field="mrp" header="MRP"></Column>
        </DataTable>
    </div>
  </div>
</template>