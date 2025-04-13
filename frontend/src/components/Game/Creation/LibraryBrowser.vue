<template>
    <div class="library-browser">
        <div v-if="isLoading" class="loading">
            <span>Loading Your Libraries</span>
            <LoadingComponent />
        </div>
      
        <template v-else>
            <LibraryCarousel 
                v-if="loggedIn & browsingLibraries"
                title="My Courses" 
                :libraries="myLibraries"
            />
        </template>
    </div>
</template>

<script>
import axios from "axios";
import { useAuthStore } from "@/store/authStore.Ts";
import LoadingComponent from "@/components/Backstage/LoadingComponent.vue";
import LibraryCarousel from "./LibraryCarousel.vue";
export default {
    name: "LibraryBrowser",
    components: {
        LoadingComponent,
        LibraryCarousel,
    },
    data() {
        return {
            isLoading: true,
            myLibraries: [],
        };
    },
    mounted() {
        this.fetchLibraries();
    },
    methods: {
        fetchLibraries() {
            axios
                .get("/api/libraries")
                .then((response) => {
                    if (this.loggedIn) {
                        this.myLibraries = response.data.mine;
                    }
                })
                .catch((error) => {
                    console.error("Failed to fetch libraries", error);
                })
                .finally(() => {
                    this.isLoading = false;
                });
        },
    },
    computed: {
        loggedIn() {
            const authStore = useAuthStore();
            return authStore.loggedIn;
        },
        browsingLibraries() {
            return this.$route.path === "/library";
        }
    }
};
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
