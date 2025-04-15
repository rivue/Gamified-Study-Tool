<template>
    <div class="game-window">
        <!-- <GameStart /> -->
        <FactoidComponent />
        <LibraryQuestion />
    </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
// import GameStart from './GameStart.vue';
import FactoidComponent from "./FactoidComponent.vue";
import LibraryQuestion from "./LibraryQuestion.vue";
import { useRoute } from 'vue-router';
import { useGameStore } from "@/store/gameStore";
import { usePopupStore } from "@/store/popupStore";
import axios from 'axios';

const route = useRoute();
const gameStore = useGameStore();
const loading = ref(true);
const abortController = new AbortController();

onMounted(async () => {
    const libraryId = route.params.id;
    const roomName = route.params.roomName;
    try {
        await gameStore.fetchLibraryDetails(libraryId, roomName);
        if (!abortController.signal.aborted && !gameStore.libraryError) {
            gameStore.startGame();
        }
    } catch (error) {
        if (!axios.isCancel(error)) {
            console.error("Error fetching library details:", error);
        }
        const popupStore = usePopupStore();
        if (error instanceof Error) {
            popupStore.showPopup(error.message);
        } else {
            popupStore.showPopup("Game Window Failed. Please try again.");
        }
    } finally {
        if (!abortController.signal.aborted) {
            loading.value = false;
        }
    }
});


// Add onUnmounted hook
onUnmounted(() => {
    console.log("GameWindow unmounting, aborting fetch.");
    abortController.abort(); // Abort the request
});
</script>

<style scoped>
.game-window {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}
</style>
