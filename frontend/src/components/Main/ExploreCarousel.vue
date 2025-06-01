<template>
    <div class="course-explorer">
        <div class="header-container">
            <div class="header-content">
                <h1 class="title">Explore Courses</h1>
                <p class="subtitle">Discover and join courses created by the community</p>
            </div>
            <!-- 
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
            </div> -->
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
                        <h3 class="course-title">{{ library.library_topic }}</h3>

                        <div class="card-stats">
                            <div class="stat">
                                <Heart class="stat-icon" />
                                <span>{{ library.likes === null ? "Likes not found" : library.likes }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-footer">
                        <div class="creator">
                            <UserCircle class="creator-icon" />
                            <span>{{ library.owner_username === null ? "Creator not found" : library.owner_username
                                }}</span>
                        </div>


                        <Input v-if="!library.is_public" v-model="joinCode" placeholder="Enter private library code"
                            @keydown.enter="joinSpecificCourse(library.id)" class="join-input m-2 h-10 p-4" />

                        <Button v-if="!joinedCourses.has(library.id)" @click="joinSpecificCourse(library.id)"
                            :disabled="joinPublicLoading.has(library.id)" class="join-card-button h-10 p-4">
                            <LoaderCircle v-if="joinPublicLoading.has(library.id)" class="mr-2 h-4 w-4 animate-spin" />
                            Join
                        </Button>
                        <Button v-else @click="goToCourse(library.id)" class="joined-card-button">
                            Go to Course
                        </Button>
                    </div>
                    <Transition name="fade">
                        <div v-if="joinPublicMessages.has(library.id)"
                            :class="['join-message', joinPublicMessageTypes.get(library.id)]">
                            {{ joinPublicMessages.get(library.id) }}
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
import { LoaderCircle, Search, Heart, UserCircle, BookOpen } from "lucide-vue-next";
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
        owner_username: string;
        is_public: boolean;
    }>;
}>();

// State
const router = useRouter();
const searchQuery = ref("");
const filteredLibraries = ref<Array<any>>([]);
const displayedLibraries = ref<Array<any>>([]);
const joinCode = ref("");

// actual list of courses 
const joinPublicMessages = ref(new Map());
const joinPublicMessageTypes = ref(new Map());
const joinPublicLoading = ref(new Map());

const libraryContainer = ref<HTMLElement | null>(null);
const joinedCourses = ref(new Set());

// Infinite scroll states
const itemsPerLoad = 6;
const currentLoadIndex = ref(0);
const isLoading = ref(false);
const hasMoreToLoad = ref(true);

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
// function getDifficultyClass(difficulty: string | undefined) {
//     if (!difficulty) return 'all-levels';

//     const lowercaseDifficulty = difficulty.toLowerCase();
//     if (lowercaseDifficulty.includes('beginner')) return 'beginner';
//     if (lowercaseDifficulty.includes('intermediate')) return 'intermediate';
//     if (lowercaseDifficulty.includes('advanced')) return 'advanced';
//     return 'all-levels';
// }

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

// async function joinCourse() {
//     if (!joinCode.value.trim()) return; 

//     joinPrivateLoading.value = true;
//     joinPrivateMessage.value = "";

//     axios
//         .post('/api/library/join', {
//             joinCode: joinCode.value.trim(),
//         })
//         .then((response) => {
//             if (response.status === 200) {
//                 // Update the local favorites map
//                 joinPrivateMessageType.value = "success";
//                 joinPrivateMessage.value = "Successfully joined course!";
//                 joinCode.value = "";

//                 // Add to local libraries array if needed
//                 if (response.data.library) {
//                     const newLibrary = response.data.library;
//                     const libraryExists = props.libraries.some(lib => lib.id === newLibrary.id);
//                     if (!libraryExists) {
//                         filteredLibraries.value.unshift(newLibrary);
//                         filterLibraries();
//                     }
//                 }
//             }
//         })
//         .catch((error) => {
//             console.error("Error updating favorite status:", error);
//             joinPrivateMessageType.value = "error";
//             joinPrivateMessage.value = error.response?.data?.message || "Failed to join course";
//         })
//         .finally(() => {
//             joinPrivateLoading.value = false;

//             // Auto-hide message after 5 seconds
//             setTimeout(() => {
//                 joinPrivateMessage.value = "";
//             }, 5000);
//         });
// }

