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
                <div class="rounded-2xl p-6 w-full max-w-2xl shadow-xl border pointer-events-auto"
                    style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-semibold">Add New Stepping Stones</h2>
                        <button @click="closeModal" style="color: var(--highlight-color);"
                                :disabled="isAddingNode"
                                :class="{ 'opacity-50 cursor-not-allowed': isAddingNode }">
                            <XMarkIcon class="w-6 h-6" />
                        </button>
                    </div>
                    <div class="space-y-6">
                        <!-- Dynamic list of node names -->
                        <div>
                            <label class="block text-sm font-medium mb-2">
                                Stepping Stone Names
                            </label>
                            <div v-for="(node, index) in newNodeNames" :key="index"
                                class="flex items-center gap-2 mb-2">
                                <input v-model="newNodeNames[index]" type="text" class="w-full p-3 border rounded-lg font-medium transition-all duration-200 focus:ring-2 focus:ring-opacity-50"
                                    style="background-color: var(--background-color-1t); color: var(--light-text); border-color: var(--color-primary-dark); focus:border-color: var(--highlight-color);"
                                    placeholder="Enter Stepping Stone name" maxlength="25" />
                                <button v-if="newNodeNames.length > 1" @click="removeNodeName(index)"
                                    class="text-red-400 hover:text-red-300 transition-colors">
                                    <XCircleIcon class="w-6 h-6" />
                                </button>
                            </div>
                            <button v-if="emptyUnit" @click="addNodeNameField"
                                class="mt-2 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 flex items-center gap-1 transition-all duration-200 hover:shadow-md"
                                style="background: var(--button-gradient); color: var(--light-text);">
                                <PlusIcon class="w-4 h-4" />
                                Add Another Node
                            </button>
                            <p v-if="nodeNameErrors.length" class="mt-1 text-sm" style="color: var(--error-color);">
                                <span v-for="(error, index) in nodeNameErrors" :key="index">{{ error }}<br v-if="index < nodeNameErrors.length - 1"></span>
                            </p>
                        </div>

                        <!-- Upload Resource Section -->
                        <div>
                            <label class="block text-sm font-medium mb-2" style="color: var(--highlight-color);">
                                Upload Resource (optional)<br>
                                <span class="opacity-65 text-xs">Note: Stepping stone content is based on this resource and all
                                    previously uploaded resources in this library</span>
                            </label>
                            <div class="border border-dashed rounded-lg p-4 text-center transition-all duration-200 hover:border-opacity-80"
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
                        
                        <!-- Modern Materials Selection Section -->
                        <div>
                            <label class="block text-sm font-medium mb-2" style="color: var(--highlight-color);">
                                Select Existing Materials (optional)
                            </label>
                            <div v-if="materials.length" class="border rounded-xl overflow-hidden shadow-sm"
                                style="background-color: var(--background-color-1t); border-color: var(--color-primary-light);">
                                
                                <!-- Search Header -->
                                <div class="p-4 border-b" style="border-color: var(--color-primary-light); background-color: var(--background-color);">
                                    <div class="relative">
                                        <Input 
                                            v-model="materialSearch" 
                                            placeholder="Search materials..." 
                                            class="pl-10 pr-4 py-2 w-full rounded-lg border transition-all duration-200 focus:ring-2 focus:ring-opacity-50" 
                                            style="background-color: var(--background-color-1t); color: var(--light-text); border-color: var(--color-primary-dark);"
                                        />
                                        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4" style="color: var(--color-primary-light);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                                        </svg>
                                    </div>
                                    <div v-if="selectedMaterialIds.length > 0" class="mt-2 flex items-center gap-2 text-sm" style="color: var(--highlight-color);">
                                        <span>{{ selectedMaterialIds.length }} material{{ selectedMaterialIds.length !== 1 ? 's' : '' }} selected</span>
                                        <button @click="selectedMaterialIds = []" class="text-xs px-2 py-1 rounded-md transition-colors hover:opacity-80" style="background-color: var(--color-primary-dark); color: var(--light-text);">
                                            Clear all
                                        </button>
                                    </div>
                                </div>
                                
                                <!-- Materials List -->
                                <div v-if="filteredMaterials.length" class="max-h-64 overflow-y-auto">
                                    <div class="divide-y" style="divide-color: var(--color-primary-light);">
                                        <div 
                                            v-for="mat in filteredMaterials" 
                                            :key="mat.id" 
                                            @click="toggleMaterial(mat.id)"
                                            class="flex items-center p-4 cursor-pointer transition-all duration-200 hover:shadow-sm"
                                            :class="{ 'selected-material': selectedMaterialIds.includes(mat.id) }"
                                            :style="selectedMaterialIds.includes(mat.id) 
                                                ? { 'background-color': 'var(--color-primary-dark)', 'background-opacity': '0.3' } 
                                                : { 'background-color': 'transparent' }"
                                        >
                                            <!-- Custom Checkbox -->
                                            <div class="flex-shrink-0 mr-4">
                                                <div class="relative">
                                                    <input 
                                                        type="checkbox" 
                                                        :value="mat.id" 
                                                        v-model="selectedMaterialIds" 
                                                        @click.stop 
                                                        class="sr-only"
                                                    />
                                                    <div 
                                                        class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all duration-200"
                                                        :style="selectedMaterialIds.includes(mat.id) 
                                                            ? { 'background-color': 'var(--highlight-color)', 'border-color': 'var(--highlight-color)' }
                                                            : { 'background-color': 'transparent', 'border-color': 'var(--color-primary-light)' }"
                                                    >
                                                        <svg v-if="selectedMaterialIds.includes(mat.id)" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                                                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <!-- File Icon -->
                                            <div class="flex-shrink-0 mr-3">
                                                <DocumentIcon class="w-8 h-8" style="color: var(--color-primary-light);" />
                                            </div>
                                            
                                            <!-- Material Info -->
                                            <div class="flex-grow min-w-0">
                                                <div class="flex items-center gap-2">
                                                    <p class="text-sm font-medium truncate" style="color: var(--highlight-color);">
                                                        {{ mat.name }}
                                                    </p>
                                                    <span v-if="mat.added_to_course_path" class="text-xs text-red-400 flex-shrink-0">(already added)</span>
                                                </div>
                                                <p class="text-xs mt-1" style="color: var(--color-primary-light);">
                                                    {{ formatFileSize(mat.size) }}
                                                </p>
                                            </div>
                                            
                                            <!-- Selection Indicator -->
                                            <div v-if="selectedMaterialIds.includes(mat.id)" class="flex-shrink-0 ml-2">
                                                <div class="w-2 h-2 rounded-full" style="background-color: var(--highlight-color);"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- No Results -->
                                <div v-else class="p-8 text-center">
                                    <svg class="w-12 h-12 mx-auto mb-2" style="color: var(--color-primary-light);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                    </svg>
                                    <p class="text-sm" style="color: var(--color-primary-light);">No materials match your search</p>
                                </div>
                            </div>
                            
                            <!-- No Materials Available -->
                            <div v-else class="border border-dashed rounded-xl p-8 text-center" style="border-color: var(--color-primary-light);">
                                <svg class="w-12 h-12 mx-auto mb-2" style="color: var(--color-primary-light);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                                <p class="text-sm" style="color: var(--color-primary-light);">No materials available in this library</p>
                            </div>
                        </div>

                        <!-- API call error message -->
                        <p v-if="apiError" class="mt-2 text-sm" style="color: var(--error-color);">
                            {{ apiError }}
                        </p>

                        <div class="flex justify-end gap-3 mt-8">
                            <button @click="closeModal" class="px-6 py-2 border rounded-lg transition-all duration-200 hover:shadow-md"
                                style="border-color: var(--color-primary); color: var(--highlight-color);"
                                :disabled="isAddingNode"
                                :class="{ 'opacity-50 cursor-not-allowed': isAddingNode }">
                                Cancel
                            </button>
                            <button @click="addNewNodes" class="px-6 py-2 rounded-lg focus:outline-none focus:ring-2 flex items-center justify-center gap-2 transition-all duration-200 hover:shadow-md"
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
import { ref, onMounted, watch, computed } from 'vue';
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
import { Input } from '@/components/ui/input';

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
const materialSearch = ref('');
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

const filteredMaterials = computed(() =>
    materials.value.filter((m: any) =>
        m.name.toLowerCase().includes(materialSearch.value.toLowerCase())
    )
);

const onMaterialCheckboxChange = (mat: any) => {
    const index = selectedMaterialIds.value.indexOf(mat.id);
    const isSelected = index !== -1;
    if (isSelected) {
        selectedMaterialIds.value.splice(index, 1);
        return;
    }
    if (mat.added_to_course_path) {
        const confirmAdd = window.confirm('This material is already added to the course. Are you sure you want to add it again?');
        if (!confirmAdd) {
            return;
        }
    }
    selectedMaterialIds.value.push(mat.id);
};

const toggleMaterial = (materialId: number) => {
    const mat = materials.value.find((m: any) => m.id === materialId);
    if (mat) {
        onMaterialCheckboxChange(mat);
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

<style scoped>
.selected-material {
    background-color: var(--color-primary-dark);
    background-opacity: 0.2;
}
</style>