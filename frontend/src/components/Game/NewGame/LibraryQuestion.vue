<template>
    <transition name="fade">
        <div v-if="questionVisible" class="question-overlay">
            <div class="question-backdrop">


                <LeaveGameWarning />

                <!-- Info icon - positioned relative to backdrop -->
                
                <div class="info-icon" @click="flipQuestion">
                    <!-- <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="11" />
                        <path d="M12 16v-4" />
                        <path d="M12 8h.01" />
                        <circle cx="12" cy="8" r="0.5" fill="currentColor" />
                    </svg> -->
                    <LightBulbIcon class="w-5 h-5" />
                    hint
                </div>

                <!-- Skip button - positioned relative to backdrop, outside of shake container -->
                <button class="skip-btn" @click="handleSkip" :disabled="store.completed">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M13 17l5-5-5-5" />
                        <path d="M6 17l5-5-5-5" />
                    </svg>
                    Skip
                </button>

                <!-- Completion message when no more questions -->
                <div v-if="question === null" class="completion-message">
                    <div class="completion-icon">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                            <polyline points="22,4 12,14.01 9,11.01" />
                        </svg>
                    </div>
                    <h2>Congratulations!</h2>
                    <p>You've completed all questions in this room!</p>
                </div>

                <!-- Question content -->
                <div v-else class="question-content">
                    <div class="question-text" v-html="question.text"></div>
                </div>

                <!-- Choices container - this is what shakes, skip button is outside -->
                <div v-if="question !== null" class="choices-container" :class="{ 'animate-shake': isShaking }">
                    <!-- One word answer input -->
                    <div v-if="question.type === 'one_word_answer'" class="input-container">
                        <div class="input-wrapper">
                            <input type="text" v-model="userAnswer" @keyup.enter="submitOneWordAnswer" :class="{
                                'input-correct': answerState.correct,
                                'input-wrong': answerState.wrong
                            }" :disabled="isDisabled" placeholder="Type your answer..." class="answer-input">
                            <button class="submit-btn" @click="submitOneWordAnswer"
                                :disabled="isDisabled || !userAnswer.trim()">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <polyline points="9,18 15,12 9,6" />
                                </svg>
                                Submit
                            </button>
                        </div>
                    </div>

                    <!-- Multiple choice buttons -->
                    <template v-else>
                        <button v-for="(choice, index) in question.choices" :key="index" :class="{
                            'choice-correct': choice === answerState.correct,
                            'choice-wrong': choice === answerState.wrong,
                            'choice-disabled': isDisabled && choice !== answerState.correct && choice !== answerState.wrong
                        }" :disabled="isDisabled" @click.stop="submitAnswer(choice)" v-html="choice"
                            class="choice-btn"></button>
                    </template>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">

import LeaveGameWarning from "./LeaveGameWarning.vue";
import { ref, computed } from "vue";
import { LightBulbIcon } from "@heroicons/vue/24/solid";
import { useRouter, useRoute } from "vue-router";
import { useGameStore } from "@/store/gameStore";
import stringSimilarity from "string-similarity";

const router = useRouter();
const route = useRoute();
const store = useGameStore();

const answerState = ref<{ correct: string | null; wrong: string | null }>({
    correct: null,
    wrong: null,
});
const isDisabled = ref(false);
const isShaking = ref(false);
const userAnswer = ref("");

