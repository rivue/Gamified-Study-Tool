<template>

    <div class="fixed left-8 right-8 top-0 bottom-0 overflow-hidden">
        <div class="fixed top-20 right-6 flex gap-6 z-10">

            <button v-if="isOwner" @click="toggleEditMode"
                class="menu-button bg-background-color-1t backdrop-blur-sm shadow-lg rounded-lg p-4 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200"
                style="color: var(--highlight-color);">
                <PencilIcon class="w-6 h-6" />
            </button>

            <button @click="goToLeaderboard"
                class="menu-button bg-background-color-1t backdrop-blur-sm shadow-md rounded-lg p-4 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200"
                style="color: var(--highlight-color);">
                <ChartBarIcon class="w-6 h-6" />
            </button>

            <button v-if="isOwner" @click="toggleSettings"
                class="menu-button bg-background-color-1t backdrop-blur-sm shadow-md rounded-lg p-4 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200"
                style="color: var(--highlight-color);">
                <CogIcon class="w-6 h-6" />
            </button>
        </div>

        <div class="fixed top-20 left-6 flex gap-6 z-10">
            <button @click="goToHome" 
                class="menu-button bg-background-color-1t backdrop-blur-sm shadow-md rounded-lg px-6 py-4 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200 font-medium"
                style="color: var(--highlight-color);">
                <span class="text-lg">My Courses</span>
            </button>

            <button v-if="!isOwner" @click="handleLeaveCourseClick"
                class="menu-button bg-background-color-1t backdrop-blur-sm shadow-md rounded-lg p-4 hover:bg-element-color-1 hover:transform hover:translate-y-[-2px] border border-color-primary-dark transition-all duration-200"
                style="color: var(--highlight-color);">
                <ArrowLeftOnRectangleIcon class="w-6 h-6" />
            </button>
        </div>

        <div class="relative flex flex-col w-full h-full">

            <div ref="scrollContainer"
                class="scrollContainer flex-1 overflow-x-auto overflow-y-hidden cursor-grab active:cursor-grabbing"
                @mousedown="startDragging" @mousemove="drag" @mouseup="stopDragging" @mouseleave="stopDragging"
                @touchstart="startDragging" @touchmove="drag" @touchend="stopDragging" @scroll="handleScroll">
                <div class="flex items-center gap-24 min-h-screen py-24 relative">

                    <!-- Left padding so first node is visible -->
                    <div class="w-24 flex-shrink-0"></div>

                    <!-- Add Unit at the beginning -->
                    <AddUnit v-if="editModeEnabled" :library-id="libraryId" :position="0"
                        :existing-units="Object.keys(rawUnitData)" :can-add-unit="isOwner"
                        @unit-added="handleUnitAdded" />

                    <!-- Unit Headers -->
                    <template v-for="([unit], unitName, unitIndex) in rawUnitData" :key="unitIndex">
                        <div class="relative -mx-12 my-12 px-16 pt-40 pb-36 border-t-2 border-b-2 flex-shrink-0"
                            :class="['unit-box', { 'unit--first': unitIndex === 0, 'unit--last': unitIndex === Object.keys(rawUnitData).length - 1 }]"
                            :style="{
                                borderColor: getUnitColor(unitIndex),
                                backgroundColor: 'var(--background-color-1t)',
                            }">


                            <!-- Unit name header -->
                            <div class="absolute -top-5 left-1/2 transform -translate-x-1/2 px-6 py-2 rounded-lg font-bold text-xl whitespace-nowrap shadow-md"
                                :style="{ backgroundColor: getUnitColor(unitIndex), color: 'var(--light-text)' }">
                                {{ unitName }}
                            </div>

                            <!-- Sections container -->
                            <div class="flex items-center">
                                <template v-if="rawUnitData[unitName].length > 0"
                                    v-for="([sectionId, sectionName], sectionIndex) in rawUnitData[unitName]"
                                    :key="sectionIndex">

                                    <AddSection v-if="editModeEnabled && isOwner" class="-mx-8" :library-id="libraryId"
                                        :unit-id="props.unitPositionMap[unitName][1]" :position="sectionIndex"
                                        :offset="getNodeOffset(getGlobalSectionIndex(unitIndex, sectionIndex) - .6)"
                                        :unit-color="getUnitColor(unitIndex)" @nodes-added="onSectionAdd" />

                                    <div class="relative flex-shrink-0 mx-12" :style="{
                                        transform: `translateY(${getNodeOffset(getGlobalSectionIndex(unitIndex, sectionIndex))}px)`,
                                    }"
                                        @click="editModeEnabled ? handleEditNodeClick() : handleNodeClick(sectionId)">



                                        <DeleteSection v-if="editModeEnabled && isOwner" :section-id="sectionId"
                                            :section-name="sectionName" />

                                        <!-- Tooltip -->
                                        <div v-if="selectedRoomId && selectedRoomId === sectionId"
                                            class="absolute -top-32 left-1/2 -translate-x-1/2 w-64 z-50"
                                            @mouseenter.stop @mouseover.stop>
                                            <div class="relative" style="pointer-events: auto;">
                                                <!-- Red close button in top-right -->
                                                <div @click.stop="selectedRoomId = null"
                                                    class="absolute -top-3 -right-3 w-8 h-8 rounded-full flex items-center justify-center cursor-pointer"
                                                    style="background-color: red;">
                                                    <XMarkIcon class="w-4 h-4" style="color: var(--light-text);" />
                                                </div>
                                                <!-- Main tooltip content -->
                                                <div class="rounded-2xl p-4 shadow-lg"
                                                    style="background-color: var(--element-color-1); color: var(--light-text);">
                                                    <div class="font-medium mb-3">{{ sectionName }}
                                                        <br>
                                                        <span
                                                            v-if="getRoomData(sectionId) && getRoomData(sectionId).lesson_state <= getRoomData(sectionId).num_lessons">
                                                            lesson {{ getRoomData(sectionId).lesson_state }} / {{
                                                                getRoomData(sectionId).num_lessons }}
                                                        </span>
                                                    </div>
                                                    <div class="relative">
                                                        <!-- Shadow element (bottom layer) -->
                                                        <div class="absolute inset-0 rounded-xl"
                                                            style="background-color: rgba(0,0,0,0.2); transform: translateY(4px);">
                                                        </div>

                                                        <!-- Button element (top layer) -->
                                                        <button @click.stop="startLesson(sectionName, sectionId)"
                                                            class="relative w-full rounded-xl py-2 px-4 font-medium flex items-center justify-center gap-2 transition-transform duration-200 hover:translate-y-1"
                                                            style="background-color: var(--light-text); color: var(--element-color-1);">
                                                            <span
                                                                v-if="getRoomData(sectionId) && getRoomData(sectionId).lesson_state <= getRoomData(sectionId).num_lessons">
                                                                PLAY
                                                            </span>
                                                            <span v-else>
                                                                REVIEW
                                                            </span>
                                                        </button>
                                                    </div>
                                                </div>
                                                <!-- Triangle pointer -->
                                                <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 transform rotate-45"
                                                    style="background-color: var(--element-color-1);" />
                                            </div>
                                        </div>

                                        <!-- Icon button with hover group -->
                                        <div class="group perspective-1000"
                                            :style="{ filter: editModeEnabled ? 'grayscale(1) brightness(0.9)' : 'none' }">
                                            <!-- Main button container with enhanced 3D transforms -->
                                            <div class="
                                            relative 
                                            transform-gpu 
                                            transition-all 
                                            duration-300 
                                            group-hover:scale-110
                                            group-hover:-translate-y-3
                                            group-hover:rotate-y-5
                                            group-active:scale-95
                                            group-active:translate-y-1
                                        ">
                                                <!-- Enhanced shadow with depth -->
                                                <div class="
                                                    absolute 
                                                    inset-0 
                                                    rounded-full 
                                                    transform-gpu 
                                                    transition-all 
                                                    duration-300
                                                    opacity-70
                                                    blur-md
                                                    group-hover:blur-lg
                                                    group-hover:scale-110
                                                    group-hover:opacity-80
                                                    group-active:scale-90
                                                    group-active:blur-sm
                                                    group-active:opacity-50
                                                " :style="{
                                                    backgroundColor: getUnitColor(unitIndex),
                                                    transform: 'translateY(10px) scale(0.85)'
                                                }">
                                                </div>

                                                <!-- Base and background elements -->
                                                <div class="relative w-48 h-48">
                                                    <!-- Bottom layer for 3D effect (shadow/base) -->
                                                    <div class="
                                                absolute 
                                                inset-0 
                                                rounded-full 
                                                transform-gpu 
                                                translate-y-2
                                                transition-all
                                                duration-300
                                                group-hover:translate-y-4
                                                group-active:translate-y-1
                                                " :style="{ backgroundColor: getUnitColor(unitIndex) }">
                                                    </div>

                                                    <!-- Main button background with subtle gradient -->
                                                    <div class="
                                                        absolute 
                                                        inset-0 
                                                        rounded-full 
                                                        flex 
                                                        items-center 
                                                        justify-center 
                                                        cursor-pointer 
                                                        shadow-lg 
                                                        transition-all 
                                                        duration-300
                                                        group-active:shadow-inner
                                                        group-hover:shadow-xl
                                                        overflow-hidden
                                                        " :style="{
                                                            background: getUnitGradient(unitIndex)
                                                        }">

                                                        <!-- Icon with enhanced transitions -->
                                                        <component
                                                            :is="getIconForIndex(getGlobalSectionIndex(unitIndex, sectionIndex))"
                                                            class="
                                                            relative
                                                            w-24 
                                                            h-24 
                                                            duration-300 
                                                            drop-shadow-lg
                                                        " style="color: var(--light-text);" />
                                                    </div>

                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <AddSection
                                        v-if="editModeEnabled && isOwner && sectionIndex === rawUnitData[unitName].length - 1"
                                        class="-mx-8" :library-id="libraryId"
                                        :unit-id="props.unitPositionMap[unitName][1]" :position="sectionIndex + 1"
                                        :offset="getNodeOffset(getGlobalSectionIndex(unitIndex, sectionIndex) + .5)"
                                        :unit-color="getUnitColor(unitIndex)" @nodes-added="onSectionAdd" />
                                </template>

                                <template v-else>
                                    <div class="flex flex-col pt-10 pb-10 items-center justify-center p-6 min-w-64">

                                        <div class="text-center mb-4 mt-2" style="color: var(--light-text);">
                                            <p class="text-lg">No stepping stones yet</p>
                                            <p class="text-sm opacity-75">Add stepping stones to get started</p>
                                        </div>

                                        <!-- owner sees the AddSection bubble -->
                                        <AddSection v-if="isOwner" :library-id="libraryId"
                                            :unit-id="props.unitPositionMap[unitName][1]" :position="0"
                                            :empty-unit="true"
                                            :offset="getNodeOffset(getGlobalSectionIndex(unitIndex, 20))"
                                            :unit-color="getUnitColor(unitIndex)" @nodes-added="onSectionAdd" />

                                        <div v-if="!isOwner" class="flex items-center gap-2 px-4 py-2 rounded-lg transition-all 
                                            duration-200 hover:scale-105 active:scale-95" :style="{
                                                background: getUnitColor(unitIndex),
                                                color: 'var(--light-text)',

                                            }">
                                            <PlusIcon class="w-0 h-5 opacity-0" />
                                            <span>Only Course owner can add stepping stones!</span>
                                            <PlusIcon class="w-0 h-5 opacity-0" />
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </div>

                        <AddUnit v-if="editModeEnabled" :library-id="libraryId" :position="unitIndex + 1"
                            :existing-units="Object.keys(rawUnitData)" :can-add-unit="isOwner"
                            @unit-added="handleUnitAdded" />

                    </template>

                    <!-- Added right padding to ensure last nodes have space -->
                    <div class="p-16"></div>
                </div>
            </div>

            <div class="flex justify-between mt-4 px-8 pb-32">

                <!-- left side -->
                <div class="flex gap-2 pointer-events-auto">
                    <button v-if="scrollPosition > 300" @click="scrollToStart(); $nextTick(handleScroll)"
                        class="p-4 rounded-full bg-black/30 backdrop-blur-sm hover:bg-black/40 shadow-md flex items-center gap-2"
                        style="color: var(--highlight-color);">
                        <ChevronDoubleLeftIcon class="w-6 h-6" />
                        <span class="mx-1">To Start</span>
                    </button>
                    <button v-if="scrollPosition > 300" @click="scroll('left'); $nextTick(handleScroll)"
                        class="p-4 rounded-full bg-black/30 backdrop-blur-sm hover:bg-black/40 shadow-md flex items-center gap-2"
                        style="color: var(--highlight-color);">
                        <ChevronLeftIcon class="w-6 h-6" />
                    </button>
                </div>

                <!-- right side -->
                <div class="flex gap-2 pointer-events-auto">
                    <button v-if="scrollPosition < (maxLeft - 300)" @click="scroll('right'); $nextTick(handleScroll)"
                        class="p-4 rounded-full bg-black/30 backdrop-blur-sm hover:bg-black/40 shadow-md"
                        style="color: var(--highlight-color);">
                        <ChevronRightIcon class="w-6 h-6" />
                    </button>
                    <button v-if="scrollPosition < (maxLeft - 300)" @click="scrollToEnd(); $nextTick(handleScroll)"
                        class="p-4 rounded-full bg-black/30 backdrop-blur-sm hover:bg-black/40 shadow-md flex items-center gap-2"
                        style="color: var(--highlight-color);">
                        <span>To End</span>
                        <ChevronDoubleRightIcon class="w-6 h-6" />
                    </button>
                </div>
            </div>
        </div>
    </div>

    <LibrarySettings v-model:showSettingsModal="showSettingsModal" :library-id="libraryId"
        :library-is-public="libraryIsPublic" :library-join-code="libraryJoinCode" :can-modify="isOwner" />

    <LeaveCourse v-model:showModal="showLeaveCourseModal" :library-id="props.libraryId"
        :library-topic="props.libraryTopic" />

