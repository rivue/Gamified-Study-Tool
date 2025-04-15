<template>

    <div class="library-list">
        <div class="list-header">

            <h1>My Courses</h1>
        </div>
        <Input class="max-w mb-4" type="text" v-model="searchQuery" @input="filterLibraries"
            @keydown="handleSearchKeydown" placeholder="Search courses..." />

        <!-- Conditional rendering based on library count -->
        <div v-if="libraries.length > 0" class="list-table">

            <Table>
                <TableBody>
                    <template v-if="paginatedLibraries.length">
                        <TableRow v-for="library in paginatedLibraries" :key="library.id"
                            class="cursor-pointer hover:bg-[var(--element-color-1)]" @click="goToLibrary(library.id)">
                            <TableCell class="font-medium">{{ library.library_topic }}</TableCell>
                            <TableCell class="text-right">
                                <button class="rounded-full p-2 hover:bg-muted" @click.stop>
                                    <span class="dots">...</span>
                                </button>
                            </TableCell>
                        </TableRow>
                    </template>
                    <TableRow v-else>
                        <TableCell colspan="5" class="h-24 text-center">
                            No results.
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>

        <!-- Display this when there are no libraries -->
        <div v-else class="no-libraries">
            <p>You don’t have any courses yet!</p>
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
import { Table, TableRow, TableBody, TableCell } from "@/components/ui/table";

// Props
const props = defineProps<{
    libraries: Array<{ clicks: number; context: any; difficulty: string; guide: string; id: number; image_url: string, language: string; language_difficulty: string; likes: number; library_topic: string }>;
}>();

// State
const currentPage = ref(1);
const itemsPerPage = 5;
const router = useRouter();
const searchQuery = ref("");
const filteredLibraries = ref<Array<any>>([]);

// Filtering function
function filterLibraries() {
    if (!searchQuery.value.trim()) {
        filteredLibraries.value = [...props.libraries];
    } else {
        const query = searchQuery.value.toLowerCase();
        filteredLibraries.value = props.libraries.filter(library =>
            library.library_topic.toLowerCase().includes(query) // ||
            //   library.language.toLowerCase().includes(query) ||
            //   library.difficulty.toLowerCase().includes(query)
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

// Initialize on component mount
onMounted(() => {
    filteredLibraries.value = [...props.libraries];
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
    margin-top: 100px;
    padding: 16px;
    background: var(--background-color-1);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.list-header {
    margin-bottom: 24px;
}

.list-header h1 {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 8px;
    color: var(--text-color);
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
    transition: background-color 0.2s ease, box-shadow 0.2s ease;
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

.dots {
    font-size: 10px;
    line-height: 0;
    color: var(--text-color-secondary);
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
    padding: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
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
    --success-color-bg: rgba(25, 135, 84, 0.1);
    --primary-color: #4361ee;
    --primary-hover: #3d55d5;
}
</style>