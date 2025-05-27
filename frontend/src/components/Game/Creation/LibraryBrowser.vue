<template>
    <div class="library-browser pb-8">
        <div v-if="isLoading" class="loading">
            <span>Loading Your Courses</span>
            <LoadingComponent />
        </div>

        <template v-else>
            <LibraryCarousel v-if="loggedIn" :libraries="myLibraries" :library-favorites-map="favoritesMap"/>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import LoadingComponent from "@/components/Backstage/LoadingComponent.vue";
import LibraryCarousel from "@/components/Game/Creation/LibraryCarousel.vue";

const authStore = useAuthStore();
const isLoading = ref(true);
const myLibraries = ref([]);
const favoritesMap = ref({});

onMounted(() => {
    fetchLibraries();
});

function fetchLibraries() {
    axios
        .get("/api/libraries")
        .then((response) => {
            if (authStore.loggedIn) {
                const combinedLibraries = [
                    ...response.data.mine,
                    ...response.data.joined_public,
                    ...response.data.joined_private
                ];
                
                myLibraries.value = combinedLibraries.sort((a, b) => 
                    a.library_topic.localeCompare(b.library_topic)
                );

                favoritesMap.value = response.data.favorites_map;
            }
        })
        .catch((error) => {
            console.error("Failed to fetch libraries", error);
        })
        .finally(() => {
            isLoading.value = false;
        });
}

const loggedIn = computed(() => authStore.loggedIn);

</script>

<style scoped>
.library-browser {
    width: 98%;
    height: 100%;
    justify-content: center;
    align-items: center;
}

.loading {
    font-size: 1.5em;
    color: var(--text-color);
    display: flex;
    align-items: center;
    gap: 0.5em;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, 500%);
}
</style>