</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick, onUnmounted, PropType } from 'vue'
import {
    StarIcon,
    BookOpenIcon,
    TrophyIcon,
    ChatBubbleBottomCenterTextIcon,
    AcademicCapIcon,
    BeakerIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
    PuzzlePieceIcon,
    RocketLaunchIcon,
    SparklesIcon,
    CogIcon,
    XMarkIcon,
    ChevronDoubleLeftIcon,
    ChevronDoubleRightIcon,
    ChartBarIcon,
    PencilIcon,
    PlusIcon,
    HomeIcon,
    ArrowLeftOnRectangleIcon
} from '@heroicons/vue/24/solid';
import { useGameStore } from '@/store/gameStore'
import { useRouter } from 'vue-router';
import { toast } from 'vue-sonner'
import LibrarySettings from "./LibrarySettings.vue";
import AddUnit from "./AddUnit.vue";
import AddSection from "./AddSection.vue"
import DeleteSection from "./DeleteSection.vue"
import LeaveCourse from './LeaveCourse.vue'; // Import the new modal

const props = defineProps({
    libraryId: {
        type: Number,
        required: true
    },
    roomNames: {
        type: Array,
        required: true
    },
    roomData: {
        type: Object,
        required: true
    },
    unitSectionMap: {
        type: Object as PropType<Record<string, any[][]>>,
        required: true
    },
    libraryIsPublic: {
        type: Boolean,
        required: true
    },
    libraryJoinCode: {
        type: [String, null],
        required: true
    },
    isOwner: {
        type: Boolean,
        required: true
    },
    unitPositionMap: {
        type: Object,
        required: true
    },
    libraryTopic: {
        type: String,
        required: true
    }
})

