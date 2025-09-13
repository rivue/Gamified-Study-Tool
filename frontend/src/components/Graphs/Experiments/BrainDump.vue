<template>
    <div class="brain-dump-container">
        <div class="fixed top-4 left-4 flex gap-6 z-10 h-12">
            <button
                @click="back"
                class="menu-button bg-background-color-1t backdrop-blur-sm shadow-md rounded-lg px-4 flex items-center gap-2 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200"
                style="color: var(--highlight-color);">
                <ArrowLeftIcon class="w-5 h-5" />
                <span>Back</span>
            </button>
        </div>

        <!-- Timer Display -->
        <div v-if="!gameEnded" class="timer-display">
            <div class="timer-card">
                <span class="timer-value">{{ formatTime(timeLeft) }}</span>
            </div>
        </div>

        <!-- Game Area -->
        <div v-if="!gameEnded && centralConcept" class="game-area">
            <BrainDumpConcepts ref="brainDumpRef" :title="centralConcept"/>
        </div>

        <!-- Results Screen -->
        <div v-else class="results-screen">
            <div class="results-container">
                <div class="results-header">
                    <h1 class="results-title">Time's Up!</h1>
                    <h2 class="results-subtitle">Your Brain Dump for: {{ centralConcept }}</h2>
                </div>

                <div class="results-summary">
                    <div class="summary-stats">
                        <div class="stat-card">
                            <span class="stat-number">{{ totalConcepts }}</span>
                            <span class="stat-label">Total Concepts</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{{ conceptsData.length }}</span>
                            <span class="stat-label">Main Concepts</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{{ totalChildConcepts }}</span>
                            <span class="stat-label">Child Concepts</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{{ totalWords }}</span>
                            <span class="stat-label">Total Words</span>
                        </div>
                       
                    </div>
                </div>

                <div class="concepts-display">
                    <h3 class="concepts-display-title">Your Concepts:</h3>
                    
                    <div v-if="conceptsData.length === 0" class="no-concepts">
                        <p>No concepts were added during this session.</p>
                    </div>

                    <div v-else class="concepts-grid">
                        <div v-for="(concept, index) in conceptsData" :key="index" class="concept-result-card">
                            <div class="concept-header">
                                <h4 class="concept-title">
                                    {{ concept.concept || 'Untitled Concept' }}
                                </h4>
                            </div>
                            
                            <div v-if="concept.description" class="concept-description">
                                <p>{{ concept.description }}</p>
                            </div>

                            <div v-if="concept.childConcepts && concept.childConcepts.length > 0" class="child-concepts-section">
                                <h5 class="child-concepts-header">Child Concepts:</h5>
                                <div class="child-concepts-grid">
                                    <div v-for="(child, childIndex) in concept.childConcepts" 
                                         :key="childIndex" 
                                         class="child-concept-card">
                                        <h6 class="child-concept-title">
                                            {{ child.name || 'Untitled' }}
                                        </h6>
                                        <p v-if="child.description" class="child-concept-description">
                                            {{ child.description }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="action-buttons">
                    <button @click="restartGame" class="action-btn restart-btn">
                        <span>Try Again</span>
                    </button>
                    <button @click="shareResults" class="action-btn share-btn">
                        <span>Share Results</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ArrowLeftIcon, ArrowPathIcon, ShareIcon } from '@heroicons/vue/24/solid'
import BrainDumpConcepts from '@/components/Graphs/Experiments/BrainDumpConcepts.vue';
import { useRoute, useRouter } from 'vue-router'
import { showExperimentsToast } from '@/utils/toasts';
import axios from 'axios';

interface ChildConcept {
    name: string;
    description?: string;
}

interface Concept {
    concept: string;
    description: string;
    childConcepts: ChildConcept[];
    collapsed: boolean;
}

// Game state
const centralConcept = ref<string | null>(null)
const timeLeft = ref<number>(180) // 3 minutes in seconds
const gameEnded = ref<boolean>(false)
const brainDumpRef = ref<InstanceType<typeof BrainDumpConcepts> | null>(null)
const conceptsData = ref<Concept[]>([])
let gameTimer: NodeJS.Timeout | null = null
const route = useRoute();
const params = ref(route.params);
const router = useRouter();
const abortController = new AbortController();

function capitalizeWords(str: string | null | undefined): string {
    if (!str) return str || ''; // Handle null or undefined input
    return str.replace(/(^|\s|[-])\S/g, match => match.toUpperCase()).replace(/-/g, ' ');
}

const totalWords = computed(() => {
    return conceptsData.value.reduce((total, concept) => {
        const conceptWords = (concept.concept || '').trim().split(/\s+/).filter(word => word.length > 0).length
        const descriptionWords = (concept.description || '').trim().split(/\s+/).filter(word => word.length > 0).length
        
        const childWords = concept.childConcepts.reduce((childTotal, child) => {
            const childNameWords = (child.name || '').trim().split(/\s+/).filter(word => word.length > 0).length
            const childDescWords = (child.description || '').trim().split(/\s+/).filter(word => word.length > 0).length
            return childTotal + childNameWords + childDescWords
        }, 0)
        
        return total + conceptWords + descriptionWords + childWords
    }, 0)
})

const totalConcepts = computed(() => {
    return conceptsData.value.length + totalChildConcepts.value
})

const totalChildConcepts = computed(() => {
    return conceptsData.value.reduce((total, concept) => total + concept.childConcepts.length, 0)
})


