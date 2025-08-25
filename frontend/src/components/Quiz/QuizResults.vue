<template>
  <div class="quiz-results">
    <div class="results-container">
      <div class="results-header">
        <div class="results-icon">
          <TrophyIcon class="w-16 h-16" />
        </div>
        <h2>Quiz Complete!</h2>
        <p>{{ quiz.title }}</p>
      </div>

      <div class="score-display">
        <div class="score-circle">
          <svg class="score-ring" width="120" height="120">
            <circle class="score-ring-bg" cx="60" cy="60" r="54" />
            <circle class="score-ring-fg" :stroke-dasharray="`${(score / quiz.questions.length) * 339.29} 339.29`" cx="60" cy="60" r="54" />
          </svg>
          <div class="score-text">
            <div class="score-percentage">{{ Math.round(score / quiz.questions.length * 100) }}%</div>
            <div class="score-fraction">{{ score }} / {{ quiz.questions.length }}</div>
          </div>
        </div>
      </div>

      <div class="results-actions">
        <button @click="$emit('retake-quiz')" class="retake-btn">
          <ArrowPathIcon class="w-5 h-5" />
          Retake Quiz
        </button>
        <button @click="$emit('back-to-list')" class="back-to-list-btn">
          Back to Quizzes
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { TrophyIcon, ArrowPathIcon } from '@heroicons/vue/24/solid'

defineProps<{
  quiz: any
  score: number
}>()

defineEmits<{
  'retake-quiz': []
  'back-to-list': []
}>()
</script>

<style scoped>
.quiz-results {
  width: 100%;
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
}

.results-container {
  background-color: #1a1a1a;
  border-radius: 1rem;
  padding: 3rem 2rem;
  text-align: center;
  border: 1px solid #2a2a2a;
}

.results-header {
  margin-bottom: 2rem;
}

.results-icon {
  margin-bottom: 1rem;
  color: #f59e0b;
}

.results-header h2 {
  margin: 0 0 0.5rem;
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
}

.results-header p {
  margin: 0;
  color: #aaa;
  font-size: 1.1rem;
}

.score-display {
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
}

.score-circle {
  width: 120px;
  height: 120px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.score-ring {
  position: absolute;
  top: 0;
  left: 0;
  transform: rotate(-90deg);
}

.score-ring-bg {
  fill: none;
  stroke: #2a2a2a;
  stroke-width: 12;
}

.score-ring-fg {
  fill: none;
  stroke: var(--accent-color-1);
  stroke-width: 12;
  stroke-linecap: round;
  transition: stroke-dasharray 0.5s ease-out;
}

.score-text {
  color: #fff;
}

.score-percentage {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1;
}

.score-fraction {
  font-size: 0.875rem;
  opacity: 0.7;
}

.results-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.retake-btn, .back-to-list-btn {
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
  background: var(--accent-color-1);
  color: var(--light-text);
}

.back-to-list-btn {
  background-color: #2a2a2a;
  color: #eee;
}

.retake-btn:hover, .back-to-list-btn:hover {
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .quiz-results {
    padding: 1rem;
  }
  
  .results-actions {
    flex-direction: column;
  }
}
</style>
