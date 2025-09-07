<template>
    <transition name="modal-fade">
        <div class="modal-backdrop" @click.self="close" role="dialog" aria-modal="true" :aria-label="`Summary of ${materialName}`">
            <div class="modal-container" ref="container">
                <header class="modal-header">
                    <h2 class="modal-title">
                        <span class="title-accent"></span>
                        Summary of {{ materialName }}
                    </h2>
                    <button @click="close" class="close-button" aria-label="Close dialog">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </header>
                <main class="modal-body">
                    <div class="summary-content prose" v-html="renderedSummary"></div>
                </main>
                <footer class="modal-footer">
                    <button @click="close" class="button-primary">
                        <span>Close</span>
                    </button>
                </footer>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, onMounted, ref, computed } from 'vue';
import { marked } from 'marked';

const props = defineProps({
    materialName: { type: String, required: true },
    summary: { type: String, default: '<p>No summary available.</p>' }
});

const emit = defineEmits(['close']);
const close = () => emit('close');

const container = ref(null);
onMounted(() => {
    requestAnimationFrame(() => container.value?.focus());
});

// Normalize single-line markdown by inserting line breaks before headings, lists, and numbers
function normalizeMarkdown(md: string): string {
    if (!md) return '';
    const hasNewlines = /\n/.test(md);
    if (hasNewlines) return md;

    let s = md.trim();
    // Newline before headings that appear mid-text
    s = s.replace(/(?<!^)\s+(#{1,6})\s+/g, '\n$1 ');
    // Newline before unordered list items like " - "
    s = s.replace(/(?<!^)\s-\s/g, '\n- ');
    // Newline before ordered list items like " 1. "
    s = s.replace(/(?<!^)\s(\d+\.)\s/g, '\n$1 ');
    // Add an extra newline after headings to improve spacing
    s = s.replace(/^(#{1,6} .*)$/gm, '$1\n');
    return s;
}

// Render the summary as Markdown if it is not already HTML
const renderedSummary = computed(() => {
    const text = props.summary || '';
    const looksLikeHtml = /<\/?[a-z][\s\S]*>/i.test(text);
    if (looksLikeHtml) return text;

    // const normalized = normalizeMarkdown(text);
    return marked.parse(text, { gfm: true, breaks: true });
});
</script>

<style scoped>
:root {
    --highlight-color: var(--element-color-1, #0d9488);
    --highlight-color-alt: var(--element-color-2, #14b8a6);
    --accent-rgb: 13, 148, 136;
    --primary-rgb: 13, 148, 136;
    --light-text: var(--text-color, #f8fafc);
}

/* ============ Transition ============ */
.modal-fade-enter-active,
.modal-fade-leave-active {
    transition: opacity .35s ease, transform .4s cubic-bezier(.22,.99,.34,1);
}
.modal-fade-enter-from,
.modal-fade-leave-to {
    opacity: 0;
    transform: translateY(10px) scale(.97);
}

/* ============ Backdrop ============ */
.modal-backdrop {
    position: fixed;
    inset: 0;
    padding: clamp(0.75rem, 2vh, 2rem);
    display: flex;
    justify-content: center;
    align-items: flex-start;
    overflow-y: auto;
    backdrop-filter: blur(14px) saturate(140%);
    -webkit-backdrop-filter: blur(14px) saturate(140%);
    background:
        radial-gradient(circle at 20% 25%, rgba(13,148,136,.15), transparent 60%),
        radial-gradient(circle at 80% 75%, rgba(13,148,136,.08), transparent 55%),
        linear-gradient(180deg, var(--background-color), rgba(10,31,31,0.95));
    z-index: 1000;
    animation: backdrop-fade .5s ease;
}

/* Push modal down a bit */
.modal-container {
    margin-top: 4.5rem;
}

/* ============ Container ============ */
.modal-container {
    position: relative;
    outline: none;
    width: min(900px, 100%);
    max-height: min(92vh, 1200px);
    background:
        linear-gradient(155deg, rgba(255,255,255,.05), rgba(255,255,255,.01)),
        linear-gradient(25deg, rgba(13,148,136,.08), transparent);
    border: 1px solid rgba(13,148,136,.25);
    box-shadow:
        0 10px 35px -5px rgba(0,0,0,.75),
        0 0 0 1px rgba(13,148,136,.25),
        0 0 0 6px rgba(13,148,136,.06) inset;
    border-radius: 1.35rem;
    display: flex;
    flex-direction: column;
    backdrop-filter: blur(22px) saturate(160%);
    -webkit-backdrop-filter: blur(22px) saturate(160%);
    overflow: hidden;
    background-color: rgba(10,31,31,.85);
}

/* Edge highlight */
.modal-container:before {
    content: "";
    pointer-events: none;
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background:
        linear-gradient(130deg,
            rgba(13,148,136,.55),
            transparent 40%,
            rgba(20,184,166,.35) 70%,
            transparent 85%);
    mix-blend-mode: overlay;
    opacity: .25;
}

/* ============ Header ============ */
.modal-header {
    position: relative;
    padding: 1.4rem 1.75rem 1.25rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.modal-title {
    font-size: clamp(1.25rem, 1.4rem + .3vw, 1.75rem);
    font-weight: 600;
    line-height: 1.15;
    letter-spacing: .5px;
    display: flex;
    align-items: center;
    gap: .75rem;
    color: #f8fafc;
    text-shadow: 0 2px 8px rgba(13,148,136,.6);
    filter: drop-shadow(0 4px 10px rgba(0,0,0,.65));
}

.title-accent {
    width: .65rem;
    height: 2.15rem;
    border-radius: .4rem;
    background: linear-gradient(180deg, var(--highlight-color), var(--highlight-color-alt));
    box-shadow: 0 0 0 3px rgba(255,255,255,.03), 0 2px 6px -1px rgba(0,0,0,.7);
}

/* ============ Close Button ============ */
.close-button {
    margin-left: auto;
    background: linear-gradient(135deg, rgba(13,148,136,.12), rgba(13,148,136,.05));
    border: 1px solid rgba(13,148,136,.35);
    color: #f8fafc;
    padding: .55rem;
    border-radius: .85rem;
    cursor: pointer;
    display: grid;
    place-items: center;
    transition: all .25s ease;
    position: relative;
}
.close-button:before {
    content:"";
    position:absolute;
    inset:0;
    border-radius: inherit;
    background: radial-gradient(circle at 30% 30%, rgba(13,148,136,.4), transparent 65%);
    opacity: 0;
    transition: opacity .35s ease;
}
.close-button:hover {
    color: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px -6px rgba(0,0,0,.65), 0 0 0 1px rgba(13,148,136,.4);
}
.close-button:hover:before { opacity: 1; }
.close-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px -2px rgba(0,0,0,.7);
}

/* ============ Body ============ */
.modal-body {
    padding: 0 1.75rem 1.75rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--highlight-color) transparent;
}
.modal-body::-webkit-scrollbar { width: .55rem; }
.modal-body::-webkit-scrollbar-track { background: transparent; }
.modal-body::-webkit-scrollbar-thumb {
    background: linear-gradient(var(--highlight-color), var(--highlight-color-alt));
    border-radius: 2rem;
    border: 1px solid rgba(255,255,255,.1);
}
.modal-body::-webkit-scrollbar-thumb:hover { filter: brightness(1.15); }

/* ============ Summary Content ============ */
.prose {
    font-size: .975rem;
    line-height: 1.6;
    color: var(--light-text);
}

.summary-content :deep(h1),
.summary-content :deep(h2),
.summary-content :deep(h3),
.summary-content :deep(h4) {
    font-weight: 600;
    line-height: 1.25;
    background: linear-gradient(92deg, var(--highlight-color), var(--highlight-color-alt) 55%);
    -webkit-background-clip: text;
    color: transparent;
    margin: 2rem 0 1rem;
    letter-spacing: .6px;
}

.summary-content :deep(h3) { font-size: 1.15rem; }

.summary-content :deep(p) {
    margin: 0 0 1rem;
    color: rgba(229,255,233,.9);
}

.summary-content :deep(ul),
.summary-content :deep(ol) {
    list-style: decimal;
    list-style-position: outside;
    padding-left: 1.6rem; /* adjust as needed */
    margin: 0 0 1.25rem 0;
}

/* Nested ordered lists */
.summary-content :deep(ol ol) {
    padding-left: 1.6rem;
}

/* Optional: small spacing between items */
.summary-content :deep(ol li) {
    margin-bottom: .55rem;
}

.summary-content :deep(ul li) {
    position: relative;
    padding: .45rem .85rem .45rem 1.6rem;
    background: linear-gradient(145deg, rgba(13,148,136,.12), rgba(13,148,136,.04));
    border: 1px solid rgba(13,148,136,.25);
    margin-bottom: .55rem;
    line-height: 1.45;
    border-radius: .85rem;
    backdrop-filter: blur(6px) saturate(150%);
    -webkit-backdrop-filter: blur(6px) saturate(150%);
    transition: background .3s ease, transform .25s ease;
}
.summary-content :deep(ul li:hover) {
    background: linear-gradient(145deg, rgba(13,148,136,.18), rgba(13,148,136,.06));
    transform: translateX(4px);
}
.summary-content :deep(ul li:before) {
    content:"";
    position:absolute;
    left:.75rem;
    top:.9rem;
    width:.55rem;
    height:.55rem;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #fff, var(--highlight-color) 70%);
    box-shadow: 0 0 0 3px rgba(13,148,136,.25), 0 0 8px -1px var(--highlight-color);
}

.summary-content :deep(code) {
    background: rgba(13,148,136,.12);
    padding: .25rem .5rem;
    border-radius: .5rem;
    font-size: .85rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
    color: #a7f3d0;
    border: 1px solid rgba(13,148,136,.35);
}

.summary-content :deep(pre code) {
    display: block;
    padding: 1rem 1.15rem;
    white-space: pre-wrap;
    background: linear-gradient(145deg, #020503, rgba(13,148,136,.08));
    box-shadow: inset 0 0 0 1px rgba(13,148,136,.25);
    border-radius: 1rem;
}

.summary-content :deep(a) {
    color: var(--highlight-color);
    text-decoration: none;
    position: relative;
    font-weight: 500;
}
.summary-content :deep(a:after) {
    content:"";
    position:absolute;
    left:0;
    bottom:-2px;
    width:100%;
    height:1px;
    background: linear-gradient(90deg, var(--highlight-color), var(--highlight-color-alt));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform .35s ease;
}
.summary-content :deep(a:hover:after) { transform: scaleX(1); }

.summary-content :deep(blockquote) {
    margin: 1.25rem 0;
    padding: 1rem 1.25rem 1rem 1.15rem;
    border-left: 4px solid var(--highlight-color);
    background: linear-gradient(120deg, rgba(13,148,136,.12), rgba(13,148,136,.04));
    border-radius: .85rem;
    font-style: italic;
    color: rgba(248,250,252,.95);
    box-shadow: 0 4px 14px -6px rgba(0,0,0,.7);
}

.summary-content :deep(b),
.summary-content :deep(strong) {
    color: #f0fdfa;
    font-weight: 600;
    text-shadow: 0 0 8px rgba(13,148,136,.35);
}

/* ============ Footer ============ */
.modal-footer {
    padding: 1.25rem 1.75rem 1.75rem;
    display: flex;
    justify-content: flex-end;
    gap: .75rem;
    background: linear-gradient(180deg, rgba(13,148,136,.08), rgba(13,148,136,.03));
    border-top: 1px solid rgba(13,148,136,.25);
    position: relative;
}
.modal-footer:before {
    content:"";
    position:absolute;
    inset:0;
    background:
        linear-gradient(90deg, rgba(13,148,136,.15), transparent 40%, transparent 60%, rgba(13,148,136,.15));
    opacity:.25;
    pointer-events:none;
}

/* ============ Buttons ============ */
.button-primary {
    position: relative;
    border: 1px solid rgba(13,148,136,.45);
    font-weight: 600;
    letter-spacing: .4px;
    padding: .85rem 1.55rem;
    font-size: .95rem;
    border-radius: .95rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    box-shadow:
        0 10px 24px -10px rgba(0,0,0,.75),
        0 4px 18px -6px rgba(13,148,136,.55),
        0 0 0 1px rgba(13,148,136,.4),
        inset 0 0 0 1px rgba(255,255,255,.15);
    transition: transform .25s cubic-bezier(.22,.99,.45,1), box-shadow .35s ease, filter .4s ease;
}
.button-primary:before {
    position:absolute;
    inset:0;
    border-radius: inherit;
    mix-blend-mode: overlay;
    opacity: 0;
    transition: opacity .5s ease;
}
.button-primary:hover {
    transform: translateY(-4px);
    box-shadow:
        0 18px 40px -18px rgba(0,0,0,.85),
        0 6px 26px -10px rgba(13,148,136,.65),
        0 0 0 1px rgba(13,148,136,.55);
}
.button-primary:hover:before { opacity: 1; }
.button-primary:active {
    transform: translateY(-1px);
    transition: transform .15s ease;
}
.button-primary:focus-visible {
    outline: 3px solid var(--highlight-color);
    outline-offset: 3px;
}

/* ============ Responsive Tweaks ============ */
@media (max-width: 640px) {
    .modal-header { padding: 1.2rem 1.25rem 1rem; }
    .modal-body { padding: 0 1.25rem 1.25rem; }
    .modal-footer { padding: 1rem 1.25rem 1.25rem; }
    .modal-title { font-size: 1.3rem; }
    .modal-container { margin-top: 3.5rem; }
}

/* ============ Reduced Motion ============ */
@media (prefers-reduced-motion: reduce) {
    .modal-fade-enter-active,
    .modal-fade-leave-active { transition: none; }
    .button-primary,
    .close-button,
    .summary-content :deep(ul li) { transition: none; }
}
@keyframes backdrop-fade {
    from { opacity: 0; }
    to { opacity: 1; }
}
</style>
