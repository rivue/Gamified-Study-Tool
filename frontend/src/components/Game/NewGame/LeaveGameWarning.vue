<template>
    <div class="close-button" @click="showLeavePopup">x</div>
    <Transition name="modal">
        <div v-if="showPopup" class="fixed inset-0 flex items-center justify-center z-50 p-4"
            style="background-color: var(--background-haze); pointer-events: auto;">
            <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border pointer-events-auto"
                style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-semibold">Leave Lesson</h2>
                    <button @click="hideLeavePopup" style="color: var(--highlight-color);">
                        <XMarkIcon class="w-6 h-6" />
                    </button>
                </div>
                <div class="space-y-4">
                    <p>
                        Are you sure you want to leave now? Your progress will be lost
                    </p>
                    <div class="flex justify-end gap-3 mt-6">
                        <button @click="hideLeavePopup" class="px-4 py-2 border rounded-lg"
                            style="border-color: var(--color-primary); color: var(--highlight-color);">
                            Stay
                        </button>
                        <button @click="handleLeave"
                            class="px-4 py-2 rounded-lg focus:outline-none focus:ring-2 flex items-center justify-center text-white"
                            style="background: var(--error-color);">
                            <span>Leave</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup lang="ts">

import { XMarkIcon } from '@heroicons/vue/24/solid';
import { useRoute, useRouter } from 'vue-router';
import { ref } from 'vue';

const showPopup = ref(false);

const route = useRoute();
const router = useRouter();

function showLeavePopup() {
    showPopup.value = true;

}

function hideLeavePopup() {
    showPopup.value = false;
}

function handleLeave() {
    router.push(`/lessons/${route.params.id}`);
}

</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

/* Optional: transition for the modal's inner content */
.modal-enter-active .rounded-2xl,
.modal-leave-active .rounded-2xl {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal-enter-from .rounded-2xl,
.modal-leave-to .rounded-2xl {
    transform: scale(0.95);
    opacity: 0;
}

.close-button {
    position: fixed; /* Change from absolute to fixed */
    width: 40px; /* Slightly larger for better touch targets */
    height: 40px;
    background: rgba(255, 0, 0, 0.8);
    color: white;
    border-radius: 50%;
    text-align: center;
    line-height: 40px;
    font-size: 1.3em;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
    top: 80px; /* Position from top of viewport */
    left: 20px; /* Position from left of viewport */
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
}

.close-button:hover {
    background: rgba(255, 0, 0, 1);
}
</style>