function shuffleArray<T>(array: T[]): void {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function submitOneWordAnswer() {
    if (isDisabled.value || !userAnswer.value.trim()) return;

    const processedAnswer = userAnswer.value.trim().toLowerCase();
    const correctAnswer = store.factoids[store.currentQuestion].questions[0].correct_choice.toLowerCase();
    const similarity = stringSimilarity.compareTwoStrings(processedAnswer, correctAnswer);
    const isCorrect = similarity > 0.7;

    submitAnswer(userAnswer.value, isCorrect);
}

function submitAnswer(choice: string, isOneWordAnswer = false) {
    const correct = store.factoids[store.currentQuestion].questions[0].correct_choice;
    const isCorrect = isOneWordAnswer ? true : correct === choice;

    if (isCorrect) {
        answerState.value.correct = choice;
        answerState.value.wrong = null;
    } else {
        answerState.value.wrong = choice;
        answerState.value.correct = null;
        isDisabled.value = true;
        isShaking.value = true;

        setTimeout(() => {
            isShaking.value = false;
            isDisabled.value = false;
            if (isOneWordAnswer) {
                userAnswer.value = "";
            }
            answerState.value.wrong = null;
        }, 1000);
    }

    setTimeout(() => {
        if (store.answerAttempt(isCorrect)) {
            resetState();
        } else {
            router.push("/login");
        }
    }, 300);
}

function resetState() {
    answerState.value.correct = null;
    answerState.value.wrong = null;
    userAnswer.value = "";
    isShaking.value = false;
}

function handleSkip() {
    store.skipQuestion();
}

function flipQuestion() {
    store.toggleFactoid();
    answerState.value.wrong = null;
    answerState.value.correct = null;
    isShaking.value = false;
}

function closeQuestion() {
    router.push(`/lessons/${route.params.id}`);
}

function format(content: string): string {
    content = content.replace(/_+/g, '___');
    content = content.replace(/\*\*([^*]*?)\*\*/g, '<strong>$1</strong>');
    content = content.replace(/\*([^*]*?)\*/g, '<em>$1</em>');
    return content;
}

const question = computed(() => {
    if (store.currentQuestion === null) return null;

    const currentFactoid = store.factoids[store.currentQuestion];
    if (
        !currentFactoid ||
        !Array.isArray(currentFactoid.questions) ||
        currentFactoid.questions.length === 0
    ) {
        console.error("Invalid question structure.");
        return null;
    }

    const currentQuestion = currentFactoid.questions[0];
    if (
        !currentQuestion ||
        !currentQuestion.question_text ||
        !currentQuestion.correct_choice ||
        !currentQuestion.question_type ||
        !Array.isArray(currentQuestion.wrong_choices)
    ) {
        console.error("Missing question fields.");
        return null;
    }

    const choices = [
        currentQuestion.correct_choice,
        ...currentQuestion.wrong_choices,
    ];
    shuffleArray(choices);

    return {
        text: format(currentQuestion.question_text),
        choices: choices.map(format),
        type: currentQuestion.question_type,
    };
});

const questionVisible = computed(() => store.questionVisible);
</script>

<style scoped>
/* Modern CSS Variables for theming */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.2);
    --backdrop-blur: blur(20px);
    --shadow-elegant: 0 8px 32px rgba(0, 0, 0, 0.3);
    --shadow-hover: 0 12px 40px rgba(0, 0, 0, 0.4);
}

.fade-enter-active,
.fade-leave-active {
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: scale(0.95);
}

.question-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    z-index: 110;
    display: flex;
    justify-content: center;
    align-items: center;
    background: radial-gradient(circle at center, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.9) 100%);
    backdrop-filter: var(--backdrop-blur);
}

