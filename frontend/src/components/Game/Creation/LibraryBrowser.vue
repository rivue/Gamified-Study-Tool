<template>
    <div class="home-page">
        <div v-if="isLoading" class="home-loading">
            <LoadingComponent />
            <p>Loading your study dashboard...</p>
        </div>

        <template v-else>
            <section class="home-hero">
                <div class="hero-copy">
                    <span class="hero-badge">Home</span>
                    <h1>Spin into your next study session</h1>
                    <p>
                        Study Slots now lives on your home page so you can plan focused work and
                        manage your courses from one place.
                    </p>
                </div>
                <div v-if="loggedIn" class="hero-stats">
                    <div class="stat-card">
                        <span class="stat-value">{{ activeCourseCount }}</span>
                        <span class="stat-label">Active courses</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{{ archivedLibraries.length }}</span>
                        <span class="stat-label">Archived</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{{ favoriteCount }}</span>
                        <span class="stat-label">Favorites</span>
                    </div>
                </div>
            </section>

            <section class="home-panels">
                <div class="slots-panel">
                    <div class="panel-header">
                        <div>
                            <h2>Study Slots</h2>
                            <p>
                                Pick the courses you want to spin or type a quick custom list whenever
                                inspiration strikes.
                            </p>
                        </div>
                    </div>
                    <div v-if="loadError" class="panel-error">{{ loadError }}</div>
                    <StudySlots
                        mode="global"
                        :available-libraries="libraryOptions"
                        :default-library-ids="defaultLibraryIds"
                    />
                </div>

                <div class="courses-panel">
                    <LibraryCarousel
                        v-if="loggedIn"
                        :libraries="myLibraries"
                        :archived-libraries="archivedLibraries"
                        :library-favorites-map="favoritesMap"
                        @libraryJoined="fetchLibraries"
                        @archive-status-changed="fetchLibraries"
                    />
                    <div v-else class="guest-message">
                        <h2>Log in to view courses</h2>
                        <p>
                            Create or join a course to unlock a personalized Study Slots experience
                            and track your progress.
                        </p>
                    </div>
                </div>
            </section>
        </template>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import LoadingComponent from "@/components/Backstage/LoadingComponent.vue";
import LibraryCarousel from "@/components/Game/Creation/LibraryCarousel.vue";
import StudySlots from "@/components/Graphs/LearningPath/StudySlots.vue";

interface LibraryOption {
    id: number;
    name: string;
}

const authStore = useAuthStore();
const isLoading = ref(true);
const myLibraries = ref<any[]>([]);
const archivedLibraries = ref<any[]>([]);
const favoritesMap = ref<Record<number, boolean>>({});
const loadError = ref("");

const loggedIn = computed(() => authStore.loggedIn);

async function fetchLibraries() {
    isLoading.value = true;
    loadError.value = "";

    try {
        if (!authStore.loggedIn) {
            myLibraries.value = [];
            archivedLibraries.value = [];
            favoritesMap.value = {};
            return;
        }

        const response = await axios.get("/api/libraries");

        archivedLibraries.value = response.data.archived || [];

        const combinedLibraries = [
            ...response.data.mine,
            ...response.data.joined_public,
            ...response.data.joined_private
        ].filter((lib: any) => !archivedLibraries.value.some((archived: any) => archived.id === lib.id));

        myLibraries.value = combinedLibraries.sort((a: any, b: any) =>
            a.library_topic.localeCompare(b.library_topic)
        );

        favoritesMap.value = response.data.favorites_map || {};
    } catch (error) {
        console.error("Failed to fetch libraries", error);
        loadError.value = "We had trouble fetching your courses. Please try again.";
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
        favoritesMap.value = {};
    }
});

const libraryOptions = computed<LibraryOption[]>(() =>
    myLibraries.value.map((library: any) => ({
        id: library.id,
        name: library.library_topic
    }))
);

const defaultLibraryIds = computed(() =>
    libraryOptions.value.slice(0, 3).map((option) => option.id)
);

const favoriteCount = computed(() => Object.values(favoritesMap.value || {}).filter(Boolean).length);
const activeCourseCount = computed(() => myLibraries.value.length);
</script>

<style scoped>
.home-page {
    width: 100%;
    min-height: 100vh;
    padding: 2rem clamp(1rem, 4vw, 3rem) 4rem;
    box-sizing: border-box;
    color: var(--light-text, #e2e8f0);
}

.home-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-top: 4rem;
    color: var(--text-color, #cbd5f5);
}

.home-loading p {
    font-size: 1.1rem;
}

.home-hero {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    padding: 2.5rem 3rem;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.28), rgba(14, 165, 233, 0.22));
    border: 1px solid rgba(148, 163, 184, 0.25);
    box-shadow: 0 30px 60px rgba(15, 23, 42, 0.25);
}

.hero-copy {
    flex: 1;
    min-width: 260px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.4rem 0.75rem;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.35);
    border: 1px solid rgba(148, 163, 184, 0.35);
    margin-bottom: 1rem;
}

.hero-copy h1 {
    font-size: clamp(1.8rem, 3vw, 2.8rem);
    margin: 0 0 0.75rem 0;
    font-weight: 700;
    color: #f8fafc;
}

.hero-copy p {
    font-size: clamp(1rem, 1.2vw, 1.15rem);
    max-width: 38rem;
    color: rgba(241, 245, 249, 0.85);
    line-height: 1.6;
    margin: 0;
}

.hero-stats {
    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    flex: 1;
    min-width: 220px;
}

.stat-card {
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid rgba(148, 163, 184, 0.35);
    border-radius: 20px;
    padding: 1.5rem 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    text-align: left;
    backdrop-filter: blur(8px);
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #f8fafc;
}

.stat-label {
    font-size: 0.95rem;
    color: rgba(226, 232, 240, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.home-panels {
    display: grid;
    gap: 2rem;
    margin-top: 2.5rem;
}

@media (min-width: 1200px) {
    .home-panels {
        grid-template-columns: minmax(0, 0.85fr) minmax(0, 1.15fr);
        align-items: start;
    }
}

.slots-panel {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 28px;
    padding: 2rem;
    box-shadow: 0 24px 50px rgba(15, 23, 42, 0.4);
    backdrop-filter: blur(14px);
    color: rgba(226, 232, 240, 0.95);
}

.panel-header {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

.panel-header h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
}

.panel-header p {
    font-size: 1rem;
    color: rgba(226, 232, 240, 0.8);
    margin: 0;
    max-width: 32rem;
    line-height: 1.6;
}

.panel-error {
    margin-bottom: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    background: rgba(248, 113, 113, 0.12);
    border: 1px solid rgba(248, 113, 113, 0.35);
    color: #fecaca;
    font-size: 0.95rem;
}

.courses-panel {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 28px;
    padding: 2rem 0;
    box-shadow: 0 24px 40px rgba(15, 23, 42, 0.35);
    backdrop-filter: blur(12px);
}

.guest-message {
    padding: 3rem;
    text-align: center;
    color: rgba(226, 232, 240, 0.85);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    align-items: center;
}

.guest-message h2 {
    font-size: 1.8rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
}

.guest-message p {
    font-size: 1rem;
    max-width: 22rem;
    line-height: 1.6;
    margin: 0;
}

@media (max-width: 768px) {
    .home-page {
        padding: 1.5rem 1rem 3rem;
    }

    .home-hero {
        padding: 2rem;
    }

    .slots-panel {
        padding: 1.5rem;
    }

    .courses-panel {
        padding: 1.5rem 0.5rem;
    }
}
</style>