async function joinSpecificCourse(id: number) {
    joinPublicLoading.value.set(id, true);
    joinPublicMessages.value.delete(id);

    axios
        .post('/api/library/join', {
            libraryId: id,
            joinCode: joinCode.value.trim(),
        })
        .then((response) => {
            if (response.status === 200) {
                // Update the local favorites map
                joinPublicMessageTypes.value.set(id, "success");
                joinPublicMessages.value.set(id, "Successfully joined course!");

                joinedCourses.value.add(id);

            }
        })
        .catch((error) => {

            console.error("Error updating favorite status:", error);
            joinPublicMessageTypes.value.set(id, "error");
            joinPublicMessages.value.set(id, error.response?.data?.message || "Failed to join course");

        })
        .finally(() => {
            joinPublicLoading.value.delete(id);

            // Auto-hide message after 5 seconds
            setTimeout(() => {
                joinPublicMessages.value.delete(id);
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
    color: var(--text-color);
    background: var(--background-color);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(26, 139, 127, 0.2);
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
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}

.subtitle {
    font-size: 1rem;
    color: var(--text-color-secondary);
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
    border: 1px solid rgba(26, 139, 127, 0.3);
    background-color: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    font-size: 0.9rem;
}

.join-input::placeholder {
    color: var(--text-color-secondary);
}

.join-button {
    height: 44px;
    border-radius: 8px;
    background: var(--button-gradient);
    color: var(--text-color);
    font-weight: 600;
    padding: 0 1.25rem;
    transition: all 0.2s;
    border: none;
}

.join-button:hover:not(:disabled) {
    background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(26, 139, 127, 0.3);
}

.join-message {
    margin-top: 0.5rem;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    font-size: 0.875rem;
    backdrop-filter: blur(10px);
}

.success {
    background-color: rgba(16, 185, 129, 0.2);
    color: var(--success-color);
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.error {
    background-color: rgba(255, 116, 108, 0.2);
    color: var(--error-color);
    border: 1px solid rgba(255, 116, 108, 0.3);
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
    color: var(--color-primary-light);
    width: 1.25rem;
    height: 1.25rem;
}

.search-input {
    width: 100%;
    height: 50px;
    padding-left: 3rem;
    border-radius: 12px;
    border: 1px solid rgba(26, 139, 127, 0.3);
    background-color: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    font-size: 1rem;
    transition: all 0.2s;
}

.search-input::placeholder {
    color: var(--text-color-secondary);
}

.search-input:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(26, 139, 127, 0.2);
    outline: none;
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
    background: var(--background-color-1t);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    cursor: pointer;
    border: 1px solid rgba(26, 139, 127, 0.2);
}

.course-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 20px rgba(26, 139, 127, 0.2);
    border-color: var(--color-primary-light);
    background: var(--background-color-2t);
}

.card-content {
    flex: 1;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
}

.course-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1rem;
    line-height: 1.4;
    color: var(--text-color);
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
    color: var(--color-primary-light);
    font-size: 0.875rem;
}

.stat-icon {
    width: 1rem;
    height: 1rem;
}

.card-footer {
    padding: 1rem 1.5rem;
    background: rgba(26, 139, 127, 0.1);
    border-top: 1px solid rgba(26, 139, 127, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.creator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-color-secondary);
    font-size: 0.875rem;
}

.creator-icon {
    width: 1rem;
    height: 1rem;
    color: var(--color-primary-light);
}

.loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    color: var(--text-color-secondary);
    gap: 0.75rem;
}

.loader-icon {
    width: 2rem;
    height: 2rem;
    color: var(--color-primary);
    animation: spin 1s linear infinite;
}

.end-message {
    text-align: center;
    padding: 1.5rem;
    color: var(--text-color-secondary);
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
    background: var(--background-color-1t);
    border-radius: 16px;
    border: 1px dashed rgba(26, 139, 127, 0.3);
}

.empty-icon {
    width: 4rem;
    height: 4rem;
    color: var(--color-primary-light);
    margin-bottom: 1.5rem;
}

.empty-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 0.75rem;
}

.empty-description {
    max-width: 400px;
    color: var(--text-color-secondary);
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
    background: var(--button-gradient);
    color: var(--text-color);
    font-weight: 600;
    border-radius: 8px;
    /* padding: 0.5rem 1rem; */
    /* font-size: 0.875rem; */
    transition: all 0.2s;
    cursor: pointer;
    border: none;
}

.join-card-button:hover:not(:disabled) {
    background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(26, 139, 127, 0.3);
}

.joined-card-button {
    background: linear-gradient(135deg, var(--success-color), #059669);
    color: var(--text-color);
    font-weight: 600;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
    transition: all 0.2s;
    cursor: pointer;
    border: none;
}

.joined-card-button:hover {
    background: linear-gradient(135deg, #059669, #047857);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
}

.join-container {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}
</style>