const rawUnitData = ref();

watch(() => props.unitSectionMap, async (newVal) => {
    rawUnitData.value = newVal;
    recalcMaxLeft()
}, { deep: true, immediate: true })

// State for adding new nodes
const gameStore = useGameStore()
const showSettingsModal = ref(false)
const showLeaveCourseModal = ref(false); // State for the leave course modal
const isOwner = ref(false)
const editModeEnabled = ref(false);

// Track selected room for tooltip
const selectedRoomId = ref(null)

// File input handling
const scrollPosition = ref(0)

// Color schemes for units
const unitColors = [
    '#2ecc71', // green
    '#f1c40f', // yellow
    '#e74c3c', // red
    '#3498db', // blue
    '#1abc9c', // teal
    '#9b59b6', // purple
    '#e67e22', // orange
]

const maxLeft = ref(0)

function recalcMaxLeft() {
    nextTick(() => {                     // wait until Vue has patched the DOM
        const sc = scrollContainer.value
        if (sc) maxLeft.value = sc.scrollWidth - sc.clientWidth
    })
}

// snap back to the first node (same 200 px offset you use on mount)
const scrollToStart = () => {
    if (!scrollContainer.value) return
    scrollContainer.value.scrollTo({ left: 0, behavior: 'smooth' })
}

