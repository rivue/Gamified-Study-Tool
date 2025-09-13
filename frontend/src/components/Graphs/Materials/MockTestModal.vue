<template>
  <QuizModal
    :material-name="testName"
    :questions="questions"
    title="Mock Test"
    @close="$emit('close')"
  />
</template>

<script setup lang="ts">
import QuizModal from './QuizModal.vue';
const props = defineProps({
  testName: { type: String, required: true },
  questions: { type: Array, default: () => [] }
});
const emit = defineEmits(['close']);
</script>
