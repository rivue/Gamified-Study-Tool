<template>
  <div class="quiz-editor">
    <div class="editor-header">
      <button @click="$emit('cancel-edit')" class="cancel-btn">Cancel</button>
      <h2>{{ editingQuiz.id ? 'Edit Quiz' : 'Create New Quiz' }}</h2>
      <button @click="saveQuiz" class="save-btn" :disabled="!canSaveQuiz">Save Quiz</button>
    </div>

    <div class="quiz-form">
      <div class="form-group">
        <label>Quiz Title</label>
        <input v-model="editingQuiz.title" type="text" placeholder="Enter quiz title..." />
      </div>
      
      <div class="form-group">
        <label>Description (Optional)</label>
        <textarea v-model="editingQuiz.description" placeholder="Enter quiz description..."></textarea>
      </div>

      <div class="questions-section">
        <div class="questions-header">
          <h3>Questions</h3>
          <button @click="addQuestion" class="add-question-btn">
            <PlusIcon class="w-4 h-4" />
            Add Question
          </button>
        </div>

        <div v-for="(question, qIndex) in editingQuiz.questions" :key="qIndex" class="question-card">
          <div class="question-header">
            <span class="question-number">Question {{ qIndex + 1 }}</span>
            <button @click="removeQuestion(qIndex)" class="remove-question-btn">
              <TrashIcon class="w-4 h-4" />
            </button>
          </div>

          <div class="form-group">
            <label>Question Text</label>
            <textarea v-model="question.text" placeholder="Enter your question..."></textarea>
          </div>

          <div class="answers-section">
            <label>Answer Options</label>
            <div v-for="(answer, aIndex) in question.answers" :key="aIndex" class="answer-option">
              <input v-model="answer.text" type="text" :placeholder="`Option ${aIndex + 1}...`" />
              <label class="correct-answer-label">
                <input 
                  type="radio" 
                  :name="`question-${qIndex}`" 
                  :value="aIndex"
                  v-model="question.correctAnswer"
                />
                <span>Correct</span>
              </label>
              <button @click="removeAnswer(qIndex, aIndex)" class="remove-answer-btn" :disabled="question.answers.length <= 2">
                <TrashIcon class="w-4 h-4" />
              </button>
            </div>
            <button @click="addAnswer(qIndex)" class="add-answer-btn" :disabled="question.answers.length >= 6">
              <PlusIcon class="w-4 h-4" />
              Add Option
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { PlusIcon, TrashIcon } from '@heroicons/vue/24/solid'

const props = defineProps<{
  editingQuiz: any
}>()

const emit = defineEmits<{
  'cancel-edit': []
  'save-quiz': [quiz: any]
}>()

const editingQuiz = ref({ ...props.editingQuiz })

watch(() => props.editingQuiz, (newVal) => {
  editingQuiz.value = { ...newVal }
}, { deep: true })

const canSaveQuiz = computed(() => {
  return editingQuiz.value.title.trim() && 
         editingQuiz.value.questions.length > 0 &&
         editingQuiz.value.questions.every(q => 
           q.text.trim() && 
           q.answers.length >= 2 && 
           q.answers.every(a => a.text.trim()) &&
           q.correctAnswer !== null
         )
})

const saveQuiz = () => {
  if (!canSaveQuiz.value) return
  emit('save-quiz', editingQuiz.value)
}

const addQuestion = () => {
  editingQuiz.value.questions.push({
    text: '',
    answers: [
      { text: '' },
      { text: '' }
    ],
    correctAnswer: null
  })
}

const removeQuestion = (index) => {
  editingQuiz.value.questions.splice(index, 1)
}

const addAnswer = (questionIndex) => {
  editingQuiz.value.questions[questionIndex].answers.push({ text: '' })
}

const removeAnswer = (questionIndex, answerIndex) => {
  const question = editingQuiz.value.questions[questionIndex]
  if (question.correctAnswer === answerIndex) {
    question.correctAnswer = null
  } else if (question.correctAnswer > answerIndex) {
    question.correctAnswer--
  }
  question.answers.splice(answerIndex, 1)
}
</script>

<style scoped>
.quiz-editor {
  background: linear-gradient(135deg, #1a1a1a 0%, #222 100%);
  border-radius: 1.5rem;
  padding: 3rem;
  border: 1px solid #333;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  width: 100%;
  box-sizing: border-box;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #2a2a2a;
}

.editor-header h2 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #fff;
}

.cancel-btn, .save-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid #333;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background-color: #2a2a2a;
  color: #eee;
}

.save-btn {
  background-color: var(--accent-color-1);
  color: var(--light-text);
  border-color: var(--accent-color-1);
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #bbb;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #333;
  border-radius: 0.5rem;
  background-color: #111;
  color: #eee;
  resize: vertical;
}

.form-group input:focus, .form-group textarea:focus {
  outline: none;
  border-color: var(--accent-color-1);
}

.questions-section {
  margin-top: 2rem;
}

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.questions-header h3 {
  margin: 0;
  color: #fff;
}

.add-question-btn, .add-answer-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: var(--accent-color-1);
  color: var(--light-text);
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: all 0.2s;
}

.question-card {
  background-color: #111;
  border: 1px solid #2a2a2a;
  border-radius: 0.5rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-number {
  font-weight: 600;
  color: var(--accent-color-1);
}

.answers-section {
  margin-top: 1rem;
}

.answer-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.answer-option input[type="text"] {
  flex: 1;
}

.correct-answer-label {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  white-space: nowrap;
}

.remove-question-btn, .remove-answer-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: all 0.2s;
  background-color: #442222;
  color: #ff8888;
}

@media (max-width: 768px) {
  .quiz-editor {
    padding: 2rem;
  }

  .answer-option {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  
  .correct-answer-label {
    justify-content: center;
  }
}
</style>
