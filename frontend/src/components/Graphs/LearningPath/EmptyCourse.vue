<template>


    <div class="relative -mx-12 my-12 px-16 pt-40 pb-36 border-t-2 border-b-2 flex-shrink-0"
        :class="['unit-box', 'unit--first', 'unit--last']" :style="{
            borderColor: '#2ecc71', // green
            backgroundColor: 'var(--background-color-1t)'
        }">


        <!-- Unit name header -->
        <div class="absolute -top-5 left-1/2 transform -translate-x-1/2 px-6 py-2 rounded-lg font-bold text-xl whitespace-nowrap shadow-md"
            :style="{ backgroundColor: '#2ecc71', color: 'var(--light-text)' }">
            Nothing here yet!
        </div>

        <!-- Sections container -->
        <div class="flex items-center">
            <div>
                <div class="flex flex-col pt-10 pb-10 items-center justify-center p-6 min-w-64">
                    <div class="text-center mb-4 mt-2" style="color: var(--light-text);">
                        <p class="text-lg">No units yet</p>
                        <p class="text-sm opacity-75">Add a unit to get started</p>
                    </div>

                    <!-- Inline Add Unit button (styled like AddSection) -->
                    <AddUnit
                        v-if="isOwner"
                        :library-id="libraryId"
                        :position="0"
                        :can-add-unit="isOwner"
                        :inline-button="true"
                        :button-color="green"
                    />

                    <div v-else class="flex items-center gap-2 px-4 py-2 rounded-lg" :style="{
                        background: '#2ecc71',
                        color: 'var(--light-text)'
                    }">
                        <PlusIcon class="w-0 h-5 opacity-0" />
                        <span>Only the course owner can add units.</span>
                        <PlusIcon class="w-0 h-5 opacity-0" />
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- <AddUnit v-if="editModeEnabled" :library-id="libraryId" :position="unitIndex + 1"
            :existing-units="Object.keys(rawUnitData)" :can-add-unit="isOwner" @unit-added="handleUnitAdded" /> -->

    <!-- remove this because we should need after we refresh the page -->
    <!-- <AddSection v-if="createdUnitId"
            :library-id="libraryId"
            :unit-id="createdUnitId"
            :position="0"
            :empty-unit="true"
            :unit-color="color"
            :auto-open="true"
            @nodes-added="handleNodesAdded" /> -->

</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { PlusIcon } from '@heroicons/vue/24/solid'
import AddUnit from './AddUnit.vue';

const props = defineProps({
    isOwner: {
        type: Boolean,
        required: true
    },
    color: {
        type: String,
        required: true
    },
    libraryId: {
        type: Number,
        required: true
    }
});

const green = '#2ecc71'; // green color
</script>

<style scoped>
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
</style>
