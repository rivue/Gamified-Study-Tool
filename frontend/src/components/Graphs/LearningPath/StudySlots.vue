<template>
    <div class="study-slots-page" :class="pageStateClass">
        <div class="slots-container">
            <header class="slots-header">
                <router-link :to="`/lessons/${libraryIdParam}`" class="back-link">
                    <ArrowLeftCircle class="icon" />
                    <span>Back to learning path</span>
                </router-link>
                <button class="music-toggle" @click="toggleMusic" :aria-pressed="!musicEnabled" aria-label="Toggle study music">
                    <component :is="musicEnabled ? Volume2 : VolumeX" class="icon" />
                    <span>{{ musicEnabled ? 'Music on' : 'Music muted' }}</span>
                </button>
            </header>

            <div class="slots-intro">
                <h1>Study Slots</h1>
                <p>Spin the reels to let chance decide your next deep-focus session and break reward.</p>
            </div>

            <section class="machine-shell" :class="machineStateClass">
                <div class="light-bar">
                    <span v-for="(_, index) in lights" :key="index"
                        :class="['bulb', bulbClass, { 'bulb-jackpot': matchType === 'three', 'bulb-win': matchType === 'two' }]"
                        :style="{ animationDelay: `${index * 0.08}s` }"></span>
                </div>

                <div class="reels-row">
                    <div v-for="(value, index) in displayedReels" :key="index"
                        :class="['reel-window', { highlight: matchIndices.includes(index) }]">
                        <span class="reel-text">{{ value || '—' }}</span>
                    </div>
                </div>
            </section>

            <div class="control-panel">
                <button class="primary" @click="spin" :disabled="!canSpin">
                    <span v-if="isSpinning">Spinning...</span>
                    <span v-else>Spin</span>
                </button>
                <button class="secondary" @click="startSession" :disabled="!isReadyToStart">
                    <Play class="icon" />
                    <span>Start session</span>
                </button>
                <button class="ghost" @click="resetGame">
                    <RotateCcw class="icon" />
                    <span>Reset</span>
                </button>
            </div>

            <p v-if="spinMessage" class="status-text">{{ spinMessage }}</p>
            <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
            <p v-if="loading" class="status-text">Loading classes...</p>
            <div v-else-if="noClassesAvailable" class="empty-state">
                <p>Add lessons to this course to unlock Study Slots.</p>
            </div>

            <section v-if="lastOutcome" class="outcome-card">
                <h2>Your next mission</h2>
                <p>
                    Focus on <strong>{{ lastOutcome.focusClass }}</strong> for
                    <strong>{{ lastOutcome.sessionMinutes }} minutes</strong> and reward yourself with a
                    <strong>{{ lastOutcome.breakMinutes }} minute</strong> break.
                </p>
                <div class="results-row">
                    <div v-for="(value, index) in lastOutcome.results" :key="`result-${index}`"
                        :class="['result-pill', { match: matchIndices.includes(index) }]">
                        {{ value }}
                    </div>
                </div>
            </section>

            <section v-if="lastOutcome" class="timer-card">
                <div class="timer-header">
                    <h2>{{ timerLabel }}</h2>
                    <span v-if="timerMode === 'session'" class="timer-tag">Deep focus</span>
                    <span v-else-if="timerMode === 'break'" class="timer-tag">Recharge</span>
                </div>
                <div class="timer-display">{{ formattedRemaining }}</div>
                <div class="progress-track">
                    <div class="progress-bar" :style="{ width: `${sessionProgress}%` }"></div>
                </div>
                <p class="timer-subtext" v-if="timerMode === 'session'">
                    {{ musicEnabled ? 'Background study music is playing.' : 'Music is muted — enable it to set the mood.' }}
                </p>
                <p class="timer-subtext" v-else-if="timerMode === 'break'">
                    Stretch, hydrate, and celebrate the win before the next spin.
                </p>
                <p class="timer-subtext" v-else-if="timerMode === 'complete'">
                    Session complete! Spin again when you are ready for another challenge.
                </p>
            </section>

            <section class="rules-card">
                <h2>How it works</h2>
                <ul>
                    <li><span>🎰</span> Tap <strong>Spin</strong> to shuffle three reels filled with your classes.</li>
                    <li><span>🏆</span> <strong>3 of a kind</strong> → 60-minute focus session + 60-minute break.</li>
                    <li><span>🔥</span> <strong>2 of a kind</strong> → 45-minute focus session + 15-minute break.</li>
                    <li><span>✨</span> <strong>All different</strong> → 20-minute focus session + 5-minute break.</li>
                    <li><span>��</span> Keep the study music on for an immersive session, then enjoy the timed break.</li>
                </ul>
            </section>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { ArrowLeftCircle, Play, RotateCcw, Volume2, VolumeX } from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();

