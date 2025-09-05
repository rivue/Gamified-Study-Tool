<script setup lang="ts">
import { inject, computed, ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
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
  props.variant === 'shad' ? 'tt-shadcn' : '',
  props.class
].filter(Boolean).join(' '))

const el = ref<HTMLElement | null>(null)
const styleObj = ref<Record<string, string>>({})

function computePosition() {
  if (!ctx?.triggerEl?.value || !el.value) return
  const t = ctx.triggerEl.value as HTMLElement
  const c = el.value as HTMLElement
  const tr = t.getBoundingClientRect()
  const cr = c.getBoundingClientRect() // dimensions only; top/left will be recalculated
  const gap = props.offset ?? 12
  let top = 0
  let left = 0
  switch (props.side) {
    case 'bottom':
      top = tr.bottom + gap
      left = tr.left + tr.width / 2 - cr.width / 2
      break
    case 'left':
      top = tr.top + tr.height / 2 - cr.height / 2
      left = tr.left - gap - cr.width
      break
    case 'right':
      top = tr.top + tr.height / 2 - cr.height / 2
      left = tr.right + gap
      break
    case 'top':
    default:
      top = tr.top - gap - cr.height
      left = tr.left + tr.width / 2 - cr.width / 2
      break
  }

  // Keep within viewport bounds (basic clamping)
  const vw = window.innerWidth
  const vh = window.innerHeight
  const padding = 4
  left = Math.max(padding, Math.min(left, vw - cr.width - padding))
  top = Math.max(padding, Math.min(top, vh - cr.height - padding))

  styleObj.value = {
    position: 'fixed',
    top: `${Math.round(top)}px`,
    left: `${Math.round(left)}px`
  }
}

function scheduleCompute() {
  // Run after DOM shows the tooltip
  nextTick(() => {
    requestAnimationFrame(() => computePosition())
  })
}

watch(() => ctx?.isOpen.value, (open) => {
  if (open) scheduleCompute()
})

watch(() => [props.side, props.offset], () => {
  if (ctx?.isOpen.value) scheduleCompute()
})

function onWinChange() {
  if (ctx?.isOpen.value) computePosition()
}

onMounted(() => {
  window.addEventListener('resize', onWinChange)
  window.addEventListener('scroll', onWinChange, true)
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', onWinChange)
  window.removeEventListener('scroll', onWinChange, true)
})
</script>

<template>
  <teleport to="body">
    <transition name="tt-fade">
      <div
        v-show="ctx?.isOpen.value"
        :id="ctx?.id"
        role="tooltip"
        :class="classes"
        :style="styleObj"
        v-if="ctx"
        ref="el"
      >
        <slot />
      </div>
    </transition>
  </teleport>
</template>

<style scoped>
.tt-fade-enter-active,
.tt-fade-leave-active { transition: opacity .12s ease; }
.tt-fade-enter-from,
.tt-fade-leave-to { opacity: 0; }

.tt-content {
  position: fixed; /* positioned via JS relative to viewport */
  background: #111;
  color: #fff;
  font-size: 12px;
  line-height: 1.25;
  padding: 6px 8px;
  border-radius: 6px;
  /* Raise above any app element, menus, modals, etc. */
  z-index: 2147483647;
  max-width: 260px;
  box-shadow: 0 4px 16px rgba(0,0,0,.25);
  pointer-events: none;
  font-weight: 500;
}

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
  z-index: 2147483647; /* ensure shadcn variant also has high z-index */
}
</style>
