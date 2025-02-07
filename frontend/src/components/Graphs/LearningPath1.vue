<template>
    <div class="learning-path-container relative w-full max-w-xl mx-auto py-8">
      <div class="flex flex-col items-center gap-4">
        <!-- Path nodes -->
        <template v-for="(node, index) in nodes" :key="index">
          <!-- Connector line -->
          <div 
            v-if="index > 0" 
            class="w-1 h-12 bg-gray-200"
            :class="{ 'bg-green-500': node.unlocked }"
          ></div>
          
          <!-- Node -->
          <div 
            class="relative"
            @click="handleNodeClick(node)"
          >
            <!-- Main circle -->
            <div 
              class="w-16 h-16 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300"
              :class="[
                node.unlocked ? 'bg-green-500 hover:bg-green-600' : 'bg-gray-200',
                node.current ? 'ring-4 ring-green-300' : ''
              ]"
            >
              <!-- Node icon -->
              <component 
                :is="node.icon" 
                class="w-8 h-8"
                :class="node.unlocked ? 'text-white' : 'text-gray-500'"
              />
            </div>
            
            <!-- Label -->
            <div 
              class="absolute -right-24 top-1/2 -translate-y-1/2 text-sm font-medium"
              :class="node.unlocked ? 'text-gray-700' : 'text-gray-400'"
            >
              {{ node.label }}
            </div>
            
            <!-- Lock icon for locked nodes -->
            <div 
              v-if="!node.unlocked" 
              class="absolute -right-2 -top-2 w-6 h-6 bg-gray-400 rounded-full flex items-center justify-center"
            >
              <LockClosedIcon class="w-3 h-3 text-white" />
            </div>
          </div>
        </template>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { 
    StarIcon, 
    BookOpenIcon, 
    TrophyIcon,
    LockClosedIcon,
    ChatBubbleBottomCenterTextIcon
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
      label: 'Achievement 1',
      icon: TrophyIcon,
      unlocked: false,
      current: false
    }
  ])
  
  const handleNodeClick = (node) => {
    if (!node.unlocked) return
    
    // Update current node
    nodes.value = nodes.value.map(n => ({
      ...n,
      current: n.id === node.id
    }))
    
    // Emit event for parent component
    emit('nodeSelected', node)
  }
  
  const emit = defineEmits(['nodeSelected'])
  </script>
  
  <style scoped>
  .learning-path-container {
    perspective: 1000px;
  }
  
  .learning-path-container > div {
    transform-style: preserve-3d;
  }
  </style>