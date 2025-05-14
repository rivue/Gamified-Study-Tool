<template>
    <transition name="fade">
        <div 
        v-if="completionVisible" 
        class="completion-overlay">
        <div 
        v-if="firstPage" 
            class="pre-completion-content">
                <div class="confetti-container">
                    <div v-for="i in 50" :key="i" :class="`confetti confetti-${i}`" :style="{
                        left: `${Math.random() * 100}%`,
                        animationDelay: `${Math.random() * 5}s`,
                        animationDuration: `${3 + Math.random() * 4}s`
                    }"></div>
                </div>
                <div class="celebration-container">
                    <div class="main-title animate-pop">Lesson Complete!</div>
                    <div class="streak-counter animate-bounce p-4 pt-8">
                        <span class="streak-days">
                            Current Streak:
                            <span class="streak-icon-container">

                                <img src="../../../assets/images/fireicon.png" alt="Fire Streak Icon" class="streak-fire-icon"
                                />
                                {{ currentStreak }}
                            </span>

                        </span>
                    </div>
                </div>
                <div class="xp-badge animate-pulse">+25 XP</div>
                <div class="cta-container">
                    <button class="primary-cta animate-pulse" @click="nextPage">
                        Continue to next Lesson
                    </button>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useGameStore } from "@/store/gameStore";
import { useUserStatsStore } from "@/store/userStatsStore";
import { storeToRefs } from "pinia";

const router = useRouter();
const gameStore = useGameStore();
const userStatsStore = useUserStatsStore();
const { currentStreak } = storeToRefs(userStatsStore);

const page = ref(0);
const showLeaderBoard = ref(false);

const completionVisible = computed(() => gameStore.completed);
const firstPage = computed(() => page.value === 0);

async function nextPage() {
    userStatsStore.resetStats(); // triggers fetchStreak in TopBar
    router.push(`/lessons/${gameStore.libraryId}`);
    page.value = 1;
}

function toggleLeaderBoard() {
    showLeaderBoard.value = true;
}
</script>

<style scoped>
/* And update the completion-overlay class to start with a softer background */
.completion-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 190;
}


.pre-completion-content {
    background-color: var(--background-color);
    color: var(--text-color);
    border-radius: 16px;
    padding: 3rem;
    max-width: 600px;
    width: 100%;
    box-sizing: border-box;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
    text-align: center;
}

.celebration-container {
    position: relative;
    z-index: 10;
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    background: #feb47b;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.sub-title {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: var(--text-color);
}

.streak-counter {
    font-size: 2rem;
    font-weight: bold;
    margin: 1.5rem 0;
    display: flex;
    justify-content: center;
}

.streak-fire {
    font-size: 2.2rem;
    animation: flame 1s infinite alternate;
}

.streak-days {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    width: auto;
    display: inline-flex;
}

.xp-badge {
    background-color: #58cc02;
    color: white;
    font-weight: bold;
    font-size: 1.5rem;
    padding: 0.5rem 1.2rem;
    border-radius: 20px;
    display: inline-block;
    margin: 1rem 0;
    box-shadow: 0 3px 0 rgba(0, 0, 0, 0.2);
}

.motivational-text {
    font-size: 1.4rem;
    margin: 1rem 0 1.5rem;
    opacity: 0.9;
}

.cta-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    margin-top: 1.5rem;
}

.primary-cta {
    background-color: #58cc02 !important;
    color: white !important;
    font-size: 1.2rem !important;
    padding: 0.8rem 2rem !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 0 #458c01 !important;
    transform: translateY(0);
    transition: transform 0.2s, box-shadow 0.2s !important;
}

.primary-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 0 #458c01 !important;
}

.primary-cta:active {
    transform: translateY(2px);
    box-shadow: 0 2px 0 #458c01 !important;
}

/* Animations */
.animate-pop {
    animation: pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.animate-bounce {
    animation: bounce 2s infinite;
}

.animate-fade-in {
    animation: fadeIn 1s;
}

.animate-slide-up {
    animation: slideUp 1.5s;
}

.animate-pulse {
    animation: pulse 2s infinite;
}

@keyframes pop {
    0% {
        transform: scale(0);
        opacity: 0;
    }

    70% {
        transform: scale(1.1);
        opacity: 1;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

@keyframes bounce {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-10px);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes slideUp {
    from {
        transform: translateY(20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

@keyframes pulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.05);
    }

    100% {
        transform: scale(1);
    }
}

@keyframes flame {
    from {
        transform: scale(1);
        filter: brightness(1);
    }

    to {
        transform: scale(1.1);
        filter: brightness(1.2);
    }
}

/* Confetti */
.confetti {
    position: absolute;
    width: 10px;
    height: 10px;
    top: -20px;
    /* Start just above the container */
    background-color: #f00;
    opacity: 0.7;
    animation: confetti-fall 5s linear infinite;
}

@keyframes confetti-fall {
    0% {
        transform: translateY(-100px) rotate(0deg);
        opacity: 1;
    }

    100% {
        transform: translateY(1000px) rotate(720deg);
        opacity: 0;
    }
}

/* Generate unique positions and colors for each confetti piece */
.confetti-container div:nth-child(odd) {
    background-color: #58cc02;
}

.confetti-container div:nth-child(3n) {
    background-color: #ff9600;
}

.confetti-container div:nth-child(3n+1) {
    background-color: #ff4b4b;
}

.confetti-container div:nth-child(5n) {
    background-color: #2b70c9;
}

.confetti-container div:nth-child(4n) {
    background-color: #a560e8;
}

.confetti-container div {
    clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
}

.confetti-container div:nth-child(even) {
    clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
}

.confetti-container div:nth-child(3n) {
    clip-path: circle(50% at 50% 50%);
}

/* Distribute confetti across the container */
.confetti-container div {
    animation-delay: calc(0.1s * var(--i, 0));
    left: calc(var(--i, 0) * 2%);
}

@media (max-width: 600px) {
    .main-title {
        font-size: 2rem;
    }

    .sub-title {
        font-size: 1.4rem;
    }

    .streak-counter {
        font-size: 1.6rem;
    }

    .xp-badge {
        font-size: 1.2rem;
    }

    .pre-completion-content {
        padding: 2rem;
        max-width: 90%;
    }
}

@keyframes confetti-fall {
    0% {
        transform: translateY(0) rotate(0deg);
        opacity: 1;
    }

    100% {
        transform: translateY(500px) rotate(720deg);
        opacity: 0;
    }
}

.streak-icon-container {
    display: flex;
    align-items: center;
}

.streak-fire-icon {
    height: 1.8rem;
    width: auto;
    margin: 0 0.3rem;
    pointer-events: none;
}
</style>