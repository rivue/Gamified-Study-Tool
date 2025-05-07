<template>
    <div class="relative -mx-12 my-12 px-12 pt-16 pb-16 border-dashed border-2 flex-shrink-0 w-24 flex items-center justify-center cursor-pointer hover:opacity-80"
        @click="openAddUnitModal"
        :style="{ borderColor: 'var(--highlight-color)', backgroundColor: 'var(--background-color-1t)' }">
        <StarIcon class="w-12 h-12" style="color: var(--highlight-color);" />
    </div>
    
    <!-- Add Unit Modal -->
    <Transition name="modal">
        <div v-if="showAddUnitModal" class="fixed inset-0 flex items-center justify-center z-50 p-4"
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
            <!-- Unit name input -->
            <div>
                <label class="block text-sm font-medium mb-1" style="color: var(--highlight-color);">Unit Name</label>
                <input v-model="newUnitName" type="text" class="w-full p-2 border rounded-lg"
                style="background-color: var(--background-color-1t); color: var(--light-text); border-color: var(--color-primary-dark);"
                placeholder="Enter unit name" maxlength="40" />
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
  import { ref } from 'vue'
  import { StarIcon, XMarkIcon } from '@heroicons/vue/24/solid'
  import axios from 'axios'
  
  const props = defineProps({
    libraryId: {
      type: String,
      required: true
    },
    position: {
      type: [Number, String], // 'start', index number, or 'end'
      required: true
    },
    existingUnits: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['unitAdded'])
  
  const showAddUnitModal = ref(false)
  const newUnitName = ref('')
  const unitNameError = ref('')
  const isAddingUnit = ref(false)
  
  // Function to open the add unit modal
  const openAddUnitModal = () => {
    newUnitName.value = ''
    unitNameError.value = ''
    showAddUnitModal.value = true
  }
  
  // Function to add a new unit
  const addNewUnit = async () => {
    // Validate unit name
    unitNameError.value = ''
    const trimmedName = newUnitName.value.trim()
    
    if (!trimmedName) {
      unitNameError.value = 'Please enter a unit name'
      return
    } else if (!/^[a-zA-Z0-9 ]+$/.test(trimmedName)) {
      unitNameError.value = 'Unit name can only contain letters, numbers and spaces'
      return
    } else if (trimmedName.length > 40) {
      unitNameError.value = 'Unit name must be 40 characters or less'
      return
    }
    
    // Check for duplicate unit names
    const formattedUnitName = trimmedName.toLowerCase().replace(/\s+/g, '_')
    const existingUnitNames = props.existingUnits.map(unit => unit.toLowerCase())
    if (existingUnitNames.includes(formattedUnitName)) {
      unitNameError.value = 'A unit with this name already exists'
      return
    }
    
    isAddingUnit.value = true
    const currentAbortController = new AbortController()
    
    try {
      // Determine position for the new unit
      let position = 0
      if (props.position === 'end') {
        position = props.existingUnits.length
      } else if (props.position === 'start') {
        position = 0
      } else {
        position = props.position
      }
      
      const response = await axios.post('/api/library/unit', {
        libraryId: props.libraryId,
        unitName: formattedUnitName,
        displayName: trimmedName,
        position: position
      }, {
        signal: currentAbortController.signal
      })
      
      if (currentAbortController.signal.aborted) return
      
      if (response.data && response.data.status === "success") {
        // Clear form and notify parent
        newUnitName.value = ''
        showAddUnitModal.value = false
        emit('unitAdded', {
          name: formattedUnitName,
          displayName: trimmedName,
          position: position
        })
      }
    } catch (error) {
      console.error('Error adding unit:', error)
      unitNameError.value = error.message || 'Failed to add unit. Please try again.'
    } finally {
      isAddingUnit.value = false
    }
  }
  </script>