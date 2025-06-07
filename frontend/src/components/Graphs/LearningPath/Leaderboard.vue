<template>
    <div class="rounded-2xl p-6 leaderboard-container">
        <!-- Back Button -->
        
        <h2 class="text-xl font-semibold mb-6 text-center" style="color: var(--highlight-color);">Leaderboard</h2>
        
        <!-- Leaderboard Table -->
        <div class="overflow-hidden rounded-lg shadow-lg border" style="border-color: var(--border-color-dark);">
            
            <!-- Loading State -->
            <div v-if="loading" class="p-8 text-center">
                <!-- <LottiePlayer
                    src="https://lottie.host/9c0c9f3e-1fS9-4d07-bS20-37415505715f/c7b8gFA8A0.json"  
                    background="transparent"
                    speed="1"
                    style="width: 150px; height: 150px; margin: auto;"
                    loop
                    autoplay
                /> -->
                <DotLottieVue autoplay loop
                                src="https://lottie.host/b96a9b39-d99b-4f64-a92d-8b39aefc27ca/73Yl9OD4Tc.lottie" />
                <p class="mt-4 text-lg" style="color: var(--text-color-secondary);">Loading leaderboard...</p>
            </div>
            
            <!-- Empty State -->
            <div v-else-if="!leaderboardData || leaderboardData.length === 0 || !leaderboardData.members || leaderboardData.members.length === 0" class="p-8 text-center">
                <p style="color: var(--text-color-secondary);">No data available to display.</p>
            </div>
            
            <!-- Leaderboard Table -->
            <div v-else class="overflow-x-auto">
                <table class="min-w-full divide-y" style="border-color: var(--border-color-light);">
                    <thead style="background-color: var(--background-color-2);">
                        <tr>
                            <th scope="col" class="px-4 py-3 text-center text-xs font-medium uppercase tracking-wider" style="color: var(--text-color-primary);">Rank</th>
                            <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider" style="color: var(--text-color-primary);">User</th>
                            <th scope="col" class="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider" style="color: var(--text-color-primary);">Score</th>
                            <th scope="col" class="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider th-completed" style="color: var(--text-color-primary);">Completed</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y" style="background-color: var(--background-color); border-color: var(--border-color-light);">
                        <tr v-for="(entry, index) in leaderboardData.members" :key="entry.username"
                            class="transition-all duration-300 ease-in-out user-row"
                            :class="{
                                'current-user-highlight': entry.username === currentUsername,
                                'top-rank': index < 3
                            }"
                            :style="{ '--user-rank-color': getRankColor(index) }">
                            
                            <td class="px-4 py-3 whitespace-nowrap text-center">
                                <div class="flex items-center justify-center">
                                    <Trophy v-if="index === 0" class="h-6 w-6 icon-rank" :style="{ color: 'var(--user-rank-color)' }" />
                                    <Award v-else-if="index === 1" class="h-6 w-6 icon-rank" :style="{ color: 'var(--user-rank-color)' }" />
                                    <Medal v-else-if="index === 2" class="h-6 w-6 icon-rank" :style="{ color: 'var(--user-rank-color)' }" />
                                    <span v-else class="font-medium text-lg rank-text" :style="{ color: 'var(--text-color-secondary)'}">{{ index + 1 }}</span>
                                </div>
                            </td>
                                 
                            <td class="px-4 py-3 whitespace-nowrap">
                                <div class="flex items-center">
                                    <!-- <img :src="entry.avatarUrl || defaultAvatar" alt="avatar" class="h-10 w-10 rounded-full mr-3 border-2" :style="{ borderColor: entry.username === currentUsername ? 'var(--highlight-color)' : 'var(--border-color-light)' }"/> -->
                                    <div class="truncate">
                                        <span class="font-semibold text-lg user-name" :style="{ color: entry.username === currentUsername ? 'var(--highlight-color)' : 'var(--text-color-primary)' }">{{ entry.name || entry.username }}</span>
                                        <span v-if="entry.username === currentUsername" class="ml-2 text-xs px-2 py-0.5 rounded-full font-medium user-tag"
                                              style="background-color: var(--highlight-color); color: var(--background-color);">You</span>
                                    </div>
                                </div>
                            </td>

                            <td class="px-4 py-3 whitespace-nowrap text-right font-medium text-lg score-text" :style="{ color: 'var(--text-color-primary)' }">
                                {{ entry.score_sum || 0 }}
                            </td>

                            <td class="px-4 py-3 whitespace-nowrap text-right text-sm completed-text" :style="{ color: 'var(--text-color-secondary)' }">
                                {{ entry.lessons_completed_count || 0 }} lessons
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
                
        <div class="mt-8 text-center back-button-container">
            <router-link :to="`/lessons/${libraryId}`" class="back-to-library-link inline-flex items-center px-6 py-3 rounded-lg text-lg font-medium transition-colors shadow-md hover:shadow-lg" style="background-color: var(--highlight-color); color: var(--background-color);">
                <ArrowLeftCircle class="h-5 w-5 mr-2" /> Back to Library
            </router-link>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '@/store/authStore';
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'
import { Trophy, Award, Medal, ArrowLeftCircle } from 'lucide-vue-next';

