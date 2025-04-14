<template>
    <div
      v-if="isVisible"
      class="next-container"
      :style="{ backgroundImage: 'url(' + gameStore.imageUrl + ')' }"
    >
      <div class="next-room-title">Where to go next?</div>
      <div class="next-room-buttons">
        <RoomButton
          v-for="(room, index) in rooms"
          :key="index"
          @click="openRoom(room.roomName)"
          :label="room.roomName"
          :isLoading="room.isLoading"
          :position="index"
        />
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from "vue";
  import { useGameStore } from "@/store/gameStore";
  import RoomButton from "./RoomButton.vue";
  
  // Store
  const gameStore = useGameStore();
  
  // Computed visibility flag
  const isVisible = computed(() => gameStore.showNext);
  
  // Room list with metadata
  const rooms = computed(() =>
    gameStore.nextRooms.map((roomName: string) => {
      const roomState = gameStore.roomStates[roomName]?.state || 0;
      return {
        roomName,
        isLoading: roomState === 1, // state === 1 means loading
      };
    })
  );
  
  // Open room
  const openRoom = (roomName: string) => {
    if (gameStore.roomStates[roomName]?.state === 2) {
      gameStore.openRoom(roomName);
    }
  };
  </script>
  
  <style scoped>
  .next-container {
    background-size: cover;
    background-position: center;
    width: 100%;
    height: 100%;
    max-width: 512px;
    max-height: 512px;
    display: flex;
    flex-direction: column-reverse;
  }
  .next-room-buttons {
    width: 90%;
    margin: 0px auto;
  }
  .next-room-title {
    font-weight: 700;
    padding: 4px;
  }
  </style>
  