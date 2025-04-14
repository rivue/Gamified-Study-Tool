<template>
    <div class="feature-grid">
      <div class="header-container">
        <h2 class="header-title">Join These Amazing Students Today</h2>
        <p class="header-description">
          Discover how our app is helping students like you achieve their learning goals.
        </p>
      </div>
  
      <Carousel
        :value="features" 
        :numVisible="3" 
        :numScroll="1"
        :responsiveOptions="responsiveOptions" 
        circular 
        :autoplayInterval="2000"
      >
        <template #item="slotProps">
          <div class="feature-card">
            <div class="icon-container">
              <component :is="slotProps.data.icon" />
            </div>
            <h3 class="feature-title">{{ slotProps.data.title }}</h3>
            <p class="feature-description">{{ slotProps.data.description }}</p>
          </div>
        </template>
      </Carousel>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
  import { 
    Brain, Book, Trophy, BarChart, Target, Users, 
    MessageSquare, Rocket, Clock, Shield 
  } from 'lucide-vue-next';
  import Carousel from 'primevue/carousel';
  
  const features = ref([
    { icon: Brain, title: "The app helped me focus on my weak areas and improve my understanding.", description: "~Harvard 25'" },
    { icon: Book, title: "I love the interactive lessons. They make learning so much more fun!", description: "~Stanford 27'" },
    { icon: Trophy, title: "The achievement system kept me motivated throughout my study sessions.", description: "~NCSU 26'" },
    { icon: BarChart, title: "I can clearly track my progress and see where I need to improve.", description: "~UC Berkeley 28'" },
    { icon: Target, title: "The app freed up so much of my time so I could focus on my final exams.", description: "~Princeton 24'" },
    { icon: Users, title: "I improved my GRE score by 15 points with the help of this app.", description: "~MIT 29'" },
    { icon: MessageSquare, title: "The AI tutor is a game changer. I get answers and explanations instantly.", description: "~University of Chicago 27'" },
    { icon: Rocket, title: "The quick start guides made it so easy to jump right into my studies.", description: "~Columbia 25'" },
    { icon: Clock, title: "Being able to learn at my own pace has been a life-saver during midterms.", description: "~Yale 26'" },
    { icon: Shield, title: "The knowledge validation quizzes helped solidify what I learned.", description: "~Duke 28'" },
    { icon: Brain, title: "The personalized learning paths really helped me master difficult concepts.", description: "~UCLA 27'" },
    { icon: Trophy, title: "Earning rewards as I progress has been a great motivator to keep studying.", description: "~MIT 30'" },
  ]);
  
  const responsiveOptions = ref([
    { breakpoint: '1024px', numVisible: 2, numScroll: 1 },
    { breakpoint: '768px', numVisible: 1, numScroll: 1 }
  ]);
  
  const slides = computed(() => {
    const s = [];
    const perSlide = 3;
    for (let i = 0; i < features.value.length; i += perSlide) {
      s.push(features.value.slice(i, i + perSlide));
    }
    return s;
  });
  
  const totalSlides = computed(() => slides.value.length);
  
  onMounted(() => {
    // Placeholder for animation state setup if needed
  });
  
  onBeforeUnmount(() => {
    // Cleanup logic if needed
  });
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
  .features-container-grid {
   display: grid;
   grid-template-columns: repeat(1, 1fr);
   gap: 2rem;
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
 .carousel-container {
 overflow: hidden;
 width: 100%;
 padding: 0 1rem;
 perspective: 1000px;
 }
 
 
   .features-container-grid {
    display: flex;
    transition: transform 0.5s ease;
    width: 100%;
    box-sizing: border-box;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    will-change: transform;
  }
   .feature-card {
    min-width: 0;
    transform-style: preserve-3d;
    transition:
      transform 0.38s ease,
      border-color 0.3s ease;
  }
   .feature-card.out {
    transform: rotateX(90deg);
    transition: transform 0.32s cubic-bezier(0.6, 0, 0.7, 0.2);
  }
   .feature-card.in {
    transform: rotateX(0deg);
  }
   .feature-card.behind {
    transform: rotateX(-90deg);
  }
   /* Existing styles remain mostly the same */
  .carousel-indicators {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 2rem;
  }
   .indicator {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    background-color: #94a3b8;
    border: none;
    cursor: pointer;
    padding: 0;
  }
   .indicator.active {
    background-color: #14b8a6;
  }
   @media (max-width: 1024px) {
    .slide {
      grid-template-columns: repeat(2, 1fr);
    }
  }
   @media (max-width: 768px) {
    .slide {
      grid-template-columns: 1fr;
    }
  }
   /* Keep all other existing styles below */
  </style>
 
 
 
 