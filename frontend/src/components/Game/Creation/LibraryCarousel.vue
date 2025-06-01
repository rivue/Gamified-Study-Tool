<template>
    <div class="library-list mt-8 m-auto">
        <div class="header-container">
            <div class="header-content">
                <h1 class="title">Courses</h1>
                <p class="subtitle">Courses you've joined or created</p>
            </div>
            <div class="join-course-container">
                <div class="join-form">
                    <Input class="join-input" type="text" v-model="joinCode" placeholder="Enter course code..."
                        @keydown.enter="joinCourse" />
                    <Button class="join-button" @click="joinCourse" :disabled="joinLoading">
                        <LoaderCircle v-if="joinLoading" class="mr-2 h-4 w-4 animate-spin" />
                        Join
                    </Button>
                </div>
                <Transition name="fade">
                    <div v-if="joinMessage" :class="['join-message', joinMessageType]">
                        {{ joinMessage }}
                    </div>
                </Transition>
            </div>
        </div>

        <div class="search-container">
            <Search class="search-icon" />
            <Input class="search-input" type="text" v-model="searchQuery" @input="filterLibraries"
                @keydown="handleSearchKeydown" placeholder="Search courses you've joined..." />
        </div>

        <!-- Conditional rendering based on library count -->
        <div v-if="libraries.length > 0" class="courses-container">
            <div class="courses-grid">
                <div v-for="library in paginatedLibraries" :key="library.id" class="course-card">
                    <div class="card-content">
                        <div class="card-header">
                            <h3 class="course-title">{{ library.library_topic }}</h3>
                            <button @click.stop="updateFavoritedStatus(library.id, libraryFavoritesMap[library.id])"
                                class="star-button p-4">
                                <StarIcon
                                    :class="['star-icon', 'h-6', 'w-6', libraryFavoritesMap[library.id] ? 'favorited' : '']"
                                />
                            </button>
                        </div>
                        <div class="card-stats">
                            <div class="stat">
                                <span v-if="library.owner_id == authStore.user.id" class="owner-badge">Owner</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-footer">
                        <Button @click="goToLibrary(library.id)" class="go-to-course-button">
                            Go to Course
                        </Button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Display this when there are no libraries -->
        <div v-else class="empty-state">
            <BookOpen class="empty-icon" />
            <h3 class="empty-title">No Courses Found</h3>
            <p class="empty-description">
                You don't have any courses yet! Use the form above to join your first course and start learning.
            </p>
        </div>

        <!-- Pagination only shows if there are libraries -->
        <div class="pagination" v-if="totalItems > 0">
            <div class="pagination-info">
                Showing {{ startIndex + 1 }}-{{ endIndex }} of {{ totalItems }} courses
            </div>
            <div class="pagination-controls">
                <button class="pagination-btn" :disabled="currentPage === 1" @click="prevPage">
                    <span class="pagination-icon">←</span> Prev
                </button>
                <div class="page-numbers">
                    <button v-for="page in displayedPages" :key="page" class="page-btn"
                        :class="{ 'active': currentPage === page }" @click="goToPage(page)">
                        {{ page }}
                    </button>
                </div>
                <button class="pagination-btn" :disabled="currentPage === totalPages" @click="nextPage">
                    Next <span class="pagination-icon">→</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Input } from "@/components/ui/input";
import { StarIcon } from "@heroicons/vue/24/solid";
import { Button } from "@/components/ui/button";
import { LoaderCircle, Search, BookOpen } from "lucide-vue-next";
import { useAuthStore } from "@/store/authStore";
import axios from "axios";

// Props
const props = defineProps<{
    libraries: Array<{ clicks: number; context: any; difficulty: string; guide: string; id: number; image_url: string, language: string; language_difficulty: string; likes: number; library_topic: string; owner_id: number }>;
    libraryFavoritesMap: Record<number, boolean>;
}>();

// State
const currentPage = ref(1);
const itemsPerPage = 6;
const router = useRouter();
const searchQuery = ref("");
const filteredLibraries = ref<Array<any>>([]);
const libraryFavoritesMap = computed(() => props.libraryFavoritesMap);
const joinCode = ref("");
const joinMessage = ref("");
const joinMessageType = ref("");
const joinLoading = ref(false);
const authStore = useAuthStore();

// so parent can refresh list
const emit = defineEmits(['libraryJoined']);

// Filtering function
function filterLibraries() {
    let libraries = [...props.libraries];

    // First, sort libraries so favorited ones appear first
    libraries.sort((a, b) => {
        const aFavorited = props.libraryFavoritesMap[a.id] === true;
        const bFavorited = props.libraryFavoritesMap[b.id] === true;

        if (aFavorited && !bFavorited) return -1;
        if (!aFavorited && bFavorited) return 1;
        return 0;
    });

    if (!searchQuery.value.trim()) {
        filteredLibraries.value = libraries;
    } else {
        const query = searchQuery.value.toLowerCase();
        filteredLibraries.value = libraries.filter(library =>
            library.library_topic.toLowerCase().includes(query)
        );
    }
    // Reset to first page when filtering
    currentPage.value = 1;
}

// Watch for changes to the libraries prop
watch(() => props.libraries, () => {
    // Update filtered libraries when props change
    filterLibraries();
}, { deep: true });

// Watch for changes to the favorites map to re-sort when favorites change
watch(() => props.libraryFavoritesMap, () => {
    // Re-sort libraries when favorites change
    filterLibraries();
}, { deep: true });

