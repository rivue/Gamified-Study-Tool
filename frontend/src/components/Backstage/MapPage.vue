<template>
    <div class="page-main-container">
        <div v-if="!loading && library && isDataValid">
            <h1 class="page-title">{{ library.data.library_topic }} Lessons</h1>
            <LearningPath :libraryId="Number(library.data.id)" :room-names="library.data.room_names"
                :room-data="library.room_data" :library-is-public="library.data.is_public"
                :unit-section-map="processedUnitSectionMap" :library-join-code="library.data.join_code" 
                :is-owner="library.data.show_settings" :unit-position-map="library.data.unit_to_position_map"
                :library-topic="library.data.library_topic"/>
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
import { onMounted, onUnmounted, ref, computed } from 'vue';
import { usePopupStore } from "@/store/popupStore";
import LearningPath from "../Graphs/LearningPath/LearningPath.vue";
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
    unit_to_section_map: any;
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
const orderedMap = ref([]);
const abortController = new AbortController();


// Add a computed property to validate data integrity
const isDataValid = computed(() => {
    if (!library.value || !library.value.data || !library.value.data.unit_to_section_map) {
        return false;
    }

    // Validate that unit_to_section_map contains valid data
    const unitMap = library.value.data.unit_to_section_map;
    console.log(library);
    // Check that it's not empty
    if (Object.keys(unitMap).length === 0) {
        console.warn("Unit to section map is empty");
        return false;
    }

    // Additional validation if needed
    return true;
});

// Process the unit section map to ensure it's safe to use
const processedUnitSectionMap = computed(() => {
    if (!isDataValid.value) {
        return {}; // Return safe default
    }

    // Make a defensive copy to avoid mutation issues
    const unitMap = JSON.parse(JSON.stringify(library.value.data.unit_to_section_map));

    // Ensure each unit has proper structure
    for (const unitName in unitMap) {
        if (!Array.isArray(unitMap[unitName])) {
            console.log(`Unit ${unitName} is not an array, fixing...`);
            unitMap[unitName] = [];
        }

        // Ensure each section in each unit has valid data
        for (let i = 0; i < unitMap[unitName].length; i++) {
            if (!unitMap[unitName][i] || !Array.isArray(unitMap[unitName][i])) {
                console.log(`Section ${i} in unit ${unitName} is invalid, fixing...`);
                unitMap[unitName][i] = [];
            }
        }
    }

    // Create an ordered map based on unit_to_position_map
    const orderedMap = {};

    // Get all entries and sort them by position
    const entries = Object.entries(unitMap);
    entries.sort((a, b) => {
        const posA = library.value.data.unit_to_position_map?.[a[0]]?.[0] || 0;
        const posB = library.value.data.unit_to_position_map?.[b[0]]?.[0] || 0;
        return posA - posB;
    });

    // Rebuild the ordered object
    entries.forEach(([key, value]) => {
        orderedMap[key] = value;
    });

    return orderedMap;
});

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

        if (response.data && response.data.data && response.data.room_data) {

            // Check for unit_to_section_map existence
            if (!response.data.data.unit_to_section_map) {
                console.error("Missing unit_to_section_map in response data");
                throw new Error("Invalid response data: missing unit_to_section_map");
            }

            library.value = {
                ...response.data,
                data: {
                    ...response.data.data,
                    library_topic: capitalizeWords(response.data.data.library_topic),
                },
            };

            // Log data structure for debugging in production if needed
            console.debug("Initialized library data structure:", JSON.stringify({ hasRoomData: response.data.room_data.length > 0, unitMapKeys: Object.keys(response.data.data.unit_to_section_map) }));
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

<style scoped></style>