const classes = ref<string[]>([]);
const displayedReels = ref<string[]>(['—', '—', '—']);
const isSpinning = ref(false);
const spinMessage = ref('Spin the reels to plan your next study mission.');
const errorMessage = ref('');
const loading = ref(true);
const hasSpun = ref(false);
const matchType = ref<'three' | 'two' | 'one' | null>(null);
const matchIndices = ref<number[]>([]);
const lastOutcome = ref<{ results: string[]; focusClass: string; sessionMinutes: number; breakMinutes: number } | null>(null);
const focusClass = ref('');
const timerMode = ref<'idle' | 'ready' | 'session' | 'break' | 'complete'>('idle');
const remainingTime = ref(0);
const musicEnabled = ref(true);

const lights = computed(() => Array.from({ length: 18 }));
const libraryIdParam = computed(() => route.params.libraryId ?? route.params.id);

const noClassesAvailable = computed(() => !loading.value && classes.value.length === 0);
const canSpin = computed(() => !isSpinning.value && classes.value.length > 0 && timerMode.value !== 'session' && timerMode.value !== 'break');
const isReadyToStart = computed(() => lastOutcome.value !== null && (timerMode.value === 'ready' || timerMode.value === 'complete'));
const timerLabel = computed(() => {
    switch (timerMode.value) {
        case 'session':
            return `Study Session · ${focusClass.value}`;
        case 'break':
            return 'Break Time';
        case 'complete':
            return 'Ready for the next spin';
        case 'ready':
            return 'Session ready';
        default:
            return 'Timer';
    }
});
const formattedRemaining = computed(() => formatTime(remainingTime.value));
const sessionDurationSeconds = computed(() => lastOutcome.value ? lastOutcome.value.sessionMinutes * 60 : 0);
const breakDurationSeconds = computed(() => lastOutcome.value ? lastOutcome.value.breakMinutes * 60 : 0);
const sessionProgress = computed(() => {
    if (timerMode.value === 'session' && sessionDurationSeconds.value) {
        const elapsed = sessionDurationSeconds.value - remainingTime.value;
        return Math.min(100, Math.max(0, Math.round((elapsed / sessionDurationSeconds.value) * 100)));
    }
    if (timerMode.value === 'break' && breakDurationSeconds.value) {
        const elapsed = breakDurationSeconds.value - remainingTime.value;
        return Math.min(100, Math.max(0, Math.round((elapsed / breakDurationSeconds.value) * 100)));
    }
    return timerMode.value === 'complete' ? 100 : 0;
});
const pageStateClass = computed(() => ({
    win: matchType.value === 'two',
    jackpot: matchType.value === 'three'
}));
const machineStateClass = computed(() => ({
    win: matchType.value === 'two',
    jackpot: matchType.value === 'three'
}));
const bulbClass = computed(() => ({
    active: matchType.value !== null
}));