// State variables
const authStore = useAuthStore();
const leaderboardData = ref<any>([]); // Using any for now, define a proper type later
const loading = ref(true);
// const sortCriteria = ref('score'); // Kept for potential future use
// const showFilterModal = ref(false); // Kept for potential future use
// const selectedTimePeriod = ref('week'); // Kept for potential future use
// const highlightCurrentUser = ref(true); // Kept for potential future use

const route = useRoute();
const libraryId = ref(route.params.libraryId);
const currentUsername = computed(() => authStore.username);

// Fetch leaderboard data
const fetchLeaderboard = async () => {
    loading.value = true;
    try {
        const response = await axios.get(`/api/library/${libraryId.value}/scores`, {
            params: {
                // No specific params needed for now based on current implementation
            }
        });
        // Assuming the API returns data in the structure { members: [...] }
        // And members are already sorted by score_sum descending
        leaderboardData.value = response.data;
    } catch (error) {
        console.error('Error fetching leaderboard:', error);
        leaderboardData.value = { members: [] }; // Ensure members array exists even on error
    } finally {
        loading.value = false;
    }
};

const getRankColor = (index: number) => {
    if (index === 0) return 'var(--gold-color, #FFD700)';
    if (index === 1) return 'var(--silver-color, #C0C0C0)';
    if (index === 2) return 'var(--bronze-color, #CD7F32)';
    return 'var(--text-color-secondary)';
};

// Initialize component
onMounted(() => {
    fetchLeaderboard();
});
</script>

<style scoped>
.leaderboard-container {
    background-color: var(--background-color); /* Use site's main background */
    color: var(--text-color-primary); /* Use site's primary text color */
    max-width: 900px; /* Slightly wider for better table layout */
    margin: 2rem auto; /* Add more margin for better page centering */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08); /* Softer shadow */
}

/* Table specific styles */
table {
    width: 100%;
    border-collapse: collapse; /* Ensures borders are neat */
}

th, td {
    padding: 1rem 1rem; /* Standardized padding */
    vertical-align: middle; /* Align content vertically */
    transition: background-color 0.2s ease-in-out;
}

th {
    background-color: var(--background-color-2t); /* Slightly different background for header */
    color: var(--text-color-secondary); /* Header text color */
    font-weight: 600; /* Bolder header text */
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.user-row:hover {
    background-color: var(--background-color-hover, rgba(var(--highlight-color-rgb, 79, 70, 229), 0.05)); /* Subtle hover */
}

.current-user-highlight {
    background-color: var(--highlight-color-translucent, rgba(var(--highlight-color-rgb, 79, 70, 229), 0.1)) !important; /* More subtle highlight */
    border-left: 5px solid var(--highlight-color); /* Prominent left border */
}

.current-user-highlight td:first-child {
    padding-left: calc(1rem - 5px); /* Adjust for border */
}


.current-user-highlight .user-name,
.current-user-highlight .score-text {
    color: var(--highlight-color) !important;
    font-weight: 600;
}

.icon-rank {
    height: 1.75rem; /* Slightly larger icons */
    width: 1.75rem;
}
.rank-text {
    font-size: 1.125rem; /* lg */
}

.user-name {
    font-size: 1.125rem; /* lg */
}
.user-tag {
    font-size: 0.75rem; /* xs */
    padding: 0.125rem 0.5rem; /* py-0.5 px-2 */
}

.score-text {
     font-size: 1.125rem; /* lg */
}
.completed-text {
    font-size: 0.875rem; /* sm */
}


/* Responsive adjustments */
@media (max-width: 768px) {
    .leaderboard-container {
        margin: 1rem;
        padding: 1rem; /* Reduced padding on smaller screens */
    }

    h2 {
        font-size: 1.25rem; /* Reduced heading size */
        margin-bottom: 1rem;
    }

    th, td {
        padding: 0.75rem 0.5rem; /* Reduced cell padding */
        font-size: 0.875rem; /* Smaller font for table content */
    }
    .icon-rank {
        height: 1.25rem;
        width: 1.25rem;
    }
    .rank-text, .user-name, .score-text {
        font-size: 0.9rem;
    }
    .completed-text, .user-tag {
        font-size: 0.7rem;
    }

    /* Hide "lessons" text part on very small screens if necessary */
    .th-completed {
        /* Consider hiding or abbreviating if space is very tight */
    }
    .completed-text span.lessons-suffix {
         display: none; /* Example: hide " lessons" text */
    }

    .back-to-library-link {
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
    }
    .back-to-library-link .h-5 { /* Target icon if needed */
        height: 1rem;
        width: 1rem;
        margin-right: 0.25rem;
    }

     .overflow-x-auto {
        overflow-x: auto; /* Ensure table scrolls horizontally if it's too wide */
    }
}

@media (max-width: 480px) {
    .user-name {
        max-width: 100px; /* Limit width of user name to prevent overflow */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .th-completed, .completed-text {
      /* Example: Make 'Completed' column less prominent or hide on very small screens */
      /* display: none; */ /* Uncomment to hide */
    }
}

/* Define rank colors if not globally available in :root of a global stylesheet */
/* These are already defined in the previous step, but good to have them here for context if this style block was separate */
:root {
    --gold-color: #FFD700;
    --silver-color: #C0C0C0;
    --bronze-color: #CD7F32;
    --highlight-color-translucent: rgba(var(--highlight-color-rgb, 79, 70, 229), 0.15);
}

.animate-spin {
    border-color: var(--highlight-color);
    border-bottom-color: transparent;
}
</style>