const fetchLibraryInfo = async (): Promise<void> => {
    try {
        const response = await axios.get(`/api/library/${route.params.id}`, {
            signal: abortController.signal
        });
        if (response.data?.data?.library_topic) {
            centralConcept.value = capitalizeWords(response.data.data.library_topic);
        } else {
            router.back();
            showExperimentsToast();
        }
    } catch (error) {
        router.back();
        showExperimentsToast();
    }
};

const back = () => {
    router.push(`/lessons/${params.value.id}`)
}

// Methods
const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
}

const startTimer = (): void => {
    gameTimer = setInterval(() => {
        if (timeLeft.value > 0) {
            timeLeft.value--
        } else {
            endGame()
        }
    }, 1000)
}

const endGame = (): void => {
    // Capture data from BrainDumpConcepts component
    if (brainDumpRef.value && brainDumpRef.value.concepts) {
        conceptsData.value = [...brainDumpRef.value.concepts]
    }
    
    gameEnded.value = true
    if (gameTimer) {
        clearInterval(gameTimer)
        gameTimer = null
    }
}

const restartGame = (): void => {
    timeLeft.value = 180
    gameEnded.value = false
    conceptsData.value = []
    startTimer()
}

const shareResults = (): void => {
    const resultsText = `I just completed a Brain Dump on "${centralConcept.value}"! 
Added ${totalConcepts.value} concepts with ${totalWords.value} total words in 3 minutes! 🧠💪`

    if (navigator.share) {
        navigator.share({
            title: 'Brain Dump Results',
            text: resultsText
        })
    } else {
        navigator.clipboard.writeText(resultsText)
        alert('Results copied to clipboard!')
    }
}

// Lifecycle
onMounted(() => {
    fetchLibraryInfo().then(() => {
        if (!centralConcept.value) {
            router.back();
            showExperimentsToast();
        }
    });
    startTimer();
    
})

onUnmounted(() => {
    abortController.abort()
    if (gameTimer) {
        clearInterval(gameTimer)
    }
})

</script>

<style scoped>
.brain-dump-container {
    padding: 20px;
    font-family: 'Arial', sans-serif;
    min-height: 100vh;
}

.game-area {
    position: relative;
    padding-top: 80px; /* Add space for timer */
}

.timer-display {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 10;
}

.timer-card {
    background: var(--background-color-1);
    border: 1px solid var(--color-primary);
    border-radius: 12px;
    padding: 0.5rem 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px); /* Adds a translucent effect */
    /* background: rgba(255, 255, 255, 0.6); Semi-transparent white background */
}

.timer-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--color-primary);
}

.results-screen {
    padding: 2rem 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.results-container {
    max-width: 1000px;
    width: 100%;
    margin: 0 auto;
}


.results-header {
    text-align: center;
    margin-bottom: 3rem;
}

.results-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--text-color);
    margin-bottom: 0.5rem;
}

.results-subtitle {
    font-size: 1.25rem;
    color: var(--text-color-secondary);
    margin: 0;
}

.results-summary {
    background: var(--background-color-1);
    border: 1px solid rgba(26, 139, 127, 0.2);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 3rem;
}

.summary-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.5rem;
}

.stat-card {
    text-align: center;
    padding: 1rem;
    background: rgba(26, 139, 127, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(26, 139, 127, 0.1);
}

.stat-number {
    display: block;
    font-size: 2rem;
    font-weight: bold;
    color: var(--color-primary);
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 0.875rem;
    color: var(--text-color-secondary);
    font-weight: 500;
}

.concepts-display {
    margin-bottom: 3rem;
}

.concepts-display-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--text-color);
    margin-bottom: 1.5rem;
    text-align: center;
}

.no-concepts {
    text-align: center;
    padding: 3rem;
    color: var(--text-color-secondary);
    font-style: italic;
}

.concepts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 1.5rem;
}

.concept-result-card {
    background: var(--background-color-1);
    border: 1px solid rgba(26, 139, 127, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
}

.concept-header {
    margin-bottom: 1rem;
}

.concept-title {
    font-size: 1.25rem;
    font-weight: bold;
    color: var(--color-primary);
    margin: 0;
}

.concept-description {
    margin-bottom: 1.5rem;
}

.concept-description p {
    color: var(--text-color);
    line-height: 1.6;
    margin: 0;
}

.child-concepts-section {
    border-top: 1px solid rgba(26, 139, 127, 0.2);
    padding-top: 1rem;
}

.child-concepts-header {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-color);
    margin: 0 0 1rem 0;
}

.child-concepts-grid {
    display: grid;
    gap: 0.75rem;
}

.child-concept-card {
    background: rgba(26, 139, 127, 0.05);
    border: 1px solid rgba(26, 139, 127, 0.15);
    border-radius: 8px;
    padding: 1rem;
}

.child-concept-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-color);
    margin: 0 0 0.5rem 0;
}

.child-concept-description {
    font-size: 0.875rem;
    color: var(--text-color-secondary);
    line-height: 1.5;
    margin: 0;
}

.action-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

.action-btn {
    padding: 1rem 2rem;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.restart-btn {
    background: var(--color-primary);
    color: white;
}

.share-btn {
    background: var(--text-color-secondary);
    color: white;
}

.action-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.menu-button {
    border-radius: 10px;
    background-color: var(--background-color-1t);
    color: var(--highlight-color);
    border: 1px solid var(--color-primary-dark);
    transition: all 0.2s ease;
}

.menu-button:hover {
    background-color: var(--element-color-1);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.menu-button:active {
    transform: translateY(0);
}

.menu-button.selected {
    background-color: var(--element-color-1);
    border-color: var(--color-primary);
    color: var(--light-text);
}
</style>