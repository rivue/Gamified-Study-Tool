<template>
    <div class="course-explorer">
        <div class="header-container">
            <div class="header-content">
                <h1 class="title">Explore Courses</h1>
                <p class="subtitle">Discover and join courses created by the community</p>
            </div>

            <div class="join-course-container">
                <div class="join-form">
                    <Input v-model="joinCode" placeholder="Enter private library code..." @keydown.enter="joinCourse"
                        class="join-input" />
                    <Button @click="joinCourse" :disabled="joinPrivateLoading" class="join-button">
                        <LoaderCircle v-if="joinPrivateLoading" class="mr-2 h-4 w-4 animate-spin" />
                        Join Private Course
                    </Button>
                </div>
                <Transition name="fade">
                    <div v-if="joinPrivateMessage" :class="['join-message', joinPrivateMessageType]">
                        {{ joinPrivateMessage }}
                    </div>
                </Transition>
            </div>
        </div>

        <div class="search-container">
            <Search class="search-icon" />
            <Input v-model="searchQuery" @input="filterLibraries" @keydown="handleSearchKeydown"
                placeholder="Search courses..." class="search-input" />
        </div>

        <!-- Course cards container -->
        <div v-if="filteredLibraries.length > 0" class="courses-container" ref="libraryContainer">
            <div class="courses-grid">
                <div v-for="library in displayedLibraries" :key="library.id" class="course-card">
                    <div class="card-content">
                        <div class="card-header">
                            <div class="difficulty-badge" :class="getDifficultyClass(library.difficulty)">
                                {{ library.difficulty || 'All Levels' }}
                            </div>
                            <div class="card-meta">
                                <span class="language-tag">{{ library.language || 'General' }}</span>
                                <span v-if="library.language_difficulty" class="language-level">{{
                                    library.language_difficulty }}</span>
                            </div>
                        </div>

                        <h3 class="course-title">{{ library.library_topic }}</h3>

                        <div class="card-stats">
                            <div class="stat">
                                <Eye class="stat-icon" />
                                <span>{{ library.clicks || 0 }}</span>
                            </div>
                            <div class="stat">
                                <Heart class="stat-icon" />
                                <span>{{ library.likes || 0 }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-footer">
                        <div class="creator">
                            <UserCircle class="creator-icon" />
                            <span>{{ library.owner_id }}</span>
                        </div>

                        <Button 
                        v-if="!joinedCourses.has(library.id)"
                        @click="joinSpecificCourse(library.id)" 
                        :disabled="joinPublicLoading"
                            class="join-card-button">
                            <LoaderCircle v-if="joinPublicLoading" class="mr-2 h-4 w-4 animate-spin" />
                            Join
                        </Button>
                        <Button
                        v-else
                        @click="goToCourse(library.id)"
                        class="joined-card-button">
                            Go to Course
                        </Button>
                    </div>
                    <Transition name="fade">
                        <div v-if="joinPublicMessage" :class="['join-message', joinPublicMessageType]">
                            {{ joinPublicMessage }}
                        </div>
                    </Transition>
                </div>
            </div>

            <!-- Loading indicator for infinite scroll -->
            <div v-if="isLoading" class="loading-indicator">
                <LoaderCircle class="loader-icon" />
                <span>Loading more courses...</span>
            </div>

            <!-- End of results message -->
            <div v-if="!hasMoreToLoad && displayedLibraries.length > 0" class="end-message">
                You've reached the end of the list
            </div>
        </div>

        <!-- Display this when there are no libraries -->
        <div v-else class="empty-state">
            <BookOpen class="empty-icon" />
            <h3 class="empty-title">No Courses Found</h3>
            <p class="empty-description">
                You don't have any courses yet. Create your first course or join one using a course code to get started.
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { LoaderCircle, Search, Eye, Heart, UserCircle, BookOpen } from "lucide-vue-next";
import axios from "axios";

// Props
const props = defineProps<{
    libraries: Array<{
        clicks: number;
        context: any;
        difficulty: string;
        guide: string;
        id: number;
        image_url: string,
        language: string;
        language_difficulty: string;
        likes: number;
        library_topic: string;
        owner_id: string;
    }>;
}>();

// State
const router = useRouter();
const searchQuery = ref("");
const filteredLibraries = ref<Array<any>>([]);
const displayedLibraries = ref<Array<any>>([]);
const joinCode = ref("");
const joinPrivateMessage = ref("");
const joinPrivateMessageType = ref("");
const joinPrivateLoading = ref(false);
const joinPublicMessage = ref("");
const joinPublicMessageType = ref("");
const joinPublicLoading = ref(false);
const libraryContainer = ref<HTMLElement | null>(null);
const joinedCourses = ref(new Set());

// Infinite scroll states
const itemsPerLoad = 6;
const currentLoadIndex = ref(0);
const isLoading = ref(false);
const hasMoreToLoad = ref(true);

// so parent can refresh list
const emit = defineEmits(['libraryJoined']);

// Filtering function
function filterLibraries() {
    let libraries = [...props.libraries];

    if (!searchQuery.value.trim()) {
        filteredLibraries.value = libraries;
    } else {
        const query = searchQuery.value.toLowerCase();
        filteredLibraries.value = libraries.filter(library =>
            library.library_topic.toLowerCase().includes(query)
        );
    }

    // Reset infinite scroll when filtering
    resetInfiniteScroll();
    loadMoreItems();
}

function resetInfiniteScroll() {
    displayedLibraries.value = [];
    currentLoadIndex.value = 0;
    hasMoreToLoad.value = true;
}

function loadMoreItems() {
    if (!hasMoreToLoad.value || isLoading.value) return;

    isLoading.value = true;

    // Simulate loading delay for better UX
    setTimeout(() => {
        const start = currentLoadIndex.value;
        const end = start + itemsPerLoad;
        const newItems = filteredLibraries.value.slice(start, end);

        if (newItems.length > 0) {
            displayedLibraries.value = [...displayedLibraries.value, ...newItems];
            currentLoadIndex.value = end;

            // Check if we've loaded all items
            hasMoreToLoad.value = currentLoadIndex.value < filteredLibraries.value.length;
        } else {
            hasMoreToLoad.value = false;
        }

        isLoading.value = false;
    }, 600);
}

// Infinite scroll handler
function handleScroll() {
    if (!libraryContainer.value) return;

    const container = libraryContainer.value;
    const bottomOfWindow = window.innerHeight + window.scrollY;
    const distanceFromBottom = container.getBoundingClientRect().bottom - window.innerHeight;

    // Load more when approaching the bottom
    if (distanceFromBottom < 200 && hasMoreToLoad.value && !isLoading.value) {
        loadMoreItems();
    }
}

// Get appropriate CSS class based on difficulty
function getDifficultyClass(difficulty: string | undefined) {
    if (!difficulty) return 'all-levels';

    const lowercaseDifficulty = difficulty.toLowerCase();
    if (lowercaseDifficulty.includes('beginner')) return 'beginner';
    if (lowercaseDifficulty.includes('intermediate')) return 'intermediate';
    if (lowercaseDifficulty.includes('advanced')) return 'advanced';
    return 'all-levels';
}

// Watch for changes to the libraries prop
watch(() => props.libraries, (newLibraries) => {
    // Update filtered libraries when props change
    filterLibraries();
}, { deep: true });

// Initialize on component mount
onMounted(() => {
    filterLibraries();
    window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
});

async function joinCourse() {
    if (!joinCode.value.trim()) return;

    joinPrivateLoading.value = true;
    joinPrivateMessage.value = "";

    axios
        .post('/api/library/join', {
            joinCode: joinCode.value.trim(),
        })
        .then((response) => {
            if (response.status === 200) {
                // Update the local favorites map
                joinPrivateMessageType.value = "success";
                joinPrivateMessage.value = "Successfully joined course!";
                joinCode.value = "";

                // Emit event to refresh libraries list
                emit('libraryJoined', response.data.library);

                // Add to local libraries array if needed
                if (response.data.library) {
                    const newLibrary = response.data.library;
                    const libraryExists = props.libraries.some(lib => lib.id === newLibrary.id);
                    if (!libraryExists) {
                        filteredLibraries.value.unshift(newLibrary);
                        filterLibraries();
                    }
                }
            }
        })
        .catch((error) => {
            console.error("Error updating favorite status:", error);
            joinPrivateMessageType.value = "error";
            joinPrivateMessage.value = error.response?.data?.message || "Failed to join course";
        })
        .finally(() => {
            joinPrivateLoading.value = false;

            // Auto-hide message after 5 seconds
            setTimeout(() => {
                joinPrivateMessage.value = "";
            }, 5000);
        });
}

function joinSpecificCourse(id: number) {
    joinPublicLoading.value = true;
    joinPublicMessage.value = "";

    axios
        .post('/api/library/join', {
            libraryId: id,
        })
        .then((response) => {
            if (response.status === 200) {
                // Update the local favorites map
                joinPublicMessageType.value = "success";
                joinPublicMessage.value = "Successfully joined course!";

                joinedCourses.value.add(id);

                // Emit event to refresh libraries list
                emit('libraryJoined', response.data.library);

            }
        })
        .catch((error) => {
            console.error("Error updating favorite status:", error);
            joinPublicMessageType.value = "error";
            joinPublicMessage.value = error.response?.data?.message || "Failed to join course";
        })
        .finally(() => {
            joinPublicLoading.value = false;

            // Auto-hide message after 5 seconds
            setTimeout(() => {
                joinPublicMessage.value = "";
            }, 5000);
        });
}

function goToCourse(libraryId: number) {
    router.push(`/lessons/${libraryId}`);
}

function handleSearchKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default form submission behavior
        filterLibraries();      // Explicitly call your filter function
    }
}
</script>

