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
            <div class="text-center mb-4 mt-2" style="color: var(--light-text);">
                <p class="text-2xl font-bold">This course is completely empty!</p>
                <p v-if="isOwner" class="text-lg opacity-75 mt-4">As the course owner, you can add content in edit mode.</p>
                <p v-else class="text-lg opacity-75 mt-4">Check back later to see when content has been added!</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

defineProps({
    isOwner: {
        type: Boolean,
        required: true
    },
    color: {
        type: String,
        required: true
    }
});
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
