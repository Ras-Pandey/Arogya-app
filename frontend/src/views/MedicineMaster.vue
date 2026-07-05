<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'

const medicines = ref([])
const companies = ref([])
const salts = ref([])
const loading = ref(true)
const showDialog = ref(false)
const isSaving = ref(false)
const isEditMode = ref(false)
const selectedMedicine = ref(null)
const form = ref({ id: null, name: '', company: null, salt: null, packing: '', hsn_code: '', tax_percentage: 12.00 })
const errors = ref({})

const fetchData = async () => {
  loading.value = true
  try {
    const [medRes, compRes, saltRes] = await Promise.all([
      axios.get('/medicines/'),
      axios.get('/companies/'),
      axios.get('/salts/')
    ])
    
    // Bulletproof array handling for all 3 lists
    medicines.value = Array.isArray(medRes.data) ? medRes.data : Object.values(medRes.data || {})
    companies.value = Array.isArray(compRes.data) ? compRes.data : Object.values(compRes.data || {})
    salts.value = Array.isArray(saltRes.data) ? saltRes.data : Object.values(saltRes.data || {})
    
  } catch (error) { 
    console.error(error) 
  } finally { 
    loading.value = false 
  }
}

const saveMedicine = async () => {
  errors.value = {}
  if (!form.value.name?.trim()) errors.value.name = "Medicine name required"
  if (!form.value.company) errors.value.company = "Company is required"
  if (Object.keys(errors.value).length > 0) return

  isSaving.value = true
  try {
    if (isEditMode.value) await axios.put(`/medicines/${form.value.id}/`, form.value)
    else await axios.post('/medicines/', form.value)
    
    showDialog.value = false
    await fetchData() // Wait for list update
    form.value = { id: null, name: '', company: null, salt: null, packing: '', hsn_code: '', tax_percentage: 12.00 }
  } catch (error) {
    console.error("Save Error:", error.response?.data || error.message);
    alert("Error saving medicine!");
  } finally { 
    isSaving.value = false 
  }
}

const handleKeyDown = (event) => {
  if (event.key === 'F2') { 
      event.preventDefault(); showDialog.value = true; isEditMode.value = false; 
      form.value = { id: null, name: '', company: null, salt: null, packing: '', hsn_code: '', tax_percentage: 12.00 }; errors.value = {} 
  }
  if (event.key === 'F3' && selectedMedicine.value) { 
      event.preventDefault(); showDialog.value = true; isEditMode.value = true; 
      form.value = {...selectedMedicine.value}; errors.value = {} 
  }
  if (event.key === 'F10' && showDialog.value) {
      event.preventDefault(); saveMedicine()
  }
}
onMounted(() => { fetchData(); window.addEventListener('keydown', handleKeyDown) })
onUnmounted(() => window.removeEventListener('keydown', handleKeyDown))
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col w-full max-w-6xl mx-auto">
      <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50 rounded-t-xl">
          <div>
            <h2 class="text-xl font-bold text-gray-800">Medicine Master</h2>
            <p class="text-xs text-gray-500 mt-1">Manage items, packing, HSN, and GST rates</p>
          </div>
          <div class="flex gap-2">
              <Button label="Edit (F3)" icon="pi pi-pencil" size="small" class="bg-blue-600 border-none hover:bg-blue-700 shadow-sm px-4" :disabled="!selectedMedicine" @click="handleKeyDown({key: 'F3', preventDefault: ()=>{}})" />
              <Button label="Add New (F2)" icon="pi pi-plus" size="small" class="bg-emerald-600 border-none hover:bg-emerald-700 shadow-sm px-4" @click="handleKeyDown({key: 'F2', preventDefault: ()=>{}})" />
          </div>
      </div>
      
      <div class="p-4">
          <DataTable v-if="medicines" :value="medicines" :loading="loading" v-model:selection="selectedMedicine" selectionMode="single" dataKey="id" stripedRows hoverableRows class="p-datatable-sm text-sm cursor-pointer">
            <Column field="name" header="Item Name"></Column>
            <Column field="packing" header="Packing"></Column>
            <Column field="company_name" header="Company"></Column>
            <Column field="tax_percentage" header="GST %">
               <template #body="slotProps">
                    <span class="font-bold text-emerald-600">{{ slotProps.data.tax_percentage }}%</span>
                </template>
            </Column>
            <template #empty><div class="text-center p-4">No medicines found. Press F2 to add.</div></template>
          </DataTable>
      </div>

      <Dialog v-model:visible="showDialog" modal :header="isEditMode ? 'Edit Medicine' : 'Add New Medicine'" :style="{ width: '40rem' }" class="p-fluid">
          <div class="grid grid-cols-2 gap-4 mt-2">
              <div class="flex flex-col gap-1 col-span-2">
                  <label class="text-sm font-semibold text-gray-700">Medicine Name <span class="text-red-500">*</span></label>
                  <InputText v-model="form.name" autofocus class="p-inputtext-sm" :class="{'border-red-500': errors.name}" @input="errors.name = null" />
                  <small v-if="errors.name" class="text-red-500 text-xs">{{ errors.name }}</small>
              </div>
              
              <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold text-gray-700">Company <span class="text-red-500">*</span></label>
                  <Dropdown v-model="form.company" :options="companies" optionLabel="name" optionValue="id" placeholder="Select Company" class="p-dropdown-sm" :class="{'border-red-500': errors.company}" @change="errors.company = null" filter />
                  <small v-if="errors.company" class="text-red-500 text-xs">{{ errors.company }}</small>
              </div>
              
              <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold text-gray-700">Salt / Formula</label>
                  <Dropdown v-model="form.salt" :options="salts" optionLabel="name" optionValue="id" placeholder="Select Salt" class="p-dropdown-sm" filter />
              </div>

              <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold text-gray-700">Packing</label>
                  <InputText v-model="form.packing" class="p-inputtext-sm" />
              </div>

              <div class="grid grid-cols-2 gap-2">
                  <div class="flex flex-col gap-1">
                      <label class="text-sm font-semibold text-gray-700">HSN Code</label>
                      <InputText v-model="form.hsn_code" class="p-inputtext-sm" />
                  </div>
                  <div class="flex flex-col gap-1">
                      <label class="text-sm font-semibold text-gray-700">GST %</label>
                      <InputText v-model="form.tax_percentage" type="number" class="p-inputtext-sm" />
                  </div>
              </div>
          </div>

          <template #footer>
              <Button :label="isEditMode ? 'Update Item (F10)' : 'Save Item (F10)'" icon="pi pi-check" :loading="isSaving" @click="saveMedicine" size="small" class="bg-emerald-600 border-none" />
          </template>
      </Dialog>
  </div>
</template>

<style>
.p-datatable .p-datatable-tbody > tr.p-highlight { background-color: #d1fae5 !important; color: #065f46 !important; }
</style>