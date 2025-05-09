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
            if (this.streakLoaded) return
            try {
                const { data } = await axios.get('/api/user/streak');
                if (data) { // Fixed: was using response.data instead of data
                    this.currentStreak = data.current_streak;
                    this.bestStreak = data.max_streak;
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