// snap back to the first node (same 200 px offset you use on mount)
const scrollToEnd = () => {
    if (!scrollContainer.value) return

    const sc = scrollContainer.value
    if (!sc) return

    /* how far we can scroll = total content width – visible width */
    scrollContainer.value.scrollTo({ left: sc.scrollWidth - sc.clientWidth, behavior: 'smooth' })
}

function toggleSettings() {
    showSettingsModal.value = !showSettingsModal.value
}

function toggleEditMode() {
    selectedRoomId.value = null;

    editModeEnabled.value = !editModeEnabled.value

    if (!editModeEnabled.value) {
        toast.success('Edit Mode Disabled', {
            description: 'You can now interact with the nodes.',
            duration: 3000,
            position: 'bottom-right',
            style: {
                background: 'var(--element-color-1)', // A slightly different background for success
                color: 'var(--light-text)',
                border: '1px solid var(--highlight-color)',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
            },
            // Consider adding a relevant icon if available in your icon set
            // icon: '✔️' // Example: Checkmark icon
        });
    }
    // If edit mode is disabled, enable it and show a toast
    else {
        toast.success('Edit Mode Enabled', {
            description: 'Node interaction is disabled in edit mode.',
            duration: 3000,
            position: 'bottom-right',
            style: {
                background: 'var(--element-color-2)', // A slightly different background for error
                color: 'var(--light-text)',
                border: '1px solid var(--highlight-color)',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
            },
        });
    }

}

