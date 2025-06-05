<template>
    <div class="brain-dump-container">
        <div class="fixed top-20 left-12 flex gap-6 z-10">
            <button @click="back"
                class="menu-button bg-background-color-1t backdrop-blur-sm shadow-md rounded-lg p-4 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200"
                style="color: var(--highlight-color);">
                <ArrowLeftIcon class="w-6 h-6" />
            </button>
        </div>
        
        <!-- Timer and Add Node Button Container -->
        <div class="timer-add-container">
            <div class="timer-container">
                <div class="timer" :class="{ 'timer-warning': timeLeft <= 30, 'timer-danger': timeLeft <= 10 }">
                    {{ formatTime(timeLeft) }}
                </div>
            </div>
            
            <!-- Add Node Button - updated styling -->
            <button v-if="!gameEnded" @click="addNode" 
                class="menu-button bg-background-color-1t backdrop-blur-sm shadow-md rounded-lg p-4 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200"
                style="color: var(--highlight-color);"
                :disabled="gameEnded">
                + Add Concept
            </button>
        </div>

        <!-- Game Area -->
        <div v-if="!gameEnded" class="game-area">
            <!-- Central Concept Node -->
            <div class="central-node p-8">
                <h2>{{ centralConcept }}</h2>
            </div>

            <!-- User Nodes -->
            <div v-for="node in userNodes" :key="node.id" class="user-node"
                :class="{ 'dragging': draggedNodeId === node.id }" :style="{ left: node.x + 'px', top: node.y + 'px' }"
                @mousedown="startDrag($event, node.id)">
                <div class="node-header drag-handle">
                    <input v-model="node.title" placeholder="Concept title..." class="node-title-input"
                        @input="updateNode(node.id, 'title', $event.target.value)" @mousedown.stop />
                    <button @click="removeNode(node.id)" class="remove-btn" @mousedown.stop>×</button>
                </div>
                <textarea v-model="node.content"
                    placeholder="Recall as much detailed information you know about this concept"
                    class="node-content-textarea" @input="updateNode(node.id, 'content', $event.target.value)"
                    @mousedown.stop></textarea>
            </div>
        </div>

        <!-- Results Screen -->
        <div v-else class="results-screen">
            <h1>Time's Up!</h1>
            <h2>Your Brain Dump for: {{ centralConcept }}</h2>

            <div class="results-summary">
                <p><strong>Concepts Added:</strong> {{ userNodes.length }}</p>
                <p><strong>Total Words:</strong> {{ totalWords }}</p>
            </div>

            <div class="concepts-list">
                <div v-for="node in userNodes" :key="node.id" class="concept-card">
                    <h3>{{ node.title || 'Untitled Concept' }}</h3>
                    <p>{{ node.content || 'No content added' }}</p>
                </div>
            </div>

            <div class="action-buttons">
                <button @click="restartGame" class="restart-btn">Try Again</button>
                <button @click="shareResults" class="share-btn">Share with Friends</button>
            </div>
        </div>
    </div>
</template>


<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ArrowLeftIcon } from '@heroicons/vue/24/solid';
import { useRoute, useRouter } from 'vue-router'
import { showExperimentsToast } from '@/utils/toasts';
import axios from 'axios';

interface UserNode {
    id: number
    title: string
    content: string
    x: number
    y: number
}

// Game state
const centralConcept = ref<string>('Statistics')
const timeLeft = ref<number>(180) // 3 minutes in seconds
const gameEnded = ref<boolean>(false)
const userNodes = ref<UserNode[]>([])
const nodeIdCounter = ref<number>(1)
let gameTimer: NodeJS.Timeout | null = null
const route = useRoute();
const params = ref(route.params);
const router = useRouter();
const abortController = new AbortController();

// Drag state
const draggedNodeId = ref<number | null>(null)
const dragOffset = ref<{ x: number, y: number }>({ x: 0, y: 0 })

function capitalizeWords(str: string | null | undefined): string {
    if (!str) return str || ''; // Handle null or undefined input
    return str.replace(/(^|\s|[-])\S/g, match => match.toUpperCase()).replace(/-/g, ' ');
}

const totalWords = computed(() => {
    return userNodes.value.reduce((total, node) => {
        const titleWords = node.title.trim().split(/\s+/).filter(word => word.length > 0).length
        const contentWords = node.content.trim().split(/\s+/).filter(word => word.length > 0).length
        return total + titleWords + contentWords
    }, 0)
})

const fetchLibraryInfo = async (): Promise<void> => {

    try {

        const response = await axios.get(`/api/library/${params.value.id}`, {
            signal: abortController.signal
        });
        if (response.data && response.data.data && response.data.data.library_topic) {
            centralConcept.value = capitalizeWords(response.data.data.library_topic);

        } else {
            router.back();
            showExperimentsToast();
        }

    } catch (error: any) {
        router.back();
        showExperimentsToast();
    } 

};

const back = () => {
    // Navigate back to the previous page
    router.push(`/lessons/${params.value.id}/experiments`)
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
    gameEnded.value = true
    if (gameTimer) {
        clearInterval(gameTimer)
        gameTimer = null
    }
}

const addNode = (): void => {
    if (gameEnded.value) return

    const newNode: UserNode = {
        id: nodeIdCounter.value++,
        title: '',
        content: '',
        x: -100 + (10 * userNodes.value.length),
        y: 70 + (10 * userNodes.value.length)
    }

    userNodes.value.push(newNode)
}

