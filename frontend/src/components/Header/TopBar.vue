<template>
    <div class="top-bar">
        <router-link to="/" custom v-slot="{ navigate }">
            <div class="app-title" @click="navigate">{{ pageTitle }}</div>
        </router-link>

        <div class="menu-buttons">
            <div v-if="loggedIn" class="streak-container">
                <div class="streak-wrapper">
                    <img class="logo" src="../../assets/images/fireicon.png" alt="Fire Streak Icon"
                        style="max-height: 24px; pointer-events: none;" />
                    <span class="streak-count">{{ currentStreak }}</span>
                </div>
                <div class="streak-dropdown rounded-2xl">
                    <div class="streak-info text-md text-[var(--highlight-color)] rounded-2xl">
                        <p class="pr-8 pl-4 pt-4 pb-4 rounded-xl">Current Streak: {{ currentStreak }}</p>
                        <p class="pr-8 pl-4 pt-4 pb-4 rounded-xl">Best Streak: {{ bestStreak }}</p>
                    </div>
                </div>
            </div>

            <button class="login-button" v-if=!loggedIn @click="navigateToLogin">
                Log in
            </button>

            <button class="menu-btn icon-btn" @click="toggleSideMenu" aria-label="side menu">
                <span class="menu-line"></span>
                <span class="menu-line"></span>
                <span class="menu-line"></span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useUserStatsStore } from "@/store/userStatsStore";
import { useMenuStore } from "@/store/menuStore";
import { useAuthStore } from "@/store/authStore";
import { computed, onMounted } from "vue";
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const loggedIn = computed(() => authStore.loggedIn);
const router = useRouter();

const userStats = useUserStatsStore();
const { currentStreak, bestStreak } = storeToRefs(userStats);

const menuStore = useMenuStore();

const pageTitle = computed(() => {
    return "rivue.ai";
});

const navigateToLogin = () => {
    if (router.currentRoute.value.path === '/login*') {
        // Clean the URL by removing query parameters
        router.replace('/login');
    } else {
        router.push('/login');
    }
};

const toggleSideMenu = (): void => {
    menuStore.toggleSideMenu();
};

onMounted(() => {
    if (loggedIn.value && userStats.streakLoaded == false) {
        userStats.fetchStreak();
    }
});
</script>
<style scoped>
.top-bar {
    position: -webkit-sticky;
    position: sticky;
    top: 0;
    width: 100%;
    z-index: 200;
    background-color: var(--background-color);
    color: var(--text-color);
    padding: 12px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(8px);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    border-bottom: 1px solid var(--color-primary-dark);
    min-height: 60px;
}

.logo {
    margin-right: 16px;
    cursor: pointer;
}

.app-title {
    display: block;
    margin: 0;
    font-size: 24px;
    text-align: left; /* Changed from center for better flex behavior */
    font-weight: 700;
    cursor: pointer;
    color: var(--text-color);
    /* Allow title to shrink but not grow excessively */
    flex: 0 1 auto;
    min-width: 0; /* Allows shrinking below content size */
    white-space: nowrap; /* Prevents title from wrapping to a new line */
    overflow: hidden; /* Hides any part of the title that doesn't fit */
    text-overflow: ellipsis; /* Adds "..." if the title is too long */
}

.menu-buttons {
    display: flex;
    gap: 12px;
    align-items: center;
    flex-shrink: 0; /* A key change: prevents this container from shrinking */
}

.login-button {
    padding: 12px 16px;
    border-radius: 10px;
    background-color: var(--background-color-1t);
    color: var(--highlight-color);
    border: 1px solid var(--color-primary-dark);
    transition: all 0.2s ease;
    font-weight: 500;
    cursor: pointer;
    font-size: 14px;
    min-height: 44px;
    display: flex;
    align-items: center;
}

