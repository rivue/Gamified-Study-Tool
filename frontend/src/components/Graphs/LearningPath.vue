<template>
    <div class="fixed left-8 right-8 top-0 bottom-0 overflow-hidden">
      <button 
        @click="scroll('left')" 
        class="fixed left-8 top-1/2 -translate-y-1/2 bg-black/30 backdrop-blur-sm shadow-lg rounded-full p-4 hover:bg-black/40 z-10"
        style="color: var(--highlight-color);"
      >
        <ChevronLeftIcon class="w-12 h-12" />
      </button>
      
      <button 
        @click="scroll('right')" 
        class="fixed right-8 top-1/2 -translate-y-1/2 bg-black/30 backdrop-blur-sm shadow-lg rounded-full p-4 hover:bg-black/40 z-10"
        style="color: var(--highlight-color);"
      >
        <ChevronRightIcon class="w-12 h-12" />
      </button>
  
      <!-- Fixed Add Stepping Stone Button - Center Top -->
      <div class="fixed top-48 left-1/2 -translate-x-1/2 z-10">
        <button 
          @click="showAddNodeModal = true" 
          class="shadow-lg rounded-full p-4 flex items-center justify-center transition-colors"
          style="background-color: var(--element-color-1); color: var(--light-text);"
        >
          <PlusIcon class="w-6 h-6" />
          <span class="ml-2 font-medium">Add New Stepping Stone</span>
        </button>
      </div>
  
      <div 
        ref="scrollContainer"
        class="w-full h-full overflow-x-auto overflow-y-hidden cursor-grab active:cursor-grabbing"
        @mousedown="startDragging"
        @mousemove="drag"
        @mouseup="stopDragging"
        @mouseleave="stopDragging"
        @touchstart="startDragging"
        @touchmove="drag"
        @touchend="stopDragging"
        @scroll="handleScroll"
      >
        <!-- Modified to ensure first node is visible -->
        <div class="flex items-center gap-24 min-h-screen py-24 relative">
          <!-- Added left padding to ensure first nodes are visible -->
          <div class="w-24 flex-shrink-0"></div>
          
          <template v-for="(roomName, index) in nodes" :key="index">
            <div 
              class="relative flex-shrink-0 group perspective"
              :style="{
                transform: `translateY(${getNodeOffset(index)}px)`
              }"
              @click="handleNodeClick(roomName)"
            >
              <!-- Tooltip -->
              <div
                v-if="selectedRoom === roomName"
                class="absolute -top-32 left-1/2 -translate-x-1/2 w-64 z-50"
              >
                <div class="relative">
                  <!-- Red close button in top-right -->
                  <div 
                    @click.stop="selectedRoom = null"
                    class="absolute -top-3 -right-3 w-8 h-8 rounded-full flex items-center justify-center cursor-pointer"
                    style="background-color: red;"
                  >
                    <XMarkIcon class="w-4 h-4" style="color: var(--light-text);" />
                  </div>
                  
                  <!-- Main tooltip content -->
                  <div class="rounded-2xl p-4 shadow-lg" style="background-color: var(--element-color-1); color: var(--light-text);">
                    <div class="font-medium mb-3">{{ formatRoomName(roomName) }} <br> 
                      <span v-if="getRoomData(roomName) && getRoomData(roomName).lesson_state <= getRoomData(roomName).num_lessons">
                        lesson {{ getRoomData(roomName).lesson_state }} / {{ getRoomData(roomName).num_lessons }}
                      </span>
                    </div>
                    <button 
                      @click.stop="startLesson(roomName)"
                      class="w-full rounded-xl py-2 px-4 font-medium flex items-center justify-center gap-2 transition-colors"
                      style="background-color: var(--light-text); color: var(--element-color-1);"
                    >
                      <span v-if="getRoomData(roomName) && getRoomData(roomName).lesson_state <= getRoomData(roomName).num_lessons">PLAY</span>
                      <span v-else>REVIEW</span>
                    </button>
                  </div>
                  
                  <!-- Triangle pointer -->
                  <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 transform rotate-45" style="background-color: var(--element-color-1);" />
                </div>
              </div>
  
              <div class="relative transform-gpu transition-all duration-300 group-hover:scale-105 group-hover:-translate-y-2">
                <div 
                  class="absolute -bottom-4 left-1/2 -translate-x-1/2 w-40 h-8 rounded-full blur-xl transform-gpu transition-all duration-300 group-hover:w-44"
                  style="background-color: var(--background-color-1t);"
                ></div>
                
                <div class="relative w-48 h-48">
                  <div 
                    class="absolute inset-0 rounded-full transform-gpu translate-y-2 blur-sm opacity-50"
                    style="background-color: var(--color-primary-darker);"
                  ></div>
                  
                  <div 
                    class="absolute inset-0 rounded-full transform-gpu translate-y-1"
                    style="background-color: var(--color-primary-dark);"
                  ></div>
                  
                  <div 
                    class="absolute inset-0 rounded-full flex items-center justify-center cursor-pointer shadow-lg transform-gpu transition-all duration-300"
                    style="background: var(--button-gradient);"
                  >
                    <component 
                      :is="getIconForIndex(index)" 
                      class="w-24 h-24 transform-gpu transition-all duration-300 group-hover:scale-110"
                      style="color: var(--light-text);"
                    />
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
        <div v-if="showAddNodeModal" class="fixed inset-0 flex items-center justify-center z-50 p-4" style="background-color: var(--background-haze);">
          <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border" style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-semibold" style="color: var(--light-text);">Add New Stepping Stone</h2>
              <button @click="showAddNodeModal = false" style="color: var(--highlight-color);">
                <XMarkIcon class="w-6 h-6" />
              </button>
            </div>
  
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium mb-1" style="color: var(--highlight-color);">Stepping Stone Name</label>
                <input 
                  v-model="newNodeName" 
                  type="text" 
                  class="w-full p-2 border rounded-lg" 
                  style="background-color: var(--background-color-1t); color: var(--light-text); border-color: var(--color-primary-dark);" 
                  placeholder="Enter node name"
                  maxlength="40"
                />
                <p v-if="nodeNameError" class="mt-1 text-sm" style="color: var(--color-primary-light);">{{ nodeNameError }}</p>
              </div>
  
              <div>
                <label class="block text-sm font-medium mb-1" style="color: var(--highlight-color);">Upload Resource (optional)<br>Note: Stepping stone content is based on this resource and all previous resources in this library</label>
                <div class="border border-dashed rounded-lg p-4 text-center" style="background-color: var(--background-color-1t); border-color: var(--color-primary-light);">
                  <input 
                    type="file" 
                    ref="fileInput"
                    @change="handleFileSelection" 
                    class="hidden" 
                    accept=".pdf,.doc,.docx,.txt"
                  />
                  <div v-if="!selectedFile" @click="$refs.fileInput.click()" class="cursor-pointer">
                    <DocumentPlusIcon class="w-12 h-12 mx-auto" style="color: var(--color-primary-light);" />
                    <p class="mt-2 text-sm" style="color: var(--highlight-color);">Click to upload (max 500KB)</p>
                    <p class="mt-1 text-xs" style="color: var(--color-primary-light);">PDF, DOC, DOCX, TXT</p>
                  </div>
                  <div v-else class="text-left">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <DocumentIcon class="w-8 h-8 mr-2" style="color: var(--color-primary-light);" />
                        <div>
                          <p class="text-sm font-medium truncate" style="color: var(--highlight-color);">{{ selectedFile.name }}</p>
                          <p class="text-xs" style="color: var(--color-primary-light);">{{ formatFileSize(selectedFile.size) }}</p>
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
                <button 
                  @click="showAddNodeModal = false" 
                  class="px-4 py-2 border rounded-lg" 
                  style="border-color: var(--color-primary); color: var(--highlight-color);"
                >
                  Cancel
                </button>
                <button 
                  @click="addNewNode" 
                  class="px-4 py-2 rounded-lg focus:outline-none focus:ring-2"
                  style="background: var(--button-gradient); color: var(--light-text);"
                  :disabled="isAddingNode"
                >
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
  
  <script setup>
  import { ref, computed, watch, onMounted } from 'vue'
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
  const newNodeName = ref('')
  const selectedFile = ref(null)
  const nodeNameError = ref('')
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
  
  const router = useRouter();
  
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
  
  // Function to add a new node
  const addNewNode = async () => {
    // Validate node name
    nodeNameError.value = ''
    const trimmedName = newNodeName.value.trim()
    
    if (!trimmedName) {
      nodeNameError.value = 'Please enter a node name'
      return
    }
    
    if (!/^[a-zA-Z ]+$/.test(trimmedName)) {
      nodeNameError.value = 'Node name can only contain letters and spaces'
      return
    }
    
    if (trimmedName.length > 40) {
      nodeNameError.value = 'Node name must be 40 characters or less'
      return
    }
    
    // Check for duplicate names
    if (localRoomNames.value.includes(trimmedName)) {
      nodeNameError.value = 'This node name already exists'
      return
    }
    
    isAddingNode.value = true
    
    try {
      // Create a FormData object for the request
      const formData = new FormData()
      formData.append('libraryId', library_id)
      formData.append('roomName', trimmedName)
      
      // Add file if present
      if (selectedFile.value) {
        formData.append('file', selectedFile.value)
      }
      
      // Send request to add the node
      const response = await axios.post('/api/library/room', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      if (response.data && response.data.status == "success") {
        // Add the new room name to the local array
        // localRoomNames.value.push(trimmedName)
        
        // Clear form
        newNodeName.value = ''
        removeFile()
        showAddNodeModal.value = false
        
        // Emit event to notify parent component
        emit('nodeAdded', trimmedName)
        window.location.reload();
      } else {

        console.log(response)

        throw new Error(response.data.message || 'Failed to add node')
      }
    } catch (error) {
      console.error('Error adding node:', error)
      nodeNameError.value = error.message || 'Failed to add node. Please try again.'
    } finally {
      isAddingNode.value = false
    }
  }
  
  // Function to get the corresponding room data by room name
  const getRoomData = (roomName) => {
    // Find the room data where room_name matches roomName
    for (let i = 0; i < props.roomData.length; i++) {
      if (props.roomData[i].room_name === roomName) {
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
    return name
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }
  
  const scrollContainer = ref(null)
  const isDragging = ref(false)
  const startX = ref(0)
  const scrollLeft = ref(0)
  
  // Scroll to center on first load
  onMounted(() => {
    // If there are nodes and the container exists, scroll to position
    // some nodes may not be visible at first depending on the starting position
    if (nodes.value.length > 0 && scrollContainer.value) {
      // Calculate an appropriate starting position based on available width
      setTimeout(() => {
        // This gives time for the layout to render before scrolling
        if (scrollContainer.value) {
          const startPosition = Math.max(0, 200); // A small offset to show the first node
          scrollContainer.value.scrollLeft = startPosition;
        }
      }, 100);
    }
  });
  
  const startDragging = (e) => {
    isDragging.value = true
    const pageX = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX
    startX.value = pageX - scrollContainer.value.offsetLeft
    scrollLeft.value = scrollContainer.value.scrollLeft
    e.preventDefault()
  }
  
  const drag = (e) => {
    if (!isDragging.value) return
    const pageX = e.type.includes('mouse') ? e.pageX : e.touches[0].pageX
    const x = pageX - scrollContainer.value.offsetLeft
    const walk = (x - startX.value) * 2
    scrollContainer.value.scrollLeft = scrollLeft.value - walk
  }
  
  const stopDragging = () => {
    isDragging.value = false
  }
  
  const getNodeOffset = (index) => {
    const amplitude = 80
    return Math.sin(index * 0.7) * amplitude
  }
  
  const handleNodeClick = (roomName) => {
    if (!isDragging.value) {
      selectedRoom.value = selectedRoom.value === roomName ? null : roomName
    }
  }
  
  const startLesson = (roomName) => {
    console.log(`Starting lesson for ${roomName}`)
    router.push(`/lessons/${library_id}/${roomName}`)
    emit('nodeSelected', roomName)
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
  
  const emit = defineEmits(['nodeSelected', 'nodeAdded'])
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