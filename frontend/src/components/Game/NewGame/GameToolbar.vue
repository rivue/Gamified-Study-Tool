<template>
  <div class="toolbar-container">
    <!-- First Row: Room Name -->
    <div class="room-name" @click="gameStore.showGameInfo">
      {{ gameStore.libraryTopic }}
    </div>

    <!-- Second Row: Toolbar -->
    <div v-if="visible" class="game-toolbar">
      <!-- Left side: Likes and Clouds -->
      <div class="left-side">
        <!-- <button
          class="toolbar-btn like-button"
          :style="{ color: isLiked ? 'var(--highlight-color)' : '' }"
          @click="likeLib"
        >
          {{ likeText }}
        </button> -->
        <!-- <div class="toolbar-btn" @click="navToPlans">☁️{{ discovery }}</div>☁️ -->
      </div>

      <!-- Right side: Score and Time -->
      <div class="right-side score-container">
        <!-- <span
          class="score"
          :class="{ 
            'animating-score': isScoreAnimating
          }"
        >
          💎{{ score }}
        </span> -->
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="progress-bar-container">
      <div class="progress-bar" :style="{ width: progressBarWidth }"></div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useGameStore } from "@/store/gameStore";
import { useAuthStore } from "@/store/authStore";

const router = useRouter();
const gameStore = useGameStore();
const authStore = useAuthStore();

const isLiked = ref(false);
const isScoreAnimating = ref(false);
const initialProgress = Math.floor(Math.random() * (17 - 8 + 1)) + 8;

watch(() => gameStore.score, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    isScoreAnimating.value = true;
    setTimeout(() => {
      isScoreAnimating.value = false;
    }, 300);
  }
});

const progressBarWidth = computed(() => {
  const progress = gameStore.currentQuestion / gameStore.factoids.length;
  const width = Math.min(initialProgress + (100 - initialProgress) * Math.pow(progress, 0.1), 100);
  return `${width}%`;
});

const score = computed(() => {
  return `${gameStore.score} (+${gameStore.multiplier})`;
});

const discovery = computed(() => {
  return authStore.cloudTokens;
});

const likeText = computed(() => {
  return isLiked.value ? "Liked 👍" : "Like 👍";
});

const visible = computed(() => {
  return !gameStore.completed;
});

function likeLib() {
  axios
    .post("/api/library/like", { libraryId: gameStore.libraryId })
    .then(() => {
      isLiked.value = true;
    })
    .catch((error) => {
      console.error("Error liking the library:", error);
    });
}

function navToPlans() {
  router.push("/plan");
}
</script>



<style scoped>
.toolbar-container {
  z-index: 111;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.room-name {
  text-align: center;
  font-size: 1.2em;
  font-weight: bold;
  padding-top: 10px;
  color: var(--text-color);
}

.game-toolbar {
  width: 100%;
  display: flex;  
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  color: var(--text-color);
}

.left-side,
.right-side {
  display: flex;
  align-items: center;
  padding: 0 0.5em;
  gap: 1em;
}

.score-container {
  display: flex;
  align-items: center;
  gap: 1em;
}

.score,

.animating-score,
/* 
@keyframes pulse {
  0% {
    transform: scale(1);
    color: var(--text-color);
  }
  50% {
    transform: scale(1.1);
    color: var(--highlight-color);
  }
  100% {
    transform: scale(1);
    color: var(--text-color);
  }
} */

.progress-bar-container {
  width: 100%;
  background-color: #0000001a;
}

.progress-bar {
  height: 4px;
  background-color: var(--element-color-1);
  transition: width 0.3s ease;
}
</style>
