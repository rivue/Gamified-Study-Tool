<template>
    <transition name="modal-fade">
        <div class="modal-backdrop" @click.self="close" role="dialog" aria-modal="true" :aria-label="`Quiz for ${materialName}`">
            <div class="modal-container" ref="container">
                <header class="modal-header">
                    <div class="quiz-info">
                        <h2 class="modal-title">
                            <span class="title-accent"></span>
                            {{ title }}: {{ materialName }}
                        </h2>
                        <div class="quiz-stats">
                            <span class="stat">{{ questions.length }} Questions</span>
                            <span class="stat">Score: {{ score }}/{{ answeredQuestions }}</span>
                        </div>
                    </div>
                    <button @click="close" class="close-button" aria-label="Close quiz">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </header>

                <!-- Progress Bar -->
                <div class="progress-section">
                    <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
                    </div>
                    <span class="progress-text">{{ currentQuestionIndex + 1 }} of {{ questions.length }}</span>
                </div>

                <main class="modal-body" v-if="!showResults">
                    <div class="question-container">
                        <div class="question-header">
                            <span class="question-number">Question {{ currentQuestionIndex + 1 }}</span>
                            <span class="question-type">{{ currentQuestion.type }}</span>
                        </div>
                        
                        <h3 class="question-text">{{ currentQuestion.question }}</h3>
                        
                        <!-- Multiple Choice -->
                        <div v-if="currentQuestion.type === 'Multiple Choice'" class="options-container">
                            <button 
                                v-for="(option, index) in currentQuestion.options" 
                                :key="index"
                                @click="selectAnswer(option)"
                                :class="['option-button', { 
                                    'selected': selectedAnswer === option,
                                    'correct': showAnswer && option === currentQuestion.correct,
                                    'incorrect': showAnswer && selectedAnswer === option && option !== currentQuestion.correct
                                }]"
                                :disabled="showAnswer"
                            >
                                <span class="option-letter">{{ String.fromCharCode(65 + index) }}</span>
                                <span class="option-text">{{ option }}</span>
                            </button>
                        </div>

                        <!-- True/False -->
                        <div v-else-if="currentQuestion.type === 'True/False'" class="tf-container">
                            <button 
                                @click="selectAnswer('True')"
                                :class="['tf-button', 'true-button', { 
                                    'selected': selectedAnswer === 'True',
                                    'correct': showAnswer && currentQuestion.correct === 'True',
                                    'incorrect': showAnswer && selectedAnswer === 'True' && currentQuestion.correct !== 'True'
                                }]"
                                :disabled="showAnswer"
                            >
                                <CheckIcon class="w-6 h-6" />
                                <span>True</span>
                            </button>
                            <button 
                                @click="selectAnswer('False')"
                                :class="['tf-button', 'false-button', { 
                                    'selected': selectedAnswer === 'False',
                                    'correct': showAnswer && currentQuestion.correct === 'False',
                                    'incorrect': showAnswer && selectedAnswer === 'False' && currentQuestion.correct !== 'False'
                                }]"
                                :disabled="showAnswer"
                            >
                                <XMarkIcon class="w-6 h-6" />
                                <span>False</span>
                            </button>
                        </div>

                        <!-- Short Answer -->
                        <div v-else-if="currentQuestion.type === 'Short Answer'" class="short-answer-container">
                            <textarea 
                                v-model="selectedAnswer"
                                :disabled="showAnswer"
                                class="answer-textarea"
                                placeholder="Type your answer here..."
                                rows="4"
                            ></textarea>
                            <div v-if="showAnswer" class="correct-answer">
                                <strong>Sample Answer:</strong> {{ currentQuestion.correct }}
                            </div>
                        </div>

                        <!-- Answer Explanation -->
                        <div v-if="showAnswer" class="explanation-container">
                            <h4>Explanation:</h4>
                            <p>{{ currentQuestion.explanation }}</p>
                        </div>
                    </div>
                </main>

                <!-- Results Screen -->
                <main v-else class="modal-body results-body">
                    <div class="results-container">
                        <div class="results-header">
                            <div class="score-circle">
                                <span class="score-percentage">{{ Math.round((score / questions.length) * 100) }}%</span>
                                <span class="score-label">Score</span>
                            </div>
                            <h3 class="results-title">Quiz Complete!</h3>
                            <p class="results-subtitle">{{ getScoreMessage() }}</p>
                        </div>

                        <div class="results-stats">
                            <div class="stat-item">
                                <span class="stat-value">{{ score }}</span>
                                <span class="stat-label">Correct</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-value">{{ questions.length - score }}</span>
                                <span class="stat-label">Incorrect</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-value">{{ questions.length }}</span>
                                <span class="stat-label">Total</span>
                            </div>
                        </div>

                        <div class="question-review">
                            <h4>Question Review</h4>
                            <div class="review-list">
                                <div 
                                    v-for="(question, index) in questions" 
                                    :key="index"
                                    :class="['review-item', { 'correct': userAnswers[index] === question.correct }]"
                                >
                                    <span class="review-number">{{ index + 1 }}</span>
                                    <span class="review-question">{{ question.question.substring(0, 50) }}...</span>
                                    <span class="review-status">
                                        <CheckIcon v-if="userAnswers[index] === question.correct" class="w-5 h-5 text-green-400" />
                                        <XMarkIcon v-else class="w-5 h-5 text-red-400" />
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>

                <footer class="modal-footer">
                    <button v-if="!showResults" @click="submitAnswer" :disabled="!selectedAnswer" class="button-secondary">
                        <span v-if="!showAnswer">Submit Answer</span>
                        <span v-else-if="currentQuestionIndex < questions.length - 1">Next Question</span>
                        <span v-else>View Results</span>
                    </button>
                    <div v-else class="results-actions">
                        <button @click="retakeQuiz" class="button-secondary">
                            <ArrowPathIcon class="w-5 h-5" />
                            <span>Retake Quiz</span>
                        </button>
                        <button @click="close" class="button-secondary">
                            <span>Close</span>
                        </button>
                    </div>
                </footer>
            </div>
        </div>
    </transition>
