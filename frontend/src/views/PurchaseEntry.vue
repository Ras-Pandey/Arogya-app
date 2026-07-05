<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const suppliers = ref([])
const medicines = ref([])
const isSaving = ref(false)

const header = ref({
    supplier: null,
    bill_no: '',
    bill_date: new Date().toISOString().split('T')[0],
})

const currentItem = ref({
    medicine: null,
    batch_no: '',
    expiry_date: '',
    qty: null,
    mrp: null,
    purchase_rate: null
})

const items = ref([])

const totalAmount = computed(() => {
    return items.value.reduce((sum, item) => sum + (item.qty * item.purchase_rate), 0)
})

const fetchData = async () => {
    try {
        const [supRes, medRes] = await Promise.all([
            axios.get('/transactions/suppliers/'),
            axios.get('/medicines/')
        ])
        suppliers.value = supRes.data
        medicines.value = medRes.data
    } catch (error) { console.error(error) }
}

const addItem = () => {
    if (!currentItem.value.medicine || !currentItem.value.batch_no || !currentItem.value.qty || !currentItem.value.mrp || !currentItem.value.purchase_rate) {
        alert("Saari fields bharna zaroori hai!")
        return
    }
    
    const selectedMed = medicines.value.find(m => m.id === currentItem.value.medicine)
    
    items.value.push({
        ...currentItem.value,
        medicine_name: selectedMed.name
    })

    currentItem.value = { medicine: null, batch_no: '', expiry_date: '', qty: null, mrp: null, purchase_rate: null }
}

// EDIT FUNCTION: Item ko wapas input grid mein laata hai
const editItem = (item, index) => {
    currentItem.value = { ...item }
    items.value.splice(index, 1)
}

const removeItem = (index) => {
    items.value.splice(index, 1)
}

const savePurchaseBill = async () => {
    if (!header.value.supplier || !header.value.bill_no || items.value.length === 0) {
        alert("Bill details incomplete hain ya items nahi hain!")
        return
    }

    isSaving.value = true
    try {
        const payload = {
            supplier: header.value.supplier,
            bill_no: header.value.bill_no,
            bill_date: header.value.bill_date,
            total_amount: totalAmount.value,
            items: items.value.map(item => ({
                medicine: item.medicine,
                batch_no: item.batch_no,
                expiry_date: item.expiry_date,
                qty: item.qty,
                mrp: item.mrp,
                purchase_rate: item.purchase_rate
            }))
        }

        await axios.post('/transactions/purchases/', payload)
        alert("Bill Saved & Stock Updated Successfully! 🎉")
        
        header.value = { supplier: null, bill_no: '', bill_date: new Date().toISOString().split('T')[0] }
        items.value = []
    } catch (error) { 
        console.error(error)
        alert("Error saving bill!")
    } finally { 
        isSaving.value = false 
    }
}

onMounted(() => { fetchData() })
</script>

