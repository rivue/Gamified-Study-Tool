// stores/loading.js
import { defineStore } from 'pinia';

export const useLoadingStore = defineStore('loadingStore', {
    state: () => ({ isLoading: false }),
    actions: {
      start() { this.isLoading = true },
      finish() { this.isLoading = false }
    }
  })