<template>
  <transition name="fade">
    <div v-if="completionVisible" class="completion-overlay">
      <div v-if="firstPage" class="pre-completion-content">
        <div class="celebratory-message">🎉 Congratulations! 🎉</div>
        <!-- <UserStats /> -->
          <!-- <div class="time-spent">Final time: {{ formattedTime }}s</div> -->
        <div class="cta-container">
          <CtaButton
            buttonText="Back To Map"
            @click="nextPage"
            :isSubmitting="isSubmitting"
          />
        </div>
      </div>
      <div v-else class="completion-content">
        <div class="suggestions-container">
          <div>{{ loading ? "Loading..." : "Continue with..." }}</div>
          <CyclingContentButton
            :options="suggestions"
            :role="someRole"
            :content_type="someContentType"
            :showType="false"
            @navigate="startSuggestion"
            class="suggestion-button"
          />
        </div>
        <div class="cta-container" v-if="!showLeaderBoard">
          <CtaButton
            buttonText="Show Leaderboard"
            @click="toggleLeaderBoard"
            :isSubmitting="isSubmitting"
          />
        </div>
        <div v-if="loggedIn" class="what-next-container">
          <div class="nav-row">
            <button class="nav-button" @click="navigateLibrary">🏛 New</button>
            <div class="separator">|</div>
            <!-- <button
              class="nav-button"
              @click="navigateExplore"
              :disabled="exploreLoading"
            > -->
              <!-- {{ exploreLoading ? "⏳Loading" : "🔍Suggest again" }}
            </button> -->
            <div class="separator">|</div>
            <button class="nav-button" @click="navigateMap">🗺️Map</button>
          </div>

          <div class="nav-row">
            <button class="nav-button" @click="navigateBack">🔙Back</button>
            <div class="separator">|</div>
            <button class="feedback-button" @click="toggleFeedback">
              {{ showFeedback ? "Hide Feedback⬆️" : "Feedback⤵️" }}
            </button>
          </div>
        </div>

        <div class="rating-feedback">
          <div v-show="showFeedback" class="feedback-form">
            <p>Rate your experience:</p>
            <div class="stars">
              <span
                v-for="n in 5"
                :key="n"
                class="star"
                @click="setRating(n)"
                :class="{ selected: n <= rating }"
              >
                ★
              </span>
            </div>
            <br />

            <textarea
              v-model="feedback"
              placeholder="Enter your feedback here..."
            ></textarea>
            <button
              :disabled="!isValid || isSubmitted"
              @click="submitFeedback"
              class="submit-btn"
            >
              {{ isSubmitted ? "Thank You" : "Submit" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore } from "@/store/authStore";
// import { useMessageStore } from "@/store/messageStore";
import { useGameStore } from "@/store/gameStore";
import { useUserStatsStore } from "@/store/userStatsStore";
import CyclingContentButton from "../Creation/CyclingContentButton.vue";
import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";
import LeaderBoard from "../LeaderBoard.vue";

const router = useRouter();
const route = useRoute();
const gameStore = useGameStore();
// const messageStore = useMessageStore();
const authStore = useAuthStore();
const userStatsStore = useUserStatsStore();

const page = ref(0);
const rating = ref(0);
const feedback = ref("");
const showFeedback = ref(false);
const isSubmitted = ref(false);
const suggestions = ref<string[]>([]);
const exploreLoading = ref(false);
const loading = ref(false);
const showLeaderBoard = ref(false);

const completionVisible = computed(() => gameStore.completed);
const isValid = computed(() => rating.value > 0 || feedback.value.trim().length > 0);
const loggedIn = computed(() => authStore.loggedIn);
const firstPage = computed(() => page.value === 0);
// const formattedTime = computed(() => gameStore.formattedTime());

function toggleLeaderBoard() {
  showLeaderBoard.value = true;
}

async function nextPage() {
    userStatsStore.resetStats(); // triggers fetchStreak in TopBar
    router.push(`/lessons/${gameStore.libraryId}`);
    page.value = 1;
}

function navigateLibrary() {
  router.push("/library");
}

function navigateBack() {
  gameStore.fetchLibraryDetails(gameStore.libraryId, gameStore.libraryTopic);
}

async function startSuggestion(suggestion: string) {
  if (loading.value) return;
  loading.value = true;

  try {
    const libraryResponse = await axios.post("/api/library/generate", {
      topic: suggestion,
    });
    const libraryId = libraryResponse.data.library_data.id;
    loading.value = false;
    router.push(`/lessons/${libraryId}`);
  } catch (error) {
    loading.value = false;
  }
}

function navigateMap() {
  router.push("/knowledge?node=" + gameStore.roomNames[12]);
}

function toggleFeedback() {
  showFeedback.value = !showFeedback.value;
}

function setRating(n: number) {
  rating.value = n;
}

function submitFeedback() {
  const sanitizeInput = (input: string) => {
    const div = document.createElement("div");
    div.textContent = input;
    return div.innerHTML;
  };

  const sanitizedMessage = sanitizeInput(feedback.value);
  const payload = new FormData();
  payload.append("message", sanitizedMessage);
  payload.append("rating", rating.value.toString());

  const routeParts = route.path.split("/");
  if (routeParts.length >= 2) {
    payload.append(
      routeParts[routeParts.length - 2],
      routeParts[routeParts.length - 1]
    );
  }

  axios
    .post("/api/feedback", payload)
    .then((response) => {
      const popupStore = usePopupStore();
      if (
        response.data &&
        response.data.message &&
        response.data.feedback_id
      ) {
        popupStore.showPopup(
          `${response.data.message} Your feedback ID is ${response.data.feedback_id}.`
        );
      } else {
        popupStore.showPopup("Feedback submitted.");
      }
      isSubmitted.value = true;
    })
    .catch((error) => {
      const popupStore = usePopupStore();
      let message = "An error occurred while submitting feedback.";
      if (
        error.response &&
        error.response.data &&
        error.response.data.error
      ) {
        message = error.response.data.error;
      }
      popupStore.showPopup(message);
    });
}

function resetFeedbackForm() {
  rating.value = 0;
  feedback.value = "";
  showFeedback.value = false;
}

watch(completionVisible, (newValue) => {
  if (newValue) {
    // this.navigateExplore();
  }
});
</script>

<style scoped>
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

.completion-content {
  background-color: transparent;
  color: var(--text-color);
  border-radius: 8px;
  padding: 2rem;
  max-width: 700px;
  text-align: center;
}

.celebratory-message {
  text-align: center;
  padding: 0.5em;
  box-shadow: 0 0 16px 16px var(--background-color-1t);
  border-radius: 16px;
  color: var(--text-color);
  font-weight: bold;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  font-size: 1.5em;
}

.what-next-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2em;
  font-weight: 700;
  opacity: 0.8;
  transition: opacity 2s;
}

