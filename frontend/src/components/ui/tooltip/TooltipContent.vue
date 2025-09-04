<script setup lang="ts">
import { inject, computed } from 'vue'
const ctx = inject<any>('tooltipCtx')
if (!ctx) console.warn('TooltipContent used outside Tooltip root')
const props = withDefaults(defineProps<{
  class?: string
  side?: 'top' | 'bottom' | 'left' | 'right'
  variant?: 'default' | 'shad'
  offset?: number
}>(), {
  side: 'top',
  variant: 'default',
  offset: 12
})
const classes = computed(() => [
  'tt-content',
  `side-${props.side}`,
  props.variant === 'shad' ? 'tt-shadcn' : '',
  props.class
].filter(Boolean).join(' '))

const offsetStyles = computed(() => {
  const offset = props.offset
  switch (props.side) {
    case 'top': return { transform: `translate(-50%, -${offset}px)` }
    case 'bottom': return { transform: `translate(-50%, ${offset}px)` }
    case 'left': return { transform: `translate(-${offset}px, -50%)` }
    case 'right': return { transform: `translate(${offset}px, -50%)` }
    default: return { transform: `translate(-50%, -${offset}px)` }
  }
})
</script>

<template>
  <transition name="tt-fade">
    <div
      v-show="ctx?.isOpen.value"
      :id="ctx?.id"
      role="tooltip"
      :class="classes"
      :style="offsetStyles"
      v-if="ctx"
    >
      <slot />
    </div>
  </transition>
</template>

<style scoped>
.tt-fade-enter-active,
.tt-fade-leave-active { transition: opacity .12s ease; }
.tt-fade-enter-from,
.tt-fade-leave-to { opacity: 0; }

.tt-content {
  position: absolute;
  top: 0;
  left: 50%;
  /* removed transform - now handled by computed style */
  background: #111;
  color: #fff;
  font-size: 12px;
  line-height: 1.25;
  padding: 6px 8px;
  border-radius: 6px;
  z-index: 9999; /* much higher z-index */
  max-width: 260px;
  box-shadow: 0 4px 16px rgba(0,0,0,.25);
  pointer-events: none;
  font-weight: 500;
}

.tt-content.side-bottom { top: 100%; }
.tt-content.side-left { left: 0; top: 50%; }
.tt-content.side-right { left: 100%; top: 50%; }

.tt-shadcn {
  background: hsl(240 10% 3.9%);
  color: hsl(0 0% 98%);
  border: 1px solid hsl(240 3.7% 15.9%);
  padding: 6px 10px;
  font-size: 12px;
  line-height: 1.25;
  border-radius: 6px;
  box-shadow:
    0 4px 6px -1px rgba(0,0,0,.25),
    0 2px 4px -2px rgba(0,0,0,.2),
    0 0 0 1px hsl(240 3.7% 15.9%);
  backdrop-filter: blur(8px);
  letter-spacing: .2px;
  z-index: 9999; /* ensure shadcn variant also has high z-index */
}
</style>
