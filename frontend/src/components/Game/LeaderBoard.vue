<template>
  <div class="leaderboard-container">
    <div v-if="isLibraryMode" class="leaderboard-header">
      <h1>Top 5 (this Library)</h1>
      <button class="mode-toggle-button" @click="toggleMode">
        <span>🌐</span>
      </button>
    </div>
    <div v-else key="globalTitle" class="leaderboard-header">
      <h1>Top 5 (Global)</h1>
      <button class="mode-toggle-button" @click="toggleMode">
        <span>🏛️</span>
      </button>
    </div>

    <div v-if="scores && scores.length > 0">
      <table class="leaderboard-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>User</th>
            <th v-if="!isLibraryMode">Library</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(score, index) in scores" :key="index">
            <td>{{ score.time }}s</td>
            <td>{{ score.email }}</td>
            <td v-if="!isLibraryMode">
              <router-link :to="`/lessons/${score.library_id}`">
                #{{ score.library_id }}
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else>
      Be the first!
    </div>

    <div v-if="!scores || scores.length < 3">
      <p class="challenge-text">
        Challenge your friends, classmates, colleagues:
      </p>
      <div class="share-link-box">
        <div class="share-link-container">
          <input
            ref="shareInput"
            class="share-link-input"
            type="text"
            :value="currentURL"
            readonly
          />
          <button class="copy-button" @click="copyShareLink">
            Copy
          </button>
        </div>
        <transition name="fade">
          <span 
            class="copy-status-message" 
            v-if="copySuccessMessageVisible"
          >
            Copied!
          </span>
        </transition>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const scores = ref<any[] | null>(null);
const libraryId = ref<number | null>(null);
const originalLibraryId = ref<number | null>(null);
const currentURL = ref(window.location.href);
const copySuccessMessageVisible = ref(false);

const isLibraryMode = computed(() => !!libraryId.value);

function checkRoute() {
  const idParam = route.params.id;
  if (idParam && typeof idParam === 'string') {
    const id = parseInt(idParam, 10);
    if (!isNaN(id)) {
      libraryId.value = id;
      originalLibraryId.value = id;
    }
  }
}

async function fetchScores() {
  try {
    let url = '/api/scores';
    if (isLibraryMode.value) {
      url = `/api/scores/library/${libraryId.value}`;
    }
    const response = await axios.get(url);
    scores.value = response.data.slice(0, 5);
  } catch (error) {
    scores.value = null;
    console.error('Error fetching scores:', error);
  }
}

function copyShareLink() {
  navigator.clipboard
    .writeText(currentURL.value)
    .then(() => {
      copySuccessMessageVisible.value = true;
      setTimeout(() => {
        copySuccessMessageVisible.value = false;
      }, 1500);
    })
    .catch((err) => {
      console.error('Failed to copy text: ', err);
    });
}

function toggleMode() {
  if (isLibraryMode.value) {
    libraryId.value = null;
  } else {
    if (originalLibraryId.value) {
      libraryId.value = originalLibraryId.value;
    } else {
      return;
    }
  }
  fetchScores();
}

onMounted(() => {
  checkRoute();
  fetchScores();
});
</script>


<style scoped>
/* Fade transition for the "Copied!" text */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.leaderboard-container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 20px;
  color: var(--text-color);
}

.leaderboard-header {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  color: var(--text-color);
}

.leaderboard-table thead {
  background: var(--background-color-2t);
}

.leaderboard-table th,
.leaderboard-table td,
.leaderboard-table tr {
  border: none;
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid var(--highlight-color);
}

.mode-toggle-button {
  margin: 0.5em;
  margin-right: 0;
  background: var(--element-color-1);
  padding: 10px 10px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  color: var(--light-text);
}

.mode-toggle-button:hover {
  background: var(--element-color-2);
}

.challenge-text {
  font-size: 1.2em;
  margin: 20px 0;
  font-weight: bold;
}

.share-link-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.share-link-container {
  display: flex;
  width: 80%;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.share-link-input {
  flex: 1;
  padding: 0.5em;
  font-size: 1em;
  text-align: center;
  background: var(--background-color);
  color: var(--text-color);
  border: 1px solid var(--highlight-color);
  border-radius: 4px;
  cursor: text;
}

.copy-button {
  background-color: var(--element-color-1);
  border: none;
  color: var(--light-text);
  padding: 0.5em 1em;
  border-radius: 4px;
  cursor: pointer;
}

.copy-button:hover {
  background-color: var(--element-color-2);
}

.copy-status-message {
  color: var(--gold-color);
  font-weight: bold;
  margin-top: 10px;
}
</style>
