<template>
    <div class="library-explorer pb-8 pt-8">
        <div v-if="isLoading" class="loading-explorer">
            <span>Loading Public Libraries</span>
            <LoadingComponent />
        </div>

        <template v-else>
            <ExploreCarousel v-if="loggedIn" :libraries="myLibraries"/>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import LoadingComponent from "@/components/Backstage/LoadingComponent.vue";
import ExploreCarousel from "@/components/Main/ExploreCarousel.vue";

const authStore = useAuthStore();
const route = useRoute();
const isLoading = ref(true);
const myLibraries = ref([]);

onMounted(() => {

    fetchLibraries();
});

function fetchLibraries() {
    axios
        .get("/api/libraries", { params: { browse: true } })
        .then((response) => {
            if (authStore.loggedIn) {
            console.log(response)
            myLibraries.value = response.data.explore_libraries.map(([library, username]) => ({
                ...library,
                owner_username: username,
                // library_topic: library.library_topic.charAt(0).toUpperCase() + library.library_topic.slice(1)
            })).sort((a, b) => 
                a.library_topic.localeCompare(b.library_topic)
            );
            }
            console.log(myLibraries.value)
        })
        .catch((error) => {

            console.error("Failed to fetch libraries", error);
        })
        .finally(() => {

            isLoading.value = false;
        });
}

const loggedIn = computed(() => authStore.loggedIn);

const browsingLibraries = computed(() => route.path === "/library");

</script>

<style scoped>
.library-explorer {
    width: 98%;
    height: 100%;
    justify-content: center;
    align-items: center;
}

.loading-explorer {
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
