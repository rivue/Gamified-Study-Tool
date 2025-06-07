<template>
    <div class="fact-sprint-container">
        <!-- Header -->
        <div class="game-header">
            <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${(score / 20) * 100}%` }"></div>
            </div>
            <div class="score-display">
                <span class="score">{{ score }}/20</span>
                <span class="streak" v-if="streak > 1">🔥 {{ streak }}</span>
            </div>
        </div>

        <!-- Game State: Playing -->
        <div v-if="gameState === 'playing'" class="game-content">
            <div class="question-card">
                <div class="question-number">Question {{ score + 1 }}</div>
                <h2 class="question-text">{{ currentQuestion.question }}</h2>
                
                <div class="answer-section">
                    <input 
                        v-model="userAnswer" 
                        @keyup.enter="submitAnswer"
                        @input="clearFeedback"
                        class="answer-input"
                        :class="{ 'correct': feedbackType === 'correct', 'incorrect': feedbackType === 'incorrect' }"
                        placeholder="Type your answer..."
                        :disabled="showingFeedback"
                        ref="answerInput"
                    />
                    
                    <button 
                        @click="submitAnswer" 
                        class="submit-btn"
                        :disabled="!userAnswer.trim() || showingFeedback"
                    >
                        Submit
                    </button>
                </div>

                <!-- Feedback -->
                <div v-if="showingFeedback" class="feedback" :class="feedbackType">
                    <div class="feedback-icon">
                        {{ feedbackType === 'correct' ? '✅' : '❌' }}
                    </div>
                    <div class="feedback-text">
                        {{ feedbackMessage }}
                    </div>
                    <div v-if="feedbackType === 'correct'" class="points-earned">
                        +{{ pointsEarned }} points
                    </div>
                </div>
            </div>

            <div class="timer-section">
                <div class="timer-circle">
                    <svg class="timer-svg" viewBox="0 0 100 100">
                        <circle 
                            class="timer-bg" 
                            cx="50" 
                            cy="50" 
                            r="45"
                        />
                        <circle 
                            class="timer-progress" 
                            cx="50" 
                            cy="50" 
                            r="45"
                            :stroke-dasharray="circumference"
                            :stroke-dashoffset="timerOffset"
                        />
                    </svg>
                    <div class="timer-text">{{ timeLeft }}s</div>
                </div>
            </div>
        </div>

        <!-- Game State: Finished -->
        <div v-if="gameState === 'finished'" class="game-results">
            <div class="results-card">
                <h2 class="results-title">🎉 Game Complete!</h2>
                <div class="final-score">
                    <span class="score-label">Final Score</span>
                    <span class="score-value">{{ totalPoints }}</span>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-value">{{ score }}</span>
                        <span class="stat-label">Correct</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">{{ maxStreak }}</span>
                        <span class="stat-label">Best Streak</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">{{ averageTime.toFixed(1) }}s</span>
                        <span class="stat-label">Avg Time</span>
                    </div>
                </div>

                <!-- Comparison with others -->
                <div class="comparison-section">
                    <h3>How you compared:</h3>
                    <div class="comparison-bars">
                        <div v-for="comparison in comparisons" :key="comparison.label" class="comparison-item">
                            <span class="comparison-label">{{ comparison.label }}</span>
                            <div class="comparison-bar">
                                <div class="comparison-fill" :style="{ width: `${comparison.percentage}%` }"></div>
                                <span class="comparison-value">{{ comparison.value }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <button @click="restartGame" class="restart-btn">
                    Play Again
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

interface Question {
    question: string
    answer: string
    category: string
}

interface Comparison {
    label: string
    value: number
    percentage: number
}

type GameState = 'playing' | 'finished'
type FeedbackType = 'correct' | 'incorrect' | ''

// Reactive state
const gameState = ref<GameState>('playing')
const score = ref(0)
const streak = ref(0)
const maxStreak = ref(0)
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const showingFeedback = ref(false)
const feedbackType = ref<FeedbackType>('')
const feedbackMessage = ref('')
const pointsEarned = ref(0)
const totalPoints = ref(0)
const timeLeft = ref(15)
const timer = ref<NodeJS.Timeout | null>(null)
const responseTimes = ref<number[]>([])
const startTime = ref<number | null>(null)
const answerInput = ref<HTMLInputElement>()

// Mock questions data
const questions = ref<Question[]>([
    { question: "What year did World War II end?", answer: "1945", category: "History" },
    { question: "What is the speed of light in vacuum (m/s)?", answer: "299792458", category: "Physics" },
    { question: "What is the capital of Australia?", answer: "Canberra", category: "Geography" },
    { question: "Who wrote 'Romeo and Juliet'?", answer: "Shakespeare", category: "Literature" },
    { question: "What is the atomic number of Carbon?", answer: "6", category: "Chemistry" },
    { question: "In what year was the iPhone first released?", answer: "2007", category: "Technology" },
    { question: "What is the largest planet in our solar system?", answer: "Jupiter", category: "Astronomy" },
    { question: "What is 15 × 7?", answer: "105", category: "Math" },
    { question: "What is the chemical symbol for Gold?", answer: "Au", category: "Chemistry" },
    { question: "Who painted the Mona Lisa?", answer: "Leonardo da Vinci", category: "Art" },
    { question: "What is the square root of 144?", answer: "12", category: "Math" },
    { question: "What year did the Berlin Wall fall?", answer: "1989", category: "History" },
    { question: "What is the hardest natural substance?", answer: "Diamond", category: "Science" },
    { question: "What is the smallest prime number?", answer: "2", category: "Math" },
    { question: "What gas makes up about 78% of Earth's atmosphere?", answer: "Nitrogen", category: "Science" },
    { question: "Who invented the telephone?", answer: "Alexander Graham Bell", category: "History" },
    { question: "What is the currency of Japan?", answer: "Yen", category: "Geography" },
    { question: "What is H2O commonly known as?", answer: "Water", category: "Chemistry" },
    { question: "How many continents are there?", answer: "7", category: "Geography" },
    { question: "What is the boiling point of water in Celsius?", answer: "100", category: "Science" }
])

// Mock comparison data
const comparisons = ref<Comparison[]>([
    { label: "Your Score", value: 0, percentage: 0 },
    { label: "Library Average", value: 12, percentage: 60 },
    { label: "Top Player", value: 18, percentage: 90 }
])

// Computed properties
const currentQuestion = computed((): Question => {
    return questions.value[currentQuestionIndex.value] || {} as Question
})

const circumference = computed((): number => {
    return 2 * Math.PI * 45
})

const timerOffset = computed((): number => {
    return circumference.value - (timeLeft.value / 15) * circumference.value
})

const averageTime = computed((): number => {
    return responseTimes.value.length > 0 
        ? responseTimes.value.reduce((a, b) => a + b, 0) / responseTimes.value.length 
        : 0
})

// Methods
const startTimer = (): void => {
    timeLeft.value = 15
    startTime.value = Date.now()
    timer.value = setInterval(() => {
        timeLeft.value--
        if (timeLeft.value <= 0) {
            handleTimeout()
        }
    }, 1000)
}

const submitAnswer = (): void => {
    if (!userAnswer.value.trim() || showingFeedback.value) return
    
    if (timer.value) {
        clearInterval(timer.value)
    }
    const responseTime = (Date.now() - (startTime.value || 0)) / 1000
    responseTimes.value.push(responseTime)
    
    const isCorrect = userAnswer.value.toLowerCase().trim() === 
        currentQuestion.value.answer.toLowerCase().trim()
    
    if (isCorrect) {
        handleCorrectAnswer(responseTime)
    } else {
        handleIncorrectAnswer()
    }
    
    showFeedback()
}

const handleCorrectAnswer = (responseTime: number): void => {
    score.value++
    streak.value++
    maxStreak.value = Math.max(maxStreak.value, streak.value)
    
    // Calculate points based on speed and streak
    const speedBonus = Math.max(0, 15 - responseTime) * 10
    const streakBonus = streak.value * 50
    pointsEarned.value = Math.round(100 + speedBonus + streakBonus)
    totalPoints.value += pointsEarned.value
    
    feedbackType.value = 'correct'
    feedbackMessage.value = responseTime < 5 ? 'Lightning fast! ⚡' : 'Correct!'
}

const handleIncorrectAnswer = (): void => {
    streak.value = 0
    pointsEarned.value = 0
    feedbackType.value = 'incorrect'
    feedbackMessage.value = `Correct answer: ${currentQuestion.value.answer}`
}

const handleTimeout = (): void => {
    streak.value = 0
    pointsEarned.value = 0
    feedbackType.value = 'incorrect'
    feedbackMessage.value = `Time's up! Answer: ${currentQuestion.value.answer}`
    showFeedback()
}

