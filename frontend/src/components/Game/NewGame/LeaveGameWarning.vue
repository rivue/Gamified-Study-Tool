<template>
    <Transition name="modal">
        <div v-if="showModal" class="fixed inset-0 flex items-center justify-center z-50 p-4"
            style="background-color: var(--background-haze); pointer-events: auto;">
            <!-- <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border pointer-events-auto"
                style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-semibold">Delete Section</h2>
                    <button @click="closeModal" style="color: var(--highlight-color);">
                        <XMarkIcon class="w-6 h-6" />
                    </button>
                </div>
                <div class="space-y-4">
                    <p>
                        Are you sure you want to leave now? Your progress will be lost
                    </p>
                    <div class="flex justify-end gap-3 mt-6">
                        <button @click="closeModal" class="px-4 py-2 border rounded-lg"
                            style="border-color: var(--color-primary); color: var(--highlight-color);"
                            :disabled="isDeleting" :class="{ 'opacity-50 cursor-not-allowed': isDeleting }">
                            Cancel
                        </button>
                        <button @click="handleLeave"
                            class="px-4 py-2 rounded-lg focus:outline-none focus:ring-2 flex items-center justify-center text-white"
                            style="background: var(--error-color);">
                            <span>Leave</span>
                        </button>
                    </div>
                </div>
            </div> -->
        </div>
    </Transition>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { XMarkIcon } from '@heroicons/vue/24/solid';
import { toast } from 'vue-sonner';

const showModal = ref(false);
const isDeleting = ref(false);

function openModal() {
    showModal.value = true;
}

function closeModal() {
    if (isDeleting.value) {
        toast.warning('Deletion is in progress. Please wait.');
        return;
    }
    showModal.value = false;
    // Values are reset in openModal, but good to ensure clean state if modal can be closed by other means
}

function handleLeave() {
    console.log("idk")
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
</style>