<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

const salts = ref([])
const loading = ref(true)
const showDialog = ref(false)
const isSaving = ref(false)
const isEditMode = ref(false)
const selectedSalt = ref(null) // Table row selection track karega

const form = ref({ id: null, name: '', description: '' })
const errors = ref({})

const fetchData = async () => {
  loading.value = true
  try {
    const response = await axios.get('/salts/')
    salts.value = response.data
  } catch (error) { console.error(error) } finally { loading.value = false }
}

const validateForm = () => {
    errors.value = {}
    if (!form.value.name.trim()) errors.value.name = "Salt Name is required."
    return Object.keys(errors.value).length === 0
}

const saveSalt = async () => {
  if (!validateForm()) return 
  isSaving.value = true
  try {
    if (isEditMode.value) {
      await axios.put(`/salts/${form.value.id}/`, form.value)
    } else {
      await axios.post('/salts/', form.value)
    }
    showDialog.value = false
    form.value = { id: null, name: '', description: '' }
    errors.value = {}
    selectedSalt.value = null
    fetchData() 
  } catch (error) { console.error(error) } finally { isSaving.value = false }
}

const deleteSalt = async () => {
    if (!selectedSalt.value) return
    const confirmDelete = confirm(`Kya aap sach me '${selectedSalt.value.name}' ko delete karna chahte hain?`)
    if (!confirmDelete) return
    try {
        await axios.delete(`/salts/${selectedSalt.value.id}/`)
        selectedSalt.value = null
        fetchData()
    } catch (error) {
        alert("Delete failed! Ye salt kisi medicine me use ho rha hai.")
    }
}

const handleKeyDown = (event) => {
  if (event.key === 'F2') { 
      event.preventDefault()
      isEditMode.value = false
      form.value = { id: null, name: '', description: '' }
      errors.value = {}
      showDialog.value = true 
  }
  if (event.key === 'F3') {
      event.preventDefault()
      if (!selectedSalt.value) return alert("Pehle table me se koi Salt select karein!")
      isEditMode.value = true
      form.value = { ...selectedSalt.value }
      errors.value = {}
      showDialog.value = true
  }
  if (event.key === 'Delete' && !showDialog.value && selectedSalt.value) {
      deleteSalt()
  }
  if (event.key === 'Escape' && showDialog.value) showDialog.value = false
  if (event.key === 'F10' && showDialog.value) { event.preventDefault(); saveSalt() }
}

onMounted(() => { fetchData(); window.addEventListener('keydown', handleKeyDown) })
onUnmounted(() => { window.removeEventListener('keydown', handleKeyDown) })
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col w-full max-w-5xl mx-auto">
      <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50 rounded-t-xl">
          <div>
            <h2 class="text-xl font-bold text-gray-800">Salt / Formula Master</h2>
            <p class="text-xs text-gray-500 mt-1">Manage chemical compositions</p>
          </div>
          <div class="flex gap-2">
              <Button label="Edit (F3)" icon="pi pi-pencil" size="small" class="bg-blue-600 border-none hover:bg-blue-700 shadow-sm px-4" :disabled="!selectedSalt" @click="handleKeyDown({key: 'F3', preventDefault: ()=>{}})" />
              <Button label="Add New (F2)" icon="pi pi-plus" size="small" class="bg-emerald-600 border-none hover:bg-emerald-700 shadow-sm px-4" @click="handleKeyDown({key: 'F2', preventDefault: ()=>{}})" />
          </div>
      </div>
      
      <div class="p-4">
          <DataTable :value="salts" :loading="loading" v-model:selection="selectedSalt" selectionMode="single" dataKey="id" stripedRows hoverableRows class="p-datatable-sm text-sm cursor-pointer">
            <Column field="name" header="Salt Name" style="width: 40%"></Column>
            <Column field="description" header="Description" style="width: 60%"></Column>
          </DataTable>
      </div>

      <Dialog v-model:visible="showDialog" modal :header="isEditMode ? 'Edit Salt' : 'Add New Salt'" :style="{ width: '28rem' }" class="p-fluid">
          <div class="flex flex-col space-y-5 mt-2">
              <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Salt Name <span class="text-red-500">*</span></label>
                  <InputText v-model="form.name" autofocus class="p-inputtext-sm" :class="{'border-red-500': errors.name}" @input="errors.name = null" />
                  <small v-if="errors.name" class="text-red-500 text-xs font-semibold">{{ errors.name }}</small>
              </div>
              <div class="flex flex-col gap-1">
                  <label class="text-sm font-semibold">Description</label>
                  <InputText v-model="form.description" class="p-inputtext-sm" />
              </div>
          </div>
          <template #footer>
              <Button :label="isEditMode ? 'Update Salt (F10)' : 'Save Salt (F10)'" icon="pi pi-check" :loading="isSaving" @click="saveSalt" size="small" class="bg-emerald-600 border-none" />
          </template>
      </Dialog>
  </div>
</template>

<style>
.p-datatable .p-datatable-tbody > tr.p-highlight { background-color: #d1fae5 !important; color: #065f46 !important; }
</style>