let reelIntervals: Array<ReturnType<typeof setInterval> | null> = [null, null, null];
let reelTimeouts: ReturnType<typeof setTimeout>[] = [];
let timerInterval: ReturnType<typeof setInterval> | null = null;
let studyMusic: HTMLAudioElement | null = null;

const formatTime = (totalSeconds: number) => {
    const clamped = Math.max(totalSeconds, 0);
    const minutes = Math.floor(clamped / 60).toString().padStart(2, '0');
    const seconds = Math.floor(clamped % 60).toString().padStart(2, '0');
    return `${minutes}:${seconds}`;
};

const fetchClasses = async () => {
    loading.value = true;
    errorMessage.value = '';
    try {
        const id = libraryIdParam.value;
        if (!id) {
            throw new Error('Missing library id');
        }
        const response = await axios.get(`/api/library/${id}`);
        if (response.data?.status !== 'success') {
            throw new Error('Unable to load classes for this library.');
        }
        const rawRooms = response.data?.data?.room_names ?? [];
        const parsed = rawRooms
            .map((room: unknown) => Array.isArray(room) ? room[0] : room)
            .filter((name: unknown): name is string => typeof name === 'string' && name.trim().length > 0);
        classes.value = parsed;
        if (parsed.length > 0) {
            setInitialReels();
        } else {
            displayedReels.value = ['—', '—', '—'];
        }
    } catch (error) {
        console.error('Failed to load classes for Study Slots:', error);
        errorMessage.value = 'Unable to load classes. Please try again later.';
    } finally {
        loading.value = false;
    }
};

const setInitialReels = () => {
    if (hasSpun.value) {
        return;
    }
    if (classes.value.length >= 3) {
        displayedReels.value = classes.value.slice(0, 3);
    } else if (classes.value.length > 0) {
        displayedReels.value = Array.from({ length: 3 }, (_, index) => classes.value[index % classes.value.length]);
    } else {
        displayedReels.value = ['—', '—', '—'];
    }
};

const clearReelAnimations = () => {
    reelIntervals.forEach(interval => interval && clearInterval(interval));
    reelIntervals = [null, null, null];
    reelTimeouts.forEach(timeout => clearTimeout(timeout));
    reelTimeouts = [];
};

const clearTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
};

const stopMusic = () => {
    if (studyMusic) {
        studyMusic.pause();
        studyMusic.currentTime = 0;
    }
};

const playMusic = () => {
    if (!musicEnabled.value || !studyMusic) {
        return;
    }
    const playPromise = studyMusic.play();
    if (playPromise) {
        playPromise.catch((error) => {
            console.warn('Unable to start audio playback:', error);
        });
    }
};

const toggleMusic = () => {
    musicEnabled.value = !musicEnabled.value;
    if (!musicEnabled.value) {
        if (studyMusic) {
            studyMusic.pause();
        }
    } else if (timerMode.value === 'session') {
        playMusic();
    }
};

const spin = () => {
    if (!canSpin.value) {
        return;
    }
    spinMessage.value = 'Spinning...';
    isSpinning.value = true;
    hasSpun.value = true;
    matchType.value = null;
    matchIndices.value = [];
    lastOutcome.value = null;
    focusClass.value = '';
    timerMode.value = 'idle';
    remainingTime.value = 0;
    clearTimer();
    stopMusic();
    clearReelAnimations();

    const finalResults: string[] = [];
    const durations = [1500, 1900, 2300];
    const speeds = [70, 90, 110];

    durations.forEach((duration, index) => {
        reelIntervals[index] = setInterval(() => {
            const randomClass = classes.value[Math.floor(Math.random() * classes.value.length)];
            displayedReels.value[index] = randomClass;
        }, speeds[index]);

        const timeout = setTimeout(() => {
            if (reelIntervals[index]) {
                clearInterval(reelIntervals[index]!);
                reelIntervals[index] = null;
            }
            const result = classes.value[Math.floor(Math.random() * classes.value.length)];
            displayedReels.value[index] = result;
            finalResults[index] = result;
            if (finalResults.filter(Boolean).length === 3) {
                finishSpin(finalResults);
            }
        }, duration);
        reelTimeouts.push(timeout);
    });
};