<template>
  <div class="w-full max-w-7xl mx-auto p-6 md:p-8 flex flex-col gap-8 font-sans">
      
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-8 py-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
              <h2 class="text-lg font-bold text-slate-800">Purchase Entry</h2>
              <span class="text-xs font-bold tracking-wider uppercase bg-blue-100 text-blue-700 px-3 py-1 rounded-full">Stock In</span>
          </div>
          
          <div class="p-8 grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                  <label class="block text-[13px] font-bold text-slate-700 mb-2">Supplier <span class="text-red-500">*</span></label>
                  <Dropdown v-model="header.supplier" :options="suppliers" optionLabel="name" optionValue="id" placeholder="Select Supplier" class="w-full erp-input" filter />
              </div>
              
              <div>
                  <label class="block text-[13px] font-bold text-slate-700 mb-2">Bill Number <span class="text-red-500">*</span></label>
                  <InputText v-model="header.bill_no" placeholder="e.g. INV-1001" class="w-full uppercase erp-input" />
              </div>
              
              <div>
                  <label class="block text-[13px] font-bold text-slate-700 mb-2">Bill Date <span class="text-red-500">*</span></label>
                  <InputText v-model="header.bill_date" type="date" class="w-full erp-input" />
              </div>
          </div>
      </div>

      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-8 py-4 border-b border-slate-200 bg-slate-50">
              <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wide">Add Item Details</h3>
          </div>

          <div class="p-8">
              <div class="grid grid-cols-12 gap-5 items-end">
                  
                  <div class="col-span-12 md:col-span-3">
                      <label class="block text-[13px] font-bold text-slate-700 mb-2">Medicine</label>
                      <Dropdown v-model="currentItem.medicine" :options="medicines" optionLabel="name" optionValue="id" placeholder="Select Item" class="w-full erp-input" filter />
                  </div>
                  
                  <div class="col-span-6 md:col-span-2">
                      <label class="block text-[13px] font-bold text-slate-700 mb-2">Batch No</label>
                      <InputText v-model="currentItem.batch_no" class="w-full uppercase erp-input" />
                  </div>
                  
                  <div class="col-span-6 md:col-span-2">
                      <label class="block text-[13px] font-bold text-slate-700 mb-2">Expiry</label>
                      <InputText v-model="currentItem.expiry_date" type="date" class="w-full erp-input" />
                  </div>
                  
                  <div class="col-span-4 md:col-span-1">
                      <label class="block text-[13px] font-bold text-slate-700 mb-2 text-center">Qty</label>
                      <InputText v-model="currentItem.qty" type="number" class="w-full text-center erp-input font-bold" />
                  </div>
                  
                  <div class="col-span-4 md:col-span-1">
                      <label class="block text-[13px] font-bold text-slate-700 mb-2 text-right">MRP</label>
                      <InputText v-model="currentItem.mrp" type="number" class="w-full text-right erp-input" />
                  </div>
                  
                  <div class="col-span-4 md:col-span-2">
                      <label class="block text-[13px] font-bold text-slate-700 mb-2 text-right">P. Rate</label>
                      <InputText v-model="currentItem.purchase_rate" type="number" class="w-full text-right erp-input font-bold text-slate-900" />
                  </div>
                  
                  <div class="col-span-12 md:col-span-1">
                      <Button icon="pi pi-plus" label="ADD" @click="addItem" class="w-full erp-btn bg-emerald-600 hover:bg-emerald-700 border-none font-bold" />
                  </div>
              </div>
          </div>
      </div>

      <div class="bg-white rounded-xl border border-slate-200 shadow-sm flex-1 flex flex-col overflow-hidden">
          <div class="flex-1 min-h-[350px]">
              <DataTable :value="items" stripedRows class="p-datatable-sm text-sm">
                <Column field="medicine_name" header="Item Description" class="font-medium text-slate-800"></Column>
                <Column field="batch_no" header="Batch"></Column>
                <Column field="expiry_date" header="Expiry"></Column>
                <Column field="qty" header="Qty" class="font-bold text-center"></Column>
                <Column field="mrp" header="MRP" class="text-right"></Column>
                <Column field="purchase_rate" header="P. Rate" class="text-right"></Column>
                <Column header="Total Amount" class="text-right">
                    <template #body="slotProps">
                        <span class="font-bold text-slate-800">₹ {{ (slotProps.data.qty * slotProps.data.purchase_rate).toFixed(2) }}</span>
                    </template>
                </Column>
                <Column header="Action" style="width: 100px; text-align: center;">
                    <template #body="slotProps">
                        <div class="flex gap-1 justify-center">
                            <Button icon="pi pi-pencil" text rounded severity="info" class="w-8 h-8 p-0" @click="editItem(slotProps.data, slotProps.index)" />
                            <Button icon="pi pi-trash" text rounded severity="danger" class="w-8 h-8 p-0" @click="removeItem(slotProps.index)" />
                        </div>
                    </template>
                </Column>
                <template #empty>
                    <div class="text-center py-16 text-slate-400 font-medium">
                        <i class="pi pi-box text-3xl mb-3 block text-slate-300"></i>
                        No items added to the bill yet.
                    </div>
                </template>
              </DataTable>
          </div>
          
          <div class="bg-slate-800 text-white p-6 flex justify-between items-center">
              <div class="flex items-center gap-4">
                  <span class="text-sm font-medium text-slate-300 uppercase tracking-wider">Total Value</span>
                  <span class="text-3xl font-bold text-emerald-400">₹ {{ totalAmount.toFixed(2) }}</span>
              </div>
              <Button label="Save Entry [F10]" icon="pi pi-check" :loading="isSaving" @click="savePurchaseBill" class="bg-emerald-500 hover:bg-emerald-400 text-slate-900 border-none px-8 py-3 font-bold text-base shadow-sm" />
          </div>
      </div>
  </div>
</template>

<style>
.erp-input, .erp-input .p-inputtext, .erp-input.p-dropdown { height: 42px !important; border-radius: 6px; }
.erp-btn { height: 42px !important; border-radius: 6px; }
input[type=number]::-webkit-inner-spin-button, input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
</style>