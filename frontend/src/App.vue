<!-- App.vue -->
<template>
    <div v-if="isLoading">
        <LoadingComponent/>
    </div>
    <div class="app-container" :class="themeClass">
        <div v-if="!hideHeaderFooter">
            <TopBar />
            <SubHeader v-if="loggedIn && shouldShowChat && subheaderExists" :key="forceUpdateKey" />
            <SideMenu />
            <MentorSelection />
        </div>

        <div class="main-content">
            <div class="another" @scroll="onScroll">
                <!-- Routes -->
                <router-view v-if="shouldShowRouterView"></router-view>
                <home-page v-else />
                <InfoPopup />
                <AdPopup />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import TopBar from "./components/Header/TopBar.vue";
import SideMenu from "./components/Header/SideMenu.vue";
import SubHeader from "./components/Header/SubHeader.vue";
import InfoPopup from "./components/Menus/InfoPopup.vue";
import AdPopup from "./components/Monetization/AdPopup.vue";
import MentorSelection from "./components/Backstage/MentorSelection.vue";
import HomePage from './components/Footer/HomePage.vue';
import { useAuthStore } from "@/store/authStore";
import { useMenuStore } from "@/store/menuStore";
import { useThemeStore } from "@/store/themeStore";
import { useMessageStore } from "@/store/messageStore";
import { useScrollStore } from "@/store/scrollStore";
import { useMentorStore } from "@/store/mentorStore";
import { useLoadingStore } from "@/store/loadingStore";
import LoadingComponent from "./components/Backstage/LoadingComponent.vue";

const router = useRouter();
const route = useRoute();
const lastVisible = ref(new Date());
const loadingStore = useLoadingStore();
const isLoading = computed(() => loadingStore.isLoading);

// Computed properties
const hideHeaderFooter = computed(() => route.meta.hideHeaderFooter);

const messageStore = useMessageStore();
const forceUpdateKey = computed(() => messageStore.progress);

const themeStore = useThemeStore();
const themeClass = computed(() => themeStore.darkMode ? "light-theme" : "");

const authStore = useAuthStore();
const loggedIn = computed(() => authStore.loggedIn);

const shouldShowChat = computed(() => {
    const path = route.path;
    return (
        path === "/lessons" ||
        path.includes("/lesson/") ||
        path.includes("/challenge/")
    );
});

const shouldShowRouterView = computed(() => route.path !== "/");

const subheaderExists = computed(() => !(messageStore.subheading === ""));

// Methods
const onScroll = (event: Event) => {
    const scrollStore = useScrollStore();
    const target = event.target as Element;
    scrollStore.scrollTop = target.scrollTop;
};

const refreshApp = () => {
    window.location.reload();
};

const handleVisibilityChange = () => {
    if (document.visibilityState === "visible") {
        const now = new Date();
        const timeDifference = (now.getTime() - lastVisible.value.getTime()) / 1000 / 60;
        if (timeDifference >= 20) {
            // 20 minutes afk to reload
            window.location.reload();
        }
    } else {
        lastVisible.value = new Date();
    }
};

onMounted(() => {
    document.addEventListener("visibilitychange", handleVisibilityChange);

    authStore.checkAuth();

    if (window.location.search === "?awake") {
        router.push("/");
    }
});

onUnmounted(() => {
    document.removeEventListener("visibilitychange", handleVisibilityChange);
});

// Watchers
watch(loggedIn, (newValue) => {
    if (!newValue) {
        console.debug("login from app");
        router.push("/login");
    }
    if (newValue && shouldShowChat.value) {
        // console.log("login fetch");
        messageStore.fetchRecentMessages(route.path);
    }
});

watch(() => route.path, () => {
    // console.log(route.path);
    if (shouldShowChat.value) {
        messageStore.fetchRecentMessages(route.path);
    } else {
        window.scrollTo(0, 0);
    }

    const menuStore = useMenuStore();
    menuStore.hideActionMenu();
    const mentorStore = useMentorStore();
    mentorStore.hide();
    if (window.innerWidth < 1750) {
        menuStore.hideSideMenu();
    }
});
</script>

<style scoped>
.app-container {
    background-color: var(--background-color);
    color: var(--text-color);
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100vw;
    z-index: 1;
}

.main-content {
    overflow-y: auto;
    flex: 1;
    display: flex;
    flex-direction: column;
}

.another {
    display: flex;
    justify-content: center;
    height: 100%;
    overflow: auto;
}
</style>