const finishSpin = (results: string[]) => {
    isSpinning.value = false;
    evaluateSpin([...results]);
};

const evaluateSpin = (results: string[]) => {
    const [first, second, third] = results;
    let outcomeType: 'three' | 'two' | 'one' = 'one';
    let focus = first;
    let session = 20;
    let breakLength = 5;
    const indices: number[] = [0];

    if (first === second && second === third) {
        outcomeType = 'three';
        session = 60;
        breakLength = 60;
        indices.splice(0, indices.length, 0, 1, 2);
        spinMessage.value = `Jackpot! ${first} takes the spotlight for a 60-minute sprint, then unwind for an hour.`;
    } else if (first === second || first === third || second === third) {
        outcomeType = 'two';
        session = 45;
        breakLength = 15;
        if (first === second || first === third) {
            focus = first;
        } else {
            focus = second;
        }
        indices.splice(0, indices.length);
        results.forEach((value, index) => {
            if (value === focus) {
                indices.push(index);
            }
        });
        spinMessage.value = `Nice match! ${focus} gets 45 minutes of focus time, followed by a 15-minute break.`;
    } else {
        outcomeType = 'one';
        focus = first;
        indices.splice(0, indices.length, 0);
        spinMessage.value = `Fresh challenge! Start with ${focus} for 20 minutes and reward yourself with a 5-minute break.`;
    }

    matchType.value = outcomeType;
    matchIndices.value = indices;
    focusClass.value = focus;
    lastOutcome.value = {
        results,
        focusClass: focus,
        sessionMinutes: session,
        breakMinutes: breakLength
    };
    remainingTime.value = session * 60;
    timerMode.value = 'ready';
};

const startSession = () => {
    if (!lastOutcome.value || !isReadyToStart.value) {
        return;
    }
    timerMode.value = 'session';
    remainingTime.value = lastOutcome.value.sessionMinutes * 60;
    playMusic();
    runTimer(() => {
        stopMusic();
        if (lastOutcome.value && lastOutcome.value.breakMinutes > 0) {
            timerMode.value = 'break';
            remainingTime.value = lastOutcome.value.breakMinutes * 60;
            runTimer(() => {
                timerMode.value = 'complete';
            });
        } else {
            timerMode.value = 'complete';
        }
    });
};

const runTimer = (onComplete?: () => void) => {
    clearTimer();
    timerInterval = setInterval(() => {
        if (remainingTime.value > 0) {
            remainingTime.value -= 1;
        } else {
            clearTimer();
            onComplete?.();
        }
    }, 1000);
};

const resetGame = () => {
    clearTimer();
    stopMusic();
    clearReelAnimations();
    isSpinning.value = false;
    hasSpun.value = false;
    matchType.value = null;
    matchIndices.value = [];
    lastOutcome.value = null;
    focusClass.value = '';
    timerMode.value = 'idle';
    remainingTime.value = 0;
    spinMessage.value = 'Spin the reels to plan your next study mission.';
    setInitialReels();
};

watch(classes, () => {
    if (!hasSpun.value) {
        setInitialReels();
    }
});

watch(libraryIdParam, () => {
    resetGame();
    fetchClasses();
});

const initAudio = () => {
    if (!studyMusic) {
        studyMusic = new Audio('https://cdn.pixabay.com/download/audio/2022/03/31/audio_3f3301f3db.mp3?filename=deep-meditation-140602.mp3');
        studyMusic.loop = true;
        studyMusic.volume = 0.25;
    }
};

const navigateBackIfMissing = () => {
    if (!libraryIdParam.value) {
        router.push('/courses');
    }
};

onMounted(() => {
    initAudio();
    navigateBackIfMissing();
    fetchClasses();
});

