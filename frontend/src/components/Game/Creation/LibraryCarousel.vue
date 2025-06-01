<template>
    <div class="library-list px-16 py-12">
        <div class="list-header-container">
            <div class="list-header">
                <h1>Courses</h1>
                <p class="course-description">Courses you've joined or created</p>
            </div>
            <div class="join-private-course">
                <div class="join-form">
                    <Input
                        class="join-input"
                        type="text"
                        v-model="joinCode"
                        placeholder="Enter course code..."
                        @keydown.enter="joinCourse"
                    />
                    <Button 
                        class="join-button" 
                        @click="joinCourse"
                        :disabled="joinLoading"
                        variant="destructive"
                    >
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

        <Input
        class="mb-4 text-lg bg-transparent border-[1px] border-solid border-[var(--text-color)] rounded-[4px] placeholder-[var(--text-color)] text-[var(--text-color)]"
        type="text" v-model="searchQuery" @input="filterLibraries" @keydown="handleSearchKeydown"
        placeholder="Search courses you've joined..." />
        
        <!-- Conditional rendering based on library count -->
        <div v-if="libraries.length > 0" class="list-table">
            <Table>
                <TableBody>
                    <template v-if="paginatedLibraries.length">
                        <TableRow v-for="library in paginatedLibraries" :key="library.id"
                            class="cursor-pointer text-[var(--text-color)] hover:text-white hover:bg-[var(--element-color-1)]"
                            @click="goToLibrary(library.id)">
                            <div class="absolute inset-0 border-[1px] border-solid border-[var(--text-color)] rounded-lg pointer-events-none"></div>
                            <TableCell class="w-16">
                                <button @click.stop="updateFavoritedStatus(library.id, libraryFavoritesMap[library.id])"
                                    class="star-button flex items-center justify-center w-8 h-8 rounded-full hover:bg-[var(--background-color-2)]">
                                    <StarIcon v-if="libraryFavoritesMap[library.id] === true"
                                        class="text-yellow-500 hover:text-yellow-400" size="20" />
                                    <StarIcon v-else class="text-white-500 hover:text-yellow-300" size="20" />
                                </button>
                            </TableCell>
                            <TableCell class="text-xl text-center p-4 w-full">{{ library.library_topic }}</TableCell>
                            <TableCell class="text-xs text-right italic opacity-70 pr-4">
                                <span v-if="library.owner_id == authStore.user.id" class="px-2 py-1 rounded-md bg-[var(--background-color-2t)]">Owner</span>
                            </TableCell>
                        </TableRow>
                    </template>
                    <TableRow v-else class="border-[1px] border-solid border-[var(--text-color)]">
                        <TableCell colspan="5" class="h-24 text-center text-xl">
                            No results
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>

        <!-- Display this when there are no libraries -->
        <div v-else class="no-libraries">
            <p>You don't have any courses yet!</p>
            <p>Use the form above to create your first course and start learning.</p>
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
import { Table, TableRow, TableBody, TableCell } from "@/components/ui/table";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { LoaderCircle } from "lucide-vue-next";
import { useAuthStore } from "@/store/authStore";
import axios from "axios";

// Props
const props = defineProps<{
    libraries: Array<{ clicks: number; context: any; difficulty: string; guide: string; id: number; image_url: string, language: string; language_difficulty: string; likes: number; library_topic: string }>;
    libraryFavoritesMap: Record<number, boolean>;
}>();

// State
const currentPage = ref(1);
const itemsPerPage = 5;
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
watch(() => props.libraries, (newLibraries) => {
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
    console.log("a;lskdjfasdf");
    console.log(id);
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
    margin-top: 50px;
    background: var(--background-color-1t);
    border: 1px solid var(--text-color);
    border-radius: 5px;
}


.list-header {
    margin-bottom: 24px;
}

.list-header h1 {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 8px;
    color: var(--text-color);
    justify-content: center;
}

.subtitle {
    color: var(--text-color-secondary);
    font-size: 15px;
}

.list-table {
    width: 100%;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border-color);
    margin-bottom: 16px;
}

