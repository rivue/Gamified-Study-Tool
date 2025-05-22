<template>
    <div class="relative flex-shrink-0">
        <div v-if="emptyUnit" class="flex items-center gap-2 px-4 py-2 rounded-lg transition-all 
                                            duration-200 hover:scale-105 active:scale-95 cursor-pointer" @click="showModal = true"
            :style="{
                background: unitColor,
                color: 'var(--light-text)'
            }">
            <PlusIcon class="w-5 h-5" />
            <span>Add Stepping Stone</span>
        </div>

        <div v-else
            class="w-16 h-16 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 hover:scale-110 hover:shadow-lg active:scale-95"
            :style="{ backgroundColor: unitColor, transform: `translateY(${offset}px)` }" @click="showModal = true">
            <PlusIcon class="w-8 h-8" style="color: var(--light-text)" />
        </div>

        <!-- the modal itself -->
        <teleport to="body">

        <Transition name="modal">
            <div v-if="showModal" class="fixed inset-0 flex items-center justify-center z-50 p-4"
                style="background-color: var(--background-haze); pointer-events: auto;">
                <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border pointer-events-auto"
                    style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-semibold">Add New Stepping Stones</h2>
                        <button @click="closeModal" style="color: var(--highlight-color);">
                            <XMarkIcon class="w-6 h-6" />
                        </button>
                    </div>
                    <div class="space-y-4">
                        <!-- Dynamic list of node names -->
                        <div>
                            <label class="block text-sm font-medium mb-1">
                                Stepping Stone Names
                            </label>
                            <div v-for="(node, index) in newNodeNames" :key="index"
                                class="flex items-center gap-2 mb-2">
                                <input v-model="newNodeNames[index]" type="text" class="w-full p-2 border rounded-lg"
                                    style="background-color: var(--background-color-1t); color: var(--light-text); border-color: var(--color-primary-dark);"
                                    placeholder="Enter Stepping Stone name" maxlength="25" />
                                <button v-if="newNodeNames.length > 1" @click="removeNodeName(index)"
                                    class="text-red-400 hover:text-red-300">
                                    <XCircleIcon class="w-6 h-6" />
                                </button>
                            </div>
                            <button v-if="emptyUnit" @click="addNodeNameField"
                                class="mt-2 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 flex items-center gap-1"
                                style="background: var(--button-gradient); color: var(--light-text);">
                                <PlusIcon class="w-4 h-4" />
                                Add Another Node
                            </button>
                            <p v-if="nodeNameErrors.length" class="mt-1 text-sm" style="color: var(--error-color);">
                                <span v-for="(error, index) in nodeNameErrors" :key="index">{{ error }}<br v-if="index < nodeNameErrors.length - 1"></span>
                            </p>
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-1" style="color: var(--highlight-color);">
                                Upload Resource (optional)<br>
                                <span class="opacity-65">Note: Stepping stone content is based on this resource and all
                                    previously uploaded resources in this library</span>
                            </label>
                            <div class="border border-dashed rounded-lg p-4 text-center"
                                style="background-color: var(--background-color-1t); border-color: var(--color-primary-light);">
                                <input type="file" ref="fileInput" @change="handleFileSelection" class="hidden"
                                    accept=".pdf,.doc,.docx,.txt" />
                                <div v-if="!selectedFile" @click="$refs.fileInput.click()" class="cursor-pointer">
                                    <DocumentPlusIcon class="w-12 h-12 mx-auto"
                                        style="color: var(--color-primary-light);" />
                                    <p class="mt-2 text-sm" style="color: var(--highlight-color);">Click to upload (max
                                        500KB)</p>
                                    <p class="mt-1 text-xs" style="color: var(--color-primary-light);">PDF, DOC, DOCX,
                                        TXT</p>
                                </div>
                                <div v-else class="text-left">
                                    <div class="flex items-center justify-between">
                                        <div class="flex items-center">
                                            <DocumentIcon class="w-8 h-8 mr-2"
                                                style="color: var(--color-primary-light);" />
                                            <div>
                                                <p class="text-sm font-medium truncate"
                                                    style="color: var(--highlight-color);">
                                                    {{ selectedFile.name }}
                                                </p>
                                                <p class="text-xs" style="color: var(--color-primary-light);">{{
                                                    formatFileSize(selectedFile.size) }}</p>
                                            </div>
                                        </div>
                                        <button @click.prevent="removeFile" class="text-red-400 hover:text-red-300">
                                            <XCircleIcon class="w-6 h-6" />
                                        </button>
                                    </div>
                                </div>
                                <p v-if="fileError" class="mt-2 text-sm text-red-400">{{ fileError }}</p>
                            </div>
                        </div>

                        <!-- API call error message -->
                        <p v-if="apiError" class="mt-2 text-sm" style="color: var(--error-color);">
                            {{ apiError }}
                        </p>

                        <div class="flex justify-end gap-3 mt-6">
                            <button @click="closeModal" class="px-4 py-2 border rounded-lg"
                                style="border-color: var(--color-primary); color: var(--highlight-color);">
                                Cancel
                            </button>
                            <button @click="addNewNodes" class="px-4 py-2 rounded-lg focus:outline-none focus:ring-2"
                                style="background: var(--button-gradient); color: var(--light-text);"
                                :disabled="isAddingNode">
                                <span v-if="isAddingNode">Adding...</span>
                                <span v-else>Add Stepping Stone</span>
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
import { ref } from 'vue';
import {
    XMarkIcon,
    DocumentPlusIcon,
    DocumentIcon,
    XCircleIcon,
    PlusIcon,
} from '@heroicons/vue/24/solid';
import axios from 'axios';