<style scoped>
.course-explorer {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    color: #1a1a1a;
    background-color: #fafafa;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.header-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    margin-bottom: 2rem;
}

@media (min-width: 768px) {
    .header-container {
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
    }
}

.header-content {
    flex: 1;
}

.title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #000000, #6366f1);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}

.subtitle {
    font-size: 1rem;
    color: #666;
    max-width: 500px;
}

.join-course-container {
    width: 100%;
    max-width: 400px;
}

.join-form {
    display: flex;
    gap: 0.5rem;
}

.join-input {
    flex: 1;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    background-color: white;
    height: 44px;
    font-size: 0.9rem;
}

.join-button {
    height: 44px;
    border-radius: 8px;
    background-color: #6366f1;
    color: white;
    font-weight: 600;
    padding: 0 1.25rem;
    transition: all 0.2s;
}

.join-button:hover:not(:disabled) {
    background-color: #4f46e5;
    transform: translateY(-2px);
}

.join-message {
    margin-top: 0.75rem;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.875rem;
    animation: fadeIn 0.3s ease;
}

.success {
    background-color: rgba(34, 197, 94, 0.1);
    color: #16a34a;
    border: 1px solid rgba(34, 197, 94, 0.2);
}

.error {
    background-color: rgba(239, 68, 68, 0.1);
    color: #dc2626;
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.search-container {
    position: relative;
    margin-bottom: 2rem;
}

.search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
    width: 1.25rem;
    height: 1.25rem;
}

