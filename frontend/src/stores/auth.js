// src/stores/auth.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: !!localStorage.getItem('user'), // Refresh hone par bhi status yaad rahega
    user: localStorage.getItem('user') || null,
  }),
  actions: {
    setLogin(username) {
      this.isAuthenticated = true;
      this.user = username;
      localStorage.setItem('user', username); // Desktop mode ke liye local storage best hai
    },
    setLogout() {
      this.isAuthenticated = false;
      this.user = null;
      localStorage.removeItem('user');
    }
  }
});