<template>
  <aside :class="{ 'slide-out': sideMenuOpen }" class="side-menu">
    
    <SideMenuButton
      v-if="!loggedIn"
      label="Log in"
      :isSelected="isRouteActive('/login')"
      @click="openRoute('/login')"
    >
    </SideMenuButton>

    <SideMenuButton
      label="My Library "
      :isSelected="isRouteActive('/library')"
      @click="openRoute('/library')"
    >
      <!-- <template v-slot:icon>🏛</template> -->
    </SideMenuButton>
<!-- TODO look at these more -->
    <!-- <SideMenuButton
      v-if="loggedIn"
      label="Lessons"
      :isSelected="isRouteActive('/lessons')"
      @click="openRoute('/lessons')"
    >
      <template v-slot:icon>&#128172;</template>
    </SideMenuButton> -->

    <!-- <SideMenuButton
      v-if="loggedIn"
      label="Knowledge Map"
      :isSelected="isRouteActive('/knowledge')"
      @click="openRoute('/knowledge')"
    >
      <template v-slot:icon>🗺️</template>
    </SideMenuButton> -->
    <!-- <SideMenuButton
      v-if="loggedIn"
      label="Progress"
      :isSelected="isRouteActive('/progress')"
      @click="openRoute('/progress')"
    >
      <template v-slot:icon>&#128200;</template>
    </SideMenuButton> -->
    <SideMenuButton
      label="Changelog"
      :isSelected="isRouteActive('/changelog')"
      @click="openRoute('/changelog')"
    > 
    </SideMenuButton>

    <SideMenuButton
      label="Contact"
      :isSelected="isRouteActive('/contact')"
      @click="openRoute('/contact')"
    >
      <!-- <template v-slot:icon>&#9993;</template> -->
    </SideMenuButton>
    
    <!-- <SideMenuButton
      label="Terms & Policies"
      :isSelected="isRouteActive('/terms')"
      @click="openRoute('/terms')"
    >
      <template v-slot:icon>&#128279;</template>
    </SideMenuButton> -->
    <SideMenuButton
      v-if="loggedIn"
      label="Settings"
      :isSelected="isRouteActive('/settings')"
      @click="openRoute('/settings')"
    >
      <!-- <template v-slot:icon>&#128295;</template> -->
    </SideMenuButton>
  </aside>
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
.side-menu {
  padding: 4px;
  margin-left: 2px;
  margin-right: 6px;
  position: fixed;
  top: 44px;
  right: -300px;
  height: fit-content;
  width: 210px;
  transition: right 0.3s ease;
  z-index: 200;
}

.slide-out {
  right: 0;
}

button {
  padding: 8px 16px;
  margin: 4px;
  background-color: var(--background-color-1t);
  border: 2px solid var(--text-color);
  border-radius: 8px;
  display: inline-block;
  width: 100%;
  backdrop-filter: blur(8px);
  transition: transform 0.2s, background-color 0.2s;
}

button:hover {
  background-color: var(--element-color-1);
  border-color: #e0e0e0;
}

button:active {
  transform: scale(0.95);
}

button.selected {
  background-color: var(--element-color-1);
  border-color: #e0e0e0;
}
</style>