const showFeedback = (): void => {
    showingFeedback.value = true
    setTimeout(() => {
        nextQuestion()
    }, 2000)
}

const clearFeedback = (): void => {
    showingFeedback.value = false
    feedbackType.value = ''
}

const nextQuestion = (): void => {
    if (score.value >= 20 || currentQuestionIndex.value >= questions.value.length - 1) {
        endGame()
        return
    }
    
    currentQuestionIndex.value++
    userAnswer.value = ''
    showingFeedback.value = false
    feedbackType.value = ''
    startTimer()
    
    nextTick(() => {
        answerInput.value?.focus()
    })
}

const endGame = (): void => {
    gameState.value = 'finished'
    // Update comparison data
    comparisons.value[0].value = score.value
    comparisons.value[0].percentage = (score.value / 20) * 100
}

const restartGame = (): void => {
    gameState.value = 'playing'
    score.value = 0
    streak.value = 0
    maxStreak.value = 0
    currentQuestionIndex.value = 0
    userAnswer.value = ''
    totalPoints.value = 0
    responseTimes.value = []
    startTimer()
    
    nextTick(() => {
        answerInput.value?.focus()
    })
}

// Lifecycle hooks
onMounted(() => {
    startTimer()
    nextTick(() => {
        answerInput.value?.focus()
    })
})

