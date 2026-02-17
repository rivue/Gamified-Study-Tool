// store/authStore.ts
import { defineStore } from 'pinia';
import axios from 'axios';
import { useUserStatsStore } from '@/store/userStatsStore';

const DISABLE_AUTH = process.env.VUE_APP_DISABLE_AUTH === 'true' || process.env.NODE_ENV !== 'production';

// Define an interface for the auth state

export interface UserData {
    id: string | null;
    username: string | null;
    firstName: string | null;
    lastName: string | null;
    email?: string | null;
    first_name?: string | null;
    last_name?: string | null;
    current_streak?: number;
    highest_streak?: number;
    // tier: string;
}
interface AuthState {
    loggedIn: boolean;
    isAuthChecked: boolean;
    user: UserData;
    cloudTokens: number;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    loggedIn: DISABLE_AUTH || localStorage.getItem('loggedIn') === 'true',
    isAuthChecked: DISABLE_AUTH,
    user: {
        id: localStorage.getItem('userId') || (DISABLE_AUTH ? 'guest' : null),
        username: localStorage.getItem('username') || (DISABLE_AUTH ? 'guest' : null),
        firstName: localStorage.getItem('firstName') || (DISABLE_AUTH ? 'Guest' : null),
        lastName: localStorage.getItem('lastName') || (DISABLE_AUTH ? 'User' : null),
        // tier: localStorage.getItem('userTier') || "free",
    },
    cloudTokens: 0, // This seems session-specific, not persisted typically
  }),
  getters: {
    // The user getter now returns the whole user object
    getUser(state): UserData {
      return state.user;
    },
    // Specific getters if needed, e.g., for direct access or computed properties
    userId(state): string | null {
        return state.user.id;
    },
    username(state): string | null {
        return state.user.username;
    },
    // userTier(state): string {
    //     return state.user.tier;
    // }
  },
  actions: {
    normalizeUserPayload(payload?: Partial<UserData>) {
      if (!payload) return null;

      const normalizedId = payload.id !== undefined && payload.id !== null ? String(payload.id) : null;
      return {
        id: normalizedId,
        username: payload.username ?? payload.email ?? null,
        firstName: payload.firstName ?? payload.first_name ?? null,
        lastName: payload.lastName ?? payload.last_name ?? null,
        current_streak: payload.current_streak,
        highest_streak: payload.highest_streak,
      };
    },
    resetAuthState() {
      this.loggedIn = false;
      this.user = {
        id: null,
        username: null,
        firstName: null,
        lastName: null,
      };
      this.cloudTokens = 0;
      localStorage.setItem('loggedIn', 'false');
      localStorage.removeItem('userId');
      localStorage.removeItem('username');
      localStorage.removeItem('firstName');
      localStorage.removeItem('lastName');
    },
    async checkAuth() {
      if (DISABLE_AUTH) {
        this.login({
          id: this.user.id || 'guest',
          username: this.user.username || 'guest',
          firstName: this.user.firstName || 'Guest',
          lastName: this.user.lastName || 'User',
        });
        this.isAuthChecked = true;
        return;
      }
      try {
        const response = await axios.get('/api/check-auth');
        if (response.data.loggedIn) {
          // Note: /api/check-auth doesn't return username, firstName, lastName.
          // These will be populated by login action if provided, or later by profile page.
        //   this.user.tier = response.data.userTier;
          this.cloudTokens = response.data.requestCount; // Assuming requestCount maps to cloudTokens
          this.user.id = String(response.data.userId);
          
        //   localStorage.setItem('userTier', this.user.tier);
          localStorage.setItem('userId', this.user.id as string); // Ensure userId is not null before setting
          
          this.loggedIn = true;
          localStorage.setItem('loggedIn', 'true');
        } else {
          this.resetAuthState();
        }
      } catch (error) {
        this.resetAuthState();
      } finally {
        this.isAuthChecked = true;
      }
    },
    // Login action updated to accept optional payload
    login(payload?: Partial<UserData>) {
      this.loggedIn = true;
      this.isAuthChecked = true;
      localStorage.setItem('loggedIn', 'true');

      const normalizedPayload = this.normalizeUserPayload(payload);
      if (normalizedPayload) {
        if (normalizedPayload.id) {
            this.user.id = normalizedPayload.id;
            localStorage.setItem('userId', normalizedPayload.id);
        }
        if (normalizedPayload.username) {
            this.user.username = normalizedPayload.username;
            localStorage.setItem('username', normalizedPayload.username);
        }
        if (normalizedPayload.firstName) {
            this.user.firstName = normalizedPayload.firstName;
            localStorage.setItem('firstName', normalizedPayload.firstName);
        }
        if (normalizedPayload.lastName) {
            this.user.lastName = normalizedPayload.lastName;
            localStorage.setItem('lastName', normalizedPayload.lastName);
        }
        // if (payload.tier) {
        //     this.user.tier = payload.tier;
        //     localStorage.setItem('userTier', payload.tier);
        // }
        if (normalizedPayload.current_streak !== undefined && normalizedPayload.highest_streak !== undefined) {
            const userStats = useUserStatsStore();
            userStats.setStreakData(normalizedPayload.current_streak, normalizedPayload.highest_streak);
        }
      }
    },
    logout() {
        if (DISABLE_AUTH) {
            this.login({
                id: 'guest',
                username: 'guest',
                firstName: 'Guest',
                lastName: 'User',
            });
            return;
        }
        this.resetAuthState();
        this.isAuthChecked = true;
    },
    async logoutFromServer() {
      if (DISABLE_AUTH) {
        this.logout();
        return;
      }

      try {
        await axios.post('/api/logout');
      } finally {
        this.logout();
      }
    },
    // Action to specifically update user details, e.g., from profile page
    updateUserDetails(details: Partial<UserData>) {
        if (details.username !== undefined) {
            this.user.username = details.username;
            if (details.username === null) localStorage.removeItem('username');
            else localStorage.setItem('username', details.username);
        }
        if (details.firstName !== undefined) {
            this.user.firstName = details.firstName;
            if (details.firstName === null) localStorage.removeItem('firstName');
            else localStorage.setItem('firstName', details.firstName);
        }
        if (details.lastName !== undefined) {
            this.user.lastName = details.lastName;
            if (details.lastName === null) localStorage.removeItem('lastName');
            else localStorage.setItem('lastName', details.lastName);
        }
        // Add other fields like tier if they can be updated this way
    },
    useToken() {
      this.cloudTokens = (this.cloudTokens || 0) + 1; // Ensure cloudTokens is a number
    },
  },
});
