<template>
    <div v-if="canAddUnit" class="relative -mx-12 my-12 flex-shrink-0 w-0 flex items-center justify-center" :class="[
        (position === 0 || position === existingUnits.length) ? 'pt-72 pb-52' : 'pt-72 pb-52 border-dashed border-2'
         ]" :style="{
            borderColor: 'var(--background-color-1t)',
            backgroundColor: 'var(--background-color-1t)',
            borderRight: 'none',
        }">
        <div class="absolute hover:opacity-80 cursor-pointer bottom-52 left-1/2 transform -translate-x-1/2 px-2 py-7 rounded-lg whitespace-nowrap shadow-md z-10"
            @click="openAddUnitModal" :style="{ backgroundColor: 'var(--background-color-1t)' }">
            <PlusIcon class="w-8 h-8" style="color: var(--highlight-color);" />
        </div>
    </div>

    <!-- Add Unit Modal -->
    <Transition name="modal">
        <div v-if="showAddUnitModal && canAddUnit" class="fixed inset-0 flex items-center justify-center z-50 p-4"
            style="background-color: var(--background-haze);">
            <div class="rounded-2xl p-6 w-full max-w-md shadow-xl border"
                style="background-color: var(--background-color); color: var(--light-text); border-color: var(--color-primary-dark);">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-semibold" style="color: var(--light-text);">Add New Unit</h2>
                    <button @click="showAddUnitModal = false" style="color: var(--highlight-color);">
                        <XMarkIcon class="w-6 h-6" />
                    </button>
                </div>
                <div class="space-y-4">
                    <!-- Unit name input - Fixed version -->
                    <div>
                        <label for="unit-name-input" class="block text-sm font-medium mb-1"
                            style="color: var(--highlight-color);">Unit Name</label>
                        <input id="unit-name-input" v-model="newUnitName" type="text"
                            class="w-full p-2 border rounded-lg"
                            style="background-color: var(--background-color-1t); font-size: 16px; color: var(--light-text); border-color: var(--color-primary-dark);"
                            placeholder="Enter unit name" maxlength="40" autocomplete="off" />
                        <p v-if="unitNameError" class="mt-1 text-sm" style="color: var(--color-primary-light);">
                            {{ unitNameError }}
                        </p>
                    </div>

                    <div class="flex gap-3 justify-end mt-6">
                        <button @click="showAddUnitModal = false" class="px-4 py-2 border rounded-lg"
                            style="border-color: var(--color-primary); color: var(--highlight-color);">
                            Cancel
                        </button>
                        <button @click="addNewUnit" class="px-4 py-2 rounded-lg focus:outline-none focus:ring-2"
                            style="background: var(--button-gradient); color: var(--light-text);"
                            :disabled="isAddingUnit">
                            <span v-if="isAddingUnit">Adding...</span>
                            <span v-else>Add Unit</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { ref, nextTick, onMounted, toRefs } from 'vue'
import { PlusIcon, XMarkIcon } from '@heroicons/vue/24/solid'
import axios from 'axios'

const props = defineProps({
    libraryId: {
        type: Number,
        required: true
    },
    position: {
        type: Number, // index number
        required: true
    },
    existingUnits: {
        type: Array,
        default: () => []
    },
    canAddUnit: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['unitAdded'])

const showAddUnitModal = ref(false)
const newUnitName = ref('')
const unitNameError = ref('')
const isAddingUnit = ref(false)
const { canAddUnit } = toRefs(props)

onMounted(() => {
    if (!canAddUnit.value) {
        showAddUnitModal.value = false
    }
});

// Function to open the add unit modal
const openAddUnitModal = () => {
    newUnitName.value = ''
    unitNameError.value = ''
    showAddUnitModal.value = true

    // Focus the input field after the modal is shown
    nextTick(() => {
        document.getElementById('unit-name-input')?.focus()
    })
}

// Function to add a new unit
const addNewUnit = async () => {

    if (!canAddUnit) {
        return;
    }

    // Validate unit name
    unitNameError.value = ''
    const trimmedName = newUnitName.value.trim()

    if (!trimmedName) {
        unitNameError.value = 'Please enter a unit name'
        return
    } else if (trimmedName.length > 25 || trimmedName.length < 4) {
        unitNameError.value = 'Unit name must be between 4 and 25 characters'
        return
    }

    // Check for duplicate unit names
    if (props.existingUnits.includes(trimmedName)) {
        unitNameError.value = 'A unit with this name already exists'
        return
    }

    isAddingUnit.value = true

    try {

        // Determine position for the new unit
        let position = props.position
        const response = await axios.post('/api/library/unit', {
            libraryId: props.libraryId,
            unitName: trimmedName,
            position: position,
        })

        if (response.data && response.data.status === "success") {
            // Clear form and notify parent
            newUnitName.value = ''
            showAddUnitModal.value = false,
            console.log('Unit added successfully:', response.data)
            location.reload();
        }
    } catch (error) {
        unitNameError.value = 'Failed to add unit. Please try again.'
    } finally {
        isAddingUnit.value = false
    }
}
</script>
