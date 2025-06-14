<template>
    <div class="features-component">
      <div class="feature" v-for="(feature, index) in features" :key="index">
        <div class="feature-icon">{{ feature.icon }}</div>
        <div class="feature-title">{{ feature.title }}</div>
        <div class="feature-description">{{ feature.description }}</div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted, ref } from 'vue';
  
  const features = ref([
    {
      icon: '🧠',
      title: 'Interactive Quizzes',
      description: 'Test your skills, reinforce your memory, and master tough concepts—effortlessly.'
    },
    {
      icon: '📖',
      title: 'Dynamic Study Modules',
      description: 'Learn at your pace, from bite-sized refreshers to deep dives—tailored exactly to you.'
    },
    {
      icon: '👥',
      title: 'Community Connection',
      description: 'Never study alone again. Join supportive groups that celebrate your progress every step of the way.'
    },
    {
      icon: '🏆',
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
    gap: 20px;
    padding-top: 3em;
    padding-bottom: 1em;
}

.feature {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 10px;
    border: 1px solid #ccccccaa;
    border-radius: 8px;
    opacity: 0;
    transform: translateY(-60px);
    background: var(--background-color-2t);
    /* Remove transition properties that suggest interactivity */
}

/* Remove hover effect */
.feature.selected {
    background: var(--background-color-1t);
    border: 1px solid #ccc;
}

.feature.visible {
    animation: fadeSlideIn 0.3s ease-out forwards;
}

.feature-title {
    font-weight: 700;
    padding-bottom: 0.5em;
}

.feature-icon {
    left: 3px;
    top: 3px;
    font-size: 24px;
    position: absolute;
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
        transform: translateY(-40px);
    }
}
  </style>
  