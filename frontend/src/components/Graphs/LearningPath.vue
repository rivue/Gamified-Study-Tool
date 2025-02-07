<template>
    <div class="fixed left-8 right-8 top-0 bottom-0 overflow-hidden">
      <button 
        @click="scroll('left')" 
        class="fixed left-8 top-1/2 -translate-y-1/2 bg-white shadow-lg rounded-full p-4 hover:bg-gray-50 z-10"
      >
        <ChevronLeftIcon class="w-12 h-12 text-gray-600" />
      </button>
      
      <button 
        @click="scroll('right')" 
        class="fixed right-8 top-1/2 -translate-y-1/2 bg-white shadow-lg rounded-full p-4 hover:bg-gray-50 z-10"
      >
        <ChevronRightIcon class="w-12 h-12 text-gray-600" />
      </button>
  
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
        <div class="flex items-center gap-32 px-24 min-h-[600px] min-w-max py-24">
          <template v-for="(roomName, index) in nodes" :key="index">
            <div 
              class="relative flex-shrink-0 group perspective"
              :style="{
                transform: `translateY(${getNodeOffset(index)}px)`
              }"
              @click="handleNodeClick(roomName)"
            >
              <div class="relative transform-gpu transition-all duration-300 group-hover:scale-105 group-hover:-translate-y-2">
                <div 
                  class="absolute -bottom-4 left-1/2 -translate-x-1/2 w-40 h-8 rounded-full bg-green-500/20 blur-xl transform-gpu transition-all duration-300 group-hover:bg-green-400/30 group-hover:w-44"
                ></div>
                
                <div class="relative w-48 h-48">
                  <div 
                    class="absolute inset-0 rounded-full bg-green-700 transform-gpu translate-y-2 blur-sm opacity-50"
                  ></div>
                  
                  <div 
                    class="absolute inset-0 rounded-full bg-green-600 transform-gpu translate-y-1"
                  ></div>
                  
                  <div 
                    class="absolute inset-0 rounded-full bg-gradient-to-br from-green-400 to-green-500 flex items-center justify-center cursor-pointer shadow-lg transform-gpu transition-all duration-300 group-hover:from-green-300 group-hover:to-green-400"
                  >
                    <component 
                      :is="getIconForIndex(index)" 
                      class="w-24 h-24 text-white transform-gpu transition-all duration-300 group-hover:scale-110"
                    />
                  </div>
                </div>
              </div>
              
              <div class="absolute -bottom-12 left-1/2 -translate-x-1/2 text-xl font-medium text-center w-48 text-gray-700">
                {{ formatRoomName(roomName) }}
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
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
    SparklesIcon
  } from '@heroicons/vue/24/solid'
  
  const props = defineProps({
    roomNames: {
      type: Array,
      required: true
    }
  })
  
  // Convert room names to nodes
  const nodes = computed(() => props.roomNames || [])
  
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
      emit('nodeSelected', roomName)
    }
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
  
  const emit = defineEmits(['nodeSelected'])
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
  </style>