</template>

<script setup>
import { defineProps, defineEmits, onMounted, ref, computed } from 'vue';
import { CheckIcon, XMarkIcon, ArrowPathIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
    materialName: { type: String, required: true },
    // Optional: pass in pre-generated questions; falls back to defaults if empty
    questions: { type: Array, required: false, default: () => [] },
    title: { type: String, default: 'Quiz' }
});

const emit = defineEmits(['close']);
const close = () => emit('close');

const container = ref(null);
const currentQuestionIndex = ref(0);
const selectedAnswer = ref('');
const showAnswer = ref(false);
const showResults = ref(false);
const userAnswers = ref([]);
const score = ref(0);

// Use passed-in questions if provided; otherwise fallback to a default mock set
const questions = ref(props.questions && props.questions.length ? props.questions : [
    {
        type: 'Multiple Choice',
        question: 'What is the primary goal of supervised learning?',
        options: [
            'To find patterns in unlabeled data',
            'To learn from labeled examples to make predictions',
            'To optimize sequential decisions via rewards',
            'To generate new data similar to training data'
        ],
        correct: 'To learn from labeled examples to make predictions',
        explanation: 'Supervised learning uses labeled training data (input-output pairs) to learn a mapping function that can make predictions on new, unseen data.'
    },
    {
        type: 'True/False',
        question: 'Overfitting occurs when a model performs well on training data but poorly on test data.',
        correct: 'True',
        explanation: 'Overfitting happens when a model learns the noise in the training data rather than the underlying pattern, leading to poor generalization on new data.'
    },
    {
        type: 'Multiple Choice',
        question: 'Which of the following is NOT a common evaluation metric for classification?',
        options: [
            'Accuracy',
            'Precision',
            'Mean Squared Error',
            'F1 Score'
        ],
        correct: 'Mean Squared Error',
        explanation: 'Mean Squared Error (MSE) is used for regression problems, not classification. The other metrics are commonly used for evaluating classification models.'
    },
    {
        type: 'Short Answer',
        question: 'Explain the bias-variance tradeoff in machine learning.',
        correct: 'The bias-variance tradeoff describes the relationship between model complexity and generalization. High bias (underfitting) means the model is too simple, while high variance (overfitting) means it\'s too complex. The goal is to find the optimal balance.',
        explanation: 'This is a fundamental concept in ML that helps understand model performance and guides model selection.'
    },
    {
        type: 'True/False',
        question: 'Neural networks always outperform traditional machine learning algorithms.',
        correct: 'False',
        explanation: 'Neural networks are powerful but not always the best choice. Traditional algorithms can be more suitable for small datasets, interpretable models, or when computational resources are limited.'
    }
]);

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value]);
const progressPercentage = computed(() => ((currentQuestionIndex.value + 1) / questions.value.length) * 100);
const answeredQuestions = computed(() => userAnswers.value.filter(answer => answer !== null).length);

