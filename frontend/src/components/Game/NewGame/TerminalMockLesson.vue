<template>
  <!-- <div class="terminal-page"> -->
    <!-- <header class="terminal-header">
      <button class="back-button" @click="goBack">
        <ArrowLeftIcon class="w-5 h-5" />
        <span>Back to Learning Path</span>
      </button>
      <h1 class="title">Terminal Coding Lesson (Mock)</h1>
    </header> -->

    <!-- <main class="terminal-content">
      <section class="lesson-card">
        <h2 class="lesson-title">Goal</h2>
        <p class="lesson-text">
          Write a simple CLI that echoes input with a line number prefix. No backend required. Complete the tasks below in the mock terminal.
        </p>
      </section>

      <section class="lesson-grid">
        <div class="editor-card">
          <div class="card-header">
            <h3>editor.js</h3>
            <button class="save-btn" @click="saveCode" :disabled="saving">
              <span v-if="saving" class="spinner"></span>
              <span v-else>Save</span>
            </button>
          </div>
          <textarea v-model="code" class="code-editor" spellcheck="false"></textarea>
          <div class="hint">
            Hint: The program should read lines from stdin and print them as "1: text", "2: text", etc.
          </div>
        </div>

        <div class="terminal-card">
          <div class="card-header">
            <h3>Mock Terminal</h3>
            <div class="terminal-actions">
              <button class="run-btn" @click="runCommand">Run</button>
              <button class="clear-btn" @click="clearOutput">Clear</button>
            </div>
          </div>
          <div class="terminal-input">
            <span class="prompt">$</span>
            <input v-model="command" @keyup.enter="runCommand" placeholder="node editor.js (then type input)" />
          </div>
          <div class="io-row">
            <textarea v-model="stdin" class="stdin" placeholder="Type input lines here..."></textarea>
            <pre class="stdout"><code>{{ output }}</code></pre>
          </div>
        </div>

        <div class="tests-card">
          <div class="card-header">
            <h3>Checks</h3>
            <button class="run-tests-btn" @click="runTests">Run Checks</button>
          </div>
          <ul class="tests">
            <li v-for="t in tests" :key="t.id" :class="['test', t.status]">
              <span class="dot"></span>
              <span class="name">{{ t.name }}</span>
              <span class="status-text">{{ t.status.toUpperCase() }}</span>
            </li>
          </ul>
        </div>
      </section>
    </main> -->
  <!-- </div> -->
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ArrowLeftIcon } from '@heroicons/vue/24/outline';

const router = useRouter();
const route = useRoute();

const code = ref(`// Echo each input line with a line number prefix
// Example: input: hello\nworld -> output: "1: hello" and "2: world"

function main(input) {
  const lines = input.split(/\r?\n/).filter(Boolean);
  return lines.map((line, idx) => `${idx + 1}: ${line}`).join('\n');
}

// Export for testing
export { main };
`);

const stdin = ref('hello\nworld');
const command = ref('node editor.js');
const output = ref('');
const saving = ref(false);

type TestCase = { id: number; name: string; status: 'pending'|'pass'|'fail' };
const tests = ref<TestCase[]>([
  { id: 1, name: 'Prefixes each line with index', status: 'pending' },
  { id: 2, name: 'Handles empty input gracefully', status: 'pending' },
  { id: 3, name: 'Works with single-line input', status: 'pending' },
]);

function goBack() {
  router.push(`/lessons/${route.params.id}`);
}

function saveCode() {
  saving.value = true;
  setTimeout(() => { saving.value = false; }, 400);
}

function clearOutput() {
  output.value = '';
}

function runCommand() {
  // Mock executor: supports a single command
  const trimmed = command.value.trim();
  if (trimmed !== 'node editor.js') {
    output.value = `bash: ${trimmed}: command not found`;
    return;
  }
  try {
    // Very naive evaluator to "execute" exported main(input)
    const fn = extractMainFunction(code.value);
    output.value = fn(stdin.value || '');
  } catch (e: any) {
    output.value = `Runtime Error: ${e?.message || String(e)}`;
  }
}

function extractMainFunction(source: string): (input: string) => string {
  // Parse out function main(input) { ... } and return as callable via new Function
  const match = source.match(/function\s+main\s*\(\s*input\s*\)\s*{([\s\S]*?)}\s*/);
  if (!match) throw new Error('No main(input) function found.');
  const body = match[1];
  // eslint-disable-next-line no-new-func
  const fn = new Function('input', body + '\n;return typeof result!==\'undefined\'?result:undefined;');
  // Wrap to capture last expression as return if needed via simple heuristic
  return (input: string) => {
    // Attempt to run body within a minimal scope
    try {
      // Provide common helpers
      const lines = (s: string) => s.split(/\r?\n/);
      // Evaluate, but ensure last statement returns
      const res = fn.call({ lines }, input);
      // Fallback: if function sets a variable output via return in body code
      if (typeof res === 'string') return res;
      // Try re-executing by compiling a proper function wrapper (safer path)
      // eslint-disable-next-line no-new-func
      const proper = new Function('input', `function __main(input){${body}}; return __main(input);`);
      return String(proper(input) ?? '');
    } catch (e) {
      throw e;
    }
  };
}

