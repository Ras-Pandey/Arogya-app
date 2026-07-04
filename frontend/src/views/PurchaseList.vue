<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'

const bills = ref([])
const selectedBill = ref(null) // Detail store karne ke liye
const displayDialog = ref(false) // Dialog control karne ke liye

const fetchBills = async () => {
    try {
        const res = await axios.get('http://127.0.0.1:8000/api/transactions/purchases/')
        bills.value = res.data
    } catch (e) { console.error(e) }
}

const showDetail = (bill) => {
    selectedBill.value = bill
    displayDialog.value = true
}

const cancelBill = async (id) => {
    if(confirm("Are you sure?")) {
        try {
            await axios.post(`http://127.0.0.1:8000/api/transactions/purchases/${id}/cancel/`)
            await fetchBills()
            displayDialog.value = false // Cancel ke baad dialog band
        } catch (e) { alert("Error!") }
    }
}

onMounted(fetchBills)
</script>

<template>
  <div class="p-4">
    <DataTable :value="bills" stripedRows paginator :rows="10">
        <Column field="bill_no" header="Bill No"></Column>
        <Column field="total_amount" header="Amount"></Column>
        <Column header="Status">
            <template #body="s">
                <span :class="s.data.is_cancelled ? 'text-red-600' : 'text-green-600'">
                    {{ s.data.is_cancelled ? 'CANCELLED' : 'ACTIVE' }}
                </span>
            </template>
        </Column>
        <Column header="Action">
            <template #body="s">
                <div class="flex gap-2">
                    <Button icon="pi pi-eye" text rounded @click="showDetail(s.data)" />
                    <Button v-if="!s.data.is_cancelled" icon="pi pi-ban" text rounded severity="danger" @click="cancelBill(s.data.id)" />
                </div>
            </template>
        </Column>
    </DataTable>

    <Dialog v-model:visible="displayDialog" modal :header="'Bill Details - ' + (selectedBill?.is_cancelled ? 'CANCELLED' : 'ACTIVE')" :style="{ width: '50vw' }">
    
    <div v-if="selectedBill?.is_cancelled" class="bg-red-500 text-white p-2 text-center font-bold mb-4 rounded">
        THIS BILL IS CANCELLED
    </div>

    <div v-if="selectedBill" class="space-y-4">
        <div class="grid grid-cols-2 gap-4 border-b pb-4">
            <p><strong>Bill No:</strong> {{ selectedBill.bill_no }}</p>
            <p><strong>Date:</strong> {{ selectedBill.bill_date }}</p>
            <p><strong>Supplier:</strong> {{ selectedBill.supplier_name }}</p>
            <p><strong>Total:</strong> ₹{{ selectedBill.total_amount }}</p>
        </div>
        
        <DataTable :value="selectedBill.items" size="small">
            <Column field="medicine" header="Medicine"></Column>
            <Column field="qty" header="Qty"></Column>
            <Column field="purchase_rate" header="Rate"></Column>
        </DataTable>
    </div>
    
    <template #footer>
        <Button label="Close" text @click="displayDialog = false" />
        <Button v-if="!selectedBill?.is_cancelled" label="Cancel Bill" severity="danger" @click="cancelBill(selectedBill.id)" />
    </template>
</Dialog>
  </div>
</template>