const selectAnswer = (answer) => {
    if (!showAnswer.value) {
        selectedAnswer.value = answer;
    }
};

const submitAnswer = () => {
    if (!showAnswer.value && selectedAnswer.value) {
        // Show the answer
        showAnswer.value = true;
        userAnswers.value[currentQuestionIndex.value] = selectedAnswer.value;
        
        // Update score
        if (selectedAnswer.value === currentQuestion.value.correct) {
            score.value++;
        }
    } else if (showAnswer.value) {
        // Move to next question or show results
        if (currentQuestionIndex.value < questions.value.length - 1) {
            currentQuestionIndex.value++;
            selectedAnswer.value = '';
            showAnswer.value = false;
        } else {
            showResults.value = true;
        }
    }
};

const getScoreMessage = () => {
    const percentage = (score.value / questions.value.length) * 100;
    if (percentage >= 90) return 'Excellent work! You\'ve mastered this material.';
    if (percentage >= 80) return 'Great job! You have a solid understanding.';
    if (percentage >= 70) return 'Good work! Review the missed topics.';
    if (percentage >= 60) return 'Not bad! Consider reviewing the material.';
    return 'Keep studying! This material needs more attention.';
};

const retakeQuiz = () => {
    currentQuestionIndex.value = 0;
    selectedAnswer.value = '';
    showAnswer.value = false;
    showResults.value = false;
    userAnswers.value = [];
    score.value = 0;
};

onMounted(() => {
    requestAnimationFrame(() => container.value?.focus());
});
</script>

