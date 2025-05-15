<template>

<!-- Settings Modal -->
<Transition name="modal">
    <div v-if="showSettingsModal" class="fixed inset-0 flex items-center justify-center z-50 p-4"
        style="background-color: var(--background-haze);">
        <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border"
            style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold" style="color: var(--light-text);">
                    Settings
                </h2>
                <button @click="toggleSettings" style="color: var(--highlight-color);">
                    <XMarkIcon class="w-6 h-6" />
                </button>
            </div>
            <!-- Info message about instant changes -->
            <div class="flex items-start gap-2 p-3 mb-4 rounded-lg"
                style="background-color: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2);">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0 mt-0.5" viewBox="0 0 20 20"
                    fill="currentColor" style="color: var(--color-primary-light);">
                    <path fill-rule="evenodd"
                        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9z"
                        clip-rule="evenodd" />
                </svg>
                <p class="text-sm" style="color: var(--color-primary-light);">
                    Changes are applied automatically and take effect immediately.
                </p>
            </div>
            <!-- 💡 Your settings controls go here: -->
            <div class="space-y-4">
                <!-- Course Visibility Toggle -->
                <div>
                    <label class="block text-sm font-medium mb-1" style="color: var(--highlight-color);">
                        Course Visibility
                    </label>
                    <div class="flex mt-2 p-2 rounded-lg" style="background-color: var(--background-color-1t);">
                        <button @click="setLibraryIsPublicStatus(true)"
                            class="flex-1 py-2 px-3 rounded-lg transition-colors" :disabled="isUpdatingVisibility"
                            :style="{
                                backgroundColor: isPublic ? 'var(--element-color-1)' : 'transparent',
                                color: isPublic ? 'var(--light-text)' : 'var(--highlight-color)'
                            }">
                            <span v-if="isUpdatingVisibility && pendingStatus === true">
                                <CogIcon class="w-5 h-5 animate-spin inline" />
                            </span>
                            <span v-else>Public</span>
                        </button>
                        <button @click="setLibraryIsPublicStatus(false)"
                            class="flex-1 py-2 px-3 rounded-lg transition-colors" :style="{
                                backgroundColor: !isPublic ? 'var(--element-color-1)' : 'transparent',
                                color: !isPublic ? 'var(--light-text)' : 'var(--highlight-color)'
                            }">
                            <span v-if="isUpdatingVisibility && pendingStatus === true">
                                <CogIcon class="w-5 h-5 animate-spin inline" />
                            </span>
                            <span v-else>Private</span>
                        </button>
                    </div>
                    <p class="text-xs mt-1" style="color: var(--color-primary-light); font-weight: bold;">
                        {{ !!(isPublic) 
                            ? 'Anyone can view this course' 
                            : joinCode === null
                                ? "Loading..." 
                                : `Only this code can access this course: ${joinCode}` }}
                    </p>
                </div>
            </div>
            <div class="mt-6 flex justify-end">
                <button @click="toggleSettings" class="px-4 py-2 rounded-lg border"
                    style="border-color: var(--color-primary); color: var(--highlight-color);">
                    Close
                </button>
            </div>
        </div>
    </div>
</Transition>
</template>


<script setup lang="ts">

import { ref, watch, onMounted, computed, toRefs } from 'vue';
import axios from 'axios';
import { XMarkIcon, CogIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
    showSettingsModal: {
        type: Boolean,
        required: true
    },
    libraryId: {
        type: Number,
        required: true
    },
    libraryIsPublic: {
        type: Boolean,
        required: true
    },
    libraryJoinCode: {
        type: [String, null],
        required: true
    },
    canModify: {
        type: Boolean,
        required: true
    }
})

const emit = defineEmits(['update:showSettingsModal']);

const showSettingsModal = computed({
  get: () => props.showSettingsModal,
  set: val => emit('update:showSettingsModal', val)
})

const isUpdatingVisibility = ref(false);
const pendingStatus = ref<boolean | null>(null);
const joinCode = ref<string | null>(null);
const isPublic = ref(false);
const { canModify } = toRefs(props);

onMounted(() => {
    // Initialize joinCode and isPublic based on props
    joinCode.value = props.libraryJoinCode;
    isPublic.value = props.libraryIsPublic;
})

watch(() => props.libraryIsPublic, (newVal) => {
    isPublic.value = newVal;
}, { immediate: true });

watch(() => props.libraryJoinCode, (newVal) => {
    joinCode.value = newVal;
}, { immediate: true });

const setLibraryIsPublicStatus = async (newStatus: boolean) => {
    
    if (isPublic.value === newStatus) {
        return; // No change needed
    }
    
    if (canModify.value === false) {
        console.log("hasoidf")
        return; // User does not have permission to change visibility
    }

    const prev = isPublic.value;
    isPublic.value = newStatus;
    isUpdatingVisibility.value = true;

    // pendingStatus.value = newStatus;
    axios.put(`/api/library/visibility_status/${props.libraryId}`, {
        libraryId: props.libraryId,
        newStatus: newStatus
    })
        .then((response) => {
            isPublic.value = newStatus;
            joinCode.value = response.data.join_code; // Update join code if needed
        })
        .catch(() => {
            // console.error('Error updating library visibility:', error);
            isPublic.value = prev; // Revert to previous state on error
        })
        .finally(() => {
            isUpdatingVisibility.value = false;
            // pendingStatus.value = null;
        });
}

function toggleSettings() {
    showSettingsModal.value = !showSettingsModal.value
}

</script>

<style scoped>


/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}
</style>

