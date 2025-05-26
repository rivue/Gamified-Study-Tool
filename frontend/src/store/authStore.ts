// store/authStore.ts
import { defineStore } from 'pinia';
import axios from 'axios';

// Define an interface for the auth state

export interface UserData {
    id: string | null;
    username: string | null;
    firstName: string | null;
    lastName: string | null;
    // tier: string;
}
interface AuthState {
    loggedIn: boolean;
    user: UserData;
    cloudTokens: number;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    loggedIn: localStorage.getItem('loggedIn') === 'true',
    user: {
        id: localStorage.getItem('userId') || null,
        username: localStorage.getItem('username') || null,
        firstName: localStorage.getItem('firstName') || null,
        lastName: localStorage.getItem('lastName') || null,
        // tier: localStorage.getItem('userTier') || "free",
    },
    cloudTokens: 0, // This seems session-specific, not persisted typically
  }),
  getters: {
    // The user getter now returns the whole user object
    user(state): UserData {
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
    async checkAuth() {
      try {
        const response = await axios.get('/api/check-auth');
        if (response.data.loggedIn) {
          // Note: /api/check-auth doesn't return username, firstName, lastName.
          // These will be populated by login action if provided, or later by profile page.
        //   this.user.tier = response.data.userTier;
          this.cloudTokens = response.data.requestCount; // Assuming requestCount maps to cloudTokens
          this.user.id = response.data.userId;
          
          localStorage.setItem('userTier', this.user.tier);
          localStorage.setItem('userId', this.user.id as string); // Ensure userId is not null before setting
          
          this.loggedIn = true;
          localStorage.setItem('loggedIn', 'true');
        } else {
          this.logout(); // Clears all user data including new fields
        }
      } catch (error) {
        this.logout();
      }
    },
    // Login action updated to accept optional payload
    login(payload?: Partial<UserData>) {
      this.loggedIn = true;
      localStorage.setItem('loggedIn', 'true');

      if (payload) {
        if (payload.id) {
            this.user.id = payload.id;
            localStorage.setItem('userId', payload.id);
        }
        if (payload.username) {
            this.user.username = payload.username;
            localStorage.setItem('username', payload.username);
        }
        if (payload.firstName) {
            this.user.firstName = payload.firstName;
            localStorage.setItem('firstName', payload.firstName);
        }
        if (payload.lastName) {
            this.user.lastName = payload.lastName;
            localStorage.setItem('lastName', payload.lastName);
        }
        // if (payload.tier) {
        //     this.user.tier = payload.tier;
        //     localStorage.setItem('userTier', payload.tier);
        // }
      }
    },
    logout() {
        this.loggedIn = false;
        this.user = {
            id: null,
            username: null,
            firstName: null,
            lastName: null,
            // tier: "free",
        };
        this.cloudTokens = 0;
        localStorage.setItem('loggedIn', 'false');
        localStorage.removeItem('userId');
        localStorage.removeItem('username');
        localStorage.removeItem('firstName');
        localStorage.removeItem('lastName');
        // localStorage.removeItem('userTier');
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
    // state: (): AuthState => ({
    //     loggedIn: localStorage.getItem('loggedIn') === 'true',
    //     user: {
    //         id: localStorage.getItem('userId') || null,
    //         username: localStorage.getItem('username') || null,
    //         firstName: localStorage.getItem('firstName') || null,
    //         lastName: localStorage.getItem('lastName') || null,
    //         // tier: localStorage.getItem('userTier') || "free",
    //     },
    //     cloudTokens: 0, // This seems session-specific, not persisted typically
    // }),
    // getters: {
    //     // The user getter now returns the whole user object
    //     getUser(state): UserData {
    //         return state.user;
    //     },
    //     // Specific getters if needed, e.g., for direct access or computed properties
    //     userId(state): string | null {
    //         return state.user.id;
    //     },
    //     username(state): string | null {
    //         return state.user.username;
    //     },
    //     // userTier(state): string {
    //     //     return state.user.tier;
    //     // }
    // },
    // actions: {
    //     async checkAuth() {
    //         try {
    //             const response = await axios.get('/api/check-auth');
    //             if (response.data.loggedIn) {
    //                 // Note: /api/check-auth doesn't return username, firstName, lastName.
    //                 // These will be populated by login action if provided, or later by profile page.
    //                 // this.user.tier = response.data.userTier;
    //                 this.cloudTokens = response.data.requestCount; // Assuming requestCount maps to cloudTokens
    //                 this.user.id = response.data.userId;

    //                 // localStorage.setItem('userTier', this.user.tier);
    //                 localStorage.setItem('userId', this.user.id as string); // Ensure userId is not null before setting

    //                 this.loggedIn = true;
    //                 localStorage.setItem('loggedIn', 'true');
    //             } else {
    //                 this.logout(); // Clears all user data including new fields
    //             }
    //         } catch (error) {
    //             this.logout();
    //         }
    //     },
    //     // Login action updated to accept optional payload
    //     login(payload?: Partial<UserData>) {
    //         console.log(payload);
    //         this.loggedIn = true;
    //         localStorage.setItem('loggedIn', 'true');

    //         if (payload) {
    //             if (payload.id) {
    //                 this.user.id = payload.id;
    //                 localStorage.setItem('userId', payload.id);
    //             }
    //             if (payload.username) {
    //                 this.user.username = payload.username;
    //                 localStorage.setItem('username', payload.username);
    //             }
    //             if (payload.firstName) {
    //                 this.user.firstName = payload.firstName;
    //                 localStorage.setItem('firstName', payload.firstName);
    //             }
    //             if (payload.lastName) {
    //                 this.user.lastName = payload.lastName;
    //                 localStorage.setItem('lastName', payload.lastName);
    //             }
    //             // if (payload.tier) {
    //             //     this.user.tier = payload.tier;
    //             //     localStorage.setItem('userTier', payload.tier);
    //             // }
    //         }
    //     },
    //     logout() {
    //         this.loggedIn = false;
    //         this.user = {
    //             id: null,
    //             username: null,
    //             firstName: null,
    //             lastName: null,
    //             // tier: "free",
    //         };
    //         this.cloudTokens = 0;
    //         localStorage.setItem('loggedIn', 'false');
    //         localStorage.removeItem('userId');
    //         localStorage.removeItem('username');
    //         localStorage.removeItem('firstName');
    //         localStorage.removeItem('lastName');
    //         // localStorage.removeItem('userTier');
    //     },
    //     // Action to specifically update user details, e.g., from profile page
    //     updateUserDetails(details: Partial<UserData>) {
    //         if (details.username !== undefined) {
    //             this.user.username = details.username;
    //             if (details.username === null) localStorage.removeItem('username');
    //             else localStorage.setItem('username', details.username);
    //         }
    //         if (details.firstName !== undefined) {
    //             this.user.firstName = details.firstName;
    //             if (details.firstName === null) localStorage.removeItem('firstName');
    //             else localStorage.setItem('firstName', details.firstName);
    //         }
    //         if (details.lastName !== undefined) {
    //             this.user.lastName = details.lastName;
    //             if (details.lastName === null) localStorage.removeItem('lastName');
    //             else localStorage.setItem('lastName', details.lastName);
    //         }
    //         // Add other fields like tier if they can be updated this way
    //     },
    //     useToken() {
    //         this.cloudTokens = (this.cloudTokens || 0) + 1; // Ensure cloudTokens is a number
    //     },
    // },

});
