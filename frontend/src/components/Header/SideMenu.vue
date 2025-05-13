<template>
    <Transition name="slide"> 
        <div v-if="sideMenuOpen" class="fixed top-16 right-0 w-64 h-auto z-50 p-4 rounded-l-2xl shadow-xl border"
            style="background-color: var(--background-color); border-color: var(--color-primary-dark);">
            <div class="space-y-3">

                <!-- Menu Buttons -->
                <div class="menu-buttons space-y-2">
                    <SideMenuButton
                        v-if="!loggedIn"
                        label="Log in"
                        :isSelected="isRouteActive('/login')"
                        @click="openRoute('/login')"
                        class="menu-button"
                    />

                    <SideMenuButton
                        label="My Libraries"
                        :isSelected="isRouteActive('/library')"
                        @click="openRoute('/library')"
                        class="menu-button"
                    />

                    
                    <SideMenuButton
                        v-if="loggedIn"
                        label="Settings"
                        :isSelected="isRouteActive('/settings')"
                        @click="openRoute('/settings')"
                        class="menu-button"
                    />
                    
                    <SideMenuButton
                        label="Contact"
                        :isSelected="isRouteActive('/contact')"
                        @click="openRoute('/contact')"
                        class="menu-button"
                    />

                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup lang="ts">
import SideMenuButton from "@/components/Menus/SideMenuButton.vue";
import { useMenuStore } from "@/store/menuStore";
import { useAuthStore } from "@/store/authStore";
import { useRouter, useRoute } from "vue-router";
import { computed } from "vue";

const menuStore = useMenuStore();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const sideMenuOpen = computed(() => menuStore.sideMenuOpen);
const loggedIn = computed(() => authStore.loggedIn);

function isRouteActive(target: string, pattern: string | null = null): boolean {
    if (target === "/" && route.path !== "/") return false;
    if (pattern && new RegExp(pattern).test(route.path)) return true;
    return route.path === target;
}

function openRoute(target: string) {
    router.push(target);
    menuStore.hideSideMenu();
}
</script>

<style scoped>
/* Slide transition */
.slide-enter-active,
.slide-leave-active {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
    transform: translateX(100%);
    opacity: 0;
}

.menu-buttons {
    display: flex;
    flex-direction: column;
}

.menu-button {
    width: 100%;
    padding: 10px 16px;
    margin-bottom: 8px;
    border-radius: 10px;
    background-color: var(--background-color-1t);
    color: var(--highlight-color);
    border: 1px solid var(--color-primary-dark);
    transition: all 0.2s ease;
    text-align: left;
    font-weight: 500;
}

.menu-button:hover {
    background-color: var(--element-color-1);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.menu-button:active {
    transform: translateY(0);
}

.menu-button.selected {
    background-color: var(--element-color-1);
    border-color: var(--color-primary);
    color: var(--light-text);
}
</style>
