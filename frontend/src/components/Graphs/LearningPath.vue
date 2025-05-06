<template>
    <div class="fixed left-8 right-8 top-0 bottom-0 overflow-hidden">

        <!-- Double‐left chevron: hide once we’ve scrolled past a bit -->
        <button v-if="scrollPosition > 300" @click="scrollToStart(); $nextTick(() => handleScroll())"
            class="fixed left-8 bottom-1/4 -translate-y-1/4 bg-black/30 backdrop-blur-sm shadow-md rounded-full p-4 hover:bg-black/40 z-10
                         flex items-center gap-2"
            style="color: var(--highlight-color);">
            <ChevronDoubleLeftIcon class="w-12 h-12" />
            <span>To Start</span>
        </button>

        <!-- Double‐right chevron -->
        <button
            v-if="scrollPosition < (maxLeft - 300)"
            @click="scrollToEnd(); $nextTick(() => handleScroll())"
            class="fixed right-8 bottom-1/4 -translate-y-1/4 bg-black/30 backdrop-blur-sm shadow-md rounded-full p-4 hover:bg-black/40 z-10
                         flex items-center gap-2"
            style="color: var(--highlight-color);"
        >
            <span>To End</span>
            <ChevronDoubleRightIcon class="w-12 h-12" />
        </button>

        <!-- Single‐left chevron -->
        <button v-if="scrollPosition > 300" @click="scroll('left'); $nextTick(() => handleScroll())"
            class="fixed left-8 top-1/4 translate-y-1/3 bg-black/30 backdrop-blur-sm shadow-md rounded-full p-4 hover:bg-black/40 z-10"
            style="color: var(--highlight-color);">
            <ChevronLeftIcon class="w-12 h-12" />
        </button>

        <!-- Single‐right chevron -->
        <button v-if="scrollPosition < (maxLeft - 300)" @click="scroll('right'); $nextTick(() => handleScroll())"
            class="fixed right-8 top-1/4 translate-y-1/3 bg-black/30 backdrop-blur-sm shadow-md rounded-full p-4 hover:bg-black/40 z-10"
            style="color: var(--highlight-color);">
            <ChevronRightIcon class="w-12 h-12" />
        </button>


        <!-- Settings Button -->
        <button @click="toggleSettings"
            class="fixed top-20 right-6 bg-black/30 backdrop-blur-sm shadow-md rounded-full p-4 hover:bg-black/40 z-10"
            style="color: var(--highlight-color);">
            <CogIcon class="w-10 h-10" />
        </button>

        <div ref="scrollContainer"
            class="scrollContainer w-full h-full overflow-x-auto overflow-y-hidden cursor-grab active:cursor-grabbing"
            @mousedown="startDragging" @mousemove="drag" @mouseup="stopDragging" @mouseleave="stopDragging"
            @touchstart="startDragging" @touchmove="drag" @touchend="stopDragging" @scroll="handleScroll">
            <div class="flex items-center gap-24 min-h-screen py-24 relative">
                <!-- Left padding so first node is visible -->
                <div class="w-24 flex-shrink-0"></div>
                <!-- Unit Headers -->
                <template v-for="([unit], unitName, unitIndex) in rawUnitData" :key="unit.unit_id">
                    <div class="relative -mx-12 my-12 px-12 pt-40 pb-36 border-t-2 border-b-2 flex-shrink-0" :style="{
                         
                        borderColor: getUnitColor(unitIndex),
                        backgroundColor: 'var(--background-color-1t)',
                        borderLeft: unitIndex === 0 ? `2px solid ${getUnitColor(unitIndex)}` : 'none',
                        borderRight:
                            unitIndex === Object.keys(rawUnitData).length - 1
                                ? `2px solid ${getUnitColor(unitIndex)}`
                                : 'none',
                        borderTopLeftRadius: unitIndex === 0 ? `0.625rem` : 'none',
                        borderBottomLeftRadius: unitIndex === 0 ? `0.625rem` : 'none',
                        borderTopRightRadius:
                            unitIndex === Object.keys(rawUnitData).length - 1 ? `0.625rem` : 'none',
                        borderBottomRightRadius:
                            unitIndex === Object.keys(rawUnitData).length - 1 ? `0.625rem` : 'none'
                    }">
                        <!-- Unit name header -->
                        <div class="absolute -top-5 left-1/2 transform -translate-x-1/2 px-6 py-2 rounded-lg font-bold text-xl whitespace-nowrap shadow-md"
                            :style="{ backgroundColor: getUnitColor(unitIndex), color: 'var(--light-text)' }">
                            {{ formatRoomName(unitName) }}
                        </div>
                        <!-- Sections container -->
                        <div class="flex items-center gap-24">
                            <template v-for="([sectionId, sectionName], sectionIndex) in rawUnitData[unitName]"
                                :key="sectionIndex">
                                <div class="relative flex-shrink-0" :style="{
                                    transform: `translateY(${getNodeOffset(getGlobalSectionIndex(unitIndex, sectionIndex))}px)`
                                }" @click="handleNodeClick(sectionId)">
                                    <!-- THIS IS THE KEY CHANGE: Moved the tooltip outside the group element that controls hovering -->
                                    <!-- Tooltip -->
                                    <div v-if="selectedRoomId && selectedRoomId === sectionId"
                                        class="absolute -top-32 left-1/2 -translate-x-1/2 w-64 z-50" @mouseenter.stop
                                        @mouseover.stop>
                                        <div class="relative" style="pointer-events: auto;">
                                            <!-- Red close button in top-right -->
                                            <div @click.stop="selectedRoomId = null"
                                                class="absolute -top-3 -right-3 w-8 h-8 rounded-full flex items-center justify-center cursor-pointer"
                                                style="background-color: red;">
                                                <XMarkIcon class="w-4 h-4" style="color: var(--light-text);" />
                                            </div>
                                            <!-- Main tooltip content -->
                                            <div class="rounded-2xl p-4 shadow-lg"
                                                style="background-color: var(--element-color-1); color: var(--light-text);">
                                                <div class="font-medium mb-3">{{ formatRoomName(sectionName) }}
                                                    <br>
                                                    <span
                                                        v-if="getRoomData(sectionId) && getRoomData(sectionId).lesson_state <= getRoomData(sectionId).num_lessons">
                                                        lesson {{ getRoomData(sectionId).lesson_state }} / {{
                                                            getRoomData(sectionId).num_lessons }}
                                                    </span>
                                                </div>
                                                <div class="relative">
                                                    <!-- Shadow element (bottom layer) -->
                                                    <div class="absolute inset-0 rounded-xl"
                                                        style="background-color: rgba(0,0,0,0.2); transform: translateY(4px);">
                                                    </div>

                                                    <!-- Button element (top layer) -->
                                                    <button @click.stop="startLesson(sectionName, sectionId)"
                                                        class="relative w-full rounded-xl py-2 px-4 font-medium flex items-center justify-center gap-2 transition-transform duration-200 hover:translate-y-1"
                                                        style="background-color: var(--light-text); color: var(--element-color-1);">
                                                        <span
                                                            v-if="getRoomData(sectionId) && getRoomData(sectionId).lesson_state <= getRoomData(sectionId).num_lessons">
                                                            PLAY
                                                        </span>
                                                        <span v-else>
                                                            REVIEW
                                                        </span>
                                                    </button>
                                                </div>
                                            </div>
                                            <!-- Triangle pointer -->
                                            <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 transform rotate-45"
                                                style="background-color: var(--element-color-1);" />
                                        </div>
                                    </div>

                                    <!-- Icon button with hover group -->
                                    <div class="group perspective-1000">
                                        <!-- Main button container with enhanced 3D transforms -->
                                        <div class="
        relative 
        transform-gpu 
        transition-all 
        duration-300 
        group-hover:scale-110
        group-hover:-translate-y-3
        group-hover:rotate-y-5
        group-active:scale-95
        group-active:translate-y-1
      ">
                                            <!-- Enhanced shadow with depth -->
                                            <div class="
            absolute 
            inset-0 
            rounded-full 
            transform-gpu 
            transition-all 
            duration-300
            opacity-70
            blur-md
            group-hover:blur-lg
            group-hover:scale-110
            group-hover:opacity-80
            group-active:scale-90
            group-active:blur-sm
            group-active:opacity-50
          " :style="{
            backgroundColor: getUnitColor(unitIndex),
            transform: 'translateY(10px) scale(0.85)'
        }">
                                            </div>

                                            <!-- Base and background elements -->
                                            <div class="relative w-48 h-48">
                                                <!-- Bottom layer for 3D effect (shadow/base) -->
                                                <div class="
              absolute 
              inset-0 
              rounded-full 
              transform-gpu 
              translate-y-2
              transition-all
              duration-300
              group-hover:translate-y-4
              group-active:translate-y-1
            " :style="{ backgroundColor: getUnitColor(unitIndex) }">
                                                </div>

                                                <!-- Main button background with subtle gradient -->
                                                <div class="
              absolute 
              inset-0 
              rounded-full 
              flex 
              items-center 
              justify-center 
              cursor-pointer 
              shadow-lg 
              transition-all 
              duration-300
              group-active:shadow-inner
              group-hover:shadow-xl
              overflow-hidden
              " :style="{
                background: getUnitGradient(unitIndex)
            }">

                                                    <!-- Icon with enhanced transitions -->
                                                    <component
                                                        :is="getIconForIndex(getGlobalSectionIndex(unitIndex, sectionIndex))"
                                                        class="
                relative
                w-24 
                h-24 
                duration-300 
                drop-shadow-lg
              " style="color: var(--light-text);" />
                                                </div>

                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>
                </template>
                <!-- Added right padding to ensure last nodes have space -->
                <div class="w-24 flex-shrink-0"></div>
            </div>
        </div>
    </div>
    <!-- Add Node Modal -->
    <Transition name="modal">
        <div v-if="showAddNodeModal" class="fixed inset-0 flex items-center justify-center z-50 p-4"
            style="background-color: var(--background-haze);">
            <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border"
                style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-semibold" style="color: var(--light-text);">Add New Stepping
                        Stones</h2>
                    <button @click="showAddNodeModal = false" style="color: var(--highlight-color);">
                        <XMarkIcon class="w-6 h-6" />
                    </button>
                </div>
                <div class="space-y-4">
                    <!-- Dynamic list of node names -->
                    <div>
                        <label class="block text-sm font-medium mb-1" style="color: var(--highlight-color);">Stepping
                            Stone
                            Names</label>
                        <div v-for="(node, index) in newNodeNames" :key="index" class="flex items-center gap-2 mb-2">
                            <input v-model="newNodeNames[index]" type="text" class="w-full p-2 border rounded-lg"
                                style="background-color: var(--background-color-1t); color: var(--light-text); border-color: var(--color-primary-dark);"
                                placeholder="Enter Stepping Stone name" maxlength="40" />
                            <button v-if="newNodeNames.length > 1" @click="removeNodeName(index)"
                                class="text-red-400 hover:text-red-300">
                                <XCircleIcon class="w-6 h-6" />
                            </button>
                            <p v-if="nodeNameErrors.length" class="mt-1 text-sm"
                                style="color: var(--color-primary-light);">
                                <!-- {{ nodeNameErrors }} -->
                                <span v-for="(error, index) in nodeNameErrors" :key="index">{{ error
                                }}<br></span>
                            </p>
                        </div>
                        <button @click="addNodeNameField" class="mt-2 text-sm font-medium flex items-center gap-1"
                            style="color: var(--highlight-color);">
                            <PlusIcon class="w-4 h-4" />
                            Add Another Node
                        </button>
                        <p v-if="nodeNameErrors.length" class="mt-1 text-sm" style="color: var(--color-primary-light);">
                            <!-- {{ nodeNameErrors }} -->
                            <span v-for="(error, index) in nodeNameErrors" :key="index">{{ error }}<br></span>
                        </p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1" style="color: var(--highlight-color);">Upload
                            Resource
                            (optional)<br>Note: Stepping stone content is based on this resource and all
                            previously
                            uploaded resources in this library </label>
                        <div class="border border-dashed rounded-lg p-4 text-center"
                            style="background-color: var(--background-color-1t); border-color: var(--color-primary-light);">
                            <input type="file" ref="fileInput" @change="handleFileSelection" class="hidden"
                                accept=".pdf,.doc,.docx,.txt" />
                            <div v-if="!selectedFile" @click="$refs.fileInput.click()" class="cursor-pointer">
                                <DocumentPlusIcon class="w-12 h-12 mx-auto"
                                    style="color: var(--color-primary-light);" />
                                <p class="mt-2 text-sm" style="color: var(--highlight-color);">Click to
                                    upload (max
                                    500KB)
                                </p>
                                <p class="mt-1 text-xs" style="color: var(--color-primary-light);">PDF, DOC,
                                    DOCX,
                                    TXT</p>
                            </div>
                            <div v-else class="text-left">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center">
                                        <DocumentIcon class="w-8 h-8 mr-2" style="color: var(--color-primary-light);" />
                                        <div>
                                            <p class="text-sm font-medium truncate"
                                                style="color: var(--highlight-color);">
                                                {{ selectedFile.name }}</p>
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
                    <div class="flex gap-3 justify-end mt-6">
                        <button @click="showAddNodeModal = false" class="px-4 py-2 border rounded-lg"
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
                            {{ !!(isPublic) ? 'Anyone can view this course' : `Only this code can access this course:
                            ${joinCode}` }}
                        </p>
                    </div>
                    <!-- Add more settings fields as needed -->
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
import { ref, watch, onMounted, onUnmounted } from 'vue'
import {
    StarIcon,
    BookOpenIcon,
    TrophyIcon,
    ChatBubbleBottomCenterTextIcon,
    AcademicCapIcon,
    BeakerIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
    PuzzlePieceIcon,
    RocketLaunchIcon,
    SparklesIcon,
    PlusIcon,
    CogIcon,
    XMarkIcon,
    DocumentPlusIcon,
    DocumentIcon,
    XCircleIcon,
    ChevronDoubleLeftIcon,
    ChevronDoubleRightIcon
} from '@heroicons/vue/24/solid'
import { useGameStore } from '@/store/gameStore'
import { useRouter } from 'vue-router';
import axios from 'axios';
const props = defineProps({
    libraryId: {
        type: String,
        required: true
    },
    roomNames: {
        type: Array,
        required: true
    },
    roomData: {
        type: Object,
        required: true
    },
    unitSectionMap: {
        type: Array,
        required: true
    },
    libraryIsPublic: {
        type: Boolean,
        required: true
    },
    libraryJoinCode: {
        type: [String, null],
        required: true
    }
})
const rawUnitData = ref();
const isPublic = ref(false);
const joinCode = ref<string | null>(null);