const removeNode = (nodeId: number): void => {
    const index = userNodes.value.findIndex(node => node.id === nodeId)
    if (index > -1) {
        userNodes.value.splice(index, 1)
    }
}

const updateNode = (nodeId: number, field: keyof UserNode, value: string): void => {
    const node = userNodes.value.find(n => n.id === nodeId)
    if (node && (field === 'title' || field === 'content')) {
        node[field] = value
    }
}

// Drag functionality
const startDrag = (event: MouseEvent, nodeId: number): void => {
    if (gameEnded.value) return

    const node = userNodes.value.find(n => n.id === nodeId)
    if (!node) return

    draggedNodeId.value = nodeId
    dragOffset.value = {
        x: event.clientX - node.x,
        y: event.clientY - node.y
    }

    document.addEventListener('mousemove', onMouseMove)
    document.addEventListener('mouseup', onMouseUp)

    // Prevent text selection while dragging
    event.preventDefault()
}

const onMouseMove = (event: MouseEvent): void => {
    if (draggedNodeId.value === null) return

    const node = userNodes.value.find(n => n.id === draggedNodeId.value)
    if (!node) return

    node.x = event.clientX - dragOffset.value.x
    node.y = event.clientY - dragOffset.value.y

    // Keep nodes within reasonable bounds
    node.x = Math.max(Math.min(node.x, window.innerWidth + 270), Math.min(node.x, window.innerWidth - 270))
    node.y = Math.max(0, Math.min(node.y, window.innerHeight - 200))
}

const onMouseUp = (): void => {
    draggedNodeId.value = null
    dragOffset.value = { x: 0, y: 0 }

    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
}

const restartGame = (): void => {
    timeLeft.value = 180
    gameEnded.value = false
    userNodes.value = []
    nodeIdCounter.value = 1
    startTimer()
}

const shareResults = (): void => {
    const resultsText = `I just completed a Brain Dump on "${centralConcept.value}"! 
Added ${userNodes.value.length} concepts with ${totalWords.value} total words in 3 minutes! 🧠💪`

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
    startTimer()
    fetchLibraryInfo();
})

onUnmounted(() => {
    abortController.abort()
    if (gameTimer) {
        clearInterval(gameTimer)
    }
    // Clean up event listeners
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
})

</script>

<style scoped>
.brain-dump-container {
    /* min-height: 100vh; */
    /* background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); */
    padding: 20px;
    font-family: 'Arial', sans-serif;
}

.timer-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.timer {
    background: white;
    padding: 15px 30px;
    border-radius: 25px;
    font-size: 2rem;
    font-weight: bold;
    color: #333;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.timer-warning {
    background: #fff3cd;
    color: #856404;
}

.timer-danger {
    background: #f8d7da;
    color: #721c24;
    animation: pulse 1s infinite;
}

@keyframes pulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.05);
    }

    100% {
        transform: scale(1);
    }
}

.game-area {
    position: relative;
    min-height: 600px;
}

.central-node {
    position: absolute;
    top: 50%;
    left: -25%;
    /* transform: translate(-50%, -50%); */
    background: white;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    z-index: 10;
}

.central-node h2 {
    margin: 0;
    color: #333;
    font-size: 1.8rem;
    text-align: center;
}

.user-node {
    position: absolute;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    /* width: 250px; */
    z-index: 5;
    cursor: move;
    transition: box-shadow 0.2s ease;
}

.user-node:hover {
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.user-node.dragging {
    z-index: 15;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    transform: rotate(2deg);
}

.node-header {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    color: black;
}

.drag-handle {
    cursor: move;
}

.node-title-input {
    flex: 1;
    padding: 8px;
    border: 1px solid black;
    border-radius: 6px;
    font-weight: bold;
    cursor: text;
}

.remove-btn {
    background: #ff4757;
    color: white;
    border: none;
    border-radius: 50%;
    width: 25px;
    height: 25px;
    cursor: pointer;
    font-size: 16px;
}

.node-content-textarea {
    /* width: 100%; */
    min-height: 90px;
    padding: 8px;
    border: 1px solid black;
    border-radius: 6px;
    resize: vertical;
    font-family: inherit;
    color: black;
    cursor: text;
}

.add-node-btn {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: #4CAF50;
    color: white;
    border: none;
    padding: 15px 25px;
    border-radius: 25px;
    font-size: 1.1rem;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease;
}

.add-node-btn:hover {
    transform: translateY(-2px);
}

.add-node-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.results-screen {
    text-align: center;
    color: white;
    max-width: 800px;
    margin: 0 auto;
}

.results-screen h1 {
    font-size: 3rem;
    margin-bottom: 10px;
}

.results-screen h2 {
    font-size: 1.5rem;
    margin-bottom: 30px;
}

.results-summary {
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 30px;
    backdrop-filter: blur(10px);
}

.results-summary p {
    font-size: 1.2rem;
    margin: 10px 0;
}

.concepts-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.concept-card {
    background: white;
    color: #333;
    padding: 20px;
    border-radius: 12px;
    text-align: left;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.concept-card h3 {
    margin: 0 0 10px 0;
    color: #667eea;
}

.concept-card p {
    margin: 0;
    line-height: 1.5;
}

.action-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
}

.restart-btn,
.share-btn {
    padding: 15px 30px;
    border: none;
    border-radius: 25px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.restart-btn {
    background: #4CAF50;
    color: white;
}

.share-btn {
    background: #2196F3;
    color: white;
}

.restart-btn:hover,
.share-btn:hover {
    transform: translateY(-2px);
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