function goToLeaderboard() {
    router.push(`/lessons/${props.libraryId}/leaderboard`)
}

function goToHome() {
    router.push("/courses");
}

function handleLeaveCourseClick() {
    showLeaveCourseModal.value = true;
}

// Get color for a unit based on its index
const getUnitColor = (unitIndex) => {
    const colorIndex = unitIndex % unitColors.length
    return unitColors[colorIndex];
}

// Get gradient for a unit based on its index
const getUnitGradient = (unitIndex) => {
    const colorIndex = unitIndex % unitColors.length;
    const baseColor = unitColors[colorIndex];

    // Create a more pronounced gradient with highlights
    return `linear-gradient(135deg, 
    ${adjustColor(baseColor, 20)} 0%, 
    ${baseColor} 50%, 
    ${adjustColor(baseColor, -20)} 100%)`;
}

// Helper function to lighten/darken colors
function adjustColor(color, percent) {
    // Convert hex to RGB
    let R = parseInt(color.substring(1, 3), 16);
    let G = parseInt(color.substring(3, 5), 16);
    let B = parseInt(color.substring(5, 7), 16);

    // Adjust brightness
    R = Math.min(255, Math.max(0, R + percent));
    G = Math.min(255, Math.max(0, G + percent));
    B = Math.min(255, Math.max(0, B + percent));

    // Convert back to hex
    const RR = R.toString(16).padStart(2, '0');
    const GG = G.toString(16).padStart(2, '0');
    const BB = B.toString(16).padStart(2, '0');

    return `#${RR}${GG}${BB}`;
}

// Get global section index (for offset and icon selection)
const getGlobalSectionIndex = (unitIndex: number, sectionIndex: number) => {
    let count = 0;
    // Sum the lengths of sections for all units before the current unitIndex
    for (let i = 0; i < unitIndex; i++) {
        const unitKeys = Object.keys(rawUnitData.value);
        const previousUnitName = unitKeys[i];
        if (rawUnitData.value[previousUnitName]) {
            count += rawUnitData.value[previousUnitName].length;
        }
    }
    return count + sectionIndex;
}

