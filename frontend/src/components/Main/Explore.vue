<template>
    <div class="library-browser pb-8">
        <div v-if="isLoading" class="loading">
            <span>Loading Public Libraries</span>
            <LoadingComponent />
        </div>

        <template v-else>
            <LibraryCarousel v-if="loggedIn" :libraries="myLibraries" :library-favorites-map="favoritesMap"/>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import LoadingComponent from "@/components/Backstage/LoadingComponent.vue";
import LibraryCarousel from "@/components/Game/Creation/LibraryCarousel.vue";

const authStore = useAuthStore();
const route = useRoute();
const isLoading = ref(true);
const myLibraries = ref([]);
const favoritesMap = ref({});

onMounted(() => {
    console.log("a;sdf")

    fetchLibraries();
});

function fetchLibraries() {
    axios
        .get("/api/libraries")
        .then((response) => {
            if (authStore.loggedIn) {

                console.log("this worls")
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
            console.log("a;sdf")

            console.error("Failed to fetch libraries", error);
        })
        .finally(() => {
            console.log("a;sdf")

            isLoading.value = false;
        });
}

const loggedIn = computed(() => authStore.loggedIn);

const browsingLibraries = computed(() => route.path === "/library");

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
