<template>
    <div class="relative -mx-12 my-12 px-16 pt-40 pb-36 border-t-2 border-b-2 flex-shrink-0 unit-box unit--first unit--last"
        :style="{
            borderColor: color,
            backgroundColor: 'var(--background-color-1t)',
        }">

        <!-- Unit name header -->
        <div class="absolute -top-5 left-1/2 transform -translate-x-1/2 px-6 py-2 rounded-lg font-bold text-xl whitespace-nowrap shadow-md"
            :style="{ backgroundColor: color, color: 'var(--light-text)' }">
            Nothing to see here!
        </div>

        <div class="flex flex-col pt-10 pb-10 items-center justify-center p-6 min-w-64">
            <div class="text-center mb-6 mt-2" style="color: var(--light-text);">
                <p class="text-2xl font-bold">This course is completely empty!</p>
                <p v-if="isOwner" class="text-lg opacity-75 mt-4">Create your first section to get started.</p>
                <p v-else class="text-lg opacity-75 mt-4">Check back later to see when content has been added!</p>
            </div>

        </div>

        <!-- After unit is created, mount AddSection with auto-open to let user add the section -->
        <AddSection v-if="createdUnitId"
            :library-id="libraryId"
            :unit-id="createdUnitId"
            :position="0"
            :empty-unit="true"
            :unit-color="color"
            :auto-open="true"
            @nodes-added="handleNodesAdded" />

    </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';
import axios from 'axios';
import AddSection from './AddSection.vue';

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

const creatingUnit = ref(false);
const createdUnitId = ref<number | null>(null);
const errorMessage = ref('');

async function createUnitAndOpenSection() {
    if (creatingUnit.value) return;
    errorMessage.value = '';
    creatingUnit.value = true;
    try {
        const response = await axios.post('/api/library/unit', {
            libraryId: props.libraryId,
            unitName: 'Unit 1',
            position: 0,
        });
        if (response.data?.status === 'success' && response.data.unit_id) {
            createdUnitId.value = response.data.unit_id;
        } else {
            errorMessage.value = response.data?.message || 'Failed to create unit';
        }
    } catch (e: any) {
        errorMessage.value = e?.response?.data?.message || e?.message || 'Failed to create unit';
    } finally {
        creatingUnit.value = false;
    }
}

function handleNodesAdded() {
    // Refresh to reflect new sections
    window.location.reload();
}
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
