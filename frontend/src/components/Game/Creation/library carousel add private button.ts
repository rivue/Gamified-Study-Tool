library carousel add private button:
<template>
    <div class="library-list px-16 py-12">
        <div class="list-header-container">
            <div class="list-header">
                <h1>My Courses</h1>
            </div>
            <!-- Join Private Course Component -->
            <div class="join-private-course">
                <div class="join-form">
                    <Input
                        class="join-input"
                        type="text"
                        v-model="joinCode"
                        placeholder="Enter course code..."
                        @keydown.enter="joinPrivateCourse"
                    />
                    <Button 
                        class="join-button" 
                        @click="joinPrivateCourse"
                        :disabled="joinLoading"
                    >
                        <LoaderCircle v-if="joinLoading" class="mr-2 h-4 w-4 animate-spin" />
                        Join
                    </Button>
                </div>
                <Transition name="fade">
                    <div v-if="joinMessage" :class="['join-message', joinMessageType]">
                        {{ joinMessage }}
                    </div>
                </Transition>
            </div>
        </div>
        <!-- Rest of your existing code -->
        <Input
            class="mb-4 text-lg bg-transparent border-[1px] border-solid border-[var(--text-color)] rounded-[4px] placeholder-[var(--text-color)] text-[var(--text-color)]"
            type="text" v-model="searchQuery" @input="filterLibraries" @keydown="handleSearchKeydown"
            placeholder="Search courses..." />
        
        <!-- Existing code continues... -->
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { StarIcon } from "@heroicons/vue/24/solid";
import { LoaderCircle } from "lucide-vue-next";
import { Table, TableRow, TableBody, TableCell } from "@/components/ui/table";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { useAuthStore } from "@/store/authStore";
import axios from "axios";

// Existing props and code...

// Private course joining functionality
const joinCode = ref("");
const joinMessage = ref("");
const joinMessageType = ref("");
const joinLoading = ref(false);

// Emit an event when a new library is joined so parent can refresh the list
const emit = defineEmits(['libraryJoined']);

async function joinPrivateCourse() {
    if (!joinCode.value.trim()) return;
    
    joinLoading.value = true;
    joinMessage.value = "";
    
    try {
        const response = await axios.post('/api/library/join', {
            code: joinCode.value.trim()
        });
        
        joinMessageType.value = "success";
        joinMessage.value = "Successfully joined course!";
        joinCode.value = "";
        
        // Emit event to refresh libraries list
        emit('libraryJoined', response.data.library);
        
        // Add to local libraries array if needed
        if (response.data.library) {
            // You could add the library to your local list here if needed
            filterLibraries(); // Re-filter to show the new library
        }
        
    } catch (error: any) {
        joinMessageType.value = "error";
        
        if (error.response) {
            if (error.response.status === 409) {
                joinMessage.value = "You have already joined that course";
            } else if (error.response.status === 404) {
                joinMessage.value = "Invalid course code";
            } else {
                joinMessage.value = "Failed to join course";
            }
        } else {
            joinMessage.value = "Network error, please try again";
        }
    } finally {
        joinLoading.value = false;
        
        // Auto-hide message after 5 seconds
        setTimeout(() => {
            joinMessage.value = "";
        }, 5000);
    }
}

// Existing methods...
</script>

<style scoped>
/* Existing styles... */

.list-header-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 24px;
}

@media (min-width: 768px) {
    .list-header-container {
        flex-direction: row;
        align-items: flex-start;
        justify-content: space-between;
    }
}

.join-private-course {
    width: 100%;
    max-width: 400px;
}

.join-form {
    display: flex;
    gap: 8px;
}

.join-input {
    flex: 1;
    background-color: var(--background-color-2t);
    border: 1px solid var(--text-color);
    border-radius: 4px;
    color: var(--text-color);
    height: 40px;
    padding: 0 12px;
}

.join-button {
    background-color: var(--element-color-1);
    color: var(--text-color);
    border: 1px solid var(--text-color);
    border-radius: 4px;
    height: 40px;
    padding: 0 16px;
    transition: all 0.2s ease;
}

.join-button:hover:not(:disabled) {
    background-color: var(--element-color-2);
}

.join-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.join-message {
    margin-top: 8px;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 14px;
    animation: fadeIn 0.3s ease-in-out;
}

.success {
    background-color: rgba(34, 197, 94, 0.2);
    color: #15803d;
    border: 1px solid rgba(34, 197, 94, 0.3);
}

.error {
    background-color: rgba(239, 68, 68, 0.2);
    color: #b91c1c;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
