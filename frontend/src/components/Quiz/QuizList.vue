<template>
  <div class="quiz-list">
    <div v-if="quizzes.length === 0" class="empty-state">
      <div class="empty-icon">
        <ClipboardDocumentListIcon class="w-24 h-24" />
      </div>
      <h2>No Quizzes Yet</h2>
      <p>Create your first multiple-choice quiz to get started!</p>
      <button @click="$emit('create-quiz')" class="create-first-quiz-btn">
        <PlusIcon class="w-5 h-5" />
        Create Your First Quiz
      </button>
    </div>
    
    <div v-else class="quiz-list-container">
      <div v-for="quiz in quizzes" :key="quiz.id" class="quiz-item" @click="$emit('take-quiz', quiz)">
        <div class="quiz-item-icon">
          <ClipboardDocumentListIcon class="w-6 h-6" />
        </div>
        <div class="quiz-item-details">
          <h3 class="quiz-item-title">{{ quiz.title }}</h3>
          <p class="quiz-item-description">{{ quiz.description || 'No description provided' }}</p>
        </div>
        <div class="quiz-item-meta">
          <span class="meta-questions">{{ quiz.questions.length }} Qs</span>
          <div class="quiz-item-actions">
            <button @click.stop="$emit('edit-quiz', quiz)" class="action-btn edit-btn" title="Edit Quiz">
              <PencilIcon class="w-4 h-4" />
            </button>
            <button @click.stop="$emit('delete-quiz', quiz.id)" class="action-btn delete-btn" title="Delete Quiz">
              <TrashIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ClipboardDocumentListIcon, PlusIcon, PencilIcon, TrashIcon } from '@heroicons/vue/24/solid'

defineProps<{
  quizzes: Array<any>
}>()

defineEmits<{
  'create-quiz': []
  'take-quiz': [quiz: any]
  'edit-quiz': [quiz: any]
  'delete-quiz': [quizId: number]
}>()
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 6rem 2rem;
  max-width: 600px;
  margin: 4rem auto;
  background: linear-gradient(135deg, #1a1a1a 0%, #222 100%);
  border-radius: 1.5rem;
  border: 1px solid #333;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.empty-icon {
  margin-bottom: 1.5rem;
  opacity: 0.6;
  color: #888;
}

.empty-state h2 {
  margin: 0 0 1rem;
  font-size: 1.75rem;
  font-weight: 600;
  color: #fff;
}

.empty-state p {
  color: #aaa;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  line-height: 1.6;
}

.create-first-quiz-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: var(--accent-color-1);
  color: var(--light-text);
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.create-first-quiz-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px var(--accent-color-1-t);
}

.quiz-list-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  width: 100%;
}

.quiz-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background-color: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quiz-item:hover {
  background-color: #222;
  border-color: var(--accent-color-1);
  transform: translateY(-2px);
}

.quiz-item-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  background: var(--accent-color-1-t);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent-color-1);
}

.quiz-item-details {
  flex: 1;
}

.quiz-item-title {
  margin: 0 0 0.25rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #fff;
}

.quiz-item-description {
  margin: 0;
  color: #aaa;
  font-size: 0.9rem;
}

.quiz-item-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #888;
}

.meta-questions {
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
}

.quiz-item-actions {
  display: flex;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.quiz-item:hover .quiz-item-actions {
  opacity: 1;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-btn {
  background-color: #333;
  color: #eee;
}

.edit-btn:hover {
  background-color: #444;
}

.delete-btn {
  background-color: #442222;
  color: #ff8888;
}

.delete-btn:hover {
  background-color: #ef4444;
  color: white;
}

@media (max-width: 768px) {
  .quiz-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .quiz-item-meta {
    width: 100%;
    justify-content: space-between;
  }

  .quiz-item-actions {
    opacity: 1;
  }
}
</style>
