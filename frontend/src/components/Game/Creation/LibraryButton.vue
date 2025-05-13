<template>
  <button class="library-button" @click="goToLibrary()" :style="{ backgroundImage: 'url(' + library.image_url + ')' }">
    <div class="info-overlay">
      <div class="top-info">
        <div class="library-topic">{{ library.library_topic }}</div>
      </div>
    </div>
  </button>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
asdf line7 - form-group topic-selection
const props = defineProps<{
    library: { id: number, library_topic: string, image_url: string };
}>();

const router = useRouter()
function goToLibrary() {
  router.push(`/lessons/${props.library.id}`);
}
</script>

<style scoped>
.library-button {
  position: relative;
  flex-shrink: 0;
  margin: 5px;
  padding: 0.5em;
  background-size: cover;
  background-position: center;
  width: 240px;
  height: 240px;
  border: none;
  cursor: pointer;
  overflow: hidden;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.library-button:hover {
  transform: scale(1.05);
}

.info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.274);
  color: rgba(255, 255, 255, 0.685);
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  transition: all ease 0.3s;
}

.info-overlay:hover {
  background: rgba(0, 0, 0, 0.6);
  color: white;

}

.top-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.library-topic, .difficulty, .likes, .clicks, .language, .language_difficulty {
    text-align: left;
  padding: 5px;
  font-size: 0.9em;
}

.library-topic{
  color: white;
  /* color: var(--text-color); */
}

.stats, .language-info {
  font-size: 0.8em;
}

</style>
