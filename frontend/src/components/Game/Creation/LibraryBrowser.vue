<template>
    <div class="library-browser">
        <div v-if="isLoading" class="loading">
            <span>Loading Your Libraries</span>
            <LoadingComponent />
        </div>

        <template v-else>
            <LibraryCarousel v-if="loggedIn && browsingLibraries" title="My Courses" :libraries="myLibraries" />
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import LoadingComponent from "@/components/Backstage/LoadingComponent.vue";
import LibraryCarousel from "./LibraryCarousel.vue";

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const isLoading = ref(true);
const myLibraries = ref([]);

onMounted(() => {
    fetchLibraries();
});

function fetchLibraries() {
    axios
        .get("/api/libraries")
        .then((response) => {
            console.log(response.data.mine);
            if (authStore.loggedIn) {
                myLibraries.value = response.data.mine;
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