<style scoped>
:root {
    --highlight-color: var(--element-color-1, #0d9488);
    --highlight-color-alt: var(--element-color-2, #14b8a6);
    --accent-rgb: 13, 148, 136;
    --success-color: #10b981;
    --error-color: #ef4444;
    --light-text: var(--text-color, #f8fafc);
}

/* ...existing modal transition and backdrop styles... */

.modal-fade-enter-active,
.modal-fade-leave-active {
    transition: opacity .35s ease, transform .4s cubic-bezier(.22,.99,.34,1);
}
.modal-fade-enter-from,
.modal-fade-leave-to {
    opacity: 0;
    transform: translateY(10px) scale(.97);
}

.modal-backdrop {
    position: fixed;
    inset: 0;
    padding: clamp(0.75rem, 2vh, 2rem);
    display: flex;
    justify-content: center;
    align-items: flex-start;
    overflow-y: auto;
    backdrop-filter: blur(14px) saturate(140%);
    -webkit-backdrop-filter: blur(14px) saturate(140%);
    background:
        radial-gradient(circle at 20% 25%, rgba(13,148,136,.15), transparent 60%),
        radial-gradient(circle at 80% 75%, rgba(13,148,136,.08), transparent 55%),
        linear-gradient(180deg, var(--background-color), rgba(10,31,31,0.95));
    z-index: 1000;
}

.modal-container {
    margin-top: 2rem;
    position: relative;
    outline: none;
    width: min(1000px, 100%);
    max-height: min(95vh, 1400px);
    background:
        linear-gradient(155deg, rgba(255,255,255,.05), rgba(255,255,255,.01)),
        linear-gradient(25deg, rgba(13,148,136,.08), transparent);
    border: 1px solid rgba(13,148,136,.25);
    box-shadow:
        0 10px 35px -5px rgba(0,0,0,.75),
        0 0 0 1px rgba(13,148,136,.25),
        0 0 0 6px rgba(13,148,136,.06) inset;
    border-radius: 1.35rem;
    display: flex;
    flex-direction: column;
    backdrop-filter: blur(22px) saturate(160%);
    -webkit-backdrop-filter: blur(22px) saturate(160%);
    overflow: hidden;
    background-color: rgba(10,31,31,.85);
}

/* Header */
.modal-header {
    position: relative;
    padding: 1.4rem 1.75rem 1rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.quiz-info {
    flex: 1;
}

.modal-title {
    font-size: clamp(1.25rem, 1.4rem + .3vw, 1.75rem);
    font-weight: 600;
    line-height: 1.15;
    letter-spacing: .5px;
    display: flex;
    align-items: center;
    gap: .75rem;
    color: #f8fafc;
    text-shadow: 0 2px 8px rgba(13,148,136,.6);
    margin-bottom: .75rem;
}

.title-accent {
    width: .65rem;
    height: 2.15rem;
    border-radius: .4rem;
    background: linear-gradient(180deg, var(--highlight-color), var(--highlight-color-alt));
    box-shadow: 0 0 0 3px rgba(255,255,255,.03), 0 2px 6px -1px rgba(0,0,0,.7);
}

.quiz-stats {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.stat {
    font-size: .875rem;
    color: rgba(248,250,252,.8);
    background: rgba(13,148,136,.1);
    padding: .25rem .75rem;
    border-radius: .5rem;
    border: 1px solid rgba(13,148,136,.2);
}

.close-button {
    margin-left: auto;
    background: linear-gradient(135deg, rgba(13,148,136,.12), rgba(13,148,136,.05));
    border: 1px solid rgba(13,148,136,.35);
    color: #f8fafc;
    padding: .55rem;
    border-radius: .85rem;
    cursor: pointer;
    display: grid;
    place-items: center;
    transition: all .25s ease;
    position: relative;
}
.close-button:before {
    content:"";
    position:absolute;
    inset:0;
    border-radius: inherit;
    background: radial-gradient(circle at 30% 30%, rgba(13,148,136,.4), transparent 65%);
    opacity: 0;
    transition: opacity .35s ease;
}
.close-button:hover {
    color: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px -6px rgba(0,0,0,.65), 0 0 0 1px rgba(13,148,136,.4);
}
.close-button:hover:before { opacity: 1; }
.close-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px -2px rgba(0,0,0,.7);
}

/* Progress */
.progress-section {
    padding: 0 1.75rem 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.progress-bar {
    flex: 1;
    height: .5rem;
    background: rgba(13,148,136,.2);
    border-radius: .25rem;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--highlight-color), var(--highlight-color-alt));
    transition: width .3s ease;
}

.progress-text {
    font-size: .875rem;
    color: rgba(248,250,252,.8);
    white-space: nowrap;
}

/* Question Content */
.modal-body {
    padding: 0 1.75rem 1.5rem;
    overflow-y: auto;
}

.question-container {
    max-width: 800px;
    margin: 0 auto;
}

.question-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.question-number {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--highlight-color);
}

.question-type {
    font-size: .875rem;
    color: rgba(248,250,252,.7);
    background: rgba(13,148,136,.15);
    padding: .25rem .75rem;
    border-radius: .5rem;
}

.question-text {
    font-size: 1.2rem;
    font-weight: 500;
    color: #f8fafc;
    margin-bottom: 2rem;
    line-height: 1.4;
}

/* Multiple Choice Options */
.options-container {
    display: flex;
    flex-direction: column;
    gap: .75rem;
}

.option-button {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.25rem;
    background: linear-gradient(145deg, rgba(13,148,136,.08), rgba(13,148,136,.03));
    border: 2px solid rgba(13,148,136,.2);
    border-radius: .75rem;
    color: #f8fafc;
    cursor: pointer;
    transition: all .2s ease;
    text-align: left;
}

.option-button:hover:not(:disabled) {
    border-color: rgba(13,148,136,.4);
    background: linear-gradient(145deg, rgba(13,148,136,.15), rgba(13,148,136,.05));
    transform: translateY(-2px);
}

.option-button.selected {
    border-color: var(--highlight-color);
    background: linear-gradient(145deg, rgba(13,148,136,.2), rgba(13,148,136,.1));
}

.option-button.correct {
    border-color: var(--success-color);
    background: linear-gradient(145deg, rgba(16,185,129,.2), rgba(16,185,129,.1));
}

.option-button.incorrect {
    border-color: var(--error-color);
    background: linear-gradient(145deg, rgba(239,68,68,.2), rgba(239,68,68,.1));
}

.option-letter {
    width: 2rem;
    height: 2rem;
    background: var(--highlight-color);
    color: #042f2e;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    flex-shrink: 0;
}

/* True/False */
.tf-container {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

.tf-button {
    flex: 1;
    max-width: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: .5rem;
    padding: 2rem 1rem;
    border-radius: 1rem;
    border: 2px solid rgba(13,148,136,.2);
    background: linear-gradient(145deg, rgba(13,148,136,.08), rgba(13,148,136,.03));
    color: #f8fafc;
    cursor: pointer;
    transition: all .2s ease;
}

.tf-button:hover:not(:disabled) {
    transform: translateY(-4px);
    border-color: rgba(13,148,136,.4);
}

.tf-button.selected {
    border-color: var(--highlight-color);
    background: linear-gradient(145deg, rgba(13,148,136,.2), rgba(13,148,136,.1));
}

.tf-button.correct {
    border-color: var(--success-color);
    background: linear-gradient(145deg, rgba(16,185,129,.2), rgba(16,185,129,.1));
}

.tf-button.incorrect {
    border-color: var(--error-color);
    background: linear-gradient(145deg, rgba(239,68,68,.2), rgba(239,68,68,.1));
}

/* Short Answer */
.short-answer-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.answer-textarea {
    width: 100%;
    padding: 1rem;
    border-radius: .75rem;
    border: 2px solid rgba(13,148,136,.2);
    background: rgba(13,148,136,.05);
    color: #f8fafc;
    font-size: 1rem;
    resize: vertical;
    min-height: 120px;
    transition: border-color .2s ease;
}

.answer-textarea:focus {
    outline: none;
    border-color: var(--highlight-color);
}

.correct-answer {
    padding: 1rem;
    background: linear-gradient(145deg, rgba(16,185,129,.15), rgba(16,185,129,.05));
    border: 1px solid rgba(16,185,129,.3);
    border-radius: .75rem;
    color: #f8fafc;
}

/* Explanation */
.explanation-container {
    margin-top: 1.5rem;
    padding: 1rem 1.25rem;
    background: linear-gradient(145deg, rgba(13,148,136,.12), rgba(13,148,136,.04));
    border: 1px solid rgba(13,148,136,.25);
    border-radius: .75rem;
}

.explanation-container h4 {
    color: var(--highlight-color);
    margin: 0 0 .5rem;
    font-size: 1rem;
}

.explanation-container p {
    color: rgba(248,250,252,.9);
    margin: 0;
    line-height: 1.5;
}

/* Results */
.results-body {
    padding: 1rem 1.75rem 1.5rem;
}

.results-container {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
}

.results-header {
    margin-bottom: 2rem;
}

.score-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--highlight-color), var(--highlight-color-alt));
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem;
    box-shadow: 0 8px 32px rgba(13,148,136,.3);
}

