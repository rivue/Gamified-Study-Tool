<!-- Factoid.vue -->
<template>
    <div v-if="factoidVisible != null && factoidText" class="factoid-overlay" @click="flipFactoid">
        <div class="factoid-box">
            <div class="factoid-content">
                <p v-html="factoidText"></p>
            </div>
        </div>
    </div>
</template>


<script setup lang="ts">
import { computed, watch, onMounted } from 'vue';
import { useGameStore } from '@/store/gameStore';

const gameStore = useGameStore();

const factoidVisible = computed(() => gameStore.factoidVisible);

const factoidText = computed(() => {

    if (gameStore.factoidVisible == null) {
        return null;
    }

    let raw = gameStore.factoids[gameStore.factoidVisible]?.factoid_text || 'No factoid text'
    // Bold
    let formatted  = raw.replace(/\*\*([^*]*?)\*\*/g, "<strong>$1</strong>");

    // Italics
    formatted = formatted.replace(/_([^_]*?)_|\*([^*]*?)\*/g, "<em>$1$2</em>");
    return formatted;
});

function flipFactoid() {
    gameStore.toggleFactoid();
}

onMounted(() => {
    watch(() => gameStore.factoidVisible, () => {
    }, { immediate: true });
});
</script>

<style scoped>
.factoid-overlay {
    position: absolute;
    height: 82%;
    aspect-ratio: 1 / 1;
    max-width: 100%;
    z-index: 110;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.factoid-box {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 96%;
}

.factoid-content {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: left;
    padding: 1em;
    z-index: 111;
    font-size: 1.2em;
    background-color: var(--background-haze);
    box-shadow: 0 16px 16px var(--background-color-2t), 0 -16px 16px var(--background-color-2t);
}
</style>
