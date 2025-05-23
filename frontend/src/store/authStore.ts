// store/authStore.ts
import { defineStore } from 'pinia';
import axios from 'axios';

// Define an interface for the auth state
interface AuthState {
    loggedIn: boolean;
    userId: string | null;
    userTier: string;
    cloudTokens: number;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    loggedIn: localStorage.getItem('loggedIn') === 'true',
    userId: localStorage.getItem('userId') || '',
    userTier: "free",
    cloudTokens: 0,
  }),
  getters: {
    user(): { id: string | null; tier: string }  {
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
        //   localStorage.setItem('userId', this.userId);
          this.login();
        }
        else {
          this.logout();
        }
      } catch (error) {
        // console.error('Error checking auth status:', error);
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