// Function to add a new node
const onSectionAdd = async () => {
    // try to get rid of in the future
    window.location.reload();
}

// Function to get the corresponding room data by section ID
const getRoomData = (sectionId: Number) => {
    for (let i = 0; i < props.roomData.length; i++) {
        if (props.roomData[i].section_id === sectionId) {
            return props.roomData[i];
        }
    }
    // Return null if not found
    return null;
}

// Array of icons to cycle through
const icons = [
    StarIcon,
    ChatBubbleBottomCenterTextIcon,
    BookOpenIcon,
    PuzzlePieceIcon,
    TrophyIcon,
    AcademicCapIcon,
    BeakerIcon,
    SparklesIcon,
    RocketLaunchIcon
]

// Get icon based on index
const getIconForIndex = (index) => {
    return icons[index % icons.length]
}

const scrollContainer = ref(null)
const isDragging = ref(false)
const startX = ref(0)
const scrollLeft = ref(0)
let scrollTimeoutId = null;

// Scroll to center on first load
onMounted(() => {

    isOwner.value = props.isOwner

    recalcMaxLeft()
    // If there are nodes and the container exists, scroll to position
    if (rawUnitData.value.length > 0 && rawUnitData.value.length > 0 && scrollContainer.value) {
        // Calculate an appropriate starting position based on available width
        scrollTimeoutId = setTimeout(() => {
            // This gives time for the layout to render before scrolling
            if (scrollContainer.value) {
                const startPosition = Math.max(0, 200); // A small offset to show the first node
                scrollContainer.value.scrollLeft = startPosition;
            }
            scrollTimeoutId = null; // Clear the timeout ID
        }, 100);
    }
    const sc = scrollContainer.value
    if (!sc) return
    maxLeft.value = sc.scrollWidth - sc.clientWidth
});

onUnmounted(() => {
    if (scrollTimeoutId) {
        clearTimeout(scrollTimeoutId); // Clear the timeout if it hasn't run yet
        console.debug("LearningPath unmounting, cleared initial scroll timeout.");
    }
});

// Add to your script section
const handleUnitAdded = (unitData) => {
    // Create a new object to store the updated unit data
    const updatedUnitData = {};
    const unitKeys = Object.keys(rawUnitData.value);

    // Insert the new unit at the specified position
    let inserted = false;

    // Loop through existing units to maintain order
    for (let i = 0; i < unitKeys.length; i++) {
        if (i === unitData.position && !inserted) {
            // Add the new unit at this position
            updatedUnitData[unitData.name] = [];
            inserted = true;
        }

        // Add the existing unit
        updatedUnitData[unitKeys[i]] = rawUnitData.value[unitKeys[i]];
    }

    // If the new unit should be at the end and wasn't inserted yet
    if (!inserted) {
        updatedUnitData[unitData.name] = [];
    }

    // Update the raw unit data
    rawUnitData.value = updatedUnitData;

    recalcMaxLeft()
}

// Add these variables
const startY = ref(0)
const hasMoved = ref(false)
const tapThreshold = 10 // pixels to consider as a tap vs drag
const router = useRouter();
const startDragging = (e) => {
    isDragging.value = true
    hasMoved.value = false
    if (e.type.includes('touch')) {
        startX.value = e.touches[0].pageX - scrollContainer.value.offsetLeft
        startY.value = e.touches[0].pageY
    } else {
        startX.value = e.pageX - scrollContainer.value.offsetLeft
        e.preventDefault() // Only prevent default for mouse events
    }
    scrollLeft.value = scrollContainer.value.scrollLeft
}
const drag = (e) => {
    if (!isDragging.value) return
    let x, y
    if (e.type.includes('touch')) {
        x = e.touches[0].pageX - scrollContainer.value.offsetLeft
        y = e.touches[0].pageY
    } else {
        x = e.pageX - scrollContainer.value.offsetLeft
        e.preventDefault()
    }
    // Calculate distance moved
    const diffX = Math.abs(x - startX.value)
    const diffY = Math.abs(y - startY.value)
    // Only consider it a drag if moved more than threshold
    if (diffX > tapThreshold || diffY > tapThreshold) {
        hasMoved.value = true
        const walk = (x - startX.value) * 2
        scrollContainer.value.scrollLeft = scrollLeft.value - walk
    }
}
const stopDragging = () => {
    isDragging.value = false
}
const handleNodeClick = (sectionId) => {
    if (!hasMoved.value) {
        selectedRoomId.value = selectedRoomId.value && selectedRoomId.value === sectionId ? null : sectionId
    }
}

