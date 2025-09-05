<script setup lang="ts">
import { inject, onMounted, onBeforeUnmount, ref } from 'vue'

const ctx = inject<any>('tooltipCtx', null)

const props = withDefaults(defineProps<{
  as?: string
  disabled?: boolean
  class?: string
}>(), {
  as: 'span',
  disabled: false
})

const Tag = props.as as any
const el = ref<HTMLElement | null>(null)

onMounted(() => {
  if (ctx && 'triggerEl' in ctx) {
    ctx.triggerEl.value = el.value
  }
})

onBeforeUnmount(() => {
  if (ctx && 'triggerEl' in ctx) {
    ctx.triggerEl.value = null
  }
})

</script>

<template>
  <Tag
    :class="['tt-trigger', props.class]"
    :tabindex="-1"
    ref="el"
    :aria-describedby="ctx?.id"
    :aria-disabled="props.disabled || undefined"
    @mouseenter="!props.disabled && ctx?.show()"
    @mouseleave="ctx?.hide()"
    @focus.prevent
    @blur.prevent
  >
    <slot />
  </Tag>
</template>

<style scoped>
.tt-trigger { 
  cursor: pointer; 
  display: inline-flex; 
  outline: none !important;
}
.tt-trigger[aria-disabled="true"] { cursor: not-allowed; opacity: .55; }
.tt-trigger:focus { outline: none !important; }
</style>