.score-percentage {
    font-size: 2rem;
    font-weight: 700;
    color: #042f2e;
}

.score-label {
    font-size: .875rem;
    color: #042f2e;
    opacity: .8;
}

.results-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0 0 .5rem;
}

.results-subtitle {
    color: rgba(248,250,252,.8);
    margin: 0;
}

.results-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 2rem;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--highlight-color);
}

.stat-label {
    font-size: .875rem;
    color: rgba(248,250,252,.7);
}

.question-review h4 {
    font-size: 1.1rem;
    color: #f8fafc;
    margin: 0 0 1rem;
}

.review-list {
    display: flex;
    flex-direction: column;
    gap: .5rem;
}

.review-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: .75rem;
    background: rgba(13,148,136,.05);
    border-radius: .5rem;
    text-align: left;
}

.review-item.correct {
    background: rgba(16,185,129,.1);
}

.review-number {
    width: 1.5rem;
    font-weight: 600;
    color: var(--highlight-color);
}

.review-question {
    flex: 1;
    color: #f8fafc;
    font-size: .875rem;
}

/* Footer */
.modal-footer {
    padding: 1.25rem 1.75rem;
    display: flex;
    justify-content: flex-end;
    gap: .75rem;
    background: linear-gradient(180deg, rgba(13,148,136,.08), rgba(13,148,136,.03));
    border-top: 1px solid rgba(13,148,136,.25);
}

