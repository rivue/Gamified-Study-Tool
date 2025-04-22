<template>
    <div class="fixed left-8 right-8 top-0 bottom-0 overflow-hidden">
        <button @click="scroll('left')"
            class="fixed left-8 top-1/2 -translate-y-1/2 bg-black/30 backdrop-blur-sm shadow-lg rounded-full p-4 hover:bg-black/40 z-10"
            style="color: var(--highlight-color);">
            <ChevronLeftIcon class="w-12 h-12" />
        </button>

        <button @click="scroll('right')"
            class="fixed right-8 top-1/2 -translate-y-1/2 bg-black/30 backdrop-blur-sm shadow-lg rounded-full p-4 hover:bg-black/40 z-10"
            style="color: var(--highlight-color);">
            <ChevronRightIcon class="w-12 h-12" />
        </button>

        <!-- Fixed Add Stepping Stone Button - Center Top -->
        <div class="fixed top-48 left-1/2 -translate-x-1/2 z-10">
            <button @click="showAddNodeModal = true"
                class="shadow-lg rounded-full p-4 flex items-center justify-center transition-colors"
                style="background-color: var(--element-color-1); color: var(--light-text);">
                <PlusIcon class="w-6 h-6" />
                <span class="ml-2 font-medium">Add New Stepping Stones</span>
            </button>
        </div>

        <div ref="scrollContainer"
            class="w-full h-full overflow-x-auto overflow-y-hidden cursor-grab active:cursor-grabbing"
            @mousedown="startDragging" @mousemove="drag" @mouseup="stopDragging" @mouseleave="stopDragging"
            @touchstart="startDragging" @touchmove="drag" @touchend="stopDragging" @scroll="handleScroll">
            <!-- Modified to ensure first node is visible -->
            <div class="flex items-center gap-24 min-h-screen py-24 relative">
                <!-- Added left padding to ensure first nodes are visible -->
                <div class="w-24 flex-shrink-0"></div>

                <template v-for="(roomName, index) in nodes" :key="index">
                    <div class="relative flex-shrink-0 group perspective" :style="{
                        transform: `translateY(${getNodeOffset(index)}px)`
                    }" @click="handleNodeClick(roomName)">
                        <!-- Tooltip -->
                        <div v-if="selectedRoom === roomName"
                            class="absolute -top-32 left-1/2 -translate-x-1/2 w-64 z-50">
                            <div class="relative">
                                <!-- Red close button in top-right -->
                                <div @click.stop="selectedRoom = null"
                                    class="absolute -top-3 -right-3 w-8 h-8 rounded-full flex items-center justify-center cursro-pointer"
                                    style="background-color: red;">
                                    <XMarkIcon class="w-4 h-4" style="color: var(--light-text);" />
                                </div>

                                <!-- Main tooltip content -->
                                <div class="rounded-2xl p-4 shadow-lg"
                                    style="background-color: var(--element-color-1); color: var(--light-text);">
                                    <div class="font-medium mb-3">{{ formatRoomName(roomName[0]) }} <br>
                                        <span
                                            v-if="getRoomData(roomName[1]) && getRoomData(roomName[1]).lesson_state <= getRoomData(roomName[1]).num_lessons">
                                            lesson {{ getRoomData(roomName[1]).lesson_state }} / {{ getRoomData(roomName[1]).num_lessons }}
                                        </span>
                                    </div>
                                    <button @click.stop="startLesson(roomName[0])"
                                        class="w-full rounded-xl py-2 px-4 font-medium flex items-center justify-center gap-2 transition-colors"
                                        style="background-color: var(--light-text); color: var(--element-color-1);">
                                        <span
                                            v-if="getRoomData(roomName[1]) && getRoomData(roomName[1]).lesson_state <= getRoomData(roomName[1]).num_lessons">PLAY</span>
                                        <span v-else>REVIEW</span>
                                    </button>
                                </div>

                                <!-- Triangle pointer -->
                                <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 transform rotate-45"
                                    style="background-color: var(--element-color-1);" />
                            </div>
                        </div>

                        <div
                            class="relative transform-gpu transition-all duration-300 group-hover:scale-105 group-hover:-translate-y-2">
                            <div class="absolute -bottom-4 left-1/2 -translate-x-1/2 w-40 h-8 rounded-full blur-xl transform-gpu transition-all duration-300 group-hover:w-44"
                                style="background-color: var(--background-color-1t);"></div>

                            <div class="relative w-48 h-48">
                                <div class="absolute inset-0 rounded-full transform-gpu translate-y-2 blur-sm opacity-50"
                                    style="background-color: var(--color-primary-darker);"></div>

                                <div class="absolute inset-0 rounded-full transform-gpu translate-y-1"
                                    style="background-color: var(--color-primary-dark);"></div>

                                <div class="absolute inset-0 rounded-full flex items-center justify-center cursor-pointer shadow-lg transform-gpu transition-all duration-300"
                                    style="background: var(--button-gradient);">
                                    <component :is="getIconForIndex(index)"
                                        class="w-24 h-24 transform-gpu transition-all duration-300 group-hover:scale-110"
                                        style="color: var(--light-text);" />
                                </div>
                            </div>
                        </div>
                    </div>
                </template>

                <!-- Added right padding to ensure last nodes have space -->
                <div class="w-24 flex-shrink-0"></div>
            </div>
        </div>

        <!-- Add Node Modal -->
        <Transition name="modal">
            <div v-if="showAddNodeModal" class="fixed inset-0 flex items-center justify-center z-50 p-4"
                style="background-color: var(--background-haze);">
                <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border"
                    style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-semibold" style="color: var(--light-text);">Add New Stepping Stones</h2>
                        <button @click="showAddNodeModal = false" style="color: var(--highlight-color);">
                            <XMarkIcon class="w-6 h-6" />
                        </button>
                    </div>

                    <div class="space-y-4">
                        <!-- Dynamic list of node names -->
                        <div>
                            <label class="block text-sm font-medium mb-1"
                                style="color: var(--highlight-color);">Stepping Stone
                                Names</label>
                            <div v-for="(node, index) in newNodeNames" :key="index"
                                class="flex items-center gap-2 mb-2">
                                <input v-model="newNodeNames[index]" type="text" class="w-full p-2 border rounded-lg"
                                    style="background-color: var(--background-color-1t); color: var(--light-text); border-color: var(--color-primary-dark);"
                                    placeholder="Enter Stepping Stone name" maxlength="40" />
                                <button v-if="newNodeNames.length > 1" @click="removeNodeName(index)"
                                    class="text-red-400 hover:text-red-300">
                                    <XCircleIcon class="w-6 h-6" />
                                </button>
                            </div>
                            <button @click="addNodeNameField" class="mt-2 text-sm font-medium flex items-center gap-1"
                                style="color: var(--highlight-color);">
                                <PlusIcon class="w-4 h-4" />
                                Add Another Node
                            </button>
                            <p v-if="nodeNameErrors.length" class="mt-1 text-sm"
                                style="color: var(--color-primary-light);">
                                <!-- {{ nodeNameErrors }} -->
                                <span v-for="(error, index) in nodeNameErrors" :key="index">{{ error }}<br></span>

                            </p>
                        </div>

                        <div>
                            <label class="block text-sm font-medium mb-1" style="color: var(--highlight-color);">Upload
                                Resource
                                (optional)<br>Note: Stepping stone content is based on this resource and all previously
                                uploaded resources in this library </label>
                            <div class="border border-dashed rounded-lg p-4 text-center"
                                style="background-color: var(--background-color-1t); border-color: var(--color-primary-light);">
                                <input type="file" ref="fileInput" @change="handleFileSelection" class="hidden"
                                    accept=".pdf,.doc,.docx,.txt" />
                                <div v-if="!selectedFile" @click="$refs.fileInput.click()" class="cursor-pointer">
                                    <DocumentPlusIcon class="w-12 h-12 mx-auto"
                                        style="color: var(--color-primary-light);" />
                                    <p class="mt-2 text-sm" style="color: var(--highlight-color);">Click to upload (max
                                        500KB)
                                    </p>
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

    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
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
    XMarkIcon,
    DocumentPlusIcon,
    DocumentIcon,
    XCircleIcon
} from '@heroicons/vue/24/solid'
import { useRouter } from 'vue-router';
import axios from 'axios';