.search-input {
    width: 100%;
    height: 50px;
    padding-left: 3rem;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    background-color: white;
    font-size: 1rem;
    transition: all 0.2s;
}

.search-input:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.course-card {
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    cursor: pointer;
    border: 1px solid #f1f5f9;
}

.course-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.08);
    border-color: #e2e8f0;
}

.card-content {
    flex: 1;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.difficulty-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    color: white;
}

.beginner {
    background-color: #10b981;
}

.intermediate {
    background-color: #f59e0b;
}

.advanced {
    background-color: #ef4444;
}

.all-levels {
    background-color: #8b5cf6;
}

.card-meta {
    display: flex;
    gap: 0.5rem;
}

.language-tag,
.language-level {
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    font-size: 0.75rem;
    background-color: #f1f5f9;
    color: #64748b;
}

.course-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1rem;
    line-height: 1.4;
    color: #1e293b;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    flex: 1;
}

.card-stats {
    display: flex;
    gap: 1rem;
    margin-top: auto;
}

.stat {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    color: #64748b;
    font-size: 0.875rem;
}

.stat-icon {
    width: 1rem;
    height: 1rem;
}

.card-footer {
    padding: 1rem 1.5rem;
    background-color: #f8fafc;
    border-top: 1px solid #f1f5f9;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.creator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #64748b;
    font-size: 0.875rem;
}

.creator-icon {
    width: 1rem;
    height: 1rem;
}

.loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    color: #64748b;
    gap: 0.75rem;
}

.loader-icon {
    width: 2rem;
    height: 2rem;
    animation: spin 1s linear infinite;
}

.end-message {
    text-align: center;
    padding: 1.5rem;
    color: #64748b;
    font-style: italic;
    font-size: 0.875rem;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4rem 2rem;
    background-color: white;
    border-radius: 16px;
    border: 1px dashed #e2e8f0;
}

.empty-icon {
    width: 4rem;
    height: 4rem;
    color: #cbd5e1;
    margin-bottom: 1.5rem;
}

.empty-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.75rem;
}

.empty-description {
    max-width: 400px;
    color: #64748b;
    line-height: 1.6;
}

/* Animations */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

@media (max-width: 640px) {
    .course-explorer {
        padding: 1.5rem;
        border-radius: 12px;
    }

    .title {
        font-size: 1.75rem;
    }

    .courses-grid {
        grid-template-columns: 1fr;
    }
}

.join-card-button {
    background-color: #6366f1;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
    transition: all 0.2s;
    cursor: pointer;
}

.joined-card-button {
  background-color: #16a34a;
  color: white;
  font-weight: 600;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  transition: all 0.2s;
  cursor: pointer;
}

.joined-card-button:hover {
  background-color: #15803d;
}
</style>