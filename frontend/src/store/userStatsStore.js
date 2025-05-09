import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStatsStore = defineStore('user', {
    state: () => ({
        currentStreak: null,
        bestStreak: null,
        streakLoaded: false,
    }),
    actions: {
        async fetchStreak() {
            console.log("gi")
            if (this.streakLoaded) return
            try {
                const { data } = await axios.get('/api/user/streak');
                console.log(data);
                if (data) { // Fixed: was using response.data instead of data
                    this.currentStreak = data.currentStreak;
                    this.bestStreak = data.bestStreak;
                }
            } catch (e) {
                console.error('Error fetching stats from backend', e);
            } finally {
                this.streakLoaded = true;
            }
        },
        resetStats() {
            this.currentStreak = null;
            this.bestStreak = null;
            this.streakLoaded = false;
        }
    },
});
