<template>
    <div class="home-slots-page">
        <header class="slots-hero">
            <RouterLink to="/home" class="back-link">
                <ArrowLeftCircle class="icon" />
                <span>Back to home</span>
            </RouterLink>
            <div class="hero-copy">
                <h1>Study Slots</h1>
                <p>
                    Spin the reels to pick a focus, then lock in a deep-work timer with built-in breaks. Choose from
                    your joined courses or improvise with a custom list every time you visit.
                </p>
            </div>
        </header>

        <section class="slots-section">
            <div v-if="loadError" class="error-banner">{{ loadError }}</div>
            <div v-if="isLoading" class="loading-overlay">
                <LoadingComponent />
                <p>Preparing your courses...</p>
            </div>
            <StudySlots
                mode="global"
                :available-libraries="libraryOptions"
                :default-library-ids="defaultLibraryIds"
            />
        </section>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/store/authStore';
import StudySlots from '@/components/Graphs/LearningPath/StudySlots.vue';
import LoadingComponent from '@/components/Backstage/LoadingComponent.vue';
import { ArrowLeftCircle } from 'lucide-vue-next';

type LibrarySummary = {
    id: number;
    library_topic: string;
};

const authStore = useAuthStore();
const isLoading = ref(true);
const loadError = ref('');
const myLibraries = ref<LibrarySummary[]>([]);
const archivedLibraries = ref<LibrarySummary[]>([]);

const loggedIn = computed(() => authStore.loggedIn);

async function fetchLibraries() {
    isLoading.value = true;
    loadError.value = '';

    try {
        if (!authStore.loggedIn) {
            myLibraries.value = [];
            archivedLibraries.value = [];
            return;
        }

        const response = await axios.get('/api/libraries');

        archivedLibraries.value = response.data.archived || [];

        const combinedLibraries = [
            ...response.data.mine,
            ...response.data.joined_public,
            ...response.data.joined_private
        ].filter((lib: LibrarySummary) => !archivedLibraries.value.some((archived) => archived.id === lib.id));

        myLibraries.value = combinedLibraries.sort((a, b) => a.library_topic.localeCompare(b.library_topic));
    } catch (error) {
        console.error('Failed to fetch libraries', error);
        loadError.value = 'We had trouble fetching your courses. You can still use a custom list in the slots.';
    } finally {
        isLoading.value = false;
    }
}

onMounted(() => {
    fetchLibraries();
});

watch(loggedIn, (value) => {
    if (value) {
        fetchLibraries();
    } else {
        myLibraries.value = [];
        archivedLibraries.value = [];
        isLoading.value = false;
        loadError.value = '';
    }
});

const libraryOptions = computed(() =>
    myLibraries.value.map((library) => ({
        id: library.id,
        name: library.library_topic
    }))
);

const defaultLibraryIds = computed(() => libraryOptions.value.slice(0, 3).map((option) => option.id));
</script>

<style scoped>
.home-slots-page {
    min-height: 100vh;
    padding: 2.5rem clamp(1rem, 4vw, 3rem) 4rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    color: var(--light-text, #e2e8f0);
}

.slots-hero {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.28), rgba(14, 165, 233, 0.22));
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 28px;
    padding: 2.5rem 3rem;
    box-shadow: 0 30px 60px rgba(15, 23, 42, 0.25);
}

.back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 1.1rem;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    background: rgba(15, 23, 42, 0.35);
    color: inherit;
    text-decoration: none;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.back-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px rgba(30, 64, 175, 0.35);
}

.hero-copy h1 {
    font-size: clamp(2rem, 4vw, 3rem);
    margin: 0;
    font-weight: 700;
    color: #f8fafc;
}

.hero-copy p {
    font-size: clamp(1rem, 1.3vw, 1.15rem);
    margin: 0;
    max-width: 46rem;
    line-height: 1.6;
    color: rgba(226, 232, 240, 0.85);
}

.slots-section {
    position: relative;
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 28px;
    padding: 2rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 24px 50px rgba(15, 23, 42, 0.4);
}

.error-banner {
    margin-bottom: 1rem;
    padding: 0.8rem 1.2rem;
    border-radius: 16px;
    background: rgba(248, 113, 113, 0.18);
    border: 1px solid rgba(248, 113, 113, 0.35);
    color: #fecaca;
    font-size: 0.95rem;
}

.loading-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    background: rgba(15, 23, 42, 0.55);
    border-radius: 28px;
    z-index: 2;
    color: rgba(226, 232, 240, 0.9);
}

.loading-overlay p {
    font-size: 1rem;
}

.icon {
    width: 1.25rem;
    height: 1.25rem;
}

@media (max-width: 768px) {
    .home-slots-page {
        padding: 1.8rem 1.1rem 3rem;
    }

    .slots-hero {
        padding: 2rem;
    }

    .slots-section {
        padding: 1.5rem;
    }
}
</style>
