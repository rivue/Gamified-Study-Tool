<template>
  <div class="relative flex-shrink-0">
    <div 
      class="w-16 h-16 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 hover:scale-110 hover:shadow-lg active:scale-95"
      :style="{ 
        backgroundColor: unitColor,
        opacity: 0.7,
      }"
      @click="openAddSectionModal"
    >
      <PlusIcon class="w-8 h-8" style="color: var(--light-text);" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { PlusIcon } from '@heroicons/vue/24/solid';

const props = defineProps({
  unitId: {
    type: [Number, String],
    required: true
  },
  unitColor: {
    type: String,
    required: true
  },
  position: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['add-section']);

const openAddSectionModal = () => {
  emit('add-section', {
    unitId: props.unitId,
    position: props.position
  });
};
</script>