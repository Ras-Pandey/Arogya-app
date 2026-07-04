<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="p-8 bg-white rounded-lg shadow-lg w-96">
      <h2 class="text-2xl font-bold text-center mb-6">{{ isLogin ? 'Login' : 'Signup' }}</h2>
      
      <div class="space-y-4">
        <InputText v-model="form.username" placeholder="Username" class="w-full" />
        <Password v-model="form.password" placeholder="Password" class="w-full" toggleMask :feedback="false" />
        
        <div v-if="!isLogin" class="space-y-4">
          <Select 
            v-model="form.question" 
            :options="['Pet Name', 'Mother Name', 'School Name']" 
            placeholder="Select Security Question" 
            class="w-full" 
          />
          <InputText v-model="form.answer" placeholder="Security Answer" class="w-full" />
        </div>

        <Button :label="isLogin ? 'Login' : 'Signup'" class="w-full" @click="handleSubmit" />
        
        <div class="text-center text-sm mt-4">
          <a @click.prevent="toggleMode" class="text-blue-600 cursor-pointer hover:underline">
            {{ isLogin ? 'Create an account' : 'Back to Login' }}
          </a>
          <br>
          <a @click.prevent="showForgot = true" class="text-gray-500 cursor-pointer hover:underline mt-2 inline-block">Forgot Password?</a>
        </div>
      </div>
    </div>

    <Dialog v-model:visible="showForgot" header="Reset Password" modal class="w-80">
      <div class="space-y-4">
        <InputText v-model="forgot.username" placeholder="Username" class="w-full" />
        <Button label="Get Security Question" @click="fetchQuestion" class="w-full" />
        
        <div v-if="forgot.question" class="space-y-4 border-t pt-4">
          <p class="text-sm font-semibold">Q: {{ forgot.question }}</p>
          <InputText v-model="forgot.answer" placeholder="Your Answer" class="w-full" />
          <Password v-model="forgot.new_password" placeholder="New Password" class="w-full" toggleMask />
          <Button label="Confirm Reset" class="w-full p-button-success" @click="resetPassword" />
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const isLogin = ref(true);
const showForgot = ref(false);
const form = ref({ username: '', password: '', question: '', answer: '' });
const forgot = ref({ username: '', question: '', answer: '', new_password: '' });

const router = useRouter();
const authStore = useAuthStore();

const toggleMode = () => {
  isLogin.value = !isLogin.value;
  form.value = { username: '', password: '', question: '', answer: '' };
};

const handleSubmit = async () => {
  try {
    const url = isLogin.value 
      ? 'http://localhost:8000/api/auth/login/' 
      : 'http://localhost:8000/api/auth/signup/';
    
    // Payload logic fix: Login ke liye sirf user/pass, Signup ke liye pura form
    const payload = isLogin.value 
      ? { username: form.value.username, password: form.value.password } 
      : form.value;

    await axios.post(url, payload);
    
    if (isLogin.value) {
      authStore.setLogin(form.value.username);
      router.push('/company');
    } else {
      alert('Signup Successful! Please login.');
      isLogin.value = true;
    }
  } catch (e) { 
    console.error(e.response?.data);
    alert('Operation Failed: ' + (e.response?.data?.error || 'Check your credentials'));
  }
};

const fetchQuestion = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/auth/get-question/', { username: forgot.value.username });
    forgot.value.question = res.data.question;
  } catch { alert('User not found!'); }
};

const resetPassword = async () => {
  try {
    await axios.post('http://localhost:8000/api/auth/reset-password/', forgot.value);
    alert('Password successfully reset!');
    showForgot.value = false;
  } catch { alert('Invalid answer or request failed!'); }
};
</script>