.question-backdrop {
    position: relative;
    background: var(--background-haze);
    background-image:
        linear-gradient(135deg, var(--background-haze) 0%, var(--background-color-2t) 100%),
        radial-gradient(circle at top right, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
    padding: 3rem;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    box-shadow: var(--shadow-elegant);
    width: 90%;
    max-width: 900px;
    min-height: 65vh;
    border-radius: 24px;
    border: 1px solid var(--glass-border);
    backdrop-filter: var(--backdrop-blur);
    transition: all 0.3s ease;
}

.question-backdrop:hover {
    box-shadow: var(--shadow-hover);
}

.info-icon {
    position: absolute;
    top: 20px;
    right: 20px;
    height: 44px;
    font-size: 0.9rem;
    font-weight: 500;
    color: white;
    gap: 12px;
    padding-right: 12px;
    padding-left: 12px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    min-width: 70px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.info-icon:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.skip-btn {
    position: absolute;
    bottom: 20px;
    right: 20px;
    padding: 12px 20px;
    font-size: 0.9rem;
    font-weight: 500;
    color: white;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 100px;
    height: 44px;
    justify-content: center;
}

.skip-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.skip-btn:disabled {
    cursor: not-allowed;
    opacity: 0.5;
}

.completion-message {
    text-align: center;
    color: var(--highlight-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}

.completion-icon {
    color: #10b981;
    animation: celebrate 0.6s ease-out;
}

.completion-message h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(135deg, var(--highlight-color), #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.completion-message p {
    font-size: 1.2rem;
    opacity: 0.9;
    margin: 0;
}

.question-content {
    width: 100%;
    max-width: 800px;
    margin-bottom: 2rem;
}

.question-text {
    text-align: center;
    padding: 2.5rem;
    border-radius: 20px;
    background: linear-gradient(135deg, var(--background-color-2t), var(--background-color-1t));
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    font-size: 1.4rem;
    font-weight: 500;
    line-height: 1.6;
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(10px);
}

.choices-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    width: 100%;
    max-width: 800px;
}

.choice-btn {
    padding: 1.5rem 2rem;
    border: 1px solid var(--glass-border);
    background: var(--glass-bg);
    color: white;
    font-size: 1.1rem;
    font-weight: 500;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    min-height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.choice-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.5s;
}

.choice-btn:hover:not(:disabled)::before {
    left: 100%;
}

.choice-btn:hover:not(:disabled) {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
    background: rgba(255, 255, 255, 0.15);
}

.choice-correct {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    border-color: #10b981 !important;
    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4) !important;
}

.choice-wrong {
    background: linear-gradient(135deg, #ef4444, #dc2626) !important;
    border-color: #ef4444 !important;
    box-shadow: 0 8px 32px rgba(239, 68, 68, 0.4) !important;
}

.choice-disabled {
    opacity: 0.5;
    cursor: not-allowed;
    animation: pulse 2s infinite;
}

.input-container {
    grid-column: 1 / -1;
    width: 100%;
}

.input-wrapper {
    display: flex;
    gap: 1rem;
    width: 100%;
    align-items: stretch;
}

.answer-input {
    flex: 1;
    padding: 1.5rem 2rem;
    font-size: 1.2rem;
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    background: var(--glass-bg);
    color: white;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2); /* Added this line */
}

.answer-input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

.answer-input:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3);
    border-color: var(--highlight-color);
    background: rgba(255, 255, 255, 0.15);
}

.input-correct {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    border-color: #10b981 !important;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.3) !important;
}

.input-wrong {
    background: linear-gradient(135deg, #ef4444, #dc2626) !important;
    border-color: #ef4444 !important;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.3) !important;
}

.submit-btn {
    padding: 1.5rem 2.5rem;
    background: linear-gradient(135deg, var(--highlight-color), #5a67d8);
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
    min-width: 120px;
    justify-content: center;
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, #5a67d8, var(--highlight-color));
}

.submit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

@keyframes shake {

    0%,
    100% {
        transform: translateX(0);
    }

    25% {
        transform: translateX(-10px);
    }

    75% {
        transform: translateX(10px);
    }
}

@keyframes celebrate {
    0% {
        transform: scale(0.5) rotate(0deg);
        opacity: 0;
    }

    50% {
        transform: scale(1.2) rotate(180deg);
        opacity: 1;
    }

    100% {
        transform: scale(1) rotate(360deg);
        opacity: 1;
    }
}

@keyframes pulse {

    0%,
    100% {
        opacity: 0.5;
    }

    50% {
        opacity: 0.8;
    }
}

.animate-shake {
    animation: shake 0.5s cubic-bezier(.36, .07, .19, .97) both;
}

/* Responsive Design */
@media (max-width: 768px) {
    .question-backdrop {
        width: 95%;
        padding: 2rem;
        min-height: 70vh;
    }

    .choices-container {
        grid-template-columns: 1fr;
        gap: 1rem;
    }

    .question-text {
        font-size: 1.2rem;
        padding: 2rem;
    }

    .choice-btn {
        font-size: 1rem;
        padding: 1.25rem 1.5rem;
        min-height: 70px;
    }

    .input-wrapper {
        flex-direction: column;
        gap: 1rem;
    }

    .submit-btn {
        width: 100%;
    }

    .completion-message h2 {
        font-size: 2rem;
    }
}

@media (max-width: 480px) {
    .question-backdrop {
        padding: 1.5rem;
    }

    .question-text {
        font-size: 1.1rem;
        padding: 1.5rem;
    }

    .skip-btn {
        bottom: 15px;
        right: 15px;
        padding: 10px 16px;
        font-size: 0.85rem;
        min-width: 85px;
        height: 40px;
    }

    .info-icon {
        top: 15px;
        right: 15px;
        width: 40px;
        height: 40px;
    }
}
</style>