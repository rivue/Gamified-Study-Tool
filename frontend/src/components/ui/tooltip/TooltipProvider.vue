<script setup lang="ts">
import { reactive, watch, provide } from 'vue'

const props = withDefaults(defineProps<{
  openDelay?: number
  closeDelay?: number
  disabled?: boolean
}>(), {
  openDelay: 0,
  closeDelay: 0,
  disabled: false
})

const cfg = reactive({
  openDelay: props.openDelay,
  closeDelay: props.closeDelay,
  disabled: props.disabled
})

watch(() => ({ ...props }), p => {
  cfg.openDelay = p.openDelay
  cfg.closeDelay = p.closeDelay
  cfg.disabled = p.disabled
})

provide('tooltipGlobalConfig', cfg)
</script>

<template>
  <slot />
</template>
