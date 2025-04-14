<!-- ChatComponent.vue -->
<template>
    <div class="main-container">
        <div class="message-history" ref="msgHistory">
            <ChatConversation />
        </div>
        <MessageInput class="message-input" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import MessageInput from "./MessageInput.vue";
import ChatConversation from "./ChatConversation.vue";
import { useScrollStore } from "@/store/scrollStore";
import { useMessageStore } from "@/store/messageStore";
import eventBus from "@/eventBus";

const msgHistory = ref<HTMLElement | null>(null);
const messageStore = useMessageStore();
const scrollStore = useScrollStore();

onMounted(() => {
    const path = window.location.pathname;
    messageStore.fetchRecentMessages(path);
    eventBus.on("scroll-to-message", handleScrollToMessage);
});

onUnmounted(() => {
    eventBus.off("scroll-to-message");
});

const handleScrollToMessage = (topPosition: number) => {
    // console.log("handleScrollToMessage" + topPosition);
    scrollStore.scrollTop = topPosition;
    if (msgHistory.value) {
        msgHistory.value.scrollTop = topPosition;
    }

    // Try another bit
    topPosition = topPosition - 12;
    scrollStore.scrollTop = topPosition;
    if (msgHistory.value) {
        msgHistory.value.scrollTop = topPosition;
    }
};
</script>

<style scoped>
.main-container {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.message-history {
    padding: 1rem;
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
    flex-grow: 1;
    overflow-y: auto;
    scrollbar-width: auto;
    scrollbar-color: transparent transparent;
    position: relative;
    display: flex;
    flex-direction: column-reverse;
}

.message-input {
    position: sticky;
    bottom: 0;
}

/* Webkit browsers (e.g., Chrome, Safari) scrollbar styles */
.message-history::-webkit-scrollbar {
    width: 12px;
}

.message-history::-webkit-scrollbar-track {
    background: transparent;
    transition: background 0.3s ease;
}

.message-history::-webkit-scrollbar-thumb {
    background-color: transparent;
    border-radius: 6px;
    transition: background-color 0.3s ease;
}

.message-history:hover {
    scrollbar-color: var(--element-color-1) var(--background-color-1t);
}

.message-history:hover::-webkit-scrollbar-track {
    background: var(--background-color-1t);
}

.message-history:hover::-webkit-scrollbar-thumb {
    background-color: var(--element-color-1);
}

.message-history::-webkit-scrollbar-thumb:hover {
    background-color: var(--element-color-2);
}
</style>