onUnmounted(() => {
    clearTimer();
    clearReelAnimations();
    stopMusic();
});
</script>

<style scoped>
.study-slots-page {
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    background: radial-gradient(circle at top, rgba(99, 102, 241, 0.35), rgba(15, 23, 42, 0.95));
    color: var(--light-text, #f8fafc);
}

.study-slots-page.win .slots-container,
.study-slots-page.jackpot .slots-container {
    box-shadow: 0 0 40px rgba(250, 204, 21, 0.35);
}

.slots-container {
    width: 100%;
    max-width: 960px;
    background: rgba(15, 23, 42, 0.8);
    border-radius: 24px;
    padding: 2.5rem;
    position: relative;
    border: 1px solid rgba(148, 163, 184, 0.2);
    backdrop-filter: blur(12px);
}

.slots-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1rem;
    border-radius: 999px;
    background: rgba(148, 163, 184, 0.18);
    color: inherit;
    text-decoration: none;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.back-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(30, 64, 175, 0.35);
}

.music-toggle {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.6rem 1rem;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.3);
    background: rgba(15, 23, 42, 0.6);
    color: inherit;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.2s ease;
}

.music-toggle:hover {
    background: rgba(148, 163, 184, 0.2);
    transform: translateY(-1px);
}

.icon {
    width: 1.25rem;
    height: 1.25rem;
}

.slots-intro {
    text-align: center;
    margin: 2rem 0 2.5rem;
}

.slots-intro h1 {
    font-size: 2.75rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.slots-intro p {
    color: rgba(226, 232, 240, 0.75);
    font-size: 1.05rem;
}

.machine-shell {
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(17, 24, 39, 0.9));
    border-radius: 28px;
    padding: 1.8rem 1.5rem 2.4rem;
    border: 2px solid rgba(59, 130, 246, 0.35);
    box-shadow: inset 0 0 10px rgba(15, 23, 42, 0.9);
    position: relative;
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.machine-shell.win {
    box-shadow: 0 0 30px rgba(250, 204, 21, 0.4);
}

.machine-shell.jackpot {
    box-shadow: 0 0 45px rgba(248, 113, 113, 0.45);
    transform: translateY(-2px);
}

.light-bar {
    display: grid;
    grid-template-columns: repeat(18, 1fr);
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.bulb {
    width: 0.9rem;
    height: 0.9rem;
    border-radius: 50%;
    background: rgba(148, 163, 184, 0.3);
    box-shadow: 0 0 6px rgba(148, 163, 184, 0.25);
    opacity: 0.7;
}

.bulb-win {
    background: #facc15;
    box-shadow: 0 0 12px rgba(250, 204, 21, 0.8);
    animation: blink 0.9s infinite alternate;
}

.bulb-jackpot {
    background: #f97316;
    box-shadow: 0 0 16px rgba(248, 113, 113, 0.85);
    animation: blink-fast 0.45s infinite alternate;
}

.reels-row {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
}

.reel-window {
    width: 180px;
    height: 170px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(148, 163, 184, 0.12), rgba(148, 163, 184, 0.08));
    border: 2px solid rgba(148, 163, 184, 0.35);
    box-shadow: inset 0 15px 30px rgba(15, 23, 42, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1rem;
    transition: transform 0.25s ease, border-color 0.25s ease;
    font-size: 1.2rem;
    font-weight: 600;
    text-transform: capitalize;
}

.reel-window.highlight {
    transform: translateY(-6px) scale(1.03);
    border-color: rgba(250, 204, 21, 0.8);
    box-shadow: 0 12px 30px rgba(250, 204, 21, 0.35);
}

.reel-text {
    line-height: 1.3;
}

.control-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
    margin: 2.5rem 0 1.5rem;
}

.control-panel button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    padding: 0.9rem 2.2rem;
    border-radius: 18px;
    font-weight: 600;
    font-size: 1rem;
    border: none;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
}

