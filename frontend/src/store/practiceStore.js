import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStatsStore = defineStore('practiceStore', {
  state: () => ({
    courseName: '',
  }),
  actions: {
    async fetchStatsFromBackend() {
      try {
        const response = await axios.get('/api/library/2');
        if (response.data) {
            console.log(response.data)
            this.courseName = "test";
        //   this.courseName = response.data.streak;
        }
      } catch (error) {
        console.error('Error fetching stats from backend', error);
      }
    },
    getStats() {
      if (this.streak === null || this.exp === null) {
        console.log("nulls")
        this.fetchStatsFromBackend();
      }
      console.log(this.courseName)
      return {
        courseName: this.courseName,
      };
    },
}});