const props = defineProps({
    libraryId: {
        type: Number,
        required: true
    },
    unitId: {
        type: [Number, String],
        required: true
    },
    position: {
        type: Number,
        required: true,
        default: -1
    },
    unitColor: {
        type: String,
        required: true
    },
    emptyUnit: {
        type: Boolean,
        default: false
    },
    offset: {
        type: Number,
    }
});

const emit = defineEmits(['nodes-added']);

const showModal = ref(false);
// State for adding new nodes
const newNodeNames = ref(['']);
const selectedFile = ref(null);
const nodeNameErrors = ref([]);
const fileError = ref('');
const apiError = ref('');
const isAddingNode = ref(false);
const fileInput = ref(null);

function closeModal() {
    showModal.value = false;
    resetForm();
}

const handleFileSelection = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    fileError.value = '';
    // Check file size (500KB limit)
    if (file.size > 512000) {
        fileError.value = 'File size exceeds 500KB limit';
        return;
    }
    // Check file type
    const allowedTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
    ];
    if (!allowedTypes.includes(file.type)) {
        fileError.value = 'Only PDF, DOC, DOCX, and TXT files are allowed';
        return;
    }
    selectedFile.value = file;
}

const removeFile = () => {
    selectedFile.value = null;
    fileError.value = '';
    if (fileInput.value) {
        fileInput.value.value = '';
    }
}

const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}

// Add a new node name field
const addNodeNameField = () => {
    newNodeNames.value.push('');
    nodeNameErrors.value.push('');
}

// Remove a node name field
const removeNodeName = (index) => {
    newNodeNames.value.splice(index, 1);
    nodeNameErrors.value.splice(index, 1);
}

// Function to add a new node
const addNewNodes = async () => {
    // Reset the API error each attempt
    apiError.value = '';
    // Validate node name
    nodeNameErrors.value = new Array(newNodeNames.value.length).fill('');
    let hasError = false;
    const trimmedNames = newNodeNames.value.map(name => name.trim());
    trimmedNames.forEach((name, index) => {
        if (!name) {
            nodeNameErrors.value[index] = 'Please enter a node name';
            hasError = true;
        } else if (name.length > 25 || name.length < 4) {
            nodeNameErrors.value[index] = 'Section name must be between 4 and 25 characters';
            hasError = true;
        } else if (trimmedNames.indexOf(name) !== index) {
            nodeNameErrors.value[index] = 'Duplicate section names are not allowed';
            hasError = true;
        }
    });
    
    if (hasError) return;
    isAddingNode.value = true;
    const currentAbortController = new AbortController();
    isAddingNode.value = false;

    try {

        // Add each node
        const formData = new FormData();
        formData.append('libraryId', props.libraryId);
        formData.append('unitId', props.unitId);
        formData.append('position', props.position);
        console.log("position: ", props.position);
        // Append all node names with the same key name
        trimmedNames.forEach(name => formData.append("sectionNames", name));
        // Add file if present (same file for all nodes)
        if (selectedFile.value) {
            formData.append('file', selectedFile.value);
        }
        const response = await axios.post('/api/library/section', formData, {
            signal: currentAbortController.signal,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        if (currentAbortController.signal.aborted) return; // Don't proceed if aborted
        if (response.data && response.data.status === "success") {
            // Clear form and emit success event
            resetForm();
            closeModal();
            emit('nodes-added');
        }
    } catch (error) {
        console.error('Error adding nodes:', error);
        // Set a distinct error message for API call failure
        apiError.value = error.response?.data?.message || error.message || 'Failed to add nodes. Please try again.';

    } finally {
        isAddingNode.value = false;
    }

}

const resetForm = () => {
    newNodeNames.value = [''];
    removeFile();
    nodeNameErrors.value = [];
    apiError.value = '';
}
</script>