.nav-row {
  display: flex;
  justify-content: center;
  margin-bottom: 5px;
}

.share-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.share-link-input {
  color: var(--text-color);
  background: var(--background-color);
  border: 1px solid var(--text-color);
  padding: 0.5rem;
  margin-right: 0.5rem;
}

.copy-button {
  background-color: var(--element-color-1);
  color: var(--text-color);
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.copy-button:hover {
  background-color: #5c2d91;
}

.stars {
  display: inline-block;
  margin-bottom: 1rem;
}

.star {
  cursor: pointer;
  color: var(--text-color);
  font-size: 1.5rem;
  transition: color 0.2s ease-in-out;
}

.star:hover,
.star.selected {
  color: #ffc107;
}

.next-button,
.share-button,
.feedback-button {
  padding: 4px;
  font-weight: 700;
  color: var(--text-color);
  transition: color 0.2s;
}

.next-button {
  font-weight: 700;
}

.next-button:hover,
.share-button:hover,
.feedback-button:hover {
  color: var(--highlight-color);
}

.feedback-form {
  background-color: var(--background-color);
  margin-top: 0.5rem;
  padding: 0.5rem;
  border: 1px solid var(--text-color);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.rating-feedback {
  padding-top: 0.5em;
}

.rating-feedback textarea {
  background-color: var(--background-color);
  color: var(--text-color);
  display: block;
  width: calc(100% - 1rem);
  height: 5rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}

.submit-btn {
  background-color: var(--element-color-1);
  color: var(--text-color);
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background-color 0.2s ease-in-out;
}

.submit-btn:disabled {
  background-color: #696969;
  cursor: default;
}

.submit-btn:hover:not(:disabled) {
  background-color: #5c2d91;
}

.separator {
  padding-left: 4px;
  padding-right: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.suggestions-container {
  padding-top: 1em;
  padding-bottom: 1em;
  display: flex;
  flex-direction: column;
}

.suggestion-button {
  margin: 2px;
}

.pre-completion-content {
  background-color: var(--background-color);
  color: var(--text-color);
  border-radius: 8px;
  padding: 2rem;
  max-width: 600px;
  width: 100%;
  box-sizing: border-box;
}

.time-spent {  font-size: 1.2rem;
  text-align: center;
  margin: 1em;
}

.completion-status {
  font-size: 1.2rem;
}
</style>
