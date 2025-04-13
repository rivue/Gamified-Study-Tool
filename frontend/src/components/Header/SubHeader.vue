<!-- SubHeader.vue -->
<template>
  <transition name="slide-fade">
    <div v-if="show" class="subheading-container">
      <div class="subheading-bar">
        <div class="bar-element">{{ subheading }}</div>
        <div class="bar-element" @click="navToPlans">☁️{{ discovery }}</div>
      </div>
      <div class="progress-bar" :style="{ width: progressBarWidth }"></div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { useMessageStore } from "@/store/messageStore";
import { useAuthStore } from "@/store/authStore";
import { useRoute, useRouter } from "vue-router";
import { computed } from "vue";

const messageStore = useMessageStore();
const authStore = useAuthStore();
const route = useRoute();
const router = useRouter();

const discovery = computed(() => authStore.cloudTokens);
const subheading = computed(() => messageStore.subheading);
const progressBarWidth = computed(() => `${messageStore.progress * 100}%`);

const show = computed(() => {
  return (
    subheading.value &&
    subheading.value.trim() !== "" &&
    route.path.startsWith("/lesson")
  );
});

function navToPlans() {
  router.push("/plan");
}
</script>

<style scoped>
.subheading-container {
  text-align: center;
  font-size: 14px;
  color: var(--text-color);
  background-color: #0000001a;
  backdrop-filter: blur(8px);
  padding: 5px 0;
  position: relative;
}

.subheading-bar{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  background-color: var(--element-color-1);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: opacity 0.5s;
}
.slide-fade-enter,
.slide-fade-leave-to {
  opacity: 0;
}

.bar-element {
  margin: 0 0.5em;
}
</style>
