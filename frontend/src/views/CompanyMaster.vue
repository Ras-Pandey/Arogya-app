<!-- <script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

const companies = ref([])
const loading = ref(true)

// Modals aur State
const showDialog = ref(false)
const isSaving = ref(false)
const isEditMode = ref(false)
const selectedCompany = ref(null) // Naya: Table me select ki hui row

const companyForm = ref({ id: null, name: '', short_name: '' })
const errors = ref({})

// const fetchData = async () => {
//   loading.value = true
//   try {
//     const response = await axios.get('http://127.0.0.1:8000/api/companies/')
//     companies.value = response.data
//   } catch (error) {
//     console.error("API Error:", error)
//   } finally {
//     loading.value = false
//   }
// }

// Validation Logic
const validateForm = () => {
    errors.value = {}
    if (!companyForm.value.name.trim()) errors.value.name = "Company name is required."
    return Object.keys(errors.value).length === 0
}

// Save (Add & Update dono handle karega)
const saveCompany = async () => {
  if (!validateForm()) return
  isSaving.value = true
  try {
    if (isEditMode.value) {
    await axios.put(`/companies/${companyForm.value.id}/`, companyForm.value)
} else {
    await axios.post('/companies/', companyForm.value)
}
    
    showDialog.value = false
    companyForm.value = { id: null, name: '', short_name: '' }
    errors.value = {}
    fetchData()
  } catch (error) {
    console.error("Save Error:", error)
  } finally {
    isSaving.value = false
  }
}

// Delete Logic
const deleteCompany = async () => {
    if (!selectedCompany.value) return
    
    // Asli app me yahan ek sweetalert ya confirmation popup hona chahiye
    const confirmDelete = confirm(`Kya aap sach me '${selectedCompany.value.name}' ko delete karna chahte hain?`)
    if (!confirmDelete) return

    try {
        await axios.delete(`/companies/${selectedCompany.value.id}/`)
        selectedCompany.value = null // Selection clear karein
        fetchData()
    } catch (error) {
        console.error("Delete Error:", error)
        alert("Delete fail ho gaya. Shayad is company ki dawaiyan database me majood hain.")
    }
}

// Keyboard Shortcuts Engine (F2, F3, Del, F10)
const handleKeyDown = (event) => {
  // Add (F2)
  if (event.key === 'F2') { 
      event.preventDefault()
      isEditMode.value = false
      companyForm.value = { id: null, name: '', short_name: '' } // Form clear
      errors.value = {}
      showDialog.value = true 
  }
  
  // Edit (F3)
  if (event.key === 'F3') {
      event.preventDefault()
      if (!selectedCompany.value) {
          alert("Pehle table me se koi company select karein!")
          return
      }
      isEditMode.value = true
      // Selected row ka data form me daalein
      companyForm.value = { ...selectedCompany.value }
      errors.value = {}
      showDialog.value = true
  }

  // Delete (Delete)
  if (event.key === 'Delete') {
      if (!showDialog.value && selectedCompany.value) {
          deleteCompany()
      }
  }

  // Close (Esc)
  if (event.key === 'Escape' && showDialog.value) showDialog.value = false
  
  // Save (F10)
  if (event.key === 'F10' && showDialog.value) { 
      event.preventDefault()
      saveCompany() 
  }
}

onMounted(() => { fetchData(); window.addEventListener('keydown', handleKeyDown) })
onUnmounted(() => { window.removeEventListener('keydown', handleKeyDown) })
</script> -->


<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const companies = ref([])
const loading = ref(true)
const showDialog = ref(false)
const isSaving = ref(false)
const isEditMode = ref(false)
const selectedCompany = ref(null)
const companyForm = ref({ id: null, name: '', short_name: '' })
const errors = ref({})

const fetchData = async () => {
  loading.value = true
  try {
    const response = await axios.get('/companies/')
    companies.value = response.data
  } catch (error) { console.error(error) } finally { loading.value = false }
}

const saveCompany = async () => {
  if (!companyForm.value.name.trim()) return (errors.value.name = "Required")
  isSaving.value = true
  try {
    if (isEditMode.value) await axios.put(`/companies/${companyForm.value.id}/`, companyForm.value)
    else await axios.post('/companies/', companyForm.value)
    showDialog.value = false
    fetchData()
  } finally { isSaving.value = false }
}

const handleKeyDown = (event) => {
  if (event.key === 'F2') { showDialog.value = true; isEditMode.value = false; companyForm.value = {} }
  if (event.key === 'F3' && selectedCompany.value) { showDialog.value = true; isEditMode.value = true; companyForm.value = {...selectedCompany.value} }
  if (event.key === 'F10' && showDialog.value) saveCompany()
}
onMounted(() => { fetchData(); window.addEventListener('keydown', handleKeyDown) })
onUnmounted(() => window.removeEventListener('keydown', handleKeyDown))
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col w-full max-w-5xl mx-auto">
      <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50 rounded-t-xl">
          <div>
            <h2 class="text-xl font-bold text-gray-800">Company Master</h2>
          </div>
          <div class="flex gap-2">
              <Button label="Edit (F3)" icon="pi pi-pencil" size="small" class="bg-blue-600 border-none hover:bg-blue-700 shadow-sm px-4" @click="handleKeyDown({key: 'F3', preventDefault: ()=>{}})" :disabled="!selectedCompany" />
              <Button label="Add New (F2)" icon="pi pi-plus" size="small" class="bg-emerald-600 border-none hover:bg-emerald-700 shadow-sm px-4" @click="handleKeyDown({key: 'F2', preventDefault: ()=>{}})" />
          </div>
      </div>
      
      <div class="p-4">
          <DataTable 
            :value="companies" 
            :loading="loading" 
            v-model:selection="selectedCompany" 
            selectionMode="single" 
            dataKey="id"
            stripedRows 
            hoverableRows 
            class="p-datatable-sm text-sm cursor-pointer">
            <Column field="name" header="Company Name" style="width: 70%"></Column>
            <Column field="short_name" header="Code" style="width: 30%"></Column>
          </DataTable>
      </div>

      <Dialog v-model:visible="showDialog" modal :header="isEditMode ? 'Edit Company' : 'Add New Company'" :style="{ width: '28rem' }" class="p-fluid">
          <div class="flex flex-col space-y-5 mt-2">
              <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold text-gray-700">Company Name <span class="text-red-500">*</span></label>
                  <InputText v-model="companyForm.name" autofocus class="p-inputtext-sm rounded-md shadow-sm" :class="{'border-red-500': errors.name}" @input="errors.name = null" />
                  <small v-if="errors.name" class="text-red-500 text-xs font-semibold">{{ errors.name }}</small>
              </div>
              <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold text-gray-700">Short Name</label>
                  <InputText v-model="companyForm.short_name" class="p-inputtext-sm rounded-md shadow-sm uppercase" />
              </div>
          </div>
          <template #footer>
              <Button :label="isEditMode ? 'Update Company (F10)' : 'Save Company (F10)'" icon="pi pi-check" :loading="isSaving" @click="saveCompany" size="small" class="bg-emerald-600 border-none hover:bg-emerald-700 font-semibold shadow-sm px-4" />
          </template>
      </Dialog>
  </div>
</template>

<style>
/* Selected row ko highlight karne ke liye thoda CSS */
.p-datatable .p-datatable-tbody > tr.p-highlight {
    background-color: #d1fae5 !important; /* Tailwind emerald-100 */
    color: #065f46 !important;
}
</style>