watch(() => props.unitSectionMap, async (newVal) => {
    rawUnitData.value = newVal;
}, { deep: true, immediate: true })

// Initialize libraryIsPublic from props
watch(() => props.libraryIsPublic, (newVal) => {
    isPublic.value = newVal;
}, { immediate: true });

watch(() => props.libraryJoinCode, (newVal) => {
    joinCode.value = newVal;
}, { immediate: true });

// State for adding new nodes
const showAddNodeModal = ref(false)
const newNodeNames = ref([''])
const selectedFile = ref(null)
const nodeNameErrors = ref([])
const fileError = ref('')
const isAddingNode = ref(false)
const gameStore = useGameStore()
const showSettingsModal = ref(false)
const isUpdatingVisibility = ref(false);
const pendingStatus = ref<boolean | null>(null);
// Track selected room for tooltip
const selectedRoomId = ref(null)
const library_id = props.libraryId;
// File input handling
const fileInput = ref(null)
const scrollPosition = ref(0)
// Color schemes for units
const unitColors = [
    '#2ecc71', // green
    '#f1c40f', // yellow
    '#3498db', // blue
    '#e74c3c', // red
]

const maxLeft = ref(0)

// snap back to the first node (same 200 px offset you use on mount)
const scrollToStart = () => {
    if (!scrollContainer.value) return
    scrollContainer.value.scrollTo({ left: 0, behavior: 'smooth' })
}

