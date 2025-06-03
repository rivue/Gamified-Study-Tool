<template>
    <div 
     class="experiments-portal">
        <div class="brain-dump-container">
            <div class="fixed top-20 left-12 flex gap-6 z-10">

                <button @click="back"
                    class="menu-button bg-background-color-1t backdrop-blur-sm shadow-md rounded-lg p-4 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200"
                    style="color: var(--highlight-color);">
                    <ArrowLeftOnRectangleIcon class="w-6 h-6" />
                </button>
            </div>
        </div>
        <header class="portal-header">
            <h1 style="color: var(--text-color);">Experiments</h1>
            <p>Different methods of studying</p>
        </header>

        <div class="experiments-grid ">
            <div v-for="experiment in experiments" :key="experiment.id" class="experiment-card"
                @click="navigateToExperiment(experiment.route)">
                <div class="card-icon">
                    <i :class="experiment.icon"></i>
                </div>
                <h3 style="color: var(--text-color);">{{ experiment.title }}</h3>
                <p>{{ experiment.description }}</p>
                <div class="card-footer">
                    <span class="difficulty" :class="experiment.difficulty">
                        {{ experiment.difficulty }}
                    </span>
                    <span class="duration">{{ experiment.duration }}</span>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">

import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ArrowLeftOnRectangleIcon } from '@heroicons/vue/24/outline';

interface Experiment {
    id: number;
    title: string;
    description: string;
    icon: string;
    difficulty: string;
    duration: string;
    route: string;
}

const route = useRoute();
const router = useRouter();
const params = ref(route.params);
const experiments: Experiment[] = [
    {
        id: 1,
        title: 'Brain Dump',
        description: 'Recall everything you remember about a topic',
        icon: 'fas fa-layer-group',
        difficulty: 'easy',
        duration: '5-15 min',
        route: 'braindump'
    },
    {
        id: 2,
        title: 'Flashcards',
        description: 'Quick-fire question and answer sessions',
        icon: 'fas fa-layer-group',
        difficulty: 'easy',
        duration: '5-15 min',
        route: 'asdf',
    },
    {
        id: 3,
        title: 'Quiz Mode',
        description: 'Timed multiple choice questions',
        icon: 'fas fa-clock',
        difficulty: 'medium',
        duration: '10-30 min',
        route: 'asdf',
    },
    {
        id: 4,
        title: 'Study Games',
        description: 'Gamified learning with points and rewards',
        icon: 'fas fa-gamepad',
        difficulty: 'easy',
        duration: '15-45 min',
        route: 'asdf',
    },
    {
        id: 5,
        title: 'Practice Tests',
        description: 'Full-length exam simulations',
        icon: 'fas fa-file-alt',
        difficulty: 'hard',
        duration: '30-120 min',
        route: 'asdf',
    },
    {
        id: 6,
        title: 'Spaced Repetition',
        description: 'AI-powered review scheduling',
        icon: 'fas fa-brain',
        difficulty: 'medium',
        duration: '10-20 min',
        route: 'asdf',
    },
    {
        id: 7,
        title: 'Memory Palace',
        description: 'Visual learning and memory techniques',
        icon: 'fas fa-building',
        difficulty: 'hard',
        duration: '20-60 min',
        route: 'asdf',
    }
];

function back() {
    router.push(`/lessons/${params.value.id}`);
}

function navigateToExperiment(route: string) {
    router.push(`/lessons/${params.value.id}/${route}`);
}

</script>

<style scoped>
.experiments-portal {
    padding: 2rem;
}

.portal-header {
    text-align: center;
    margin-bottom: 3rem;
}

.portal-header h1 {
    font-size: 2.5rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

.portal-header p {
    font-size: 1.2rem;
    color: #7f8c8d;
}

.experiments-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.experiment-card {
    background-color: var(--background-color-1t);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid var(--color-primary-dark);
}

.experiment-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    background-color: var(--element-color-1);
}

.card-icon {
    text-align: center;
    margin-bottom: 1rem;
}

.card-icon i {
    font-size: 3rem;
    color: #3498db;
}

.experiment-card h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #2c3e50;
    text-align: center;
}

.experiment-card p {
    color: #7f8c8d;
    text-align: center;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.difficulty {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
}

.difficulty.easy {
    background: #d5f4e6;
    color: #27ae60;
}

.difficulty.medium {
    background: #fef9e7;
    color: #f39c12;
}

.difficulty.hard {
    background: #fadbd8;
    color: #e74c3c;
}

.duration {
    color: #95a5a6;
    font-size: 0.9rem;
}

.menu-button {
    border-radius: 10px;
    background-color: var(--background-color-1t);
    color: var(--highlight-color);
    border: 1px solid var(--color-primary-dark);
    transition: all 0.2s ease;
}

.menu-button:hover {
    background-color: var(--element-color-1);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.menu-button:active {
    transform: translateY(0);
}

.menu-button.selected {
    background-color: var(--element-color-1);
    border-color: var(--color-primary);
    color: var(--light-text);
}
</style>