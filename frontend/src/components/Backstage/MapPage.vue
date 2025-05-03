<template>
    <div class="page-main-container">
        <div v-if="!loading && library">
            <h1 class="page-title">{{ library.data.library_topic }} Lessons</h1>
            <LearningPath 
            :libraryId="library.data.id"
            :room-names="library.data.room_names"
            :room-data="library.room_data"
            :unit-section-map="library.data.unit_to_section_map" 
            :library-is-public="library.data.is_public"
            />
        </div>
        <div v-else-if="loading">
            <p>Loading...</p>
        </div>
        <div v-else>
            <p>Failed to load data.</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { onMounted, onUnmounted, ref } from 'vue';
import { usePopupStore } from "@/store/popupStore";
import LearningPath from "../Graphs/LearningPath.vue";
import axios from 'axios';

// Define component name
defineOptions({
  name: "MapPage"
});

// Define interfaces for type safety
interface LibraryData {
  id: string;
  library_topic: string;
  room_names: string[];
  [key: string]: any;
}

interface Library {
  data: LibraryData;
  room_data: any[];
  [key: string]: any;
}

const route = useRoute();
const libraryId = route.params.id as string;
const library = ref<Library | null>(null);
const loading = ref(true);
const abortController = new AbortController();

// Utility function to capitalize words
function capitalizeWords(str: string | null | undefined): string {
    if (!str) return str || ''; // Handle null or undefined input
    return str.replace(/(^|\s|[-])\S/g, match => match.toUpperCase()).replace(/-/g, ' ');
}

// Fetch library data
const fetchLibraryData = async (): Promise<void> => {
    
    try {

        const response = await axios.get(`/api/library/${libraryId}`, {
            signal: abortController.signal
        });
        console.debug("response: ", response);
        if (response.data && response.data.data && response.data.room_data) {
            library.value = {
                ...response.data,
                data: {
                    ...response.data.data,
                    library_topic: capitalizeWords(response.data.data.library_topic),
                },
            };
        } else {
            throw new Error("Invalid response data");
        }

    } catch (error: any) {
        // Handle the error
        const popupStore = usePopupStore();
        popupStore.showPopup(error.message || "Learning map failed. Please try again.");
    } finally {
        if (!abortController.signal.aborted) {
            // Only set loading to false if the request was not aborted
            loading.value = false;
        }
    }
};

// Fetch data on component mount
onMounted(fetchLibraryData);

onUnmounted(() => {
    // Abort the fetch request if the component is unmounted
    abortController.abort();
});
</script>

<style scoped>

</style>