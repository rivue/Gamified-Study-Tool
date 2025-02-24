<template>
    <div class="top-bar">
        <router-link to="/" custom v-slot="{ navigate }">
            <div class="app-title" @click="navigate">{{ pageTitle }}</div>
        </router-link>

        <div class="menu-buttons">
            <router-link to="/library" custom v-slot="{ navigate }">
                <button class="menu-btn" @click="navigate" aria-label="menu action 1">
                    My Library
                </button>
            </router-link>
            <button class="menu-btn" @click="toggleSideMenu" aria-label="menu action 2">
                Contact
            </button>
            <button class="menu-btn icon-btn" @click="toggleSideMenu" aria-label="side menu">
                <span class="menu-line"></span>
                <span class="menu-line"></span>
                <span class="menu-line"></span>
            </button>
        </div>
    </div>
</template>

<script>
import { useMenuStore } from "@/store/menuStore";
import { useThemeStore } from "@/store/themeStore";

export default {
    name: "TopBar",
    computed: {
        logoPath() {
            const themeStore = useThemeStore();
            return themeStore.darkMode
                ? require("@/assets/images/ascendance_logo-black.png")
                : require("@/assets/images/ascendance_logo.png");
        },
        pageTitle() {
            if (this.$route.path.includes("lesson/")) {
                // return "Ascendance (rivur)·📖";
                return "rivur.";
            } else if (this.$route.path.includes("challenge/")) {
                // return "Ascendance (rivur)·🎯";
                return "rivur.";
            } else if (this.$route.path.includes("progress/")) {
                // return "Ascendance (rivur)·📈";
                return "rivur.";
            } else if (this.$route.path.includes("achievements/")) {
                // return "Ascendance (rivur)·🏅";
                return "rivur.";
            } else if (this.$route.path.includes("settings/")) {
                // return "Ascendance (rivur)·🔧";
                return "rivur.";
            } else {
                // return "Ascendance·(rivur)☁️";
                return "rivur.";
            }
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

.menu-btn.icon-btn:hover {
    color: var(--element-color-3);
    transform: translateY(-1px);
}

.menu-btn.text-btn {
    min-width: 100px;
    /* ensures consistent button width */
    text-align: right;
    justify-content: flex-end;
}
</style>