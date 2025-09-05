<script setup lang="ts">
import { inject, ref, provide, watch, onUnmounted } from 'vue'

const props = withDefaults(defineProps<{
  open?: boolean
  disabled?: boolean
}>(), {
  open: undefined,
  disabled: false
})

const globalCfg = inject<any>('tooltipGlobalConfig', { openDelay: 0, closeDelay: 0, disabled: false })
const isOpen = ref(false)
const triggerEl = ref<HTMLElement | null>(null)
let timer: number | undefined

function show() {
  if (props.disabled || globalCfg.disabled) return
  clearTimeout(timer)
  timer = window.setTimeout(() => { 
    isOpen.value = true 
  }, globalCfg.openDelay)
}

function hide(immediate = false) {
  clearTimeout(timer)
  if (immediate) {
    isOpen.value = false
  } else {
    timer = window.setTimeout(() => { 
      isOpen.value = false 
    }, globalCfg.closeDelay)
  }
}

// Only update if open prop is explicitly provided
watch(() => props.open, (newVal) => {
  if (newVal !== undefined) {
    clearTimeout(timer)
    isOpen.value = !!newVal
  }
}, { immediate: true })

// Cleanup on unmount
onUnmounted(() => {
  clearTimeout(timer)
})

// Create unique ID for each tooltip instance
const tooltipId = `tt-${Math.random().toString(36).slice(2, 11)}`

provide('tooltipCtx', {
  isOpen,
  show,
  hide,
  id: tooltipId,
  triggerEl
})
</script>

<template>
  <div class="tt-root">
    <slot />
  </div>
</template>

<style scoped>
/* Use inline flow and avoid creating a new containing block so absolute elements
   inside triggers are not re-anchored (prevents Y shifting). */
.tt-root { display: inline; position: static; }
</style>