.control-panel button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.control-panel .primary {
    background: linear-gradient(135deg, #38bdf8, #6366f1);
    color: white;
    box-shadow: 0 12px 25px rgba(99, 102, 241, 0.4);
}

.control-panel .primary:not(:disabled):hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 35px rgba(14, 165, 233, 0.45);
}

.control-panel .secondary {
    background: rgba(59, 130, 246, 0.18);
    color: #e0e7ff;
    border: 1px solid rgba(99, 102, 241, 0.35);
}

.control-panel .secondary:not(:disabled):hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 32px rgba(99, 102, 241, 0.3);
}

.control-panel .ghost {
    background: rgba(15, 23, 42, 0.4);
    color: rgba(226, 232, 240, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.35);
}

.control-panel .ghost:hover {
    transform: translateY(-2px);
}

.status-text {
    text-align: center;
    color: rgba(226, 232, 240, 0.8);
    margin-bottom: 0.5rem;
}

.error-text {
    text-align: center;
    color: #fca5a5;
    margin-bottom: 0.5rem;
}

.empty-state {
    text-align: center;
    margin-bottom: 1.5rem;
    color: rgba(226, 232, 240, 0.75);
}

.outcome-card,
.timer-card,
.rules-card {
    background: rgba(15, 23, 42, 0.65);
    border-radius: 22px;
    padding: 1.8rem;
    margin-top: 1.8rem;
    border: 1px solid rgba(99, 102, 241, 0.18);
}

.outcome-card h2,
.timer-card h2,
.rules-card h2 {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 0.6rem;
}

.outcome-card p {
    color: rgba(226, 232, 240, 0.85);
    margin-bottom: 1rem;
}

.results-row {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
}

.result-pill {
    background: rgba(99, 102, 241, 0.25);
    color: #e0e7ff;
    padding: 0.6rem 1.1rem;
    border-radius: 999px;
    text-transform: capitalize;
    font-weight: 600;
}

.result-pill.match {
    background: linear-gradient(135deg, #facc15, #f97316);
    color: #1f2937;
}

.timer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

.timer-tag {
    font-size: 0.85rem;
    font-weight: 600;
    background: rgba(16, 185, 129, 0.2);
    color: #6ee7b7;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
}

.timer-display {
    font-size: 2.75rem;
    font-weight: 700;
    text-align: center;
    margin: 1rem 0;
}

.progress-track {
    width: 100%;
    height: 10px;
    background: rgba(148, 163, 184, 0.2);
    border-radius: 999px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(135deg, #38bdf8, #6366f1);
    transition: width 0.3s ease;
}

.timer-subtext {
    margin-top: 1rem;
    color: rgba(226, 232, 240, 0.75);
    text-align: center;
}

.rules-card ul {
    display: grid;
    gap: 0.8rem;
    margin-top: 1rem;
}

.rules-card li {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: rgba(226, 232, 240, 0.85);
}

.rules-card li span {
    font-size: 1.2rem;
}

@keyframes blink {
    from {
        opacity: 0.5;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1.1);
    }
}

@keyframes blink-fast {
    from {
        opacity: 0.4;
        transform: scale(0.92);
    }
    to {
        opacity: 1;
        transform: scale(1.15);
    }
}

@media (max-width: 900px) {
    .reels-row {
        gap: 1rem;
    }

    .reel-window {
        width: 150px;
        height: 150px;
    }
}

@media (max-width: 640px) {
    .study-slots-page {
        padding: 1.2rem;
    }

    .slots-container {
        padding: 1.8rem 1.4rem;
    }

    .reels-row {
        flex-direction: column;
        align-items: center;
    }

    .reel-window {
        width: 80%;
        max-width: 280px;
    }

    .control-panel {
        flex-direction: column;
    }

    .control-panel button {
        width: 100%;
    }
}
</style>
