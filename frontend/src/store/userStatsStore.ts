import { defineStore } from 'pinia';
import axios from 'axios';

interface UserStatsState {
    currentStreak: number | null;
    bestStreak: number | null;
    streakLoaded: boolean;
}

interface StreakResponse {
    current_streak: number;
    max_streak: number;
}

export const useUserStatsStore = defineStore('user', {
    state: (): UserStatsState => ({
        currentStreak: null,
        bestStreak: null,
        streakLoaded: false,
    }),
    actions: {
        async fetchStreak() {
            try {
                const { data } = await axios.get<StreakResponse>('/api/user/streak');
                if (data) {
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
    }
});
