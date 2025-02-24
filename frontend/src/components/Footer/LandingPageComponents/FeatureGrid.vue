<template>
    <div class="feature-grid">
      <!-- Header for the section -->
      <div class="header-container">
        <h2 class="header-title">Join These Amazing Students Today</h2>
        <p class="header-description">
          Discover how our app is helping students like you achieve their learning goals.
        </p>
      </div>
  
      <div class="features-container">
        <div v-for="(feature, index) in features" :key="index" class="feature-card">
          <div class="icon-container">
            <component :is="feature.icon" />
          </div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import {
    Brain,
    Book,
    Trophy,
    BarChart,
    Target,
    Users,
    MessageSquare,
    Rocket,
    Clock,
    Shield
  } from 'lucide-vue-next'
  
  export default {
    name: 'FeatureGrid',
    components: {
      Brain,
      Book,
      Trophy,
      BarChart,
      Target,
      Users,
      MessageSquare,
      Rocket,
      Clock,
      Shield
    },
    data() {
      return {
        features: [
          {
            "icon": "Brain",
            "title": "The app helped me focus on my weak areas and improve my understanding.",
            "description": "~Harvard 25'"
          },
          {
            "icon": "Book",
            "title": "I love the interactive lessons. They make learning so much more fun!",
            "description": "~Stanford 27'"
          },
          {
            "icon": "Trophy",
            "title": "The achievement system kept me motivated throughout my study sessions.",
            "description": "~NCSU 26'"
          },
          {
            "icon": "BarChart",
            "title": "I can clearly track my progress and see where I need to improve.",
            "description": "~UC Berkeley 28'"
          },
          {
            "icon": "Target",
            "title": "The app freed up so much of my time so I could focus on my final exams.",
            "description": "~Princeton 24'"
          },
          {
            "icon": "Users",
            "title": "I improved my GRE score by 15 points with the help of this app.",
            "description": "~MIT 29'"
          },
          {
            "icon": "MessageSquare",
            "title": "The AI tutor is a game changer. I get answers and explanations instantly.",
            "description": "~University of Chicago 27'"
          },
          {
            "icon": "Rocket",
            "title": "The quick start guides made it so easy to jump right into my studies.",
            "description": "~Columbia 25'"
          },
          {
            "icon": "Clock",
            "title": "Being able to learn at my own pace has been a life-saver during midterms.",
            "description": "~Yale 26'"
          },
          {
            "icon": "Shield",
            "title": "The knowledge validation quizzes helped solidify what I learned.",
            "description": "~Duke 28'"
          },
          {
            "icon": "Brain",
            "title": "The personalized learning paths really helped me master difficult concepts.",
            "description": "~UCLA 27'"
          },
          {
            "icon": "Trophy",
            "title": "Earning rewards as I progress has been a great motivator to keep studying.",
            "description": "~MIT 30'"
          }
        ]
      }
    }
  }
  </script>
  
  <style scoped>
  .feature-grid {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 4rem 1rem;
    background-color: var(--background-color);
  }
  
  .header-container {
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .header-title {
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.5rem;
  }
  
  .header-description {
    font-size: 1rem;
    color: #94a3b8;
    line-height: 1.5;
  }
  
  .features-container {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 2rem;
  }
  
  @media (min-width: 768px) {
    .features-container {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  @media (min-width: 1024px) {
    .features-container {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  
  .feature-card {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 1.5rem;
    border-radius: 0.5rem;
    background-color: var(--background-color-1t);
    border: 1px solid #134e4a;
    transition: all 0.3s ease;
  }
  
  .feature-card:hover {
    border-color: #14b8a6;
  }
  
  .icon-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    background-color: var(--background-color);
    margin-bottom: 1rem;
    padding: 0.5rem;
  }
  
  .icon-container :deep(svg) {
    width: 1.5rem;
    height: 1.5rem;
    color: #14b8a6;
  }
  
  .feature-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: white;
    margin-bottom: 0.5rem;
  }
  
  .feature-description {
    font-size: 0.875rem;
    color: #94a3b8;
    line-height: 1.5;
  }
  </style>
  