function runTests() {
  tests.value = tests.value.map(t => ({ ...t, status: 'pending' }));
  try {
    const fn = extractMainFunction(code.value);
    const results: Array<'pass'|'fail'> = [];
    // Test 1
    const out1 = fn('a\nb');
    results.push(out1.trim() === '1: a\n2: b' ? 'pass' : 'fail');
    // Test 2
    const out2 = fn('');
    results.push(out2.trim() === '' ? 'pass' : 'fail');
    // Test 3
    const out3 = fn('xyz');
    results.push(out3.trim() === '1: xyz' ? 'pass' : 'fail');
    tests.value = tests.value.map((t, i) => ({ ...t, status: results[i] }));
  } catch (e) {
    tests.value = tests.value.map(t => ({ ...t, status: 'fail' }));
  }
}
</script>

<style scoped>
.terminal-page { padding: 1.5rem; color: var(--light-text); background: var(--background-color); min-height: 100vh; }
.terminal-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.back-button { display: inline-flex; gap: .5rem; align-items: center; padding: .5rem .75rem; border-radius: .5rem; background: var(--background-color-1t); border: 1px solid var(--color-primary-dark); color: var(--highlight-color); }
.title { font-size: 1.5rem; font-weight: 600; }
.terminal-content { max-width: 1200px; margin: 0 auto; display: grid; gap: 1rem; }
.lesson-card { background: var(--background-color-1t); border: 1px solid var(--color-primary-dark); border-radius: .75rem; padding: 1rem; }
.lesson-title { font-weight: 600; margin-bottom: .25rem; }
.lesson-text { opacity: .9; }
.lesson-grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
@media (min-width: 1024px) { .lesson-grid { grid-template-columns: 1.1fr 1fr; grid-auto-rows: minmax(200px, auto); } }
.editor-card, .terminal-card, .tests-card { background: var(--background-color-1t); border: 1px solid var(--color-primary-dark); border-radius: .75rem; padding: .75rem; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: .5rem; }
.save-btn, .run-btn, .clear-btn, .run-tests-btn { padding: .35rem .6rem; border-radius: .5rem; border: 1px solid var(--color-primary-dark); background: var(--element-color-1); color: var(--light-text); }
.spinner { width: 1rem; height: 1rem; border-radius: 9999px; border: 2px solid #fff; border-right-color: transparent; display: inline-block; animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.code-editor { width: 100%; height: 260px; background: #0b1020; color: #e0eaff; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; resize: vertical; border-radius: .5rem; padding: .75rem; border: 1px solid var(--color-primary-dark); }
.hint { margin-top: .5rem; font-size: .875rem; opacity: .8; }
.terminal-input { display: flex; align-items: center; gap: .5rem; margin-bottom: .5rem; }
.prompt { color: #9cdcfe; }
.terminal-input input { flex: 1; padding: .4rem .5rem; background: #0f1629; color: #e0eaff; border: 1px solid var(--color-primary-dark); border-radius: .5rem; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; }
.io-row { display: grid; grid-template-columns: 1fr; gap: .5rem; }
@media (min-width: 1024px) { .io-row { grid-template-columns: 1fr 1fr; } }
.stdin { width: 100%; min-height: 200px; background: #0f1629; color: #e0eaff; border: 1px solid var(--color-primary-dark); border-radius: .5rem; padding: .5rem; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; }
.stdout { width: 100%; min-height: 200px; background: #0b1020; color: #9fef00; border: 1px solid var(--color-primary-dark); border-radius: .5rem; padding: .5rem; overflow: auto; }
.tests { list-style: none; padding: 0; margin: 0; display: grid; gap: .35rem; }
.test { display: flex; align-items: center; gap: .5rem; padding: .4rem .5rem; border-radius: .5rem; border: 1px solid var(--color-primary-dark); }
.test .dot { width: .6rem; height: .6rem; border-radius: 9999px; background: gray; }
.test .name { flex: 1; }
.test.pending .dot { background: #a8a8a8; }
.test.pass .dot { background: #22c55e; }
.test.fail .dot { background: #ef4444; }
.test .status-text { font-size: .75rem; opacity: .9; }
</style>
