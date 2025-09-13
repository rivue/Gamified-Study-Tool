<template>
  <div class="inline-flex">
    <Tooltip>
      <TooltipTrigger>
        <button @click="openModal"
                class="action-button delete-button"
                :disabled="isDeleting"
                :class="{ 'opacity-50 cursor-not-allowed': isDeleting }"
                title="Delete Material">
          <TrashIcon class="w-5 h-5" />
        </button>
      </TooltipTrigger>
      <TooltipContent variant="shad" side="top" :offset="5">
        Delete this material
      </TooltipContent>
    </Tooltip>

    <teleport to="body">
      <Transition name="modal">
        <div v-if="showModal" class="fixed inset-0 flex items-center justify-center z-50 p-4"
             style="background-color: var(--background-haze); pointer-events: auto;">
          <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border pointer-events-auto"
               style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-semibold">Delete Material</h2>
              <button @click="closeModal" style="color: var(--highlight-color);"
                      :disabled="isDeleting"
                      :class="{ 'opacity-50 cursor-not-allowed': isDeleting }">
                <XMarkIcon class="w-6 h-6" />
              </button>
            </div>
            <div class="space-y-4">
              <p>
                Are you sure you want to delete
                <strong style="color: var(--highlight-color);">"{{ materialName }}"</strong>?
                This action cannot be undone.
              </p>
              <div>
                <label for="confirmationInputMaterial" class="block text-sm font-medium mb-1">
                  To confirm, please type the material name:
                </label>
                <input id="confirmationInputMaterial" v-model="confirmationInput" type="text"
                       class="w-full p-2 border rounded-lg"
                       style="background-color: var(--background-color-1t); color: var(--light-text); border-color: var(--color-primary-dark);"
                       :placeholder="materialName"
                       :disabled="isDeleting" />
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
                        :disabled="isDeleting"
                        :class="{ 'opacity-50 cursor-not-allowed': isDeleting }">
                  Cancel
                </button>
                <button @click="handleDeleteMaterial"
                        class="px-4 py-2 rounded-lg focus:outline-none focus:ring-2 flex items-center justify-center text-white"
                        style="background: var(--error-color);"
                        :disabled="!isConfirmationValid || isDeleting"
                        :class="{ 'opacity-50 cursor-not-allowed': !isConfirmationValid || isDeleting, 'hover:opacity-90 active:opacity-80': isConfirmationValid && !isDeleting }">
                  <span v-if="isDeleting">
                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </span>
                  <span v-else>Delete</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import axios from 'axios';
import { toast } from 'vue-sonner';
import { TrashIcon, XMarkIcon } from '@heroicons/vue/24/outline';
import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";

const props = defineProps({
  materialId: {
    type: Number,
    required: true
  },
  materialName: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['material-deleted', 'delete-error']);

const showModal = ref(false);
const confirmationInput = ref('');
const isDeleting = ref(false);
const apiError = ref('');
const confirmationError = ref('');

const isConfirmationValid = computed(() => confirmationInput.value === props.materialName);

watch(confirmationInput, (newValue) => {
  if (newValue && !isConfirmationValid.value) {
    confirmationError.value = 'The typed name does not match the material name.';
  } else {
    confirmationError.value = '';
  }
});

function openModal() {
  showModal.value = true;
  confirmationInput.value = '';
  apiError.value = '';
  confirmationError.value = '';
}

function closeModal() {
  if (isDeleting.value) {
    toast.warning('Deletion is in progress. Please wait.');
    return;
  }
  showModal.value = false;
  confirmationInput.value = '';
  apiError.value = '';
  confirmationError.value = '';
}

async function handleDeleteMaterial() {
  if (!isConfirmationValid.value || isDeleting.value) return;

  apiError.value = '';
  isDeleting.value = true;
  const toastId = toast.loading(`Deleting material "${props.materialName}"...`);

  try {
    const response = await axios.delete(`/api/materials/${props.materialId}`);
    if (response.status === 200 || response.status === 204 || (response.data && response.data.status === 'success')) {
      toast.success(`Material "${props.materialName}" deleted successfully.`, { id: toastId });
      emit('material-deleted', props.materialId);
      closeModal();
    } else {
      const errorMessage = 'An unexpected error occurred while deleting the material.';
      apiError.value = errorMessage;
      toast.error(errorMessage, { id: toastId });
      emit('delete-error', { materialId: props.materialId, message: errorMessage });
    }
  } catch (error: any) {
    console.error('Error deleting material:', error);
    const errorMessage = 'Failed to delete material. Please try again.';
    apiError.value = errorMessage;
    toast.error(errorMessage, { id: toastId });
    emit('delete-error', { materialId: props.materialId, message: errorMessage });
  } finally {
    isDeleting.value = false;
  }
}
</script>

<style scoped>
.action-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--element-color-1);
  border: 1px solid var(--color-primary-dark);
  color: var(--light-text);
  transition: all 0.2s ease;
  cursor: pointer;
}

.action-button:hover:not(:disabled) {
  background-color: var(--element-color-2);
  transform: scale(1.05);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.delete-button:hover:not(:disabled) {
  background-color: #e74c3c;
  color: white;
}

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