onUnmounted(() => {
    if (timer.value) {
        clearInterval(timer.value)
    }
})
</script>

<style scoped>
/* Keep the existing styles unchanged */
.fact-sprint-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.game-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.progress-bar {
    flex: 1;
    height: 8px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    margin-right: 20px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4CAF50, #8BC34A);
    border-radius: 4px;
    transition: width 0.3s ease;
}

.score-display {
    display: flex;
    align-items: center;
    gap: 15px;
    color: white;
    font-weight: 600;
}

.score {
    font-size: 1.5em;
}

.streak {
    font-size: 1.2em;
    animation: pulse 1s infinite;
}

.game-content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 30px;
    align-items: start;
}

.question-card {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.question-number {
    color: #666;
    font-size: 0.9em;
    margin-bottom: 10px;
}

.question-text {
    font-size: 1.5em;
    margin-bottom: 30px;
    color: #333;
    line-height: 1.4;
}

.answer-section {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
}

.answer-input {
    flex: 1;
    padding: 15px 20px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    font-size: 1.1em;
    transition: all 0.3s ease;
}

.answer-input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.answer-input.correct {
    border-color: #4CAF50;
    background: #f8fff8;
}

.answer-input.incorrect {
    border-color: #f44336;
    background: #fff8f8;
}

.submit-btn {
    padding: 15px 25px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
}

.submit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.feedback {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 20px;
    border-radius: 10px;
    font-weight: 600;
    animation: slideUp 0.3s ease;
}

.feedback.correct {
    background: #e8f5e8;
    color: #2e7d32;
}

.feedback.incorrect {
    background: #ffebee;
    color: #c62828;
}

.feedback-icon {
    font-size: 1.5em;
}

.points-earned {
    margin-left: auto;
    font-size: 1.2em;
    color: #4CAF50;
}

.timer-section {
    display: flex;
    justify-content: center;
}

.timer-circle {
    position: relative;
    width: 120px;
    height: 120px;
}

.timer-svg {
    width: 100%;
    height: 100%;
    transform: rotate(-90deg);
}

.timer-bg {
    fill: none;
    stroke: rgba(255, 255, 255, 0.2);
    stroke-width: 8;
}

.timer-progress {
    fill: none;
    stroke: #fff;
    stroke-width: 8;
    stroke-linecap: round;
    transition: stroke-dashoffset 1s linear;
}

.timer-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 1.5em;
    font-weight: 600;
}

.game-results {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 60vh;
}

.results-card {
    background: white;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    max-width: 500px;
    width: 100%;
}

.results-title {
    font-size: 2em;
    margin-bottom: 30px;
    color: #333;
}

.final-score {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
}

.score-label {
    color: #666;
    font-size: 1.1em;
}

.score-value {
    font-size: 3em;
    font-weight: 700;
    color: #667eea;
    margin-top: 10px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 30px;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
}

.stat-value {
    font-size: 1.8em;
    font-weight: 600;
    color: #333;
}

.stat-label {
    color: #666;
    font-size: 0.9em;
    margin-top: 5px;
}

.comparison-section {
    margin: 30px 0;
    text-align: left;
}

.comparison-section h3 {
    margin-bottom: 20px;
    color: #333;
}

.comparison-item {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
}

.comparison-label {
    width: 100px;
    font-size: 0.9em;
    color: #666;
}

.comparison-bar {
    flex: 1;
    height: 30px;
    background: #e0e0e0;
    border-radius: 15px;
    position: relative;
    overflow: hidden;
}

.comparison-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 15px;
    transition: width 1s ease;
}

.comparison-value {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: white;
    font-weight: 600;
    font-size: 0.9em;
}

.restart-btn {
    padding: 15px 30px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1em;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.restart-btn:hover {
    transform: translateY(-2px);
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 768px) {
    .game-content {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .answer-section {
        flex-direction: column;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
</style>