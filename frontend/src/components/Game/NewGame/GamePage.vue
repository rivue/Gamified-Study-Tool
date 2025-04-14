<template>
    <div class="game-page">
        <game-toolbar />
        <game-window />
        <library-completion />
    </div>
</template>

<script setup lang="ts">

import { useGameStore } from "@/store/gameStore";

import GameWindow from "./GameWindow.vue";
import LibraryCompletion from './LibraryCompletion.vue';
import GameToolbar from './GameToolbar.vue';
import { onBeforeRouteLeave } from "vue-router";

onBeforeRouteLeave((to, from, next) => {
    console.log("successfully unmounted");
    useGameStore.resetGameState();
    next();
});

</script>

<style scoped>
.game-page {
    display: flex;
    flex-direction: column;
    width: 100%;
}
</style>