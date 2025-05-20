<template>
    <!-- Button View -->
    <div v-if="!showModal" class="relative flex-shrink-0 mx-6">
        <div class="w-16 h-16 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 hover:scale-110 hover:shadow-lg active:scale-95"
            :style="{
                backgroundColor: unitColor,
                opacity: 0.7,
            }" @click="openModal">
            <PlusIcon class="w-8 h-8" style="color: var(--light-text);" />
        </div>
    </div>

    <!-- Modal View -->
    <div v-if="showModal" class="fixed inset-0 flex items-center justify-center z-50">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="closeModal"></div>

        <!-- Modal Content -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md relative">
            <button @click="closeModal" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
                <XMarkIcon class="w-6 h-6" />
            </button>

            <h2 class="text-xl font-bold mb-4">Add Stepping Stone</h2>

            <form @submit.prevent="submitForm">
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">Name</label>
                    <input v-model="sectionName" type="text"
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Enter stepping stone name" required>
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">Description (optional)</label>
                    <textarea v-model="description"
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Enter description" rows="3"></textarea>
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">Number of Lessons</label>
                    <input v-model.number="numLessons" type="number" min="1"
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        required>
                </div>

                <div class="flex justify-end gap-3 mt-6">
                    <button type="button" @click="closeModal"
                        class="px-4 py-2 border rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                        Cancel
                    </button>
                    <button type="submit" class="px-4 py-2 rounded-lg"
                        :style="{ backgroundColor: unitColor, color: 'var(--light-text)' }" :disabled="loading">
                        <span v-if="loading">Creating...</span>
                        <span v-else>Create</span>
                    </button>
                </div>
            </form>

            <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-700 rounded-lg">
                {{ error }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { PlusIcon, XMarkIcon } from '@heroicons/vue/24/solid';
import { useApiService } from '@/services/apiService'; // Adjust to your API service import

const props = defineProps({
    libraryId: {
        type: Number,
        required: true
    },
    unitId: {
        type: [Number, String],
        required: true
    },
    unitColor: {
        type: String,
        required: true
    },
    position: {
        type: Number,
        required: true
    }
});

const emit = defineEmits(['section-added']);

// Form state
const showModal = ref(false);
const sectionName = ref('');
const description = ref('');
const numLessons = ref(1);
const loading = ref(false);
const error = ref('');
const apiService = useApiService(); // Adjust based on your API service setup
// For empty unit modal
const showEmptyUnitModal = ref(false)
const emptyUnitSectionName = ref('')
const emptyUnitDescription = ref('')
const emptyUnitNumLessons = ref(1)
const emptyUnitLoading = ref(false)
const emptyUnitError = ref('')
const emptyUnitId = ref(null)
const emptyUnitColor = ref('')

const openEmptyUnitModal = (unitName) => {
    emptyUnitId.value = props.unitPositionMap[unitName][1]
    emptyUnitColor.value = getUnitColor(Object.keys(rawUnitData.value).indexOf(unitName))
    showEmptyUnitModal.value = true
}

const submitEmptyUnitForm = async () => {
    try {
        emptyUnitLoading.value = true
        emptyUnitError.value = ''
        
        const response = await apiService.post('/api/sections', {
            name: emptyUnitSectionName.value,
            description: emptyUnitDescription.value,
            num_lessons: emptyUnitNumLessons.value,
            unit_id: emptyUnitId.value,
            library_id: props.libraryId,
            position: 0
        })
        
        if (response.status === 201) {
            showEmptyUnitModal.value = false
            onSectionAdd()
        } else {
            emptyUnitError.value = 'Failed to create stepping stone'
        }
    } catch (err) {
        console.error('Error creating section:', err)
        emptyUnitError.value = 'An error occurred while creating the stepping stone'
    } finally {
        emptyUnitLoading.value = false
    }
}
const openModal = () => {
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
    sectionName.value = '';
    description.value = '';
    numLessons.value = 1;
    error.value = '';
};

const submitForm = async () => {
    try {
        loading.value = true;
        error.value = '';

        const response = await apiService.post('/api/sections', {
            name: sectionName.value,
            description: description.value,
            num_lessons: numLessons.value,
            unit_id: props.unitId,
            library_id: props.libraryId,
            position: props.position
        });

        if (response.status === 201) {
            emit('section-added');
            closeModal();
        } else {
            error.value = 'Failed to create stepping stone';
        }
    } catch (err) {
        console.error('Error creating section:', err);
        error.value = 'An error occurred while creating the stepping stone';
    } finally {
        loading.value = false;
    }
};
</script>