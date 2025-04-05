<template>
    <div class="page-main-container">
        <div v-if="!loading && library">
            <h1 class="page-title">{{ library.data.library_topic }} Lessons</h1>
            <LearningPath 
            :libraryId="library.data.id"
            :room-names="library.data.room_names"
            :room-data="library.room_data" />
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
import { onMounted, onUnmounted, ref } from 'vue';
import { usePopupStore } from "@/store/popupStore";
import LearningPath from "../Graphs/LearningPath.vue";
import axios from 'axios';

// Utility function to capitalize words
function capitalizeWords(str) {
    if (!str) return str; // Handle null or undefined input
    return str.replace(/(^|\s|[-])\S/g, match => match.toUpperCase()).replace(/-/g, ' ');
}

export default {
    name: "MapPage",
    components: {LearningPath},
    setup() {
        const route = useRoute();
        const libraryId = route.params.id;
        const library = ref(null);
        const loading = ref(true);
        const abortController = new AbortController();

        // Fetch library data
        const fetchLibraryData = async () => {
            try {
                const response = await axios.get(`/api/library/${libraryId}`, {
                    signal: abortController.signal // Pass the signal to axios
                });
                console.log("response: ", response);
                if (response.data && response.data.data && response.data.room_data) {

                    library.value = {
                        ...response.data,
                        data: {
                            ...response.data.data,
                            library_topic: capitalizeWords(response.data.data.library_topic),
                        },
                    };
                    
                    console.log(library.value.data.room_names)
                } else {
                    throw new Error("Invalid response data");
                }
            } catch (error) {
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

        return { library, loading };
    },
};
</script>

<style scoped>

</style>