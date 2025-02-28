// store/authStore.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedIn: localStorage.getItem('loggedIn') === 'true',
    userId: localStorage.getItem('userId') || '',
    userTier: "free",
    cloudTokens: 0,
  }),
  getters: {
    user() {
      return {
        id: this.userId,
        tier: this.userTier
      };
    }
  },
  actions: {
    async checkAuth() {
      // console.log("Checking authentication");
      try {
        const response = await axios.get('/api/check-auth');
        if (response.data.loggedIn) {
          this.userTier = response.data.userTier;
          this.cloudTokens = response.data.requestCount;
          this.userId = response.data.userId;
          localStorage.setItem('userId', this.userId);
          this.login();
        }
        else {
          this.logout();
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        this.logout();
      }
      // console.log("Auth:" + this.loggedIn);
    },
    login() {
      this.loggedIn = true;
      localStorage.setItem('loggedIn', 'true');
    },
    logout() {
        this.loggedIn = false;
        this.userId = null;
        this.userTier = "free";
        this.cloudTokens = 0;
        localStorage.setItem('loggedIn', 'false');
        localStorage.removeItem('userId');
    },
    useToken() {
      this.cloudTokens = this.cloudTokens + 1;
    },
  },
});
