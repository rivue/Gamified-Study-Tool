<!-- Factoid.vue -->
<template>
    <transition name="factoid-fade">
        <div v-if="factoidVisible != null && factoidText" class="factoid-overlay" @click="flipFactoid">
            <div class="factoid-modal">
                <div class="factoid-content">
                    <p v-html="factoidText"></p>
                </div>
            </div>
        </div>
    </transition>
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
    let formatted = raw.replace(/\*\*([^*]*?)\*\*/g, "<strong>$1</strong>");

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
/* Fade transition from top */
.factoid-fade-enter-active,
.factoid-fade-leave-active {
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.factoid-fade-enter-from {
    opacity: 0;
    transform: translateY(-50px);
}

.factoid-fade-leave-to {
    opacity: 0;
    transform: translateY(-50px);
}

.factoid-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    z-index: 120; /* Higher than LibraryQuestion's z-index of 110 */
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(10px);
}

.factoid-modal {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(20px);
    max-width: 80%;
    max-height: 80%;
    overflow-y: auto;
    position: relative;
}

.factoid-content {
    padding: 2rem;
    text-align: left;
    font-size: 1.2em;
    color: var(--highlight-color);
    line-height: 1.6;
}

.factoid-content p {
    margin: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .factoid-modal {
        max-width: 90%;
        max-height: 85%;
    }
    
    .factoid-content {
        padding: 1.5rem;
        font-size: 1.1em;
    }
}

@media (max-width: 480px) {
    .factoid-modal {
        max-width: 95%;
        max-height: 90%;
    }
    
    .factoid-content {
        padding: 1rem;
        font-size: 1em;
    }
}
</style>
