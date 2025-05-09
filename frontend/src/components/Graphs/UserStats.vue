<template>
    <div class="stats-container rounded-xl border shadow-md" 
             style="background-color: var(--background-color); border-color: var(--color-primary-dark);">
        <div class="header-row">
            <h3 class="stats-title" style="color: var(--highlight-color);">Your Progress</h3>
            
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Current Streak</div>
                <StreakFire :streak="streak" />
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Max Streak</div>
                <div class="stat-value">{{ maxStreak }}</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Experience</div>
                <ExpProgressBar :newExp="exp" />
            </div>
            
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue";
// import { useUserStatsStore } from "@/store/userStatsStore";
import StreakFire from "./StreakFire.vue";
import ExpProgressBar from "./ExpProgressBar.vue";
import ProgressPage from "../Backstage/ProgressPage.vue";

export default defineComponent({
    name: "UserStats",
    components: {
        StreakFire, ExpProgressBar, ProgressPage
    },
    setup() {
        // const userStatsStore = useUserStatsStore();
        // userStatsStore.getStats();

        // const streak = computed(() => userStatsStore.streak);
        // const exp = computed(() => userStatsStore.exp);
        // const maxStreak = computed(() => userStatsStore.maxStreak);
        // const questionsAnswered = computed(() => userStatsStore.questionsAnswered);
        const streak = 4;
        const exp = 152;
        const maxStreak = 7;
        const questionsAnswered = 42;

        return {
            streak,
            exp,
            maxStreak,
            questionsAnswered
        };
    },
    methods: {
        goToSettings() {
            this.$router.push("/settings");
        }
    }
});
</script>

<style scoped>
.stats-container {
    display: flex;
    flex-direction: column;
    padding: 1.25rem;
    margin: 1rem 0;
    max-width: 32rem;
    width: 100%;
    transition: transform 0.2s, box-shadow 0.2s;
}

.stats-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.stats-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0;
}

.settings-icon {
    background: none;
    border: none;
    cursor: pointer;
    color: var(--color-primary-light);
    transition: color 0.2s;
}

.settings-icon:hover {
    color: var(--highlight-color);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
}

.stat-card {
    padding: 1rem;
    border-radius: 0.75rem;
    background-color: var(--background-color-1t, rgba(255, 255, 255, 0.05));
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: background-color 0.2s;
}

.stat-card:hover {
    background-color: var(--element-color-1, rgba(255, 255, 255, 0.1));
}

.stat-label {
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: var(--color-primary-light, #6b7280);
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--highlight-color);
}

@media (max-width: 640px) {
    .stats-grid {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 400px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
</style>
