<!-- App.vue -->
<template>
    <Toaster />
    <TooltipProvider :openDelay="180" :closeDelay="80">
        <div class="app-container" :class="themeClass">
            <div v-if="!hideHeaderFooter">
                <TopBar />
                <SideMenu />
                <MentorSelection />
            </div>
            
            <div class="main-content">
                <div class="another" @scroll="onScroll">
                    <!-- Routes -->
                    <router-view v-if="shouldShowRouterView"></router-view>
                    <!-- <home-page v-else /> -->
                    <InfoPopup />
                    <AdPopup />
                </div>
            </div>
            <KatelynBirthdaySurprise v-if="showKatelynSurprise" @close="handleBirthdayClose" />
        </div>
    </TooltipProvider>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import TopBar from "./components/Header/TopBar.vue";
import SideMenu from "./components/Header/SideMenu.vue";
import InfoPopup from "./components/Menus/InfoPopup.vue";
import AdPopup from "./components/Monetization/AdPopup.vue";
import MentorSelection from "./components/Backstage/MentorSelection.vue";
import { useAuthStore } from "@/store/authStore";
import { useMenuStore } from "@/store/menuStore";
import { useThemeStore } from "@/store/themeStore";
import { useMessageStore } from "@/store/messageStore";
import { useScrollStore } from "@/store/scrollStore";
import { useMentorStore } from "@/store/mentorStore";
import { useLoadingStore } from "@/store/loadingStore";
import { useUserStatsStore } from "@/store/userStatsStore";
import { Toaster } from '@/components/ui/sonner'
import { TooltipProvider } from '@/components/ui/tooltip'
import 'vue-sonner/style.css' // vue-sonner v2 requires this import
import KatelynBirthdaySurprise from '@/components/Celebration/KatelynBirthdaySurprise.vue'

const router = useRouter();
const route = useRoute();
const lastVisible = ref(new Date());

// Computed properties
const hideHeaderFooter = computed(() => route.meta.hideHeaderFooter);

const messageStore = useMessageStore();

const themeStore = useThemeStore();
const themeClass = computed(() => themeStore.darkMode ? "light-theme" : "");

const authStore = useAuthStore();
const loggedIn = computed(() => authStore.loggedIn);

const userStatsStore = useUserStatsStore();

const shouldShowChat = computed(() => {
    const path = route.path;
    return (
        path === "/lessons" ||
        path.includes("/lesson/") ||
        path.includes("/challenge/")
    );
});

const shouldShowRouterView = computed(() => route.path !== "/");

const showKatelynSurprise = ref(false);
const katelynDismissed = ref(false);
const isKatelynTesting = ref(false);
const BIRTHDAY_EMAIL = 'brownkt27@gmail.com';
const BIRTHDAY_SESSION_KEY = 'katelyn-birthday-surprise';
const BIRTHDAY_TEST_FLAG = 'katelyn-birthday-test-flag';

const getSessionStore = () => {
    if (typeof window === 'undefined') {
        return null;
    }
    return window.sessionStorage;
};

const getLocalStore = () => {
    if (typeof window === 'undefined') {
        return null;
    }
    return window.localStorage;
};

const clearKatelynDismissal = () => {
    const sessionStore = getSessionStore();
    sessionStore?.removeItem(`${BIRTHDAY_SESSION_KEY}-dismissed`);
    katelynDismissed.value = false;
};

const maybeShowKatelynSurprise = () => {
    if (katelynDismissed.value && !isKatelynTesting.value) {
        return;
    }

    if (!authStore.loggedIn && !isKatelynTesting.value) {
        showKatelynSurprise.value = false;
        return;
    }

    const username = authStore.user.username?.toLowerCase();
    const isBirthdayMatch = username === BIRTHDAY_EMAIL;
    if (isKatelynTesting.value || isBirthdayMatch) {
        const sessionStore = getSessionStore();
        if (isBirthdayMatch && sessionStore && !sessionStore.getItem(BIRTHDAY_SESSION_KEY)) {
            sessionStore.setItem(BIRTHDAY_SESSION_KEY, new Date().toISOString());
        }
        showKatelynSurprise.value = true;
    } else {
        showKatelynSurprise.value = false;
    }
};

const handleBirthdayClose = () => {
    katelynDismissed.value = true;
    showKatelynSurprise.value = false;
    const sessionStore = getSessionStore();
    sessionStore?.setItem(`${BIRTHDAY_SESSION_KEY}-dismissed`, 'true');
};

const hydrateDismissState = () => {
    const sessionStore = getSessionStore();
    if (sessionStore?.getItem(`${BIRTHDAY_SESSION_KEY}-dismissed`)) {
        katelynDismissed.value = true;
    }
};

const applyTestingFlagFromQuery = () => {
    if (typeof window === 'undefined') {
        return;
    }
    const localStore = getLocalStore();
    const params = new URLSearchParams(window.location.search);
    if (params.has('katelynTest')) {
        const value = params.get('katelynTest');
        if (value === '1') {
            localStore?.setItem(BIRTHDAY_TEST_FLAG, 'true');
            isKatelynTesting.value = true;
            clearKatelynDismissal();
        } else if (value === '0') {
            localStore?.removeItem(BIRTHDAY_TEST_FLAG);
            isKatelynTesting.value = false;
        }
    } else {
        const storedValue = localStore?.getItem(BIRTHDAY_TEST_FLAG);
        if (storedValue === 'true') {
            isKatelynTesting.value = true;
            clearKatelynDismissal();
        }
    }
};


// Methods
const onScroll = (event: Event) => {
    const scrollStore = useScrollStore();
    const target = event.target as Element;
    scrollStore.scrollTop = target.scrollTop;
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
    if (authStore.loggedIn) {
        userStatsStore.fetchStreak();
    }

    applyTestingFlagFromQuery();
    hydrateDismissState();
    maybeShowKatelynSurprise();

    if (window.location.search === "?awake") {
        router.push("/");
    }
});

onUnmounted(() => {
    document.removeEventListener("visibilitychange", handleVisibilityChange);
});

// Watchers
watch(() => authStore.loggedIn, (loggedIn) => {
  if (loggedIn) userStatsStore.fetchStreak();
  else         userStatsStore.resetStats();
});

watch(loggedIn, (newValue) => {
    if (!newValue) {
        console.debug("login from app");
        router.push("/login");
        if (!isKatelynTesting.value) {
            showKatelynSurprise.value = false;
        }
    }
    if (newValue && shouldShowChat.value) {
        // console.log("login fetch");
        messageStore.fetchRecentMessages(route.path);
    }
    if (newValue) {
        const sessionStore = getSessionStore();
        katelynDismissed.value = sessionStore?.getItem(`${BIRTHDAY_SESSION_KEY}-dismissed`) === 'true';
        maybeShowKatelynSurprise();
    }
});

watch(() => authStore.user.username, () => {
    if (authStore.loggedIn) {
        maybeShowKatelynSurprise();
    }
});

watch(isKatelynTesting, () => {
    if (isKatelynTesting.value) {
        clearKatelynDismissal();
    }
    maybeShowKatelynSurprise();
});

watch(() => route.path, () => {
    // console.log(route.path);
    if (shouldShowChat.value) {
        // messageStore.fetchRecentMessages(route.path);
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
    overscroll-behavior-x: none;
    overscroll-behavior-y: none;
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
    overflow-y: auto; /* Only vertical scroll */
    overflow-x: hidden; /* Disable horizontal swipe */
    overscroll-behavior: contain; /* Prevent pull-to-refresh and bounce */
    touch-action: pan-y; /* Only allow vertical scrolling gestures */
}
</style>
