<template>
    <div class="brain-dump-container">
        <div class="fixed top-20 left-12 flex gap-6 z-10">
            <button @click="back"
                class="menu-button bg-background-color-1t backdrop-blur-sm shadow-md rounded-lg p-4 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200"
                style="color: var(--highlight-color);">
                <ArrowLeftIcon class="w-6 h-6" />
            </button>
        </div>
        <!-- Game Area -->
        <div v-if="!gameEnded" class="game-area">
            <BrainDumpConcepts />
        </div>

        <!-- Results Screen -->
        <div v-else class="results-screen">
            <h1>Time's Up!</h1>
            <h2>Your Brain Dump for: {{ centralConcept }}</h2>

            <div class="results-summary">
                <p><strong>Concepts Added:</strong> {{ totalConcepts }}</p>
                <p><strong>Parent Concepts:</strong> {{ userNodes.length }}</p>
                <p><strong>Child Concepts:</strong> {{ totalChildConcepts }}</p>
                <p><strong>Total Words:</strong> {{ totalWords }}</p>
            </div>

            <div class="concepts-list">
                <div v-for="node in userNodes" :key="node.id" class="concept-card">
                    <h3>{{ node.title || 'Untitled Concept' }}</h3>
                    <p>{{ node.content || 'No content added' }}</p>
                    
                    <div v-if="node.children && node.children.length > 0" class="child-concepts">
                        <h4>Sub-concepts:</h4>
                        <div v-for="child in node.children" :key="child.id" class="child-concept-card">
                            <h5>{{ child.title || 'Untitled Sub-concept' }}</h5>
                            <p>{{ child.content || 'No content added' }}</p>
                        </div>
                    </div>
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
import BrainDumpConcepts from '@/components/Graphs/Experiments/BrainDumpConcepts.vue';
import { useRoute, useRouter } from 'vue-router'
import { showExperimentsToast } from '@/utils/toasts';
import axios from 'axios';

interface ChildNode {
    id: number
    title: string
    content: string
}

interface UserNode {
    id: number
    title: string
    content: string
    x: number
    y: number
    children: ChildNode[]
}

// Game state
const centralConcept = ref<string>('Statistics')
const timeLeft = ref<number>(5) // 3 minutes in seconds
const gameEnded = ref<boolean>(false)
const userNodes = ref<UserNode[]>([])
const nodeIdCounter = ref<number>(1)
const childIdCounter = ref<number>(1)
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
        
        const childWords = node.children.reduce((childTotal, child) => {
            const childTitleWords = child.title.trim().split(/\s+/).filter(word => word.length > 0).length
            const childContentWords = child.content.trim().split(/\s+/).filter(word => word.length > 0).length
            return childTotal + childTitleWords + childContentWords
        }, 0)
        
        return total + titleWords + contentWords + childWords
    }, 0)
})

const totalConcepts = computed(() => {
    return userNodes.value.length + totalChildConcepts.value
})

const totalChildConcepts = computed(() => {
    return userNodes.value.reduce((total, node) => total + node.children.length, 0)
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
        y: 70 + (10 * userNodes.value.length),
        children: []
    }

    userNodes.value.push(newNode)
}

const addChildNode = (parentId: number): void => {
    if (gameEnded.value) return

    const parentNode = userNodes.value.find(node => node.id === parentId)
    if (!parentNode) return

    const newChild: ChildNode = {
        id: childIdCounter.value++,
        title: '',
        content: ''
    }

    parentNode.children.push(newChild)
}

const updateChildNode = (parentId: number, childId: number, field: keyof ChildNode, value: string): void => {
    const parentNode = userNodes.value.find(node => node.id === parentId)
    if (!parentNode) return

    const childNode = parentNode.children.find(child => child.id === childId)
    if (childNode && (field === 'title' || field === 'content')) {
        childNode[field] = value
    }
}

const removeChildNode = (parentId: number, childId: number): void => {
    const parentNode = userNodes.value.find(node => node.id === parentId)
    if (!parentNode) return

    const childIndex = parentNode.children.findIndex(child => child.id === childId)
    if (childIndex > -1) {
        parentNode.children.splice(childIndex, 1)
    }
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
.game-area {
    position: relative;
    min-height: 600px;
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
.child-concepts {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #e0e0e0;
}
.child-concepts h4 {
    margin: 0 0 10px 0;
    color: #555;
    font-size: 1rem;
}
.child-concept-card {
    background: #f8f9fa;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 8px;
    border-left: 3px solid #667eea;
}
.child-concept-card h5 {
    margin: 0 0 6px 0;
    color: #333;
    font-size: 0.9rem;
}
.child-concept-card p {
    margin: 0;
    font-size: 0.85rem;
    color: #666;
    line-height: 1.4;
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

</style>