.table-header,
.library-item {
    display: grid;
    /* Define columns here - ADJUST THESE values as needed for your design */
    grid-template-columns:
        minmax(100px, 2fr)
        /* col-name: min 100px, flexible */
        minmax(80px, 1fr)
        /* col-status: min 80px, flexible */
        minmax(120px, 1fr)
        /* col-stats: min 100px, flexible */
        minmax(48px, 48px);
    /* col-actions: fixed 48px */
    align-items: center;
    /*padding: 14px 16px; /* Keep padding */
    gap: 16px;
    /* Add gap for spacing between grid cells */

    /* --- Key Additions for Horizontal Scrolling --- */
    padding-bottom: 10px;
}


.library-item {
    display: flex;
    flex-wrap: wrap;
    /* Allow items to wrap to the next line */
    align-items: center;
    /* Align items nicely vertically */
    gap: 12px 16px;
    /* Row gap, Column gap */
    padding: 16px;
    border: 1px solid var(--border-color);
    /* Add border to each item */
    border-radius: 8px;
    /* Rounded corners for card look */
    margin-bottom: 16px;
    /* Space between cards */
    background-color: var(--background-color-1);
    /* Ensure items have background */
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.table-header {
    /* padding: 14px 16px;
    background-color: var(--background-color-2);
    border-bottom: 1px solid var(--border-color);
    color: var(--text-color-secondary);
    font-size: 14px;
    font-weight: 600; */
    display: none;
}

.library-item:last-child {
    border-bottom: none;
}

.library-item:hover {
    background-color: var(--element-color-1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.col-name h3 {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-color);
    margin: 0;
    /* Allow name text itself to wrap if extremely long */
    white-space: normal;
    word-break: break-word;
    /* Break long words if needed */
}

.col-status {
    background: none;
    border: none;
    cursor: pointer;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.2s ease;
}

.col-status:hover {
    background-color: var(--background-color-2);
}

.col-stats {
    display: flex;
    flex-wrap: wrap;
    /* Allow stats themselves to wrap if needed */
    gap: 12px;
    /* Gap between individual stats */
    align-items: center;
    /* Ensure stats can appear on new line */
    flex-basis: 100%;
    /* Default to taking full width when wrapped below name/status */
    justify-content: flex-start;
    /* Align stats to the start */
}

@media (min-width: 400px) {

    /* Example breakpoint where stats might fit better beside status */
    .col-stats {
        flex-basis: auto;
        /* Allow stats to sit beside status */
        justify-content: flex-end;
    }

    .col-status {
        margin-right: 0;
    }
}

.stat {
    font-size: 14px;
    color: var(--text-color-secondary);
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-weight: 500;
    white-space: nowrap;
    /* Prevent text within a stat from wrapping */
    flex-shrink: 0;
}

.col-date {
    font-size: 14px;
    color: var(--text-color-secondary);
}

@media (min-width: 768px) {
    .list-table {
        /* Re-add border styling to the table container */
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }

    /* Show the header and style it as a grid */
    .table-header {
        display: grid;
        /* Use grid layout */
        grid-template-columns: 80px minmax(150px, 2fr) 1fr 1fr 48px;
        /* Define columns */
        padding: 14px 16px;
        background-color: var(--background-color-2);
        border-bottom: 1px solid var(--border-color);
        color: var(--text-color-secondary);
        font-size: 14px;
        font-weight: 600;
        gap: 16px;
        /* Add gap */
        /* Ensure header text doesn't wrap undesirably */
        white-space: nowrap;
    }

    .table-header>div {
        overflow: hidden;
        text-overflow: ellipsis;
    }


    .library-item {
        display: grid;
        /* Switch back to grid */
        grid-template-columns: 80px minmax(150px, 2fr) 1fr 1fr 48px;
        /* Same columns as header */
        flex-wrap: nowrap;
        /* Disable wrapping for grid */
        border: none;
        /* Remove individual item border */
        border-radius: 0;
        /* Remove individual item radius */
        margin-bottom: 0;
        /* Remove margin between items */
        border-bottom: 1px solid var(--border-color);
        /* Use bottom border */
        gap: 16px;
        /* Add gap */
        /* Ensure grid text content truncates if needed */
        white-space: nowrap;
    }

    .library-item>div {
        overflow: hidden;
        text-overflow: ellipsis;
        /* Allow normal whitespace wrapping WITHIN cells if specifically desired */
        /* white-space: normal; */
    }

    .library-item:last-child {
        border-bottom: none;
    }

    .col-name {
        /* Re-apply specific styling for grid if needed */
        min-width: 0;
        /* Allow shrinking in grid */
    }

    .col-name h3 {
        /* Re-apply truncation for grid */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }


    .col-status {
        margin-right: 0;
        /* Reset margin override */
    }

    .col-stats {
        display: flex;
        flex-wrap: nowrap;
        /* Prevent stats wrapping on desktop */
        gap: 16px;
        flex-basis: auto;
        /* Reset flex-basis */
        justify-content: flex-start;
        /* Reset justify */
    }
}


.pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

.pagination-info {
    color: var(--background-color-1);
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
    border: 1px solid var(--border-color);
    background: var(--background-color-1);
    color: var(--text-color);
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
}

.pagination-btn:hover:not(:disabled) {
    background: var(--background-color-2);
    border-color: var(--text-color-secondary);
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
    border-radius: 6px;
    border: 1px solid var(--border-color);
    background: var(--background-color-1);
    color: var(--text-color);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.page-btn:hover {
    background: var(--background-color-2);
    border-color: var(--text-color-secondary);
}

.page-btn.active {
    background: var(--primary-color, #4361ee);
    color: white;
    border-color: var(--primary-color, #4361ee);
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(67, 97, 238, 0.3);
    transform: scale(1.05);
}

/* Styles for no-libraries message */
.no-libraries {
    text-align: center;
    padding: 40px;
    color: var(--text-color-secondary);
    font-size: 16px;
}

.no-libraries p {
    margin: 8px 0;
}

/* Fallback styles if CSS variables are not defined */
:root {
    --background-color-1: #ffffff;
    --background-color-2: #f8f9fa;
    --background-color-3: #e9ecef;
    --text-color: #212529;
    --text-color-secondary: #6c757d;
    --border-color: #dee2e6;
    --success-color: #198754;
    --success-color-bg: rgba(42, 87, 66, 0.1);
    --primary-color: #4361ee;
    --primary-hover: #3d55d5;
}


.list-header-container {
    display: flex;
    flex-direction: column;
    position: relative;
}

@media (min-width: 768px) {
    .list-header-container {
        flex-direction: row;
        align-items: flex-start;
        justify-content: center;
    }
    
    .list-header {
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        text-align: center;
    }
    
    .join-private-course {
        margin-left: auto;
    }
}

.join-private-course {
    width: 100%;
    max-width: 400px;
}

.join-form {
    display: flex;
    gap: 8px;
}

.join-input {
    flex: 1;
    background-color: var(--background-color-2t);
    border: 1px solid var(--text-color);
    border-radius: 4px;
    color: var(--text-color);
    height: 40px;
    padding: 0 12px;
}

.join-button {
    background-color: var(--element-color-1);
    color: var(--text-color);
    border: 1px solid var(--text-color);
    border-radius: 4px;
    height: 40px;
    padding: 0 16px;
    transition: all 0.2s ease;
}

.join-button:hover:not(:disabled) {
    background-color: var(--element-color-2);
}

.join-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.join-message {
    margin-top: 8px;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 14px;
    animation: fadeIn 0.3s ease-in-out;
}

.success {
    background-color: rgba(34, 197, 94, 0.2);
    color: #15803d;
    border: 1px solid rgba(34, 197, 94, 0.3);
}

.error {
    background-color: rgba(239, 68, 68, 0.3);
    color: #dc2626;
    border: 1px solid rgba(239, 68, 68, 0.4);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>