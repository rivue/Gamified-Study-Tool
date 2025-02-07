<template>
    <div class="page-main-container">
        <div v-if="!loading && library">
            <h1 class="page-title">{{ library.data.library_topic }} Learning Map 🗺️</h1>
            <LearningPath @nodeSelected="handleNodeSelect" />
        </div>
        <div v-else-if="loading">
            <p>Loading...</p>
        </div>
        <div v-else>
            <p>Failed to load data.</p>
        </div>
    </div>
</template>

<script>
import { useRoute } from "vue-router";
import { onMounted, ref } from 'vue';
import { usePopupStore } from "@/store/popupStore";
import LearningPath from "../Graphs/LearningPath.vue";
import axios from 'axios';

// Utility function to capitalize words
function capitalizeWords(str) {
    if (!str) return str; // Handle null or undefined input
    return str.replace(/(^|\s|[-])\S/g, match => match.toUpperCase()).replace(/-/g, ' ');
}

export default {
    name: "KnowledgePage",
    components: {LearningPath},
    setup() {
        const route = useRoute();
        const libraryId = route.params.id;
        const library = ref(null);
        const loading = ref(true);

        // Fetch library data
        const fetchLibraryData = async () => {
            try {
                const response = await axios.get(`/api/library/${libraryId}`);
                if (response.data && response.data.data) {
                    library.value = {
                        ...response.data,
                        data: {
                            ...response.data.data,
                            library_topic: capitalizeWords(response.data.data.library_topic),
                        },
                    };
                    console.log(response)
                } else {
                    throw new Error("Invalid response data");
                }
            } catch (error) {
                // Handle the error
                const popupStore = usePopupStore();
                popupStore.showPopup(error.message || "Learning map failed. Please try again.");
            } finally {
                loading.value = false;
            }
        };

        // Fetch data on component mount
        onMounted(fetchLibraryData);

        return { library, loading };
    },
};
</script>

<style scoped>
/* Add your styles here */
</style>