<template>
    <div class="rounded-2xl p-6">
        <!-- Back Button -->
        
        <h2 class="text-xl font-semibold mb-4" style="color: var(--highlight-color);">Leaderboard</h2>
        
        <!-- Leaderboard Table -->
        <div class="overflow-hidden rounded-lg border">
            
            <!-- Loading State -->
            <div v-if="loading" class="p-8 text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 mx-auto mb-2"></div>
                <p>Loading leaderboard...</p>
            </div>
            
            <!-- Empty State -->
            <div v-else-if="leaderboardData.length === 0" class="p-8 text-center">
                <p>No data available</p>
            </div>
            
            <!-- Leaderboard Entries -->
            <div v-else class="divide-y" style="border-color: var(--color-primary-dark);">
                <div v-for="(entry, index) in leaderboardData.members" :key="entry.user_id"
                class="grid grid-cols-12 gap-2 p-3 items-center transition-colors"
                :class="{'opacity-85': highlightCurrentUser && entry.user_id !== currentUserId}"
                :style="{
                    backgroundColor: entry.user_id === currentUserId ? 'var(--background-color-2t)' : 'var(--background-color)',
                }">
                         {{ entry.user_id }}
                         
                         <!-- User Info -->
                         <div class="col-span-7 flex items-center">
                             <div class="truncate">
                                 <span :class="{ 'font-semibold': entry.user_id === currentUserId }">{{ entry.name }}</span>
                                 <span v-if="entry.user_id === currentUserId" class="ml-2 text-xs px-1 rounded"
                                 style="background-color: var(--highlight-color); color: var(--background-color);">You</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <router-link :to="`/library/${libraryId}`" class="inline-flex items-center mb-4 mt-16 px-4 py-2 rounded-lg text-base font-medium transition-colors" style="background-color: var(--background-color-2t); color: var(--highlight-color);">
                <span class="mr-2">←</span> Back to Library
            </router-link>

    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

// State variables
const leaderboardData = ref([]);
const loading = ref(true);
const sortCriteria = ref('score');
const showFilterModal = ref(false);
const selectedTimePeriod = ref('week');
const highlightCurrentUser = ref(true);
const libraryId = ref(null);
const currentUserId = ref(null); // TODO: Replace with actual user ID

// Fetch leaderboard data
const fetchLeaderboard = async () => {
    loading.value = true;
    try {

        axios.get(`/api/library/${libraryId.value}/scores`, {
            params: {
                libraryId: libraryId.value,
            }
        })
        .then(response => {
            leaderboardData.value = response.data;
        })
        .catch(error => {
            console.error('Error fetching leaderboard:', error);
            leaderboardData.value = [];
        })
        .finally(() => {
            loading.value = false;
        });

        // Apply default sort
        // sortByScore();
    } catch (error) {
        console.error('Error fetching leaderboard:', error);
        leaderboardData.value = [];
    } finally {
        loading.value = false;
    }
};

// Sort methods
// const sortByScore = () => {
//     sortCriteria.value = 'score';
//     leaderboardData.value.sort((a, b) => b.score - a.score);
// };

// const sortByName = () => {
//     sortCriteria.value = 'name';
//     leaderboardData.value.sort((a, b) => a.name.localeCompare(b.name));
// };

// Filter methods
const applyFilters = () => {
    showFilterModal.value = false;
    fetchLeaderboard(); // Re-fetch with new filters
};

const resetFilters = () => {
    selectedTimePeriod.value = 'week';
    highlightCurrentUser.value = true;
};

// Initialize component
onMounted(() => {
    const route = useRoute(); // Access the route object
    libraryId.value = route.params.libraryId; 
    console.log(route.params.libraryId);
    fetchLeaderboard();
});
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}
</style>