// Initialize on component mount
onMounted(() => {
    filterLibraries(); // Use the filterLibraries function which already sorts favorited items first
});

// Computed values
const totalItems = computed(() => filteredLibraries.value.length);
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage));
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage);
const endIndex = computed(() =>
    Math.min(startIndex.value + itemsPerPage, totalItems.value)
);

const paginatedLibraries = computed(() =>
    filteredLibraries.value.slice(startIndex.value, endIndex.value)
);

const displayedPages = computed(() => {
    const range: number[] = [];
    const maxVisiblePages = 5;

    if (totalPages.value <= maxVisiblePages) {
        for (let i = 1; i <= totalPages.value; i++) {
            range.push(i);
        }
    } else {
        let start = Math.max(1, currentPage.value - 2);
        let end = Math.min(totalPages.value, start + maxVisiblePages - 1);

        if (end - start + 1 < maxVisiblePages) {
            start = Math.max(1, end - maxVisiblePages + 1);
        }

        for (let i = start; i <= end; i++) {
            range.push(i);
        }
    }

    return range;
});

// Methods
function goToLibrary(id: number) {
    router.push(`/lessons/${id}`);
}

async function joinCourse() {
    if (!joinCode.value.trim()) return;

    joinLoading.value = true;
    joinMessage.value = "";

    axios
        .post('/api/library/join', {
            joinCode: joinCode.value.trim(),
        })
        .then((response) => {
            if (response.status === 200) {
                // Update the local favorites map
                joinMessageType.value = "success";
                joinMessage.value = "Successfully joined course!";
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
            console.log(error);
            console.error("Error updating favorite status:", error);
            joinMessageType.value = "error";
            joinMessage.value = error.response?.data?.message || "Failed to join course";

        })
        .finally(() => {
            joinLoading.value = false;

            // Auto-hide message after 5 seconds
            setTimeout(() => {
                joinMessage.value = "";
            }, 5000);

        });

}

function updateFavoritedStatus(libraryId: number, oldStatus: boolean) {
    const newStatus = oldStatus === true ? false : true;
    axios
        .put(`/api/library/favorited_status/${libraryId}`, {
            newStatus: newStatus,
        })
        .then((response) => {
            if (response.status === 200) {
                // Update the local favorites map
                props.libraryFavoritesMap[libraryId] = newStatus;
            }
        })
        .catch((error) => {
            console.log(error);
            console.error("Error updating favorite status:", error);
        });
}

function handleSearchKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default form submission behavior
        filterLibraries();      // Explicitly call your filter function
    }
}

function prevPage() {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
}

function nextPage() {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
}

function goToPage(page: number) {
    currentPage.value = page;
}
</script>

<style scoped>
.library-list {
    max-width: 1200px;
    /* margin: 0 auto; */
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
    text-align: center; /*  the text */
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
    height: 44px;
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

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.course-title {
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.4;
    color: var(--text-color);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    flex: 1;
    margin-right: 1rem;
}

.star-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.3rem;
    border-radius: 50%;
    transition: background-color 0.2s ease;
    /* display: flex; */
    /* align-items: center; */
    /* justify-content: center; */
}

.star-button:hover {
    background-color: rgba(26, 139, 127, 0.1);
}

.star-icon {
    color: var(--text-color-secondary);
    transition: color 0.2s ease;
}

.star-button:hover .star-icon.favorited {
    color: #ffd363;
}

.star-button:hover .star-icon:not(.favorited) {
    color: #fadc90;
}

.star-icon.favorited {
    color: #fbbf24;
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

.owner-badge {
    background-color: rgba(26, 139, 127, 0.2);
    color: var(--color-primary);
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid rgba(26, 139, 127, 0.3);
}

.card-footer {
    padding: 1rem 1.5rem;
    background: rgba(26, 139, 127, 0.1);
    border-top: 1px solid rgba(26, 139, 127, 0.2);
    display: flex;
    justify-content: center;
    align-items: center;
}

.go-to-course-button {
    width: 100%;
    background: var(--button-gradient);
    color: var(--text-color);
    font-weight: 600;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    transition: all 0.2s;
    cursor: pointer;
    border: none;
}

.go-to-course-button:hover {
    background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(26, 139, 127, 0.3);
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

.pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 2rem;
}

.pagination-info {
    color: var(--text-color-secondary);
    font-size: 14px;
    font-weight: 500;
}

.pagination-controls {
    display: flex;
    gap: 8px;
    align-items: center;
}

.pagination-btn {
    padding: 8px 14px;
    border: 1px solid rgba(26, 139, 127, 0.3);
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
}

.pagination-btn:hover:not(:disabled) {
    background: rgba(26, 139, 127, 0.2);
    border-color: var(--color-primary);
}

.pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination-icon {
    font-size: 12px;
}

.page-numbers {
    display: flex;
    gap: 4px;
}

.page-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    border: 1px solid rgba(26, 139, 127, 0.3);
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.page-btn:hover {
    background: rgba(26, 139, 127, 0.2);
    border-color: var(--color-primary);
}

.page-btn.active {
    background: var(--button-gradient);
    color: white;
    border-color: var(--color-primary);
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(26, 139, 127, 0.3);
    transform: scale(1.05);
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

@media (max-width: 640px) {
    .library-list {
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
</style>
