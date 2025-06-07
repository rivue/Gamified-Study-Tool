<template>
    <transition name="fade">
        <div v-if="questionVisible" class="question-overlay">
            <div class="question-backdrop">

                <LeaveGameWarning />

                <div class="info-icon" @click="flipQuestion">i</div>
                <!-- Completion message when no more questions -->
                <div v-if="question === null" class="completion-message">
                    Congratulations, you've completed all questions in this room!
                </div>
                <div v-else class="question-content">
                    <p v-html="question.text"></p>
                </div>

                <div v-if="question !== null" class="choices-container" :class="{ 'shake': isShaking }">
                    <div v-if="question.type === 'one_word_answer'" class="input-container">
                        <input type="text" v-model="userAnswer" @keyup.enter="submitOneWordAnswer" :class="{
                            'correct': answerState.correct,
                            'wrong': answerState.wrong
                        }" :disabled="isDisabled" placeholder="Type your answer...">
                        <button class="submit-btn" @click="submitOneWordAnswer"
                            :disabled="isDisabled || !userAnswer.trim()">
                            Submit
                        </button>
                    </div>
                    <div v-else v-for="(choice, index) in question.choices" :key="index">
                        <button :class="{
                            correct: choice === answerState.correct,
                            wrong: choice === answerState.wrong,
                            disabledButton: isDisabled
                        }" :disabled="isDisabled" @click.stop="submitAnswer(choice)" v-html="choice"></button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">

import LeaveGameWarning from "./LeaveGameWarning.vue";
import { ref, computed } from "vue";
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
    return content
        .replace(/\*\*([^*]*?)\*\*/g, "<strong>$1</strong>")
        .replace(/_([^_]*?)_|\*([^*]*?)\*/g, "<em>$1$2</em>");
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
.completion-message {
    text-align: center;
    font-size: 1.4em;
    color: var(--highlight-color);
}

.question-overlay {
    position: fixed;
    /* Changed from absolute to fixed */
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    z-index: 110;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
    /* Added semi-transparent background */
}

.question-backdrop {
    position: relative;
    background-color: var(--background-haze);
    padding: 2em;
    /* Increased padding */
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    box-shadow: 0 16px 16px var(--background-color-2t),
        0 -16px 16px var(--background-color-2t);
    width: 80%;
    /* Set width to 80% of viewport */
    max-width: 800px;
    /* Maximum width */
    min-height: 60vh;
    /* Minimum height */
    border-radius: 12px;
    /* Added rounded corners */
}

/* Moved info icon to top right */
.info-icon {
    position: absolute;
    top: 10px;
    right: 10px;
    /* Changed from left to right */
    width: 30px;
    height: 30px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    text-align: center;
    line-height: 30px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
}

.info-icon:hover {
    background: rgba(255, 255, 255, 0.5);
}

.question-content {
    text-align: center;
    width: 90%;
    padding: 30px;
    /* Increased padding */
    border-radius: 12px;
    background-image: linear-gradient(to right,
            var(--background-color-2t),
            var(--background-color-1t));
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 1.4em;
    margin: 20px 0;
}

.choices-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    /* Increased gap */
    width: 90%;
    margin-top: 30px;
}

button {
    padding: 20px;
    /* Increased padding */
    width: 100%;
    height: 100%;
    border: none;
    background-color: var(--background-color-1t);
    border: 1px solid var(--background-color-2t);
    font-size: 1.2em;
    /* Increased font size */
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    transition: all ease 0.2s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

button.correct {
    background-color: green;
    color: white;
}

button.wrong {
    background-color: red;
    color: white;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

button.disabledButton {
    pointer-events: none;
    animation: fadeDisable 1s forwards;
}

@keyframes fadeDisable {
    0% {
        opacity: 1;
    }

    50% {
        opacity: 0.5;
    }

    100% {
        opacity: 1;
    }
}

/* Added responsive design for smaller screens */
@media (max-width: 768px) {
    .question-backdrop {
        width: 95%;
        padding: 1em;
    }

    .choices-container {
        grid-template-columns: 1fr;
        /* Stack buttons on mobile */
    }

    .question-content {
        font-size: 1.2em;
    }

    button {
        font-size: 1em;
    }
}

.input-container {
    grid-column: 1 / -1;
    display: flex;
    gap: 10px;
    width: 100%;
}

input {
    flex: 1;
    padding: 20px;
    font-size: 1.2em;
    border: 1px solid var(--background-color-2t);
    border-radius: 12px;
    background-color: var(--background-color-1t);
    transition: all 0.3s ease;
}

input:focus {
    outline: none;
    box-shadow: 0 0 0 2px var(--highlight-color);
}

input.correct {
    background-color: green;
    color: white;
    border-color: green;
}

input.wrong {
    background-color: red;
    color: white;
    border-color: red;
}

.submit-btn {
    padding: 20px 30px;
    white-space: nowrap;
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

.shake {
    animation: shake 0.5s cubic-bezier(.36, .07, .19, .97) both;
}

@media (max-width: 768px) {
    .input-container {
        flex-direction: column;
    }

    .submit-btn {
        width: 100%;
    }
}
</style>