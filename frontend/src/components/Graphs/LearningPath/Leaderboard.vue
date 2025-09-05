<template>
    <div class="leaderboard-page">
        <!-- Confetti Animation -->
        <canvas id="confetti-canvas" v-show="showConfetti"></canvas>

        <div class="leaderboard-container">
            <!-- Header -->
            <div class="leaderboard-header">
                <h1 class="leaderboard-title">Leaderboard</h1>
                <p class="leaderboard-subtitle">See who's on top of the game!</p>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="loading-container">
                <DotLottieVue autoplay loop src="https://lottie.host/b96a9b39-d99b-4f64-a92d-8b39aefc27ca/73Yl9OD4Tc.lottie" />
                <p>Loading Leaderboard...</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="!leaderboardData || leaderboardData.length === 0 || !leaderboardData.members || leaderboardData.members.length === 0" class="empty-state">
                <p>No data available to display.</p>
            </div>

            <!-- Leaderboard Content -->
            <div v-else>
                <!-- Top 3 Users -->
                <div class="top-three-container">
                    <div v-for="(user, index) in topThree" :key="user.username" :class="['rank-card', 'rank-' + (index + 1)]">
                        <div class="rank-badge">{{ index + 1 }}</div>
                        <img :src="user.avatarUrl || defaultAvatar" alt="avatar" class="rank-avatar">
                        <p class="rank-name">{{ getDisplayName(user) }}</p>
                        <p class="rank-points">{{ user.points || 0 }} pts</p>
                    </div>
                </div>

                <!-- Other Users -->
                <ul class="leaderboard-list">
                    <li v-for="(user, index) in otherUsers" :key="user.username" class="leaderboard-item" :class="{ 'current-user-highlight': user.username === currentUsername }">
                        <div class="user-rank">{{ index + 4 }}</div>
                        <img :src="user.avatarUrl || defaultAvatar" alt="avatar" class="user-avatar">
                        <div class="user-info">
                            <p class="user-name">{{ getDisplayName(user) }}</p>
                            <span v-if="user.username === currentUsername" class="user-tag">You</span>
                        </div>
                        <div class="user-points">{{ user.points || 0 }} pts</div>
                    </li>
                </ul>
            </div>

            <!-- Back Button -->
            <div class="back-button-container">
                <router-link :to="`/lessons/${libraryId}`" class="back-to-library-link">
                    <ArrowLeftCircle class="h-5 w-5 mr-2" /> Back to Library
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '@/store/authStore';
import { DotLottieVue } from '@lottiefiles/dotlottie-vue';
import { ArrowLeftCircle } from 'lucide-vue-next';
import confetti from 'canvas-confetti';

// State variables
const authStore = useAuthStore();
const leaderboardData = ref<any>({ members: [] });
const loading = ref(true);
const route = useRoute();
const libraryId = ref(route.params.libraryId);
const currentUsername = computed(() => authStore.username);
const showConfetti = ref(false);

const defaultAvatar = 'https://i.pravatar.cc/150?u=a042581f4e29026704d';

// Computed properties for top 3 and other users
const topThree = computed(() => leaderboardData.value.members.slice(0, 3));
const otherUsers = computed(() => leaderboardData.value.members.slice(3));

// Helper to display a concise username without exposing full email addresses
const getDisplayName = (user: any) => {
    if (user?.name && user.name.trim() !== '') {
        return user.name;
    }
    return user?.username?.split('@')[0] || user?.username;
};

// Fetch leaderboard data
const fetchLeaderboard = async () => {
    loading.value = true;
    try {
        const response = await axios.get(`/api/library/${libraryId.value}/scores`);
        leaderboardData.value = response.data;
        checkConfetti();
    } catch (error) {
        console.error('Error fetching leaderboard:', error);
        leaderboardData.value = { members: [] };
    } finally {
        loading.value = false;
    }
};

// Trigger confetti if the current user is in the top 3
const checkConfetti = () => {
    const currentUserRank = leaderboardData.value.members.findIndex(
        (user: any) => user.username === currentUsername.value
    );
    if (currentUserRank !== -1 && currentUserRank < 3) {
        showConfetti.value = true;
        const canvas = document.getElementById('confetti-canvas') as HTMLCanvasElement;
        if(canvas) {
            const myConfetti = confetti.create(canvas, {
                resize: true,
                useWorker: true,
            });
            myConfetti({
                particleCount: 150,
                spread: 60,
            });
        }
    }
};

onMounted(() => {
    fetchLeaderboard();
});
</script>

<style scoped>
.leaderboard-page {
    background: linear-gradient(135deg, #1e1e2f 0%, #1d1b31 100%);
    min-height: 100vh;
    padding: 2rem;
    color: #fff;
}

.leaderboard-container {
    max-width: 800px;
    margin: auto;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.leaderboard-header {
    text-align: center;
    margin-bottom: 2rem;
}

.leaderboard-title {
    font-size: 2.5rem;
    font-weight: bold;
    text-shadow: 0 0 10px #fff, 0 0 20px #ff00ff, 0 0 30px #00ffff;
}

.leaderboard-subtitle {
    font-size: 1.2rem;
    color: #a9a9c4;
}

.loading-container, .empty-state {
    text-align: center;
    padding: 4rem 0;
}

.top-three-container {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 1rem;
    margin-bottom: 2rem;
}

.rank-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    transition: transform 0.3s ease;
    width: 150px;
}

.rank-card:hover {
    transform: translateY(-10px);
}

.rank-1 {
    order: 2;
    width: 180px;
    padding-bottom: 2.5rem;
    background: linear-gradient(145deg, #ffdf00, #d4af37);
    color: #000;
}

.rank-2 {
    order: 1;
    width: 160px;
    background: linear-gradient(145deg, #c0c0c0, #a9a9a9);
    color: #000;
}

.rank-3 {
    order: 3;
    width: 160px;
    background: linear-gradient(145deg, #cd7f32, #a0522d);
    color: #000;
}

.rank-badge {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.rank-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 3px solid #fff;
    margin: 0 auto 1rem;
}

.rank-name {
    font-weight: bold;
    font-size: 1.1rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.rank-points {
    font-size: 1rem;
}

.leaderboard-list {
    list-style: none;
    padding: 0;
}

.leaderboard-item {
    display: flex;
    align-items: center;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    margin-bottom: 0.5rem;
    transition: background-color 0.3s ease;
}

.leaderboard-item:hover {
    background: rgba(255, 255, 255, 0.1);
}

.current-user-highlight {
    background: rgba(0, 255, 255, 0.2);
    border: 1px solid #00ffff;
}

.user-rank {
    font-size: 1.2rem;
    font-weight: bold;
    width: 40px;
    text-align: center;
}

.user-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin: 0 1rem;
}

.user-info {
    flex-grow: 1;
    min-width: 0;
}

.user-name {
    font-weight: bold;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.user-tag {
    background: #00ffff;
    color: #1e1e2f;
    padding: 0.2rem 0.5rem;
    border-radius: 5px;
    font-size: 0.8rem;
    margin-left: 0.5rem;
}

.user-points {
    font-size: 1.1rem;
    font-weight: bold;
}

.back-button-container {
    text-align: center;
    margin-top: 2rem;
}

.back-to-library-link {
    display: inline-flex;
    align-items: center;
    padding: 0.8rem 1.5rem;
    background: #00ffff;
    color: #1e1e2f;
    border-radius: 10px;
    text-decoration: none;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.back-to-library-link:hover {
    background: #00cccc;
}

#confetti-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
    pointer-events: none;
}
</style>
