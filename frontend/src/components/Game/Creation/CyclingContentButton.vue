<template>
    <div
      class="cycling-content-button"
      :class="{ loading: props.options.length === 0 }"
    >
      <button @click="prevOption" class="arrow-button left-arrow">
        &#x25C0;
      </button>
  
      <button @click="() => navigateToContent(content as string)" class="content-display">
        <div v-if="loadedOptions" class="content-name">
          {{ contentWithoutEmoji }}
        </div>
        <div v-else class="content-name">Loading...</div>
        <span v-if="hasContentEmoji" class="emoji-indicator">
          {{ extractedEmoji }}
        </span>
      </button>
  
      <button @click="nextOption" class="arrow-button right-arrow">
        &#x25B6;
      </button>
    </div>
  </template>


<script setup lang="ts">
import { ref, computed, defineProps, defineEmits } from 'vue';

const props = defineProps<{ options: string[]; showType?: boolean }>();
const emit = defineEmits<{
  (e: 'navigate', value: string): void;
}>();

const currentIndex = ref(0);

const loadedOptions = computed(() => props.options.length > 0);
const content = computed(() => props.options[currentIndex.value]);

const hasContentEmoji = computed(() => {
  if (!content.value) return false;
  const emojiRegex = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;
  return emojiRegex.test(content.value);
});

const extractedEmoji = computed(() => {
  if (!content.value) return '';
  const match = content.value.match(
    /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u
  );
  return match ? match[0] : '';
});

const contentWithoutEmoji = computed(() => {
  if (!content.value) return '';
  return content.value.replace(extractedEmoji.value, '').trim();
});

function navigateToContent(role: string) {
  emit('navigate', role);
}

function nextOption() {
  if (currentIndex.value < props.options.length - 1) {
    currentIndex.value++;
  } else {
    currentIndex.value = 0;
  }
}

function prevOption() {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  } else {
    currentIndex.value = props.options.length - 1;
  }
}
</script>

<style scoped>
.cycling-content-button {
  display: flex;
  align-items: center;
  justify-content: center;
}

.arrow-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  padding: 0 10px;
}

.content-display {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  background: var(--element-color-1);
  border: 2px solid var(--background-color-1t);
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  transition: border-color 0.3s ease;
  position: relative;
}

.loading .content-display {
  opacity: 0.5; /* Adjust opacity for loading state */
}

.content-name {
  padding: 8px;
  font-weight: 700;
}

.emoji-indicator {
  font-size: 1.5rem;
}

.completed-button {
  opacity: 0.6;
  position: relative;
}

.completed-button::after {
  content: "✓";
  color: #50c878;
  font-weight: bold;
  font-size: 1.2rem;
  position: absolute;
  right: 10px;
  top: 70%;
  transform: translateY(-50%);
}
</style>
