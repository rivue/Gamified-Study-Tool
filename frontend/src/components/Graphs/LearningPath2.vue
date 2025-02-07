<template>
    <div class="relative w-full max-w-6xl mx-auto py-8">
      <!-- Navigation buttons -->
      <button 
        @click="scroll('left')" 
        class="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-12 bg-white shadow-lg rounded-full p-4 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed z-10"
        :disabled="scrollPosition <= 0"
      >
        <ChevronLeftIcon class="w-8 h-8 text-gray-600" />
      </button>
      
      <button 
        @click="scroll('right')" 
        class="absolute right-0 top-1/2 -translate-y-1/2 translate-x-12 bg-white shadow-lg rounded-full p-4 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed z-10"
        :disabled="scrollPosition >= maxScroll"
      >
        <ChevronRightIcon class="w-8 h-8 text-gray-600" />
      </button>
  
      <!-- Scrollable container -->
      <div 
        ref="scrollContainer"
        class="overflow-x-hidden relative"
        @scroll="handleScroll"
      >
        <div class="flex items-center gap-4 px-16">
          <!-- Path nodes -->
          <template v-for="(node, index) in nodes" :key="index">
            <!-- Connector line -->
            <div 
              v-if="index > 0" 
              class="h-1 w-24 bg-gray-200"
              :class="{ 'bg-green-500': node.unlocked }"
            ></div>
            
            <!-- Node -->
            <div 
              class="relative flex-shrink-0"
              @click="handleNodeClick(node)"
            >
              <!-- Main circle -->
              <div 
                class="w-32 h-32 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 shadow-md"
                :class="[
                  node.unlocked ? 'bg-green-500 hover:bg-green-600' : 'bg-gray-200',
                  node.current ? 'ring-8 ring-green-300' : ''
                ]"
              >
                <!-- Node icon -->
                <component 
                  :is="node.icon" 
                  class="w-16 h-16"
                  :class="node.unlocked ? 'text-white' : 'text-gray-500'"
                />
              </div>
              
              <!-- Label -->
              <div 
                class="absolute -bottom-8 left-1/2 -translate-x-1/2 text-base font-medium text-center w-32"
                :class="node.unlocked ? 'text-gray-700' : 'text-gray-400'"
              >
                {{ node.label }}
              </div>
              
              <!-- Lock icon for locked nodes -->
              <div 
                v-if="!node.unlocked" 
                class="absolute -right-2 -top-2 w-10 h-10 bg-gray-400 rounded-full flex items-center justify-center shadow-sm"
              >
                <LockClosedIcon class="w-6 h-6 text-white" />
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { 
    StarIcon, 
    BookOpenIcon, 
    TrophyIcon,
    LockClosedIcon,
    ChatBubbleBottomCenterTextIcon,
    AcademicCapIcon,
    BeakerIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
    PuzzlePieceIcon,
    RocketLaunchIcon,
    SparklesIcon
  } from '@heroicons/vue/24/solid'
  
  // Node data
  const nodes = ref([
    {
      id: 1,
      label: 'Start Here',
      icon: StarIcon,
      unlocked: true,
      current: true
    },
    {
      id: 2,
      label: 'Basic Phrases',
      icon: ChatBubbleBottomCenterTextIcon,
      unlocked: true,
      current: false
    },
    {
      id: 3,
      label: 'Grammar Basics',
      icon: BookOpenIcon,
      unlocked: false,
      current: false
    },
    {
      id: 4,
      label: 'Practice Quiz',
      icon: PuzzlePieceIcon,
      unlocked: false,
      current: false
    },
    {
      id: 5,
      label: 'Achievement 1',
      icon: TrophyIcon,
      unlocked: false,
      current: false
    },
    {
      id: 6,
      label: 'Advanced Topics',
      icon: AcademicCapIcon,
      unlocked: false,
      current: false
    },
    {
      id: 7,
      label: 'Lab Practice',
      icon: BeakerIcon,
      unlocked: false,
      current: false
    },
    {
      id: 8,
      label: 'Quick Review',
      icon: SparklesIcon,
      unlocked: false,
      current: false
    },
    {
      id: 9,
      label: 'Final Challenge',
      icon: RocketLaunchIcon,
      unlocked: false,
      current: false
    }
  ])
  
  const scrollContainer = ref(null)
  const scrollPosition = ref(0)
  const maxScroll = ref(0)
  
  const handleNodeClick = (node) => {
    if (!node.unlocked) return
    
    nodes.value = nodes.value.map(n => ({
      ...n,
      current: n.id === node.id
    }))
    
    emit('nodeSelected', node)
  }
  
  const scroll = (direction) => {
    const container = scrollContainer.value
    const scrollAmount = 300
    
    if (direction === 'left') {
      container.scrollBy({ left: -scrollAmount, behavior: 'smooth' })
    } else {
      container.scrollBy({ left: scrollAmount, behavior: 'smooth' })
    }
  }
  
  const handleScroll = () => {
    const container = scrollContainer.value
    scrollPosition.value = container.scrollLeft
    maxScroll.value = container.scrollWidth - container.clientWidth
  }
  
  onMounted(() => {
    handleScroll()
  })
  
  const emit = defineEmits(['nodeSelected'])
  </script>
  
  <style scoped>
  .overflow-x-hidden {
    -webkit-overflow-scrolling: touch;
    scroll-behavior: smooth;
  }
  </style>