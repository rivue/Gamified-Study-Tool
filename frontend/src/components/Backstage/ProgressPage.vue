<!-- ProgressPage.vue -->
<template>
    <div class="progress-container flex-col">
        <h1 class="page-title">{{ pageEmoji }} Your Progress</h1>
        <div class="button-container">
            <MenuButton class="square-button" label="<" @click="changePage(-1)" />
            <p class="section-title">{{ pageTitle }}</p>
            <MenuButton class="square-button" label=">" @click="changePage(1)" />
        </div>

        <div class="progress-section" v-if="dataLoaded && currentPageIndex === 0">
            <ProgressGraph :data="userProgress" />
            <div class="statistics overview-statistics">
                <div class="stat-item">
                    <span class="stat-value">{{ totalCompleted }}</span>
                    <span class="stat-label">✅ Total Completed</span>
                </div>

                <div class="stat-item">
                    <span class="stat-value">{{ currentStreak }}</span>
                    <span class="stat-label">🔥 Current Streak</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{{ maxStreak }}</span>
                    <span class="stat-label">❤️‍🔥 Best Streak</span>
                </div>
            </div>
        </div>

        <div class="progress-section" v-if="dataLoaded && currentPageIndex === 1">
            <user-stats/>
            <div class="statistics">
                <table>
                    <thead>
                        <tr>
                            <th></th>
                            <th>🏛Libraries</th>
                            <th>📖Lessons</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><span class="stat-label">Total</span></td>
                            <td>
                                <span class="stat-value">{{ totalLibraries }}</span>
                            </td>
                            <td>
                                <span class="stat-value">{{ totalLessons }}</span>
                            </td>
                        </tr>
                        <tr>
                            <td><span class="stat-label">Percentage Completed</span></td>
                            <td>
                                <span class="stat-value">{{ percentCompletedLibraries }}%</span>
                            </td>
                            <td>
                                <span class="stat-value">{{ percentCompletedLessons }}%</span>
                            </td>
                        </tr>
                        <tr>
                            <td><span class="stat-label">Completed</span></td>
                            <td>
                                <span class="stat-value">{{ completedLibraries }}</span>
                            </td>
                            <td>
                                <span class="stat-value">{{ completedLessons }}</span>
                            </td>
                        </tr>
                        <tr>
                            <td><span class="stat-label">Active</span></td>
                            <td>
                                <span class="stat-value">{{ activeLibraries }}</span>
                            </td>
                            <td>
                                <span class="stat-value">{{ activeLessons }}</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from "axios";
import ProgressGraph from "../Graphs/ProgressGraph.vue";
import MenuButton from "../Menus/MenuButton.vue";
import UserStats from "../Graphs/UserStats.vue";

interface ProgressData {
    labels: string[];
    datasets: any[];
}

// Reactive state
const currentPageIndex = ref(0);
const userProgress = ref<ProgressData>({ labels: [], datasets: [] });
const totalCompleted = ref(0);
const totalLessons = ref(0);
const activeLessons = ref(0);
const completedLessons = ref(0);
const totalLibraries = ref(0);
const activeLibraries = ref(0);
const completedLibraries = ref(0);
const percentCompletedLessons = ref(0);
const percentCompletedLibraries = ref(0);
const maxStreak = ref(0);
const currentStreak = ref(0);
const dataLoaded = ref(false);

// Computed properties
const pageEmoji = computed(() => {
    if (currentPageIndex.value === 0) {
        return "📈";
    } else if (currentPageIndex.value === 1) {
        return "🧮";
    } else {
        return "";
    }
});

const pageTitle = computed(() => {
    if (currentPageIndex.value === 0) {
        return "Progress Overview";
    } else if (currentPageIndex.value === 1) {
        return "Detailed Statistics";
    } else {
        return "";
    }
});

// Methods
const changePage = (direction: number) => {
    const maxPageIndex = 1;
    currentPageIndex.value += direction;
    if (currentPageIndex.value < 0) {
        currentPageIndex.value = maxPageIndex;
    } else if (currentPageIndex.value > maxPageIndex) {
        currentPageIndex.value = 0;
    }
};

// Lifecycle hook
onMounted(async () => {
    // try {
    //     const response = await axios.get("/api/user-progress");
    //     if (response.data.status === "success") {
            userProgress.value = 3; //response.data.progress.lineGraph;
            totalCompleted.value = 3; //response.data.progress.totalCompleted;
            totalLessons.value = 3; //response.data.progress.totalLessons;
            activeLessons.value = 3; //response.data.progress.activeLessons;
            completedLessons.value = 3; //response.data.progress.completedLessons;
            totalLibraries.value = 3; //response.data.progress.totalLibrarys;
            activeLibraries.value = 3; //response.data.progress.activeLibrarys;
            completedLibraries.value = 3; //response.data.progress.completedLibrarys;
            percentCompletedLessons.value = 3; //response.data.progress.percentCompletedLessons;
            percentCompletedLibraries.value = 3; //response.data.progress.percentCompletedLibrarys;
            maxStreak.value = 3; //response.data.progress.maxStreak;
            currentStreak.value = 3; //response.data.progress.currentStreak;
            dataLoaded.value = true;
    //     } else {
    //         console.error("Failed to fetch user progress");
    //     }
    // } catch (error) {
    //     console.error("Error fetching user progress:", error);
    // }
});
</script>

<style scoped>
.progress-container {
    margin-top: 1em;
    padding: 16px;
    display: flex;
    align-items: center;
    width: 100%;
}

.progress-section {
    margin-top: 16px;
    width: 100%;
    max-width: 720px;
    background-color: var(--background-color-1t);
    border-radius: 8px;
}

.button-container {
    width: 100%;
    max-width: 720px;
    display: flex;
    justify-content: space-around;
    align-items: center;
}

.square-button {
    padding-left: 1em;
    padding-right: 1em;
    width: 48px;
    height: 48px;
    min-width: 30px;
    line-height: 25px;
    text-align: center;
    font-weight: 700;
}

.section-title {
    font-size: 1.5em;
    flex-grow: 1;
    text-align: center;
}

.statistics {
    margin-top: 1em;
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.statistics > div {
    margin-bottom: 8px;
}

.spread {
    width: 100%;
    justify-content: space-around;
    align-items: center;
}

.stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    border-bottom: 1px solid var(--text-color);
}

.stat-value {
    font-weight: bold;
    font-size: 1.2em;
}

.stat-label {
    font-size: 0.9em;
    padding-left: 8px;
    color: var(--text-color);
    opacity: 0.9;
}

th {
    font-size: 1.5em;
}

table {
    width: 100%;
    table-layout: fixed;
}
</style>