.results-actions {
    display: flex;
    gap: .75rem;
}

.button-secondary {
    position: relative;
    border: 1px solid rgba(13,148,136,.45);
    font-weight: 600;
    letter-spacing: .4px;
    padding: .85rem 1.55rem;
    font-size: .95rem;
    border-radius: .95rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    box-shadow:
        0 10px 24px -10px rgba(0,0,0,.75),
        0 4px 18px -6px rgba(13,148,136,.55),
        0 0 0 1px rgba(13,148,136,.4),
        inset 0 0 0 1px rgba(255,255,255,.15);
    transition: transform .25s cubic-bezier(.22,.99,.45,1), box-shadow .35s ease, filter .4s ease;
}

.button-secondary {
    background: linear-gradient(120deg, rgba(13,148,136,.2), rgba(13,148,136,.1));
    color: #f8fafc;
}

.button-secondary:before {
    content:"";
    position:absolute;
    inset:0;
    border-radius: inherit;
    background: radial-gradient(circle at 30% 30%, rgba(13,148,136,.4), transparent 65%);
    mix-blend-mode: overlay;
    opacity: 0;
    transition: opacity .5s ease;
}

.button-secondary:hover {
    transform: translateY(-4px);
    box-shadow:
        0 18px 40px -18px rgba(0,0,0,.85),
        0 6px 26px -10px rgba(13,148,136,.65),
        0 0 0 1px rgba(13,148,136,.55);
}

.button-secondary:hover:before { 
    opacity: 1; 
}

.button-secondary:active {
    transform: translateY(-1px);
    transition: transform .15s ease;
}

.button-secondary:focus-visible {
    outline: 3px solid var(--highlight-color);
    outline-offset: 3px;
}

/* Responsive */
@media (max-width: 768px) {
    .modal-container {
        margin-top: 1rem;
    }
    
    .quiz-stats {
        gap: .75rem;
    }
    
    .tf-container {
        flex-direction: column;
    }
    
    .results-stats {
        gap: 1rem;
    }
    
    .results-actions {
        flex-direction: column;
        width: 100%;
    }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
    .modal-fade-enter-active,
    .modal-fade-leave-active { transition: none; }
    .button-secondary,
    .close-button,
    .option-button,
    .tf-button { transition: none; }
}
</style>