// snap back to the first node (same 200 px offset you use on mount)
const scrollToEnd = () => {
    if (!scrollContainer.value) return

    /* how far we can scroll = total content width – visible width */
    scrollContainer.value.scrollTo({ left: maxLeft.value, behavior: 'smooth' })
}

function toggleSettings() {
    showSettingsModal.value = !showSettingsModal.value
}
// Get color for a unit based on its index
const getUnitColor = (unitIndex) => {
    const colorIndex = unitIndex % unitColors.length
    return unitColors[colorIndex];
}
// Get gradient for a unit based on its index
const getUnitGradient = (unitIndex) => {
    const colorIndex = unitIndex % unitColors.length;
    const baseColor = unitColors[colorIndex];

    // Create a more pronounced gradient with highlights
    return `linear-gradient(135deg, 
    ${adjustColor(baseColor, 20)} 0%, 
    ${baseColor} 50%, 
    ${adjustColor(baseColor, -20)} 100%)`;
}

// Helper function to lighten/darken colors
function adjustColor(color, percent) {
    // Convert hex to RGB
    let R = parseInt(color.substring(1, 3), 16);
    let G = parseInt(color.substring(3, 5), 16);
    let B = parseInt(color.substring(5, 7), 16);

    // Adjust brightness
    R = Math.min(255, Math.max(0, R + percent));
    G = Math.min(255, Math.max(0, G + percent));
    B = Math.min(255, Math.max(0, B + percent));

    // Convert back to hex
    const RR = R.toString(16).padStart(2, '0');
    const GG = G.toString(16).padStart(2, '0');
    const BB = B.toString(16).padStart(2, '0');

    return `#${RR}${GG}${BB}`;
}
const setLibraryIsPublicStatus = async (newStatus: boolean) => {
    if (isPublic.value === newStatus) {
        return; // No change needed
    }
    const prev = isPublic.value;
    isPublic.value = newStatus;
    isUpdatingVisibility.value = true;
    // pendingStatus.value = newStatus;
    axios.post(`/api/library/visibility_status/${library_id}`, {
        libraryId: library_id,
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
// Get global section index (for offset and icon selection)
const getGlobalSectionIndex = (unitIndex: number, sectionIndex: number) => {
    let count = 0;
    // Sum the lengths of sections for all units before the current unitIndex
    for (let i = 0; i < unitIndex; i++) {
        const unitKeys = Object.keys(rawUnitData.value);
        const previousUnitName = unitKeys[i];
        if (rawUnitData.value[previousUnitName]) {
            count += rawUnitData.value[previousUnitName].length;
        }
    }
    return count + sectionIndex;
}
const handleFileSelection = (event) => {
    const file = event.target.files[0]
    if (!file) return
    fileError.value = ''
    // Check file size (500KB limit)
    if (file.size > 512000) {
        fileError.value = 'File size exceeds 500KB limit'
        return
    }
    // Check file type
    const allowedTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
    ]
    if (!allowedTypes.includes(file.type)) {
        fileError.value = 'Only PDF, DOC, DOCX, and TXT files are allowed'
        return
    }
    selectedFile.value = file
}
const removeFile = () => {
    selectedFile.value = null
    fileError.value = ''
    if (fileInput.value) {
        fileInput.value.value = ''
    }
}
const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / 1048576).toFixed(1) + ' MB'
}
// Add a new node name field
const addNodeNameField = () => {
    newNodeNames.value.push('')
    nodeNameErrors.value.push('')
}
// Remove a node name field
const removeNodeName = (index) => {
    newNodeNames.value.splice(index, 1)
    nodeNameErrors.value.splice(index, 1)
}
// Function to add a new node
const addNewNodes = async () => {
    // Validate node name
    nodeNameErrors.value = new Array(newNodeNames.value.length).fill('')
    let hasError = false
    const trimmedNames = newNodeNames.value.map(name => name.trim())
    trimmedNames.forEach((name, index) => {
        if (!name) {
            nodeNameErrors.value[index] = 'Please enter a node name'
            hasError = true
        } else if (!/^[a-zA-Z ]+$/.test(name)) {
            nodeNameErrors.value[index] = 'Node name can only contain letters and spaces'
            hasError = true
        } else if (name.length > 40) {
            nodeNameErrors.value[index] = 'Node name must be 40 characters or less'
            hasError = true
        } else if (trimmedNames.indexOf(name) !== index) {
            nodeNameErrors.value[index] = 'Duplicate node name in this form'
            hasError = true
        }
    })
    if (hasError) return
    isAddingNode.value = true
    const currentAbortController = new AbortController();
    try {
        // Add each node
        const formData = new FormData()
        formData.append('libraryId', library_id)
        // Append all room names with the same key name
        trimmedNames.forEach(room => formData.append("roomNames", room));
        // Add file if present (same file for all nodes)
        if (selectedFile.value) {
            console.debug(selectedFile.value)
            formData.append('file', selectedFile.value)
        }
        const response = await axios.post('/api/library/room', formData, {
            signal: currentAbortController.signal,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        if (currentAbortController.signal.aborted) return; // Don't proceed if aborted
        if (response.data && response.data.status === "success") {
            // Clear form and refresh to show new nodes
            newNodeNames.value = [''] // Reset to one empty field
            removeFile()
            showAddNodeModal.value = false
            window.location.reload();
        }
    } catch (error) {
        console.error('Error adding nodes:', error)
        nodeNameErrors.value[0] = error.message || 'Failed to add nodes. Please try again.'
    } finally {
        isAddingNode.value = false
    }
}
// Function to get the corresponding room data by section ID
const getRoomData = (sectionId: Number) => {
    for (let i = 0; i < props.roomData.length; i++) {
        if (props.roomData[i].section_id === sectionId) {
            return props.roomData[i];
        }
    }
    // Return null if not found
    return null;
}
// Array of icons to cycle through
const icons = [
    StarIcon,
    ChatBubbleBottomCenterTextIcon,
    BookOpenIcon,
    PuzzlePieceIcon,
    TrophyIcon,
    AcademicCapIcon,
    BeakerIcon,
    SparklesIcon,
    RocketLaunchIcon
]
// Get icon based on index
const getIconForIndex = (index) => {
    return icons[index % icons.length]
}
// Format room name for display
const formatRoomName = (name) => {
    if (!name) return '';
    return name
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
}
const scrollContainer = ref(null)
const isDragging = ref(false)
const startX = ref(0)
const scrollLeft = ref(0)
let scrollTimeoutId = null;
// Scroll to center on first load
onMounted(() => {
    joinCode.value = props.libraryJoinCode;
    // If there are nodes and the container exists, scroll to position
    if (rawUnitData.value.length > 0 && scrollContainer.value) {
        // Calculate an appropriate starting position based on available width
        scrollTimeoutId = setTimeout(() => {
            // This gives time for the layout to render before scrolling
            if (scrollContainer.value) {
                const startPosition = Math.max(0, 200); // A small offset to show the first node
                scrollContainer.value.scrollLeft = startPosition;
            }
            scrollTimeoutId = null; // Clear the timeout ID
        }, 100);
    }
    const sc = scrollContainer.value
    if (!sc) return
    maxLeft.value = sc.scrollWidth - sc.clientWidth
});
onUnmounted(() => {
    if (scrollTimeoutId) {
        clearTimeout(scrollTimeoutId); // Clear the timeout if it hasn't run yet
        console.debug("LearningPath unmounting, cleared initial scroll timeout.");
    }
});
// Add these variables
const startY = ref(0)
const hasMoved = ref(false)
const tapThreshold = 10 // pixels to consider as a tap vs drag
const router = useRouter();
const startDragging = (e) => {
    isDragging.value = true
    hasMoved.value = false
    if (e.type.includes('touch')) {
        startX.value = e.touches[0].pageX - scrollContainer.value.offsetLeft
        startY.value = e.touches[0].pageY
    } else {
        startX.value = e.pageX - scrollContainer.value.offsetLeft
        e.preventDefault() // Only prevent default for mouse events
    }
    scrollLeft.value = scrollContainer.value.scrollLeft
}
const drag = (e) => {
    if (!isDragging.value) return
    let x, y
    if (e.type.includes('touch')) {
        x = e.touches[0].pageX - scrollContainer.value.offsetLeft
        y = e.touches[0].pageY
    } else {
        x = e.pageX - scrollContainer.value.offsetLeft
        e.preventDefault()
    }
    // Calculate distance moved
    const diffX = Math.abs(x - startX.value)
    const diffY = Math.abs(y - startY.value)
    // Only consider it a drag if moved more than threshold
    if (diffX > tapThreshold || diffY > tapThreshold) {
        hasMoved.value = true
        const walk = (x - startX.value) * 2
        scrollContainer.value.scrollLeft = scrollLeft.value - walk
    }
}
const stopDragging = () => {
    isDragging.value = false
}
const handleNodeClick = (sectionId) => {
    if (!hasMoved.value) {
        selectedRoomId.value = selectedRoomId.value && selectedRoomId.value === sectionId ? null : sectionId
    }
}
const getNodeOffset = (index) => {
    const amplitude = 75;
    // Add a slight phase shift for more natural movement
    return Math.sin(index * 0.6) * amplitude;
}
const startLesson = (sectionName, sectionId) => {
    gameStore.setSectionId(sectionId);
    router.push({
        name: 'GamePage',
        params: { id: library_id, roomName: encodeURIComponent(sectionName) },
    })
}
const scroll = (direction) => {
    if (!scrollContainer.value) return
    const scrollAmount = 600
    const currentScroll = scrollContainer.value.scrollLeft
    scrollContainer.value.scrollTo({
        left: direction === 'left' ? currentScroll - scrollAmount : currentScroll + scrollAmount,
        behavior: 'smooth'
    })
}
const handleScroll = () => {
    // guard against nulls during mount/unmount
    const sc = scrollContainer.value
    if (!sc) return

    // copy the browser‑reported scrollLeft into the ref
    scrollPosition.value = sc.scrollLeft
}

</script>
<style scoped>
.overflow-x-auto {
    -webkit-overflow-scrolling: touch;
    scroll-behavior: smooth;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
}

.overflow-x-auto::-webkit-scrollbar {
    display: none;
}

.overflow-x-auto {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.perspective {
    perspective: 1000px;
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

.perspective-1000 {
    perspective: 1000px;
}

.rotate-y-5 {
    transform: rotateY(5deg);
}

@keyframes pulse {

    0%,
    100% {
        opacity: 0.4;
        transform: scale(0.98);
    }

    50% {
        opacity: 0.8;
        transform: scale(1.02);
    }
}

.animate-pulse-slow {
    animation: pulse 3s ease-in-out infinite;
}

@media (max-width: 600px) {
    .scrollContainer {
        position: static !important;
        /* let it flow in the document */
        transform: none !important;
        /* cancel any translateY() you had */
        margin: 0.5rem auto 0;
        /* just a little space under the title */
        width: 100%;
        /* full width so it’s centered */
        display: flex;
        /* keep your flex layout */
        justify-content: center;
        /* center the items horizontally */
    }
}
</style>