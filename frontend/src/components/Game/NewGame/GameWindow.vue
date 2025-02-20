<template>
    <div class="game-window">
        <GameStart />
        <FactoidComponent />
        <LibraryQuestion />
    </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import GameStart from './GameStart.vue';
import FactoidComponent from "./FactoidComponent.vue";
import LibraryQuestion from "./LibraryQuestion.vue";
import { useRoute, useRouter } from 'vue-router';
import { useGameStore } from "@/store/gameStore";

export default {
    name: 'GameWindow',
    components: {
        GameStart,
        FactoidComponent,
        LibraryQuestion,
    },
    setup() {
        const route = useRoute();
        const router = useRouter();
        const gameStore = useGameStore();
        const loading = ref(true);

        onMounted(async () => {
            const libraryId = route.params.id;
            const roomName = route.params.roomName;
            try {
                // Wait for the async action to finish
                await gameStore.fetchLibraryDetails(libraryId, roomName);

            } catch (error) {
                console.error("Error fetching library details:", error);
                router.push(`/knowledge/${libraryId}`);

            } finally {
                loading.value = false;  // Stop loading when the action is complete
            }

            if (gameStore.libraryError) {
                // If there was an error, navigate away
                router.push(`/knowledge/${libraryId}`);
            }
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
