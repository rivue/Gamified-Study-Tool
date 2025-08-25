<template>
  <div class="quiz-manager">
    <header v-if="!showQuizTaker" class="quiz-header">
      <div class="header-content">
        <div class="header-left">
          <button @click="goBack" class="back-button">
            <ArrowLeftIcon class="w-5 h-5" />
            <span>Back to Course</span>
          </button>
        </div>
        <h1 class="page-title">Quiz Manager</h1>
        <button @click="createNewQuiz" class="back-button">
          <PlusIcon class="w-5 h-5" />
          <span>Create Quiz</span>
        </button>
      </div>
    </header>

    <main class="quiz-content" :class="{ 'quiz-taking': showQuizTaker }">
      <QuizList 
        v-if="!showQuizEditor && !showQuizTaker && !showResults"
        :quizzes="quizzes"
        @create-quiz="createNewQuiz"
        @take-quiz="takeQuiz"
        @edit-quiz="editQuiz"
        @delete-quiz="deleteQuiz"
      />

      <QuizTaker
        v-if="showQuizTaker && currentQuiz && !showResults"
        :quiz="currentQuiz"
        @exit-quiz="exitQuiz"
        @quiz-completed="handleQuizCompleted"
      />

      <QuizResults
        v-if="showResults && quizCompleted"
        :quiz="currentQuiz"
        :score="score"
        @retake-quiz="retakeQuiz"
        @back-to-list="backToList"
      />

      <QuizEditor
        v-if="showQuizEditor && !showQuizTaker && !showResults"
        :editing-quiz="editingQuiz"
        @cancel-edit="cancelEdit"
        @save-quiz="saveQuiz"
      />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeftIcon, PlusIcon } from '@heroicons/vue/24/solid'
import { toast } from 'vue-sonner'
import QuizList from '@/components/Quiz/QuizList.vue'
import QuizTaker from '@/components/Quiz/QuizTaker.vue'
import QuizResults from '@/components/Quiz/QuizResults.vue'
import QuizEditor from '@/components/Quiz/QuizEditor.vue'

const router = useRouter()
const route = useRoute()

const libraryId = ref(parseInt(route.params.id as string))
const quizzes = ref([])
const showQuizEditor = ref(false)
const showQuizTaker = ref(false)
const showResults = ref(false)
const quizCompleted = ref(false)
const currentQuiz = ref(null)
const score = ref(0)

const editingQuiz = ref({
  id: null,
  title: '',
  description: '',
  questions: []
})

const goBack = () => {
  router.push(`/lessons/${libraryId.value}`)
}

const createNewQuiz = () => {
  editingQuiz.value = {
    id: null,
    title: '',
    description: '',
    questions: []
  }
  showQuizEditor.value = true
}

const editQuiz = (quiz) => {
  editingQuiz.value = JSON.parse(JSON.stringify(quiz))
  showQuizEditor.value = true
}

const cancelEdit = () => {
  showQuizEditor.value = false
  editingQuiz.value = { id: null, title: '', description: '', questions: [] }
}

const saveQuiz = (quizData) => {
  const fullQuizData = {
    ...quizData,
    libraryId: libraryId.value,
    createdAt: quizData.id ? quizData.createdAt : new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }

  if (quizData.id) {
    const index = quizzes.value.findIndex(q => q.id === quizData.id)
    quizzes.value[index] = fullQuizData
    toast.success('Quiz updated successfully!')
  } else {
    fullQuizData.id = Date.now()
    quizzes.value.push(fullQuizData)
    toast.success('Quiz created successfully!')
  }

  localStorage.setItem(`quizzes_${libraryId.value}`, JSON.stringify(quizzes.value))
  
  showQuizEditor.value = false
  editingQuiz.value = { id: null, title: '', description: '', questions: [] }
}

const deleteQuiz = (quizId) => {
  if (confirm('Are you sure you want to delete this quiz?')) {
    quizzes.value = quizzes.value.filter(q => q.id !== quizId)
    localStorage.setItem(`quizzes_${libraryId.value}`, JSON.stringify(quizzes.value))
    toast.success('Quiz deleted successfully!')
  }
}

const takeQuiz = (quiz) => {
  currentQuiz.value = quiz
  showResults.value = false
  quizCompleted.value = false
  showQuizTaker.value = true
}

const exitQuiz = () => {
  if (confirm('Are you sure you want to exit the quiz? Your progress will be lost.')) {
    backToList()
  }
}

const handleQuizCompleted = (finalScore) => {
  score.value = finalScore
  quizCompleted.value = true
  showResults.value = true
  showQuizTaker.value = false
}

const retakeQuiz = () => {
  showResults.value = false
  quizCompleted.value = false
  showQuizTaker.value = true
}

const backToList = () => {
  showQuizTaker.value = false
  currentQuiz.value = null
  showResults.value = false
  quizCompleted.value = false
}

onMounted(() => {
  const saved = localStorage.getItem(`quizzes_${libraryId.value}`)
  if (saved) {
    quizzes.value = JSON.parse(saved)
  } else {
    quizzes.value = [
      {
        id: 1,
        title: "Introduction to JavaScript",
        description: "Test your knowledge of basic JavaScript concepts",
        questions: [
          {
            text: "What is the correct way to declare a variable in JavaScript?",
            answers: [
              { text: "var myVariable = 5;" },
              { text: "variable myVariable = 5;" },
              { text: "v myVariable = 5;" },
              { text: "declare myVariable = 5;" }
            ],
            correctAnswer: 0
          },
          {
            text: "Which of the following is NOT a JavaScript data type?",
            answers: [
              { text: "String" },
              { text: "Boolean" },
              { text: "Float" },
              { text: "Number" }
            ],
            correctAnswer: 2
          }
        ],
        createdAt: new Date().toISOString(),
        libraryId: libraryId.value
      },
    ];
    localStorage.setItem(`quizzes_${libraryId.value}`, JSON.stringify(quizzes.value))
  }
})
</script>

<style scoped>
.quiz-manager {
  min-height: 100vh;
  background-color: #0a0a0a;
  color: #eee;
  display: flex;
  flex-direction: column;
  width: 100%;
}

.quiz-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #222 100%);
  border-bottom: 1px solid #333;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  flex-shrink: 0;
  width: 100%;
}

.header-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  border-radius: 0.75rem;
  border: 1px solid #444;
  background: rgba(255, 255, 255, 0.05);
  color: #ccc;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #555;
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  justify-content: center;
  background: linear-gradient(135deg, #fff 0%, #ccc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.025em;
}

.quiz-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  width: 100%;
  box-sizing: border-box;
}

.quiz-content.quiz-taking {
  padding: 0;
}

@media (max-width: 768px) {
  .quiz-header {
    padding: 1rem 1.5rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
    width: 100%;
  }
  
  .header-left {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .quiz-content {
    padding: 1rem;
  }
  
  .quiz-content.quiz-taking {
    padding: 0;
  }
}
</style>
