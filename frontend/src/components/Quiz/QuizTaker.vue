<template>
  <div class="quiz-taker">
    <div class="quiz-container">
      <div class="quiz-header-info">
        <h2 class="quiz-name">{{ quiz.title }}</h2>
        <button @click="$emit('exit-quiz')" class="exit-btn">
          <XMarkIcon class="w-5 h-5" />
          Exit Quiz
        </button>
      </div>

      <div class="questions-container">
        <div 
          v-for="(question, questionIndex) in quiz.questions" 
          :key="questionIndex"
          class="question-block"
          :class="{ 'answered': userAnswers[questionIndex] !== null }"
        >
          <div class="question-header">
            <div class="question-number">Question {{ questionIndex + 1 }}</div>
            <div v-if="showResults && userAnswers[questionIndex] !== null" class="question-result">
              <CheckIcon v-if="userAnswers[questionIndex] === question.correctAnswer" class="w-5 h-5 text-green-400" />
              <XMarkIcon v-else class="w-5 h-5 text-red-400" />
            </div>
          </div>
          
          <div class="question-text">{{ question.text }}</div>
          
          <div class="answers-container">
            <div 
              v-for="(answer, answerIndex) in question.answers" 
              :key="answerIndex"
              class="answer-item"
              :class="{ 
                'selected': userAnswers[questionIndex] === answerIndex,
                'correct': showResults && answerIndex === question.correctAnswer,
                'incorrect': showResults && userAnswers[questionIndex] === answerIndex && answerIndex !== question.correctAnswer,
                'disabled': showResults
              }"
              @click="!showResults && selectAnswer(questionIndex, answerIndex)"
            >
              <div class="answer-marker">
                <div class="answer-marker-inner"></div>
              </div>
              <span class="answer-text">{{ answer.text }}</span>
              <div v-if="showResults" class="answer-indicator">
                <CheckIcon v-if="answerIndex === question.correctAnswer" class="w-5 h-5 text-green-400" />
                <XMarkIcon v-else-if="userAnswers[questionIndex] === answerIndex" class="w-5 h-5 text-red-400" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="quiz-actions">
        <button 
          v-if="!showResults"
          @click="submitQuiz" 
          :disabled="!allQuestionsAnswered"
          class="submit-btn"
          :class="{ 'pulse': allQuestionsAnswered }"
        >
          Submit Quiz
        </button>
        
        <div v-if="showResults" class="result-actions">
          <div class="final-score">
            <h3>Your Score: {{ score }} / {{ quiz.questions.length }} ({{ Math.round(score / quiz.questions.length * 100) }}%)</h3>
          </div>
          <div class="action-buttons">
            <button @click="retakeQuiz" class="retake-btn">
              <ArrowPathIcon class="w-5 h-5" />
              Retake Quiz
            </button>
            <button @click="finishQuiz" class="finish-btn">
              View Results
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { XMarkIcon, CheckIcon, ArrowPathIcon } from '@heroicons/vue/24/solid'

const props = defineProps<{
  quiz: any
}>()

const emit = defineEmits<{
  'exit-quiz': []
  'quiz-completed': [score: number]
}>()

const userAnswers = ref(Array(props.quiz.questions.length).fill(null))
const showResults = ref(false)
const score = ref(0)

const answeredCount = computed(() => {
  return userAnswers.value.filter(answer => answer !== null).length
})

const allQuestionsAnswered = computed(() => {
  return answeredCount.value === props.quiz.questions.length
})

const selectAnswer = (questionIndex, answerIndex) => {
  userAnswers.value[questionIndex] = answerIndex
}

const submitQuiz = () => {
  if (!allQuestionsAnswered.value) return
  
  // Calculate score
  score.value = 0
  props.quiz.questions.forEach((question, index) => {
    if (userAnswers.value[index] === question.correctAnswer) {
      score.value++
    }
  })
  
  showResults.value = true
  
  // Scroll to top to show results
  const container = document.querySelector('.quiz-taker')
  if (container) {
    container.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const retakeQuiz = () => {
  userAnswers.value = Array(props.quiz.questions.length).fill(null)
  showResults.value = false
  score.value = 0
  
  // Scroll to top
  const container = document.querySelector('.quiz-taker')
  if (container) {
    container.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const finishQuiz = () => {
  emit('quiz-completed', score.value)
}
</script>

<style scoped>
.quiz-taker {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
  box-sizing: border-box;
  overflow-y: auto;
}

.quiz-container {
  background-color: #1a1a1a;
  border-radius: 1rem;
  padding: 2rem;
  border: 1px solid #2a2a2a;
}

.quiz-header-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #2a2a2a;
}

.quiz-name {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #fff;
}

.exit-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #2a2a2a;
  color: #aaa;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.exit-btn:hover {
  background-color: #442222;
  color: #ff8888;
}

.questions-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 3rem;
}

.question-block {
  padding: 1.5rem;
  background-color: #222;
  border: 1px solid #333;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-number {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--accent-color-1);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.question-result {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
}

.question-text {
  font-size: 1.125rem;
  font-weight: 600;
  color: #fff;
  line-height: 1.4;
  margin-bottom: 1.5rem;
}

.answers-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.answer-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: #1a1a1a;
  border: 1px solid #333;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.answer-item:hover:not(.disabled) {
  border-color: var(--accent-color-1);
  background-color: #252525;
}

.answer-item.selected {
  border-color: var(--accent-color-1);
  background-color: var(--accent-color-1-t);
}

.answer-item.correct {
  border-color: #10b981;
  background-color: rgba(16, 185, 129, 0.1);
}

.answer-item.incorrect {
  border-color: #ef4444;
  background-color: rgba(239, 68, 68, 0.1);
}

.answer-item.disabled {
  cursor: not-allowed;
}

.answer-marker {
  width: 24px;
  height: 24px;
  border: 2px solid #555;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.answer-marker-inner {
  width: 12px;
  height: 12px;
  background-color: transparent;
  border-radius: 50%;
  transition: all 0.2s ease;
  transform: scale(0);
}

.answer-item.selected .answer-marker {
  border-color: var(--accent-color-1);
}

.answer-item.selected .answer-marker-inner {
  background-color: var(--accent-color-1);
  transform: scale(1);
}

.answer-text {
  flex: 1;
  font-size: 1rem;
  color: #eee;
}

.answer-indicator {
  flex-shrink: 0;
}

.quiz-actions {
  text-align: center;
  padding: 2rem 0;
  border-top: 1px solid #333;
}

.submit-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2.5rem;
  background: var(--accent-color-1);
  color: var(--light-text);
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.submit-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #555;
}

.submit-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px var(--accent-color-1-t);
}

.submit-btn.pulse {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 var(--accent-color-1-t);
  }
  70% {
    box-shadow: 0 0 0 10px transparent;
  }
  100% {
    box-shadow: 0 0 0 0 transparent;
  }
}

.result-actions {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  align-items: center;
}

.final-score {
  text-align: center;
}

.final-score h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #fff;
  background: linear-gradient(135deg, var(--accent-color-1), #4c51bf);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.retake-btn, .finish-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.retake-btn {
  background: #555;
  color: #eee;
}

.finish-btn {
  background: var(--accent-color-1);
  color: var(--light-text);
}

.retake-btn:hover, .finish-btn:hover {
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .quiz-taker {
    padding: 1rem;
  }
  
  .quiz-container {
    padding: 1.5rem;
  }
  
  .quiz-header-info {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .question-block {
    padding: 1rem;
  }
  
  .action-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .retake-btn, .finish-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
