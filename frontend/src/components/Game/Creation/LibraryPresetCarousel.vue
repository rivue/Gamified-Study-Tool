<template>
    <div class="preset-carousel-container">
      <h3 class="carousel-title">Start with a Preset</h3>
      <div class="carousel">
        <div
          v-for="(preset, index) in presets"
          :key="index"
          class="preset-card"
          @click="selectPreset(preset)"
        >
          <div class="preset-card-content">
            <h4 class="preset-name">{{ preset.displayName }}</h4>
            <p class="preset-description">{{ preset.courseName }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineEmits } from 'vue';
  
  interface Preset {
    displayName: string;
    courseName: string;
    topicName: string;
    subTopicNames: string[];
    pdfPlaceholderFileName: string;
  }
  
  const presets: Preset[] = [
    {
      displayName: 'Python Programming',
      courseName: 'Introduction to Python',
      topicName: 'Python Basics',
      subTopicNames: ['Variables & Data Types', 'Control Flow', 'Functions', 'File I/O'],
      pdfPlaceholderFileName: 'python_basics.pdf',
    },
    {
      displayName: 'World History',
      courseName: 'Ancient Civilizations',
      topicName: 'Ancient Rome',
      subTopicNames: ['The Roman Republic', 'The Roman Empire', 'Fall of Rome', 'Roman Mythology'],
      pdfPlaceholderFileName: 'ancient_rome.pdf',
    },
    {
      displayName: 'Creative Writing',
      courseName: 'Fiction Writing Workshop',
      topicName: 'Elements of Fiction',
      subTopicNames: ['Character Development', 'Plot & Structure', 'Setting & Worldbuilding', 'Dialogue'],
      pdfPlaceholderFileName: 'fiction_writing.pdf',
    },
    {
      displayName: 'Digital Marketing',
      courseName: 'Social Media Marketing',
      topicName: 'Platform Strategies',
      subTopicNames: ['Facebook & Instagram', 'Twitter (X)', 'LinkedIn', 'TikTok'],
      pdfPlaceholderFileName: 'social_media_marketing.pdf',
    },
    {
      displayName: 'Personal Finance',
      courseName: 'Managing Your Money',
      topicName: 'Budgeting & Saving',
      subTopicNames: ['Creating a Budget', 'Saving Strategies', 'Investing Basics', 'Debt Management'],
      pdfPlaceholderFileName: 'personal_finance.pdf',
    },
    {
      displayName: 'Graphic Design',
      courseName: 'Fundamentals of Design',
      topicName: 'Core Principles',
      subTopicNames: ['Color Theory', 'Typography', 'Layout & Composition', 'Branding Basics'],
      pdfPlaceholderFileName: 'graphic_design_fundamentals.pdf',
    },
    {
      displayName: 'Music Theory',
      courseName: 'Introduction to Music',
      topicName: 'Musical Elements',
      subTopicNames: ['Rhythm & Meter', 'Melody & Harmony', 'Scales & Modes', 'Chord Progressions'],
      pdfPlaceholderFileName: 'music_theory_intro.pdf',
    },
    {
      displayName: 'Data Science',
      courseName: 'Data Analysis with Pandas',
      topicName: 'Data Manipulation',
      subTopicNames: ['DataFrames & Series', 'Data Cleaning', 'Grouping & Aggregation', 'Data Visualization Intro'],
      pdfPlaceholderFileName: 'pandas_data_analysis.pdf',
    },
  ];
  
  const emit = defineEmits(['preset-selected']);
  
  const selectPreset = (preset: Preset) => {
    emit('preset-selected', preset);
  };
  </script>
  
  <style scoped>
  /* Define a CSS variable for the carousel background for easier reuse in gradients */
  :root {
    --carousel-bg-color: rgba(26, 139, 127, 0.03);
  }
  
  .preset-carousel-container {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background-color: var(--carousel-bg-color); /* Use variable */
    border-radius: 12px;
    border: 1px solid rgba(26, 139, 127, 0.1);
    /* position: relative; /* Not strictly needed here if pseudo-elements are on .carousel */
  }
  
  .carousel-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-color, #2c3e50); /* Fallback color */
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .carousel {
    display: flex;
    overflow-x: auto;
    padding-bottom: 1rem; /* Space for scrollbar if it were visible */
    padding-top: 1rem;
    gap: 1rem;
    position: relative; /* Needed for the pseudo-elements to be positioned correctly */
  }
  
  /* Hide scrollbar for WebKit browsers */
  .carousel::-webkit-scrollbar {
    display: none;
  }
  
  /* Hide scrollbar for IE, Edge, and Firefox */
  .carousel {
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;  /* Firefox */
  }
  
  /* Subtle fade edges for the carousel */
  .carousel::before,
  .carousel::after {
    content: '';
    position: absolute;
    top: 0;
    bottom: 1rem; /* Align with padding-bottom of .carousel to avoid overlap if scrollbar was visible */
    width: 40px;   /* Width of the fade effect */
    pointer-events: none; /* Allows clicking through the fade */
    z-index: 2; /* Ensure it's above cards */
  }
  
  .carousel::before {
    left: 0;
    background: linear-gradient(to right, var(--carousel-bg-color) 15%, transparent);
  }
  
  .carousel::after {
    right: 0;
    background: linear-gradient(to left, var(--carousel-bg-color) 15%, transparent);
  }
  
  .preset-card {
    flex: 0 0 auto;
    width: 220px;
    background: var(--background-color-1t, rgba(255, 255, 255, 0.7)); /* Fallback */
    backdrop-filter: blur(6px); /* Slightly more blur */
    border-radius: 10px;
    border: 1px solid rgba(26, 139, 127, 0.15); /* Softer border */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* Softer, more diffused shadow */
    cursor: pointer;
    transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), border-color 0.3s ease;
    overflow: hidden;
  }
  
  .preset-card:hover {
    transform: translateY(-5px); /* Slightly more lift */
    box-shadow: 0 8px 18px rgba(26, 139, 127, 0.18); /* Enhanced shadow on hover */
    border-color: var(--color-primary-light, #1de9b6); /* Fallback primary color */
  }
  
  .preset-card-content {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }
  
  .preset-name {
    font-size: 1.05rem; /* Slightly refined size */
    font-weight: 600;
    color: var(--text-color, #2c3e50); /* Fallback color */
    margin-bottom: 0.5rem;
    line-height: 1.3;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .preset-description {
    font-size: 0.82rem; /* Slightly refined size */
    color: var(--text-color-secondary, #555e66); /* Fallback color */
    line-height: 1.45; /* Adjusted for readability */
    white-space: normal;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    min-height: calc(0.82rem * 1.45 * 2); /* font-size * line-height * 2 lines */
    /* max-height is implicitly handled by -webkit-line-clamp for webkit browsers */
  }
  </style>
  