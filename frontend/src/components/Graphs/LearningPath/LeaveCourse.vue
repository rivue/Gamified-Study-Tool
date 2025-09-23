<template>
    <teleport to="body">
        <Transition name="modal">
            <div v-if="showModal" class="fixed inset-0 flex items-center justify-center z-50 p-4"
                style="background-color: var(--background-haze); pointer-events: auto;">
                <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border pointer-events-auto"
                    style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-semibold">Remove Course</h2>
                        <button @click="closeModal" style="color: var(--highlight-color);"
                            :disabled="isLeaving"
                            :class="{ 'opacity-50 cursor-not-allowed': isLeaving }">
                            <XMarkIcon class="w-6 h-6" />
                        </button>
                    </div>
                    <div class="space-y-4">
                        <p>
                            Are you sure you want to remove the course
                            <strong style="color: var(--highlight-color);">"{{ libraryTopic }}"</strong>?
                            This action cannot be undone.
                        </p>
                        <div>
                            <label for="confirmationInputLeave" class="block text-sm font-medium mb-1">
                                To confirm, please type the course name:
                            </label>
                            <input id="confirmationInputLeave" v-model="confirmationInput" type="text"
                                class="w-full p-2 border rounded-lg"
                                style="background-color: var(--background-color-1t); color: var(--light-text); border-color: var(--color-primary-dark);"
                                :placeholder="libraryTopic"
                                :disabled="isLeaving" />
                            <p v-if="confirmationError && !isConfirmationValid" class="mt-1 text-sm" style="color: var(--error-color);">
                                {{ confirmationError }}
                            </p>
                        </div>

                        <p v-if="apiError" class="mt-2 text-sm" style="color: var(--error-color);">
                            {{ apiError }}
                        </p>

                        <div class="flex justify-end gap-3 mt-6">
                            <button @click="closeModal" class="px-4 py-2 border rounded-lg"
                                style="border-color: var(--color-primary); color: var(--highlight-color);"
                                :disabled="isLeaving"
                                :class="{ 'opacity-50 cursor-not-allowed': isLeaving }">
                                Cancel
                            </button>
                            <button @click="handleLeaveCourse"
                                class="px-4 py-2 rounded-lg focus:outline-none focus:ring-2 flex items-center justify-center text-white"
                                style="background: var(--error-color);" 
                                :disabled="!isConfirmationValid || isLeaving"
                                :class="{ 
                                    'opacity-50 cursor-not-allowed': !isConfirmationValid || isLeaving, 
                                    'hover:opacity-90 active:opacity-80': isConfirmationValid && !isLeaving 
                                }">
                                <span v-if="isLeaving">
                                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg"
                                        fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                        </path>
                                    </svg>
                                </span>
                                <span v-else>Leave Course</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </Transition>
    </teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { XMarkIcon } from '@heroicons/vue/24/solid'; // Using XMarkIcon for close
import { toast } from 'vue-sonner';
import axios from 'axios';
import { useRouter } from 'vue-router';

const props = defineProps({
    showModal: {
        type: Boolean,
        required: true
    },
    libraryId: {
        type: Number,
        required: true
    },
    libraryTopic: {
        type: String,
        required: true
    },
    fromExplore: {
        type: Boolean,
        required: false,
        default: false
    }
});

const emit = defineEmits(['update:showModal', 'course-left']);

const router = useRouter();

const confirmationInput = ref('');
const isLeaving = ref(false);
const apiError = ref('');
const confirmationError = ref('');

const isConfirmationValid = computed(() => confirmationInput.value === props.libraryTopic);

watch(confirmationInput, (newValue) => {
    if (newValue && newValue !== props.libraryTopic) {
        confirmationError.value = 'The typed name does not match the course name.';
    } else {
        confirmationError.value = '';
    }
});

watch(() => props.showModal, (newVal) => {
    if (newVal) {
        // Reset fields when modal becomes visible
        confirmationInput.value = '';
        apiError.value = '';
        confirmationError.value = '';
        isLeaving.value = false;
    }
});

function closeModal() {
    if (isLeaving.value) {
        toast.warning('Action in progress. Please wait.');
        return;
    }
    emit('update:showModal', false);
}

async function handleLeaveCourse() {
    if (!isConfirmationValid.value || isLeaving.value) {
        if (!isConfirmationValid.value) {
            confirmationError.value = 'The typed name does not match the course name.';
        }
        return;
    }
    
    apiError.value = ''; 
    isLeaving.value = true;
    const toastId = toast.loading(`Leaving course "${props.libraryTopic}"...`);

    try {
        const response = await axios.delete(`/api/library/${props.libraryId}/leave`);
        console.log(response)
        if (response.status === 200 && response.data?.status === "success") {
            toast.success(`Successfully left "${props.libraryTopic}".`, { id: toastId });
            emit('course-left', props.libraryId);
            closeModal();
            if (props.fromExplore) {
                router.push('/home'); 
            }
        } else {
            const errorMessage = 'An unexpected error occurred.';
            apiError.value = errorMessage;
            toast.error(errorMessage, { id: toastId });
        }
    } catch (error: any) {
        console.error('Error leaving course:', error);
        const errorMessage = 'Failed to leave course. Please try again.';
        apiError.value = errorMessage;
        toast.error(errorMessage, { id: toastId });
       
    } finally {
        isLeaving.value = false;
    }
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
