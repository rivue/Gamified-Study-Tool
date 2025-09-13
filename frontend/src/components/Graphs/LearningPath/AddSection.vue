<template>
    <div
        class="relative flex-shrink-0"
        :style="!emptyUnit
            ? {
                ...(typeof offset === 'number' ? { transform: `translateY(${offset}px)` } : {}),
                height: '0px',
                overflow: 'visible'
              }
            : {}">
        <Tooltip>
            <TooltipTrigger>
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
                    :style="{ backgroundColor: unitColor }" @click="showModal = true">
                    <PlusIcon class="w-8 h-8" style="color: var(--light-text)" />
                </div>
            </TooltipTrigger>
            <TooltipContent variant="shad" side="top" :offset="3">
                {{ emptyUnit ? 'Add the first stepping stone' : 'Add a new stepping stone' }}
            </TooltipContent>
        </Tooltip>

        <!-- the modal itself -->
        <teleport to="body">

        <Transition name="modal">
            <div v-if="showModal" class="fixed inset-0 flex items-center justify-center z-50 p-4"
                style="background-color: var(--background-haze); pointer-events: auto;">
                <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border pointer-events-auto"
                    style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-semibold">Add New Stepping Stones</h2>
                        <!-- <button @click="closeModal" style="color: var(--highlight-color);"> -->
                                  <button @click="closeModal" style="color: var(--highlight-color);"
                                :disabled="isAddingNode"
                                :class="{ 'opacity-50 cursor-not-allowed': isAddingNode }">
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
                                <input v-model="newNodeNames[index]" type="text" class="w-full p-2 border rounded-lg font-medium"
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
                        <div>
                            <label class="block text-sm font-medium mb-1" style="color: var(--highlight-color);">
                                Select Existing Materials (optional)
                            </label>
                            <div v-if="materials.length" class="border rounded-lg p-2 max-h-40 overflow-y-auto"
                                style="background-color: var(--background-color-1t); border-color: var(--color-primary-light);">
                                <div v-for="mat in materials" :key="mat.id" class="flex items-center gap-2 mb-1">
                                    <input type="checkbox" :value="mat.id" v-model="selectedMaterialIds" :id="`mat-${mat.id}`" />
                                    <label :for="`mat-${mat.id}`" class="flex-1 text-sm" style="color: var(--highlight-color);">
                                        {{ mat.name }} ({{ formatFileSize(mat.size) }})
                                    </label>
                                </div>
                            </div>
                            <p v-else class="text-sm opacity-70">No materials available.</p>
                        </div>

                        <!-- API call error message -->
                        <p v-if="apiError" class="mt-2 text-sm" style="color: var(--error-color);">
                            {{ apiError }}
                        </p>

                        <!-- <div class="flex justify-end gap-3 mt-6">
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
                        </div> -->
                        <div class="flex justify-end gap-3 mt-6">
                            <button @click="closeModal" class="px-4 py-2 border rounded-lg"
                                style="border-color: var (--color-primary); color: var(--highlight-color);"
                                :disabled="isAddingNode"
                                :class="{ 'opacity-50 cursor-not-allowed': isAddingNode }">
                                Cancel
                            </button>
                            <button @click="addNewNodes" class="px-4 py-2 rounded-lg focus:outline-none focus:ring-2 flex items-center justify-center"
                                style="background: var(--button-gradient); color: var(--light-text);"
                                :disabled="isAddingNode">
                                <span v-if="isAddingNode">
                                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                </span>
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
import { ref, onMounted, watch } from 'vue';
import {
    XMarkIcon,
    DocumentPlusIcon,
    DocumentIcon,
    XCircleIcon,
    PlusIcon,
} from '@heroicons/vue/24/solid'
import { toast } from 'vue-sonner';
import axios from 'axios';
import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";

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
    },
    // If true, opens the modal automatically when mounted
    autoOpen: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['nodes-added']);

const showModal = ref(false);
// State for adding new nodes
const newNodeNames = ref(['']);
const selectedFile = ref(null);
const materials = ref<any[]>([]);
const selectedMaterialIds = ref<number[]>([]);
const nodeNameErrors = ref([]);
const fileError = ref('');
const apiError = ref('');
const isAddingNode = ref(false);
const fileInput = ref(null);

onMounted(() => {
    if (props.autoOpen) {
        showModal.value = true;
    }
});

const fetchMaterials = async () => {
    try {
        const response = await axios.get(`/api/materials/course/${props.libraryId}`);
        materials.value = response.data.filter((m: any) => m.size <= 5 * 1024 * 1024);
    } catch (error) {
        console.error('Failed to fetch materials:', error);
    }
};

watch(showModal, (val) => {
    if (val) {
        fetchMaterials();
    }
});

function closeModal() {
    if (isAddingNode.value) {
        toast.error('Please wait for the section to be added.');
        return;
    }
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
    if (isAddingNode.value) {
        return;
    }
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
    const toastId = toast.loading('Creating Stepping Stone...');
    isAddingNode.value = true;
    const currentAbortController = new AbortController();

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
        // Include selected existing materials
        selectedMaterialIds.value.forEach(id => formData.append('materialIds', id.toString()));
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
         } else {
            // Handle cases where response.data or response.data.status is not as expected
            // but it's not a network error caught by the catch block.
            const errorMessage = response.data?.message || 'An unexpected error occurred when creating section.';
            apiError.value = errorMessage;
            toast.error(errorMessage, { id: toastId });
         }
    } catch (error) {
        console.error('Error adding nodes:', error);
        // Set a distinct error message for API call failure
        const errorMessage = error.response?.data?.message || error.message || 'Failed to add section. Please try again.';
        apiError.value = errorMessage;
        toast.error(errorMessage, { id: toastId });
    } finally {
        isAddingNode.value = false;
    }

}

const resetForm = () => {
    newNodeNames.value = [''];
    removeFile();
    selectedMaterialIds.value = [];
    nodeNameErrors.value = [];
    apiError.value = '';
}
</script>