const handleEditNodeClick = () => {
    toast.warning('Edit Mode Active', {
        description: 'Node interaction is disabled in edit mode.',
        duration: 3000,
        position: 'bottom-right',
        style: {
            background: 'var(--element-color-2)', // A slightly different background for info
            color: 'var(--light-text)',
            border: '1px solid var(--highlight-color)',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        },
        // Consider adding a relevant icon if available in your icon set
        // icon: 'ℹ️' // Example: Information icon
    });
}

const getNodeOffset = (index) => {
    const amplitude = 75;
    // Add a slight phase shift for more natural movement
    return Math.sin(index * 0.6) * amplitude;
}
const startLesson = (sectionName, sectionId) => {
    gameStore.setSectionId(sectionId);
    router.push({
        name: 'GamePage',
        params: { id: props.libraryId, roomName: sectionName },
    })
}
const scroll = (direction) => {
    if (!scrollContainer.value) return
    const scrollAmount = 600
    const currentScroll = scrollContainer.value.scrollLeft
    scrollContainer.value.scrollTo({
        left: direction === 'left' ? currentScroll - scrollAmount : currentScroll + scrollAmount,
        behavior: 'smooth'
    })
}
const handleScroll = () => {
    // guard against nulls during mount/unmount
    const sc = scrollContainer.value
    if (!sc) return

    // copy the browser‑reported scrollLeft into the ref
    scrollPosition.value = sc.scrollLeft
}

</script>
<style scoped>
.overflow-x-auto {
    -webkit-overflow-scrolling: touch;
    scroll-behavior: smooth;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
}

.overflow-x-auto::-webkit-scrollbar {
    display: none;
}

.overflow-x-auto {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.perspective {
    perspective: 1000px;
}

.perspective-1000 {
    perspective: 1000px;
}

.rotate-y-5 {
    transform: rotateY(5deg);
}

@keyframes pulse {

    0%,
    100% {
        opacity: 0.4;
        transform: scale(0.98);
    }

    50% {
        opacity: 0.8;
        transform: scale(1.02);
    }
}

.animate-pulse-slow {
    animation: pulse 3s ease-in-out infinite;
}

@media (max-width: 600px) {
    .scrollContainer {
        position: static !important;
        /* let it flow in the document */
        transform: none !important;
        /* cancel any translateY() you had */
        margin: 0.5rem auto 0;
        /* just a little space under the title */
        width: 100%;
        /* full width so it’s centered */
        display: flex;
        /* keep your flex layout */
        justify-content: center;
        /* center the items horizontally */
    }
}

.unit-box {
    border-top: 2px solid currentColor;
    border-bottom: 2px solid currentColor;
}

.unit--first {
    border-left: 2px solid currentColor;
    border-top-left-radius: 0.625rem;
    border-bottom-left-radius: 0.625rem;
}

.unit--last {
    border-right: 2px solid currentColor;
    border-top-right-radius: 0.625rem;
    border-bottom-right-radius: 0.625rem;
}

.menu-button {
    border-radius: 10px;
    background-color: var(--background-color-1t);
    color: var(--highlight-color);
    border: 1px solid var(--color-primary-dark);
    transition: all 0.2s ease;
}

.menu-button:hover {
    background-color: var(--element-color-1);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.menu-button:active {
    transform: translateY(0);
}

.menu-button.selected {
    background-color: var(--element-color-1);
    border-color: var(--color-primary);
    color: var(--light-text);
}
</style>