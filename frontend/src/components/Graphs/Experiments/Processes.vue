<template>
    <div class="process-game-container">
        <div class="game-header">
            <h1 class="game-title">Process Master: Krebs Cycle</h1>
            <div class="progress-bar">
                <div 
                    class="progress-fill" 
                    :style="{ width: `${(currentStep / totalSteps) * 100}%` }"
                ></div>
            </div>
            <div class="score-board">
                <span class="score">Score: {{ score }}</span>
                <span class="streak">🔥 {{ streak }}</span>
            </div>
        </div>

        <div v-if="gameState === 'playing'" class="game-content">
            <div class="step-card">
                <div class="step-number">Step {{ currentStep }}</div>
                <div class="input-section">
                    <div class="input-group">
                        <label>Process Name:</label>
                        <input 
                            v-model="userAnswers.name" 
                            @keyup.enter="checkAnswer"
                            placeholder="Enter the name of this step..."
                            class="answer-input"
                        />
                    </div>
                    <div class="input-group">
                        <label>Description:</label>
                        <textarea 
                            v-model="userAnswers.description" 
                            @keyup.ctrl.enter="checkAnswer"
                            placeholder="Describe what happens in this step..."
                            class="answer-textarea"
                            rows="4"
                        ></textarea>
                    </div>
                </div>
                <button @click="checkAnswer" class="submit-btn" :disabled="!canSubmit">
                    Submit Answer
                </button>
            </div>

            <div v-if="showFeedback" class="feedback-section">
                <div class="correct-answer">
                    <h3>Correct Answer:</h3>
                    <div class="answer-card">
                        <strong>{{ currentProcessStep.name }}</strong>
                        <p>{{ currentProcessStep.description }}</p>
                    </div>
                </div>
                <button @click="nextStep" class="next-btn">Next Step →</button>
            </div>
        </div>

        <div v-if="gameState === 'completed'" class="completion-screen">
            <div class="completion-header">
                <h2>Process Complete!</h2>
                <div class="final-score">
                    <div class="score-circle">
                        <span class="score-number">{{ Math.round((score / (totalSteps * 100)) * 100) }}%</span>
                        <span class="score-label">Accuracy</span>
                    </div>
                </div>
            </div>

            <div class="comparison-section">
                <h3>How You Compare</h3>
                <div class="comparison-stats">
                    <div class="stat-card">
                        <div class="stat-value">{{ averageAccuracy }}%</div>
                        <div class="stat-label">Library Average</div>
                    </div>
                    <div class="stat-card highlight">
                        <div class="stat-value">{{ userRanking }}</div>
                        <div class="stat-label">Your Ranking</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ totalAttempts }}</div>
                        <div class="stat-label">Total Attempts</div>
                    </div>
                </div>
            </div>

            <div class="leaderboard">
                <h4>Top Responses</h4>
                <div class="response-list">
                    <div 
                        v-for="(response, index) in topResponses" 
                        :key="index"
                        class="response-item"
                    >
                        <div class="response-rank">{{ index + 1 }}</div>
                        <div class="response-content">
                            <div class="response-name">{{ response.stepName }}</div>
                            <div class="response-desc">{{ response.description }}</div>
                            <div class="response-meta">
                                <span class="response-user">by {{ response.username }}</span>
                                <span class="response-score">{{ response.accuracy }}%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="action-buttons">
                <button @click="restartGame" class="restart-btn">Play Again</button>
                <button @click="shareResults" class="share-btn">Share Results</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface ProcessStep {
    name: string
    description: string
}

interface UserAnswers {
    name: string
    description: string
}

interface TopResponse {
    stepName: string
    description: string
    username: string
    accuracy: number
}

type GameState = 'playing' | 'completed'

// Reactive state
const gameState = ref<GameState>('playing')
const currentStep = ref<number>(1)
const score = ref<number>(0)
const streak = ref<number>(0)
const showFeedback = ref<boolean>(false)
const userAnswers = ref<UserAnswers>({
    name: '',
    description: ''
})

const krebsSteps: ProcessStep[] = [
    {
        name: 'Acetyl-CoA Formation',
        description: 'Pyruvate is converted to acetyl-CoA by pyruvate dehydrogenase complex, releasing CO2 and NADH'
    },
    {
        name: 'Citrate Formation',
        description: 'Acetyl-CoA combines with oxaloacetate to form citrate, catalyzed by citrate synthase'
    },
    // {
    //     name: 'Isocitrate Formation',
    //     description: 'Citrate is rearranged to isocitrate through cis-aconitate intermediate by aconitase'
    // },
    // {
    //     name: 'α-Ketoglutarate Formation',
    //     description: 'Isocitrate is oxidized to α-ketoglutarate by isocitrate dehydrogenase, producing NADH and CO2'
    // },
    // {
    //     name: 'Succinyl-CoA Formation',
    //     description: 'α-ketoglutarate is converted to succinyl-CoA by α-ketoglutarate dehydrogenase, producing NADH and CO2'
    // },
    // {
    //     name: 'Succinate Formation',
    //     description: 'Succinyl-CoA is converted to succinate by succinate thiokinase, generating GTP (or ATP)'
    // },
    // {
    //     name: 'Fumarate Formation',
    //     description: 'Succinate is oxidized to fumarate by succinate dehydrogenase, producing FADH2'
    // },
    // {
    //     name: 'Malate Formation',
    //     description: 'Fumarate is hydrated to malate by fumarase enzyme'
    // },
    // {
    //     name: 'Oxaloacetate Regeneration',
    //     description: 'Malate is oxidized to oxaloacetate by malate dehydrogenase, producing NADH and completing the cycle'
    // }
]

