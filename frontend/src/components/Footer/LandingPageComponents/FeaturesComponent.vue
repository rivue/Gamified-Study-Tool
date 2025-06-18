<template>
  <div class="features-component">
    <div class="feature" v-for="(feature, index) in features" :key="index">
    <div class="feature-icon-wrapper">
      <component :is="feature.icon" class="feature-icon" />
    </div>
    <h3 class="feature-title">{{ feature.title }}</h3>
    <p class="feature-description">{{ feature.description }}</p>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import {
  AcademicCapIcon,
  BookOpenIcon,
  UserGroupIcon,
  TrophyIcon
} from '@heroicons/vue/24/solid';

const features = ref([
  {
  icon: AcademicCapIcon,
  title: 'Interactive Quizzes',
  description: 'Test your skills, reinforce your memory, and master tough concepts—effortlessly.'
  },
  {
  icon: BookOpenIcon,
  title: 'Dynamic Study Modules',
  description: 'Learn at your pace, from bite-sized refreshers to deep dives—tailored exactly to you.'
  },
  {
  icon: UserGroupIcon,
  title: 'Community Connection',
  description: 'Never study alone again. Join supportive groups that celebrate your progress every step of the way.'
  },
  {
  icon: TrophyIcon,
  title: 'Friendly Competition',
  description: 'Challenge your friends, climb the ranks, and turn studying into a game you can\'t stop playing.'
  },
]);

function observeFeatures() {
  const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
    entry.target.classList.add('visible');
    }
  });
  }, { threshold: 0.1 });

  document.querySelectorAll('.feature').forEach((feature) => {
  observer.observe(feature);
  });
}

onMounted(() => {
  observeFeatures();
});
</script>

<style scoped>
.features-component {
  max-width: 1200px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2.5rem;
  padding: 4rem 0;
}

.feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
  border-radius: 1rem;
  opacity: 0;
  transform: translateY(-60px);
  background: var(--background-color-2t);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
}

.feature-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  background: var(--background-color-1t);
  margin-bottom: 1rem;
}

.feature-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--text-color);
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--text-color);
}

.feature-description {
  font-size: 1rem;
  line-height: 1.5;
  color: var(--text-color-secondary);
}

@media (max-width: 1000px) {
  .features-component {
  grid-template-columns: 1fr;
  }
}

@keyframes fadeSlideIn {
  from {
  opacity: 0;
  transform: translateY(-60px);
  }
  to {
  opacity: 1;
  transform: translateY(0);
  }
}

.feature.visible {
  animation: fadeSlideIn 0.5s ease-out forwards;
}

  </style>
  