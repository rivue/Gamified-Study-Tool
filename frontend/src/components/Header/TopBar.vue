<template>
    <div class="top-bar">
        <router-link to="/" custom v-slot="{ navigate }">
            <div class="app-title" @click="navigate">{{ pageTitle }}</div>
        </router-link>
        <div class="menu-buttons">
            <div v-if="loggedIn" class="streak-container">
                <div class="streak-wrapper">
                    <img class="logo" src="../../../dist/img/fireicon.png" alt="Logo"
                        style="max-height: 24px; pointer-events: none;" />
                    <span class="streak-count">{{ currentStreak }}</span>
                </div>
                <div class="streak-dropdown">
                    <div class="streak-info">
                        <p>Current Streak: {{ currentStreak }} days</p>
                        <p>Best Streak: {{ bestStreak }} days</p>
                    </div>
                </div>
            </div>
            <button class="menu-btn icon-btn" @click="toggleSideMenu" aria-label="side menu">
                <span class="menu-line"></span>
                <span class="menu-line"></span>
                <span class="menu-line"></span>
            </button>
        </div>
    </div>
</template>

<script>
import { storeToRefs } from "pinia";
import { useUserStatsStore } from "@/store/userStatsStore";
import { useMenuStore } from "@/store/menuStore";
import { useThemeStore } from "@/store/themeStore";
import { useAuthStore } from "@/store/authStore";
import { computed } from "vue";

export default {
    name: "TopBar",
    setup() {
        const authStore = useAuthStore();
        const loggedIn = computed(() => authStore.loggedIn);

        const userStats = useUserStatsStore();
        const { currentStreak, bestStreak } = storeToRefs(userStats);

        return {
            loggedIn,
            currentStreak,
            bestStreak
        };
    },
    computed: {
        logoPath() {
            const themeStore = useThemeStore();
            return themeStore.darkMode
                ? require("@/assets/images/rivueai_logo-black.png")
                : require("@/assets/images/rivueai_logo.png");
        },
        pageTitle() {
            return "rivue.ai";
        },
    },
    methods: {
        toggleSideMenu() {
            const menuStore = useMenuStore();
            menuStore.toggleSideMenu();
        },
    },
};
</script>

<style scoped>
.top-bar {
    position: -webkit-sticky;
    position: sticky;
    top: 0;
    width: 100%;
    z-index: 200;
    background-color: var(--background-color-1t);
    color: var(--text-color);
    padding: 4px;
    padding-left: 8px;
    padding-right: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(8px);
    box-shadow: 0 0 2px 2px var(--background-color-1t);
}

.logo {
    margin-right: 16px;
    cursor: pointer;
}

.app-title {
    /* font-family: "Arial", sans-serif; */
    display: block;
    margin: 0;
    font-size: 24px;
    text-align: center;
    font-weight: 700;
    cursor: pointer;
}

.menu-buttons {
    display: flex;
    gap: 16px;
    align-items: center;
}

.menu-btn {
    display: flex;
    cursor: pointer;
    padding: 4px 0;
    border: none;
    background: transparent;
    color: var(--text-color);
    font-size: 14px;
    transition: all 0.2s ease;
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
    padding: 8px;
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
    /* ensures consistent button width */
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
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.streak-container:hover {
    background-color: var(--background-color-2t);
}

.streak-container:hover .streak-dropdown {
    display: block;
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

.streak-wrapper {
    display: flex;
    align-items: center;
}

.streak-dropdown {
    display: block;
    opacity: 0;
    position: absolute;
    top: 100%;
    left: -20%;
    transform: translateX(-50%) translateY(-5px);
    background-color: var(--background-color-2);
    border: 1px solid var(--highlight-color);
    border-radius: 6px;
    padding: 10px 12px;
    margin-top: 8px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    min-width: 180px;
    transition: opacity 0.2s ease, transform 0.2s ease;
    pointer-events: none;
}

.streak-container:hover .streak-dropdown {
    pointer-events: auto;
}

.streak-info p {
    margin: 4px 0;
    font-size: 14px;
    white-space: nowrap;
    display: flex;
    justify-content: space-between;
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
    border-left: 1px solid var(--highlight-color);
    border-top: 1px solid var(--highlight-color);
    transform: translateX(-50%) rotate(45deg);
}
</style>