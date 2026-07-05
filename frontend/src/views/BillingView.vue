<template>
  <div class="p-6 bg-gray-50 min-h-screen no-print">
    <div class="flex justify-between mb-6 bg-white p-4 rounded shadow">
      <h2 class="text-xl font-bold text-gray-800">New Bill <span class="text-sm font-normal text-gray-500 ml-2">| Press F10 to Save & Print</span></h2>
      <div class="space-x-4 flex items-center">
        <InputText v-model="customerName" placeholder="Customer Name / Mobile" class="w-64" />
        <span class="font-bold text-blue-900 bg-blue-100 px-3 py-1 rounded">#{{ invoiceNumber }}</span>
      </div>
    </div>

    <div class="bg-white rounded shadow">
      <table class="w-full border-collapse">
        <thead class="bg-gray-800 text-white">
          <tr class="text-left">
            <th class="p-3 w-2/5">Item Name & Batch (F2 Search)</th>
            <th class="p-3 w-24">Qty</th>
            <th class="p-3 w-32">Rate (₹)</th>
            <th class="p-3 w-32">Total (₹)</th>
            <th class="p-3 w-24 text-center">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr class="bg-blue-50 border-b-2 border-blue-300">
            <td class="p-2">
              <InputText 
                :value="currentEntry.name ? `${currentEntry.name} (B: ${currentEntry.batch_no})` : ''"
                placeholder="Press F2 to Search Stock..." 
                class="w-full border-blue-400 bg-white font-semibold text-blue-900" 
                readonly
                @keydown.f2.prevent="openSearch"
                @click="openSearch"
              />
            </td>
            <td class="p-2">
              <input 
                id="active-qty-input"
                type="number" 
                v-model.number="currentEntry.qty" 
                class="w-full p-2 border rounded border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-600" 
                :disabled="!currentEntry.name"
                min="1"
                @keydown.enter.prevent="addToCart"
              />
            </td>
            <td class="p-2 font-medium text-gray-700">{{ currentEntry.rate > 0 ? currentEntry.rate.toFixed(2) : '0.00' }}</td>
            <td class="p-2 font-bold text-blue-800">{{ currentEntry.rate > 0 ? (currentEntry.qty * currentEntry.rate).toFixed(2) : '0.00' }}</td>
            <td class="p-2 text-center">
              <Button icon="pi pi-plus" class="p-button-rounded p-button-success p-button-text" @click="addToCart" :disabled="!currentEntry.name" />
            </td>
          </tr>

          <tr v-for="(item, index) in cart" :key="index" class="border-b hover:bg-gray-50 transition-colors">
            <td class="p-3">
              <span class="font-bold text-gray-800">{{ item.name }}</span><br>
              <span class="text-xs text-gray-500">Batch: {{ item.batch_no }} | Exp: {{ item.expiry_date }}</span>
            </td>
            <td class="p-2">
              <InputNumber v-model="item.qty" class="w-full" :min="1" :max="item.max_stock" />
            </td>
            <td class="p-3">{{ item.rate.toFixed(2) }}</td>
            <td class="p-3 font-bold">{{ (item.qty * item.rate).toFixed(2) }}</td>
            <td class="p-2 text-center">
              <Button icon="pi pi-trash" class="p-button-rounded p-button-danger p-button-text" @click="removeFromCart(index)" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-6 flex justify-end">
      <div class="bg-slate-800 text-white p-6 rounded-lg w-72 shadow-lg">
        <div class="flex justify-between mb-4 text-emerald-400 font-bold text-2xl border-t border-slate-600 pt-2">
          <span>Net Payable:</span>
          <span>₹{{ grandTotal.toFixed(2) }}</span>
        </div>
        <Button 
          label="Save & Print (F10)" 
          icon="pi pi-print" 
          class="w-full p-button-success p-button-lg" 
          @click="saveAndPrint" 
          :disabled="cart.length === 0 || isSaving" 
          :loading="isSaving"
        />
      </div>
    </div>

    <Dialog v-model:visible="showSearchModal" header="Search Active Stock" :modal="true" :style="{ width: '60vw' }">
      <div class="mb-4">
        <InputText v-model="searchQuery" placeholder="Type medicine name..." class="w-full p-inputtext-lg" id="search-input" autofocus />
      </div>
      
      <ul class="border rounded max-h-80 overflow-y-auto">
        <li v-if="isLoading" class="p-4 text-center text-gray-500">Loading Stock...</li>
        <li v-if="!isLoading && filteredStock.length === 0" class="p-4 text-center text-gray-500">No stock found</li>
        
        <li v-for="stock in filteredStock" :key="stock.stock_id" class="p-3 border-b hover:bg-blue-50 cursor-pointer flex justify-between items-center" @click="selectMedicine(stock)">
          <div>
            <p class="font-bold text-gray-900 text-lg">{{ stock.name }}</p>
            <p class="text-sm text-gray-600">Batch: <span class="font-semibold">{{ stock.batch_no }}</span> | Exp: {{ stock.expiry_date }}</p>
          </div>
          <div class="text-right">
            <p class="font-bold text-emerald-600 text-lg">₹{{ stock.mrp.toFixed(2) }}</p>
            <p class="text-xs font-bold text-blue-700 bg-blue-100 px-2 py-1 rounded inline-block mt-1">Stock: {{ stock.stock }}</p>
          </div>
        </li>
      </ul>
    </Dialog>
  </div>
  
  <div class="print-only" id="thermal-receipt">
    <div class="receipt-header text-center">
      <h2 class="font-bold text-xl">Arogya Medical Store</h2>
      <p class="text-sm">Mahavir Enclave, New Delhi</p>
      <hr class="my-2 border-dashed border-gray-400" />
      <div class="flex justify-between text-sm">
        <span>Bill: {{ invoiceNumber }}</span>
        <span>Date: {{ new Date().toLocaleDateString() }}</span>
      </div>
      <hr class="my-2 border-dashed border-gray-400" />
    </div>

    <table class="w-full text-sm receipt-table">
      <thead>
        <tr class="border-b border-gray-400 text-left">
          <th>Item</th>
          <th>Qty</th>
          <th>Amt</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in cart" :key="index">
          <td>{{ item.name }}<br><span style="font-size: 10px;">{{ item.batch_no }}</span></td>
          <td>{{ item.qty }}</td>
          <td>{{ (item.qty * item.rate).toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
    <hr class="my-2 border-dashed border-gray-400" />
    <div class="flex justify-between font-bold text-lg">
      <span>Total:</span>
      <span>₹{{ grandTotal.toFixed(2) }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue';
import axios from 'axios';

const cart = ref([]);
const customerName = ref('');
const invoiceNumber = ref('INV-' + Math.floor(Date.now() / 1000));
const currentEntry = ref({ medicine_id: null, name: '', batch_no: '', expiry_date: '', rate: 0, qty: 1, max_stock: 0 });

const showSearchModal = ref(false);
const searchQuery = ref('');
const allActiveStock = ref([]);
const isLoading = ref(false);
const isSaving = ref(false);

const grandTotal = computed(() => cart.value.reduce((acc, item) => acc + (item.qty * item.rate), 0));

const fetchActiveStock = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get('http://localhost:8000/api/transactions/stock/available/');
    allActiveStock.value = response.data;
  } catch (error) {
    console.error("Error fetching stock:", error);
  } finally {
    isLoading.value = false;
  }
};

const filteredStock = computed(() => {
  if (!searchQuery.value) return allActiveStock.value;
  const query = searchQuery.value.toLowerCase();
  return allActiveStock.value.filter(s => s.name.toLowerCase().includes(query) || s.batch_no.toLowerCase().includes(query));
});

const openSearch = () => {
  showSearchModal.value = true;
  searchQuery.value = '';
  if (allActiveStock.value.length === 0) fetchActiveStock();
  setTimeout(() => {
    const searchInput = document.getElementById('search-input');
    if(searchInput) searchInput.focus();
  }, 100);
};

const selectMedicine = (stock) => {
  currentEntry.value = { 
    medicine_id: stock.medicine_id, 
    name: stock.name, 
    batch_no: stock.batch_no,
    expiry_date: stock.expiry_date,
    rate: stock.mrp, 
    qty: 1,
    max_stock: stock.stock
  };
  showSearchModal.value = false;
  
  nextTick(() => {
    const qtyInput = document.getElementById('active-qty-input');
    if (qtyInput) {
      qtyInput.focus();
      qtyInput.select();
    }
  });
};

const addToCart = () => {
  if (!currentEntry.value.name) return;
  // Check if same medicine AND same batch exists
  const existingItem = cart.value.find(item => item.medicine_id === currentEntry.value.medicine_id && item.batch_no === currentEntry.value.batch_no);
  
  if (existingItem) {
    if(existingItem.qty + currentEntry.value.qty > existingItem.max_stock) {
      alert("Cannot add more than available stock!");
      return;
    }
    existingItem.qty += currentEntry.value.qty;
  } else {
    if(currentEntry.value.qty > currentEntry.value.max_stock) {
      alert("Cannot add more than available stock!");
      return;
    }
    cart.value.push({ ...currentEntry.value });
  }
  currentEntry.value = { medicine_id: null, name: '', batch_no: '', expiry_date: '', rate: 0, qty: 1, max_stock: 0 };
};

const removeFromCart = (index) => {
  cart.value.splice(index, 1);
};

const saveAndPrint = async () => {
  isSaving.value = true;
  try {
    const payload = {
      invoice_number: invoiceNumber.value,
      customer_name: customerName.value,
      total_amount: grandTotal.value,
      net_payable: grandTotal.value,
      items: cart.value.map(item => ({
        medicine_id: item.medicine_id,
        batch_no: item.batch_no,
        quantity: item.qty,
        rate: item.rate,
        amount: item.qty * item.rate
      }))
    };

    await axios.post('http://localhost:8000/api/transactions/invoice/create/', payload);
    window.print();
    
    // Reset Everything
    cart.value = [];
    customerName.value = '';
    invoiceNumber.value = 'INV-' + Math.floor(Date.now() / 1000);
    fetchActiveStock(); // Refresh stock silently
    
  } catch (error) {
    alert('Failed to save bill. Error: ' + JSON.stringify(error.response?.data || error.message));
  } finally {
    isSaving.value = false;
  }
};

const handleKeydown = (event) => {
  if (event.key === 'F2') { event.preventDefault(); openSearch(); }
  if (event.key === 'F10') { event.preventDefault(); if(cart.value.length > 0 && !isSaving.value) saveAndPrint(); }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
  fetchActiveStock();
});
onUnmounted(() => window.removeEventListener('keydown', handleKeydown));
</script>

<style>
@media screen { .print-only { display: none !important; } }
@media print {
  .no-print { display: none !important; }
  .print-only {
    display: block !important; width: 80mm; margin: 0; padding: 10px;
    font-family: 'Courier New', Courier, monospace; color: #000;
  }
  .receipt-table th, .receipt-table td { padding: 4px 2px; }
  @page { margin: 0; }
}
</style>