<template>
    <div class="game-window">
        <!-- <GameStart /> -->
        <FactoidComponent />
        <LibraryQuestion />
    </div>
</template>

<script>
import { onMounted, onUnmounted, ref } from 'vue';
// import GameStart from './GameStart.vue';
import FactoidComponent from "./FactoidComponent.vue";
import LibraryQuestion from "./LibraryQuestion.vue";
import { useRoute } from 'vue-router';
import { useGameStore } from "@/store/gameStore";
import { usePopupStore } from "@/store/popupStore";
import axios from 'axios';

export default {
    name: 'GameWindow',
    components: {
        // GameStart,
        FactoidComponent,
        LibraryQuestion,
    },

    setup() {
        const route = useRoute();
        // const router = useRouter();
        const gameStore = useGameStore();
        const loading = ref(true);
        const abortController = new AbortController();

        onMounted(async () => {
            const libraryId = route.params.id;
            const roomName = route.params.roomName;
            try {
                
                await gameStore.fetchLibraryDetails(libraryId, roomName, abortController.signal);
                // Check if the library data is valid
                if (!abortController.signal.aborted && !gameStore.libraryError) {
                    gameStore.startGame();
                 } else if (gameStore.libraryError) {
                    // Optional: handle error even if aborted, or just let finally handle loading
                 }

            } catch (error) {
                if (!axios.isCancel(error)) {
                    console.error("Error fetching library details:", error);
                }
                
                const popupStore = usePopupStore();
                popupStore.showPopup(error.message || "Game Window Failed. Please try again.");

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

        return { loading };
    }
};
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