const props = defineProps({
    libraryId: {
        type: Number,
        required: true
    },
    roomNames: {
        type: Array,
        required: true
    },
    roomData: {
        type: Object,
        required: true
    }

})

// State for adding new nodes
const showAddNodeModal = ref(false)
const newNodeNames = ref([''])
const selectedFile = ref(null)
const nodeNameErrors = ref([])
const fileError = ref('')
const isAddingNode = ref(false)

// Local copy of room names for reactivity
const localRoomNames = ref([...props.roomNames])

// Convert room names to nodes
const nodes = computed(() => localRoomNames.value || [])

// Update local copy when props change
watch(() => props.roomNames, (newVal) => {
    localRoomNames.value = [...newVal]
})

// Track selected room for tooltip
const selectedRoom = ref(null)

const library_id = props.libraryId;

// File input handling
const fileInput = ref(null)

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
    } else if (localRoomNames.value.includes(name)) {
      nodeNameErrors.value[index] = 'This node name already exists'
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
    // for (const name of trimmedNames) {
        // formData.append('roomNames', name)
    // }
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
        for (const name of trimmedNames) {
            localRoomNames.value.push(name)
        }
    }

    // Clear form
    newNodeNames.value = [''] // Reset to one empty field
    removeFile()
    showAddNodeModal.value = false
    window.location.reload(); // TODO for showing new nodes / stepping stones, but theres 
    // probably a better way to do this
  } catch (error) {
    console.error('Error adding nodes:', error)
    nodeNameErrors.value[0] = error.message || 'Failed to add nodes. Please try again.'
  } finally {
    isAddingNode.value = false
  }
}

// Function to get the corresponding room data by room name
const getRoomData = (sectionId: any) => {
    // Find the room data where room_name matches roomName
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
const formatRoomName = (name: string) => {
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
    // If there are nodes and the container exists, scroll to position
    // some nodes may not be visible at first depending on the starting position
    if (nodes.value.length > 0 && scrollContainer.value) {
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

const handleNodeClick = (roomName) => {
    if (!hasMoved.value) {
        selectedRoom.value = selectedRoom.value === roomName ? null : roomName
    }
}

const getNodeOffset = (index) => {
    const amplitude = 80
    return Math.sin(index * 0.7) * amplitude
}

const startLesson = (roomName) => {
    router.push(`/lessons/${library_id}/${roomName}`)
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

// Handle scroll event (if needed)
const handleScroll = () => {
    // Implement if needed
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
</style>