.login-button:hover {
    background-color: var(--element-color-1);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-button:active {
    transform: translateY(0);
}

.menu-btn {
    display: flex;
    cursor: pointer;
    padding: 12px;
    border: none;
    background: transparent;
    color: var(--text-color);
    font-size: 14px;
    transition: all 0.2s ease;
    min-height: 44px;
    min-width: 44px;
    align-items: center;
    justify-content: center;
}

.menu-btn.primary {
    background-color: var(--element-color-1);
}

.menu-btn:hover {
    color: var(--element-color-3);
    transform: translateY(-1px);
}

.menu-btn:active {
    transform: translateY(0);
}

.menu-btn.icon-btn {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 12px;
}

.menu-line {
    background-color: var(--text-color);
    height: 2px;
    width: 20px;
    transition: all 0.2s ease;
}

.menu-btn:hover .menu-line {
    width: 24px;
}

.menu-btn.text-btn {
    min-width: 100px;
    text-align: right;
    justify-content: flex-end;
}

.streak-count {
    font-size: 16px;
    font-weight: 600;
    margin-left: -12px;
}

.streak-container {
    position: relative;
    display: inline-flex;
    align-items: center;
    padding: 8px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s ease;
    min-height: 44px;
}

.streak-container:hover {
    background-color: var(--background-color-2t);
}

.streak-wrapper {
    display: flex;
    align-items: center;
}

.streak-dropdown {
    display: none;
    opacity: 0;
    position: absolute;
    top: 100%;
    left: -20%;
    transform: translateX(-50%) translateY(-5px);
    background-color: var(--background-color);
    border: 1px solid var(--color-primary-dark);
    padding: 10px 12px;
    margin-top: 8px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    min-width: 180px;
    transition: opacity 0.2s ease, transform 0.2s ease;
    pointer-events: none;
    backdrop-filter: blur(8px);
}

.streak-container:hover .streak-dropdown {
    display: block;
    opacity: 1;
    transform: translateX(-50%) translateY(0);
    pointer-events: auto;
}

.streak-info p {
    margin: 4px 0;
    white-space: nowrap;
    display: flex;
    justify-content: space-between;
    background-color: var(--background-color-2t);
    border: 1px solid var(--color-primary-dark);
    margin-bottom: 8px;
}

.streak-dropdown::before {
    content: '';
    position: absolute;
    top: -6px;
    left: 70%;
    transform: translateX(-50%);
    width: 12px;
    height: 12px;
    background-color: var(--background-color-2);
    border-left: 1px solid var(--color-primary-dark);
    border-top: 1px solid var(--color-primary-dark);
    transform: translateX(-50%) rotate(45deg);
}

/* Mobile Optimizations */
@media only screen and (max-width: 768px) {
    .top-bar {
        padding: 8px 12px;
        gap: 12px; /* Add gap to ensure spacing */
    }
    
    .app-title {
        font-size: 20px;
    }
    
    .menu-buttons {
        gap: 8px;
    }
    
    .login-button {
        padding: 10px 12px;
        font-size: 13px;
    }
    
    .streak-dropdown {
        left: -50%;
        min-width: 160px;
    }
}

@media only screen and (max-width: 480px) {
    .top-bar {
        padding: 8px;
        min-height: 56px;
        gap: 8px; /* Reduce gap for smaller screens */
    }
    
    .app-title {
        font-size: 18px;
    }
    
    .menu-buttons {
        gap: 4px; /* Tighter gap for the buttons */
    }
    
    .login-button {
        padding: 8px 10px;
        font-size: 12px;
        min-height: 40px;
    }
    
    .streak-container {
        padding: 6px 8px;
        min-height: 40px;
    }
    
    .menu-btn {
        padding: 8px;
        min-height: 40px;
        min-width: 40px;
    }
    
    .streak-count {
        font-size: 14px;
        margin-left: -8px; /* Reduced the aggressive negative margin */
    }
    
    .logo {
        max-height: 20px;
        margin-right: 8px;
    }
    
    .streak-dropdown {
        left: -80%;
        min-width: 140px;
        font-size: 12px;
    }
    
    .streak-info p {
        font-size: 12px;
        padding: 8px 6px;
    }
}

/* Touch device optimizations */
@media (hover: none) and (pointer: coarse) {
    .streak-container:active {
        background-color: var(--background-color-2t);
    }
    
    .streak-container:active .streak-dropdown {
        display: block;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
        pointer-events: auto;
    }
    
    .login-button:hover {
        transform: none;
        box-shadow: none;
    }
    
    .menu-btn:hover {
        transform: none;
    }
    
    .menu-btn:hover .menu-line {
        width: 20px;
    }
}
</style>