// Mock comparison data
const averageAccuracy = ref<number>(78)
const userRanking = ref<string>('12th')
const totalAttempts = ref<number>(156)
const topResponses = ref<TopResponse[]>([
    {
        stepName: 'Citrate Formation',
        description: 'Acetyl-CoA joins with oxaloacetate forming citrate via citrate synthase in the first committed step',
        username: 'BioChem_Master',
        accuracy: 95
    },
    {
        stepName: 'Isocitrate Formation', 
        description: 'Citrate undergoes isomerization to isocitrate through aconitase enzyme action',
        username: 'StudyGuru_23',
        accuracy: 92
    },
    {
        stepName: 'α-Ketoglutarate Formation',
        description: 'Isocitrate oxidation produces first NADH and CO2 while forming α-ketoglutarate',
        username: 'MedStudent_Pro',
        accuracy: 89
    }
])

// Computed properties
const totalSteps = computed<number>(() => krebsSteps.length)

const currentProcessStep = computed<ProcessStep>(() => {
    return krebsSteps[currentStep.value - 1]
})

const canSubmit = computed<boolean>(() => {
    return userAnswers.value.name.trim() !== '' && userAnswers.value.description.trim() !== ''
})

// Methods
const checkAnswer = (): void => {
    if (!canSubmit.value) return
    
    const correctStep = currentProcessStep.value
    const nameScore = calculateSimilarity(userAnswers.value.name, correctStep.name)
    const descScore = calculateSimilarity(userAnswers.value.description, correctStep.description)
    const stepScore = Math.round((nameScore + descScore) / 2)
    
    score.value += stepScore
    
    if (stepScore >= 80) {
        streak.value++
    } else {
        streak.value = 0
    }
    
    showFeedback.value = true
}

const calculateSimilarity = (answer: string, correct: string): number => {
    // Simple similarity calculation - replace with more sophisticated algorithm
    const answerWords = answer.toLowerCase().split(' ')
    const correctWords = correct.toLowerCase().split(' ')
    let matches = 0
    
    answerWords.forEach(word => {
        if (correctWords.some(cWord => cWord.includes(word) || word.includes(cWord))) {
            matches++
        }
    })
    
    return Math.min(100, (matches / correctWords.length) * 100)
}

const nextStep = (): void => {
    if (currentStep.value >= totalSteps.value) {
        gameState.value = 'completed'
    } else {
        currentStep.value++
        userAnswers.value = { name: '', description: '' }
        showFeedback.value = false
    }
}

const restartGame = (): void => {
    gameState.value = 'playing'
    currentStep.value = 1
    score.value = 0
    streak.value = 0
    showFeedback.value = false
    userAnswers.value = { name: '', description: '' }
}

const shareResults = (): void => {
    // Share functionality
    console.log('Sharing results...')
}
</script>


<style scoped>
.process-game-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    font-family: 'Inter', sans-serif;
}

.game-header {
    text-align: center;
    margin-bottom: 30px;
}

.game-title {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 20px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.progress-bar {
    background: rgba(255,255,255,0.2);
    height: 8px;
    border-radius: 4px;
    margin: 20px auto;
    max-width: 400px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    transition: width 0.3s ease;
}

.score-board {
    display: flex;
    justify-content: center;
    gap: 30px;
    color: white;
    font-size: 1.2rem;
    font-weight: 600;
}

.game-content {
    max-width: 800px;
    margin: 0 auto;
}

.step-card {
    background: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    margin-bottom: 30px;
}

.step-number {
    font-size: 1.5rem;
    font-weight: 700;
    color: #667eea;
    text-align: center;
    margin-bottom: 30px;
}

.input-group {
    margin-bottom: 25px;
}

.input-group label {
    display: block;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
}

.answer-input, .answer-textarea {
    width: 100%;
    padding: 15px;
    border: 2px solid #e1e5e9;
    border-radius: 12px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

.answer-input:focus, .answer-textarea:focus {
    outline: none;
    border-color: #667eea;
}

.submit-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease;
    display: block;
    margin: 0 auto;
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
}

.submit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.feedback-section {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

.answer-card {
    background: #f8fffe;
    border-left: 4px solid #4ade80;
    padding: 20px;
    border-radius: 8px;
    margin: 15px 0;
}

.next-btn {
    background: #4ade80;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    float: right;
}

.completion-screen {
    max-width: 900px;
    margin: 0 auto;
    background: white;
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.1);
}

.completion-header {
    text-align: center;
    margin-bottom: 40px;
}

.score-circle {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    color: white;
    margin: 20px 0;
}

.score-number {
    font-size: 2rem;
    font-weight: 700;
}

.score-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

.comparison-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.stat-card {
    text-align: center;
    padding: 20px;
    background: #f8fafc;
    border-radius: 16px;
}

.stat-card.highlight {
    background: linear-gradient(135deg, #667eea20, #764ba220);
    border: 2px solid #667eea;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #667eea;
}

.leaderboard {
    margin: 40px 0;
}

.response-list {
    space-y: 15px;
}

.response-item {
    display: flex;
    gap: 15px;
    padding: 20px;
    background: #f8fafc;
    border-radius: 12px;
    margin-bottom: 15px;
}

.response-rank {
    font-size: 1.5rem;
    font-weight: 700;
    color: #667eea;
    min-width: 30px;
}

.response-content {
    flex: 1;
}

.response-name {
    font-weight: 600;
    color: #333;
    margin-bottom: 5px;
}

.response-desc {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 10px;
}

.response-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #888;
}

.action-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-top: 40px;
}

.restart-btn, .share-btn {
    padding: 15px 30px;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.restart-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
}

.share-btn {
    background: white;
    color: #667eea;
    border: 2px solid #667eea;
}

.restart-btn:hover, .share-btn:hover {
    transform: translateY(-2px);
}
</style>