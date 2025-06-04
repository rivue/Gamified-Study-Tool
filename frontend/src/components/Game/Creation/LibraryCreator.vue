<template>
    <div>
        <div>
            <div>
                <!-- Header -->
                <div class="header-section">
                    <h1 class="main-title">Create Your Course</h1>
                    <p class="main-subtitle">Build an engaging learning experience from your materials</p>
                </div>

                <!-- Stepper Navigation -->
                <div class="stepper-nav">
                    <div class="stepper-container">
                        <div v-for="(step, index) in steps" :key="step.value" class="stepper-item">
                            <!-- Step Circle -->
                            <div :class="['step-circle', {
                                'active': currentTab === step.value,
                                'completed': getStepIndex(currentTab) > index && !hasStepErrors(step.value),
                                'pending': getStepIndex(currentTab) < index,
                                'error': hasStepErrors(step.value) && getStepIndex(currentTab) > index
                            }]">
                                <span v-if="hasStepErrors(step.value) && getStepIndex(currentTab) > index"
                                    class="error-icon">!</span>
                                <span v-else-if="getStepIndex(currentTab) > index && !hasStepErrors(step.value)"
                                    class="check-icon">✓</span>
                                <span v-else class="step-number">{{ index + 1 }}</span>
                            </div>

                            <!-- Step Label -->
                            <div :class="['step-info', {
                                'active': currentTab === step.value,
                                'completed': getStepIndex(currentTab) > index && !hasStepErrors(step.value),
                                'error': hasStepErrors(step.value) && getStepIndex(currentTab) > index
                            }]">
                                <div class="step-title">{{ step.label }}</div>
                                <div class="step-description">
                                    <span v-if="hasStepErrors(step.value) && getStepIndex(currentTab) > index"
                                        class="error-indicator">
                                        Has errors
                                    </span>
                                    <span v-else>{{ step.description }}</span>
                                </div>
                            </div>

                            <!-- Connector Line -->
                            <div v-if="index < steps.length - 1" :class="['step-connector', {
                                'completed': getStepIndex(currentTab) > index && !hasStepErrors(step.value)
                            }]"></div>
                        </div>
                    </div>
                </div>

                <!-- Error Summary (shown only in settings tab) -->
                <div v-if="currentTab === 'settings' && hasPreviousStepErrors" class="error-summary">
                    <div class="error-summary-header">
                        <span class="error-icon">⚠️</span>
                        <span class="error-title">Please fix the following issues:</span>
                    </div>
                    <div class="error-list">
                        <div v-if="hasStepErrors('basics')" class="error-item" @click="currentTab = 'basics'">
                            <span class="error-step">Course Basics:</span>
                            <span class="error-details">{{ getStepErrorSummary('basics') }}</span>
                        </div>
                        <div v-if="hasStepErrors('structure')" class="error-item" @click="currentTab = 'structure'">
                            <span class="error-step">Course Structure:</span>
                            <span class="error-details">{{ getStepErrorSummary('structure') }}</span>
                        </div>
                    </div>
                </div>


                <!-- Form Content -->
                <div class="form-content" @keydown.enter="handleSubmit">
                    <!-- Loading State with Lottie Animation -->
                    <div v-if="buttonDisabled.isSubmitting" class="loading-overlay">
                        <div class="loading-content">
                            <DotLottieVue 
                                autoplay 
                                loop 
                                src="https://lottie.host/b96a9b39-d99b-4f64-a92d-8b39aefc27ca/73Yl9OD4Tc.lottie" 
                            />
                            <h2 class="loading-title">Creating Your Course</h2>
                            <p class="loading-subtitle">This may take a few moments while we process your materials...</p>
                            
                            <!-- Rotating Educational Messages -->
                            <div class="loading-messages">
                                <Transition name="fade" mode="out-in">
                                    <div :key="currentMessageIndex" class="loading-message">
                                        {{ loadingMessages[currentMessageIndex] }}
                                    </div>
                                </Transition>
                            </div>
                        </div>
                    </div>

                    <!-- Rest of the template remains the same -->
                    <template v-else>
                        <!-- ... existing template content ... -->
                        <div v-if="currentTab === 'basics'" class="step-content">
                            <!-- Keep existing basics content -->
                            <div class="section-card">
                                <div class="card-header">
                                    <h2 class="section-title">Course Information</h2>
                                    <p class="section-description">Give your course a name and upload your source
                                        material
                                    </p>
                                </div>

                                <div class="form-group">
                                    <label class="form-label">Course Name</label>
                                    <input type="text" v-model="topic" ref="topicInput"
                                        :class="['form-input', { 'error': formattedErrors.topic?._errors?.length }]"
                                        placeholder="e.g., Introduction to Biology, Advanced Calculus..."
                                        maxlength="100" @focus="selectInputText" @paste="handlePaste" />
                                    <div class="input-hint">Must be 4-25 characters long</div>
                                    <div v-if="formattedErrors.topic?._errors?.length" class="error-text">
                                        {{ formattedErrors.topic._errors[0] }}
                                    </div>
                                </div>

                                <div class="form-group">
                                    <label class="form-label">Course Material</label>
                                    <div class="file-upload-area" :class="{ 'has-file': selectedFile }">
                                        <input type="file" id="fileInput" ref="fileInput" @change="handleFileUpload"
                                            :class="{ 'error': formattedErrors.selectedFile?._errors?.length }"
                                            accept=".pdf" class="file-input" />
                                        <div v-if="!selectedFile" class="upload-placeholder">
                                            <div class="upload-icon">📄</div>
                                            <div class="upload-text">
                                                <span class="upload-main">Click to upload PDF</span>
                                                <span class="upload-sub">Maximum size: 500KB</span>
                                            </div>
                                        </div>
                                        <div v-else class="selected-file-display">
                                            <div class="file-info">
                                                <div class="file-icon">📄</div>
                                                <div class="file-details">
                                                    <span class="file-name">{{ selectedFile.name }}</span>
                                                    <span class="file-size">{{ formatFileSize(selectedFile.size)
                                                    }}</span>
                                                </div>
                                            </div>
                                            <button class="remove-file" @click="removeFile" type="button">✕</button>
                                        </div>
                                    </div>
                                    <div v-if="formattedErrors.selectedFile?._errors?.length" class="error-text">
                                        {{ formattedErrors.selectedFile._errors[0] }}
                                    </div>
                                    <div class="input-hint">This file will be used to generate content for your course
                                        topics</div>
                                </div>
                            </div>
                        </div>

                        <!-- Step 2: Course Structure -->
                        <div v-if="currentTab === 'structure'" class="step-content">
                            <div class="section-card">
                                <div class="card-header">
                                    <h2 class="section-title">Course Structure</h2>
                                    <p class="section-description">Organize your course into topics and subtopics</p>
                                </div>

                                <!-- Example Structure -->
                                <div class="example-card">
                                    <div class="example-header">Example Structure</div>
                                    <div class="example-content">
                                        <div class="example-topic">
                                            <strong>Topic:</strong> "Cell Biology"
                                            <div class="example-subtopics">
                                                <strong>Subtopics:</strong> "Cell Membrane", "Mitochondria", "Nucleus"
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Topics List -->
                                <div class="topics-list">
                                    <div v-for="(group, groupIndex) in groups" :key="groupIndex" class="topic-card">
                                        <div class="topic-header">
                                            <input type="text" v-model="group.name" placeholder="Enter topic name..."
                                                maxlength="40"
                                                :class="['topic-input', { 'error': formattedErrors.groups?.[groupIndex]?.name?._errors?.length }]" />
                                            <button class="remove-topic-btn" @click="removeGroup(groupIndex)"
                                                type="button">✕</button>
                                        </div>
                                        <div v-if="formattedErrors.groups?.[groupIndex]?.name?._errors?.length"
                                            class="error-text">
                                            {{ formattedErrors.groups[groupIndex].name._errors[0] }}
                                        </div>

                                        <div class="subtopics-section">
                                            <div v-if="group.sections.length > 0" class="subtopics-list">
                                                <div v-for="(section, sectionIndex) in group.sections"
                                                    :key="sectionIndex" class="subtopic-item">
                                                    <input type="text" v-model="group.sections[sectionIndex]"
                                                        placeholder="Enter subtopic name..." maxlength="40"
                                                        class="subtopic-input" />
                                                    <button class="remove-subtopic-btn"
                                                        @click="removeSection(groupIndex, sectionIndex)"
                                                        type="button">✕</button>
                                                </div>
                                            </div>

                                            <button class="add-subtopic-btn" @click="addSection(groupIndex)"
                                                :disabled="group.sections.length >= 15 || disableExtras" type="button">
                                                + Add Subtopic
                                            </button>

                                            <div v-if="formattedErrors.groups?.[groupIndex]?.sections?._errors?.length"
                                                class="error-text">
                                                {{ formattedErrors.groups[groupIndex].sections._errors[0] }}
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Add Topic Button -->
                                    <button class="add-topic-btn" @click="addGroup"
                                        :disabled="groups.length >= 10 || disableExtras" type="button">
                                        + Add Topic
                                    </button>
                                </div>

                                <div v-if="formattedErrors.groups?._errors?.length" class="error-text">
                                    {{ formattedErrors.groups._errors[0] }}
                                </div>

                                <div class="structure-hints">
                                    <div class="hint">📝 You can create up to 10 topics with 15 subtopics each</div>
                                    <div class="hint">✨ Don't worry about adding everything now - you can expand later!
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Step 3: Settings -->
                        <div v-if="currentTab === 'settings'" class="step-content">
                            <div class="section-card">
                                <div class="card-header">
                                    <h2 class="section-title">Course Settings</h2>
                                    <p class="section-description">Configure how others can access your course</p>
                                </div>

                                <div class="visibility-section">
                                    <label class="form-label">Course Visibility</label>
                                    <div class="visibility-toggle">
                                        <button type="button"
                                            :class="['visibility-option', { 'active': visibilityTab === 'public' }]"
                                            @click="visibilityTab = 'public'">
                                            <Globe class="option-icon" />
                                            <div class="option-content">
                                                <div class="option-title">Public</div>
                                                <div class="option-desc">Anyone can join</div>
                                            </div>
                                        </button>
                                        <button type="button"
                                            :class="['visibility-option', { 'active': visibilityTab === 'private' }]"
                                            @click="visibilityTab = 'private'">
                                            <Lock class="option-icon" />
                                            <div class="option-content">
                                                <div class="option-title">Private</div>
                                                <div class="option-desc">Requires join code to join</div>
                                            </div>
                                        </button>
                                    </div>
                                </div>

                                <!-- Create Button -->
                                <div class="create-section">
                                    <button type="button" class="create-button" @click="handleSubmit"
                                        :disabled="buttonDisabled.isSubmitting || buttonDisabled.noRooms">
                                        <span v-if="buttonDisabled.isSubmitting" class="button-loading">
                                            <div class="spinner"></div>
                                            Creating Course...
                                        </span>
                                        <span v-else-if="buttonDisabled.noRooms">
                                            Add Topics to Continue
                                        </span>
                                        <span v-else>
                                            Create Course
                                        </span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>

                <!-- Navigation -->
                <div  v-if="!buttonDisabled.isSubmitting" class="navigation-section">
                    <button v-if="currentTab !== 'basics'" class="nav-button secondary" @click="goToPreviousStep"
                        type="button">
                        ← Previous
                    </button>
                    <div class="nav-spacer"></div>
                    <button v-if="currentTab !== 'settings'" class="nav-button primary" @click="goToNextStep"
                        type="button">
                        Next →
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Keep all existing imports and logic...
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from "axios";
import { z } from "zod";

import { Lock, Globe } from "lucide-vue-next";
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore } from "@/store/authStore";

// Keep all existing interfaces and schemas...
interface Group {
    name: string;
    sections: string[];
    newSectionName: string;
    sectionError: boolean;
    isEditing?: boolean;
    editingName?: string;
}

const groupSchema = z.object({
    name: z.string()
        .min(4, "Topic names must be at least 4 characters")
        .max(25, "Topic names must be at most 25 characters")
        .refine(val => !val.startsWith(" ") && !val.endsWith(" "),
            "Topic names must not start or end with a space"),
    sections: z.array(z.string())
        .min(1, "Every Topic must have at least one section")
        .superRefine((sections, ctx) => {
            const lengthIssues = sections.some(
                section => section.length < 4 || section.length > 25
            );

            if (lengthIssues) {
                ctx.addIssue({
                    code: z.ZodIssueCode.custom,
                    message: "All subtopic names must be between 4 and 25 characters"
                });
                return;
            }

            const whitespaceIssues = sections.some(
                section => section.startsWith(" ") || section.endsWith(" ")
            );

            if (whitespaceIssues) {
                ctx.addIssue({
                    code: z.ZodIssueCode.custom,
                    message: "Subtopic names must not start or end with a space"
                });
                return;
            }

            if (sections.length !== new Set(sections.map(s => s.toLowerCase())).size) {
                ctx.addIssue({
                    code: z.ZodIssueCode.custom,
                    message: "Duplicate subtopic names are not allowed within a topic"
                });
            }
        })
});

const formSchema = z.object({
    topic: z.string()
        .min(4, "Course name must be at least 4 characters")
        .max(25, "Course name must be at most 25 characters")
        .refine(val => !val.startsWith(" ") && !val.endsWith(" "),
            "Course name must not start or end with a space"),
    visibility: z.boolean(),
    selectedFile: z.instanceof(File, { message: "Must have at least one file - we wouldn't know what to generate!" }),
    groups: z.array(groupSchema)
        .min(1, "Must have at least one Topic (and topic names can't be empty)")
        .refine(
            groups => {
                const names = groups.map(g => g.name.toLowerCase());
                return names.length === new Set(names).size;
            },
            "Duplicate topic names are not allowed"
        )
});

// Keep all existing state...
const router = useRouter();
const authStore = useAuthStore();
const popupStore = usePopupStore();

const groups = ref<Group[]>([]);
const topic = ref("");
const libraryDifficulty = ref("Normal");
const buttonDisabled = ref({
    noRooms: true,
    isSubmitting: false,
});
const selectedFile = ref<File | null>(null);
const topicInput = ref<HTMLInputElement | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const visibilityTab = ref<'public' | 'private'>('public');
const isPublic = computed<boolean>(() => visibilityTab.value === 'public');
const formattedErrors = ref<ReturnType<z.ZodError["format"]>>({} as any)
const currentTab = ref<'basics' | 'structure' | 'settings'>('basics');
const validationAttempted = ref(false);

// Loading messages state
const currentMessageIndex = ref(0);
let messageInterval: NodeJS.Timeout | null = null;

// Educational loading messages
const loadingMessages = ref([
    "Setting up the classroom...",
    "Sharpening the pencils...",
    "Moving desks so you don't talk to your friends...",
    "Grading yesterday's homework...",
    "Creating lesson plans...",
    "Preparing pop quizzes (there's one tomorrow!)...",
    "Dusting off encyclopedias...",
    "Calling substitute teachers...",
    "Checking attendance...",
    "Organizing study groups...",
    "Writing on the chalkboard...",
    "Updating the syllabus...",
    "Brewing teacher's coffee...",
    "Organizing field trips...",
    "Ringing the school bell..."
]);

// Updated steps with descriptions
const steps = computed(() => [
    { value: 'basics', label: 'Course Basics', description: 'Name and materials' },
    { value: 'structure', label: 'Course Structure', description: 'Topics and subtopics' },
    { value: 'settings', label: 'Settings', description: 'Fine tune your experience' }
]);

const disableExtras = computed(() => {
    return !authStore.loggedIn;
});

// Keep all existing helper functions and methods...
const getStepIndex = (step: string) => {
    return steps.value.findIndex(s => s.value === step);
};

const goToNextStep = () => {
    const currentIndex = getStepIndex(currentTab.value);
    if (currentIndex < steps.value.length - 1) {
        currentTab.value = steps.value[currentIndex + 1].value as 'basics' | 'structure' | 'settings';
    }
};

const goToPreviousStep = () => {
    const currentIndex = getStepIndex(currentTab.value);
    if (currentIndex > 0) {
        currentTab.value = steps.value[currentIndex - 1].value as 'basics' | 'structure' | 'settings';
    }
};

// Message rotation function
const startMessageRotation = () => {
    messageInterval = setInterval(() => {
        currentMessageIndex.value = (currentMessageIndex.value + 1) % loadingMessages.value.length;
    }, 3000);
};

const stopMessageRotation = () => {
    if (messageInterval) {
        clearInterval(messageInterval);
        messageInterval = null;
    }
};

// Keep all other existing methods...
const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const addGroup = () => {
    if (groups.value.length < 10) {
        groups.value.push({
            name: "",
            sections: [],
            newSectionName: "",
            sectionError: false,
            isEditing: false,
            editingName: ''
        });
        buttonDisabled.value.noRooms = false;
    }
};

const removeGroup = (groupIndex: number) => {
    groups.value.splice(groupIndex, 1);
    if (getTotalSectionCount() === 0) {
        buttonDisabled.value.noRooms = true;
    }
};

const addSection = (groupIndex: number) => {
    const group = groups.value[groupIndex];
    if (group.sections.length < 15) {
        group.sections.push("");
        buttonDisabled.value.noRooms = false;
    }
};

const removeSection = (groupIndex: number, sectionIndex: number) => {
    groups.value[groupIndex].sections.splice(sectionIndex, 1);
    if (getTotalSectionCount() === 0) {
        buttonDisabled.value.noRooms = true;
    }
};

const handlePaste = (event: ClipboardEvent) => {
    if (!event.clipboardData) return;
    const pastedText = event.clipboardData.getData("text");
    if (pastedText.length > 80) {
        popupStore.showPopup(
            "Briefly describe the topic you wish to learn about in up to 80 characters.</br>Add other info into the <b>Extra</b> field."
        );
    }
};

const selectInputText = (event: FocusEvent) => {
    if (event.target instanceof HTMLInputElement) {
        event.target.select();
    }
};

const handleFileUpload = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
        const file = input.files[0];
        if (file.size > 15 * 1024 * 1024) {
            popupStore.showPopup("File size must be less than 15MB");
            if (fileInput.value) fileInput.value.value = '';
            return;
        }
        selectedFile.value = file;
    }
};

const hasStepErrors = (step: 'basics' | 'structure' | 'settings') => {
    // Only show errors if validation has been attempted
    if (!validationAttempted.value) return false;

    const payload = {
        topic: topic.value,
        visibility: isPublic.value,
        selectedFile: selectedFile.value,
        groups: groups.value.map(g => ({
            name: g.name,
            sections: g.sections.filter(s => s.trim() !== "")
        })).filter(g => g.name.trim() !== "")
    }

    try {
        formSchema.parse(payload)
        return false
    } catch (e) {
        if (e instanceof z.ZodError) {
            const errors = e.format()

            switch (step) {
                case 'basics':
                    return !!(errors.topic?._errors?.length || errors.selectedFile?._errors?.length)
                case 'structure':
                    return !!(errors.groups?._errors?.length ||
                        (errors.groups && typeof errors.groups === 'object' &&
                            Object.keys(errors.groups).some(key => key !== '_errors')))
                case 'settings':
                    return false
                default:
                    return false
            }
        }
    }
    return false
}

const hasPreviousStepErrors = computed(() => {
    // Only show errors if validation has been attempted
    if (!validationAttempted.value) return false;
    return hasStepErrors('basics') || hasStepErrors('structure')
})

const getStepErrorSummary = (step: 'basics' | 'structure') => {
    // Only show errors if validation has been attempted
    if (!validationAttempted.value) return '';

    const payload = {
        topic: topic.value,
        visibility: isPublic.value,
        selectedFile: selectedFile.value,
        groups: groups.value.map(g => ({
            name: g.name,
            sections: g.sections.filter(s => s.trim() !== "")
        })).filter(g => g.name.trim() !== "")
    }

    try {
        formSchema.parse(payload)
        return ''
    } catch (e) {
        if (e instanceof z.ZodError) {
            const errors = e.format()

            switch (step) {
                case 'basics':
                    const basicErrors = []
                    if (errors.topic?._errors?.length) basicErrors.push('Course name')
                    if (errors.selectedFile?._errors?.length) basicErrors.push('Course material')
                    return basicErrors.join(', ')
                case 'structure':
                    const structureErrors = []
                    if (errors.groups?._errors?.length) structureErrors.push('Topics required')
                    if (errors.groups && typeof errors.groups === 'object') {
                        const hasGroupErrors = Object.keys(errors.groups).some(key => key !== '_errors')
                        if (hasGroupErrors) structureErrors.push('Topic/subtopic names')
                    }
                    return structureErrors.join(', ')
                default:
                    return ''
            }
        }
    }
    return ''
}

const removeFile = () => {
    selectedFile.value = null;
    if (fileInput.value) fileInput.value.value = '';
};

const getTotalSectionCount = () => {
    return groups.value.reduce((total, group) => total + group.sections.length, 0);
};

const resetErrors = () => {
    formattedErrors.value = {} as any
};

function validateForm(data: unknown) {
    resetErrors()
    validationAttempted.value = true;
    try {
        formSchema.parse(data)
        return true
    } catch (e) {
        if (e instanceof z.ZodError) {
            formattedErrors.value = e.format()
        }
        return false
    }
}

// Keep existing handleSubmit function...
async function handleSubmit() {
    
    const payload = {
        topic: topic.value,
        visibility: isPublic.value,
        selectedFile: selectedFile.value,
        groups: groups.value.map(g => ({
            name: g.name,
            sections: g.sections.filter(s => s.trim() !== "")
        })).filter(g => g.name.trim() !== "")
    }
    
    if (!validateForm(payload)) {
        return
    }

    buttonDisabled.value.isSubmitting = true;
    startMessageRotation(); // Start rotating messages
    
    const formData = new FormData();

    if (selectedFile.value) {
        formData.append("selectedFile", selectedFile.value);
    }

    payload.groups.forEach((group, index) => {
        formData.append(`groupNames[${index}]`, group.name);
        group.sections.forEach(section => {
            formData.append(`groupSections[${index}][]`, section);
        });
    });

    formData.append("topic", topic.value);
    formData.append("language", "English");
    formData.append("extraContext", "");
    formData.append("languageDifficulty", "Normal");
    formData.append("libraryDifficulty", libraryDifficulty.value);
    formData.append("guide", "Azalea");
    formData.append("visibility", isPublic.value.toString());

    if (selectedFile.value) {
        formData.append("selectedFile", selectedFile.value);
    }

    axios
        .post("/api/library/generate", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
        .then((response) => {
            const libraryId = response.data.library_data.id;
            router.push(`/lessons/${libraryId}`);
        })
        .catch((error) => {
            console.error("Error:", error);
            if (error.response && error.response.status === 403) {
                popupStore.showPopup(
                    "You have reached the limit.</br>Please login to continue."
                );
                router.push("/login");
            }
            if (
                error.response &&
                error.response.status === 400 &&
                error.response.data &&
                error.response.data.error
            ) {
                popupStore.showPopup(error.response.data.error);
            }
        })
        .finally(() => {
            buttonDisabled.value.isSubmitting = false;
            stopMessageRotation(); // Stop rotating messages
        });
};

onMounted(() => {
    libraryDifficulty.value = "Normal";
});

onUnmounted(() => {
    stopMessageRotation(); // Clean up interval on component unmount
});

</script>

<style scoped>

/* Header */
.header-section {
    text-align: center;
    margin-bottom: 3rem;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.75rem;
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}

.main-subtitle {
    font-size: 1.1rem;
    color: var(--text-color-secondary);
    margin: 0;
}

/* Stepper Navigation */
.stepper-nav {
    margin-bottom: 3rem;
}

.stepper-container {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    position: relative;
    max-width: 600px;
    margin: 0 auto;
}

.stepper-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    flex: 1;
}

.step-circle {
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.75rem;
    border: 2px solid rgba(26, 139, 127, 0.3);
    background: var(--background-color-1);
    color: var(--text-color-secondary);
    transition: all 0.3s ease;
    position: relative;
    z-index: 2;
}

.step-circle.active {
    background: var(--color-primary);
    border-color: var(--color-primary);
    color: var(--text-color);
    box-shadow: 0 0 0 4px rgba(26, 139, 127, 0.2);
    transform: scale(1.1);
}

.step-circle.completed {
    background: var(--color-primary);
    border-color: var(--color-primary);
    color: var(--text-color);
}

.step-circle.pending {
    background: var(--background-color-1);
    border-color: rgba(26, 139, 127, 0.2);
    color: var(--text-color-secondary);
}

.check-icon {
    font-size: 1.2rem;
    font-weight: bold;
}

.step-number {
    font-size: 1rem;
    font-weight: 600;
}

.step-info {
    text-align: center;
    max-width: 120px;
    background-color: var(--background-color);
}

.step-title {
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
    color: var(--text-color-secondary);
    transition: color 0.3s ease;
}

.step-description {
    font-size: 0.75rem;
    color: var(--text-color-secondary);
    opacity: 0.7;
    line-height: 1.3;
}

.step-info.active .step-title,
.step-info.completed .step-title {
    color: var(--text-color);
}

.step-info.active .step-description {
    opacity: 1;
}

.step-connector {
    position: absolute;
    top: 1.5rem;
    left: calc(50% + 1.5rem);
    right: calc(-50% + 1.5rem);
    height: 2px;
    background: rgba(26, 139, 127, 0.2);
    z-index: 1;
    transition: background-color 0.3s ease;
}

.step-connector.completed {
    background: var(--color-primary);
}

/* Keep all existing form styles */
.step-content {
    margin-bottom: 2rem;
}

.section-card {
    background: rgba(26, 139, 127, 0.05);
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid rgba(26, 139, 127, 0.1);
}

.card-header {
    margin-bottom: 2rem;
    text-align: center;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--text-color);
}

.section-description {
    color: var(--text-color-secondary);
    margin: 0;
}

/* Form Elements */
.form-group {
    margin-bottom: 1.5rem;
}

.form-label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-color);
}

.form-input {
    width: 100%;
    padding: 0.875rem 1rem;
    border: 1px solid rgba(26, 139, 127, 0.3);
    border-radius: 8px;
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    font-size: 1rem;
    transition: all 0.2s;
}

.form-input:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(26, 139, 127, 0.2);
}

.form-input.error {
    border-color: var(--error-color);
}

.input-hint {
    font-size: 0.875rem;
    color: var(--text-color-secondary);
    margin-top: 0.5rem;
}

.error-text {
    color: var(--error-color);
    font-size: 0.875rem;
    margin-top: 0.5rem;
}

/* File Upload */
.file-upload-area {
    border: 2px dashed rgba(26, 139, 127, 0.3);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    background: rgba(26, 139, 127, 0.05);
}

.file-upload-area:hover {
    border-color: var(--color-primary);
    background: rgba(26, 139, 127, 0.1);
}

.file-upload-area.has-file {
    border-style: solid;
    background: rgba(26, 139, 127, 0.1);
}

.file-input {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
}

.upload-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.upload-icon {
    font-size: 3rem;
}

.upload-text {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.upload-main {
    font-weight: 600;
    color: var(--text-color);
}

.upload-sub {
    font-size: 0.875rem;
    color: var(--text-color-secondary);
}

.selected-file-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    background: var(--background-color-1);
    border-radius: 8px;
}

.file-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.file-icon {
    font-size: 2rem;
}

.file-details {
    display: flex;
    flex-direction: column;
}

.file-name {
    font-weight: 600;
    color: var(--text-color);
}

.file-size {
    font-size: 0.875rem;
    color: var(--text-color-secondary);
}

.remove-file {
    background: none;
    border: none;
    color: var(--text-color-secondary);
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 4px;
    transition: all 0.2s;
}

.remove-file:hover {
    color: var(--error-color);
    background: rgba(255, 0, 0, 0.1);
}

/* Example Card */
.example-card {
    background: rgba(26, 139, 127, 0.1);
    border: 1px solid rgba(26, 139, 127, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
}

.example-header {
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--color-primary);
}

.example-topic {
    color: var(--text-color);
}

.example-subtopics {
    margin-left: 1rem;
    margin-top: 0.5rem;
    color: var(--text-color-secondary);
}

/* Topics and Subtopics */
.topics-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.topic-card {
    background: var(--background-color-1);
    border: 1px solid rgba(26, 139, 127, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
}

.topic-header {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.topic-input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid rgba(26, 139, 127, 0.3);
    border-radius: 8px;
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    font-weight: 600;
    font-size: 1.1rem;
}

.topic-input:focus {
    outline: none;
    border-color: var(--color-primary);
}

.topic-input.error {
    border-color: var(--error-color);
}

.remove-topic-btn {
    background: none;
    border: none;
    color: var(--text-color-secondary);
    cursor: pointer;
    padding: 0.75rem;
    border-radius: 6px;
    transition: all 0.2s;
}

.remove-topic-btn:hover {
    color: var(--error-color);
    background: rgba(255, 0, 0, 0.1);
}

.subtopics-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.subtopic-item {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

.subtopic-input {
    flex: 1;
    padding: 0.625rem;
    border: 1px solid rgba(26, 139, 127, 0.3);
    border-radius: 6px;
    background: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
}

.subtopic-input:focus {
    outline: none;
    border-color: var(--color-primary);
}

.remove-subtopic-btn {
    background: none;
    border: none;
    color: var(--text-color-secondary);
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 4px;
    transition: all 0.2s;
}

.remove-subtopic-btn:hover {
    color: var(--error-color);
    background: rgba(255, 0, 0, 0.1);
}

.add-subtopic-btn {
    width: 100%;
    padding: 0.75rem;
    border: 1px dashed rgba(26, 139, 127, 0.5);
    border-radius: 8px;
    background: transparent;
    color: var(--color-primary);
    cursor: pointer;
    transition: all 0.2s;
}

.add-subtopic-btn:hover:not(:disabled) {
    background: rgba(26, 139, 127, 0.1);
    border-style: solid;
}

.add-subtopic-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.add-topic-btn {
    width: 100%;
    padding: 2rem;
    border: 2px dashed rgba(26, 139, 127, 0.3);
    border-radius: 12px;
    background: transparent;
    color: var(--text-color-secondary);
    cursor: pointer;
    font-size: 1.1rem;
    transition: all 0.2s;
}

.add-topic-btn:hover:not(:disabled) {
    color: var(--color-primary);
    border-color: var(--color-primary);
    background: rgba(26, 139, 127, 0.05);
}

.add-topic-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.structure-hints {
    margin-top: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.hint {
    font-size: 0.875rem;
    color: var(--text-color-secondary);
    text-align: center;
}

/* Visibility Settings */
.visibility-section {
    margin-bottom: 2rem;
}

.visibility-toggle {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 0.75rem;
}

.visibility-option {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    border: 2px solid rgba(26, 139, 127, 0.2);
    border-radius: 12px;
    background: rgba(26, 139, 127, 0.05);
    cursor: pointer;
    transition: all 0.2s;
}

.visibility-option:hover {
    border-color: var(--color-primary);
    background: rgba(26, 139, 127, 0.1);
}

.visibility-option.active {
    border-color: var(--color-primary);
    background: rgba(26, 139, 127, 0.2);
}

.option-icon {
    font-size: 1.5rem;
}

.option-content {
    text-align: left;
}

.option-title {
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 0.25rem;
}

.option-desc {
    font-size: 0.875rem;
    color: var(--text-color-secondary);
}

/* Create Button */
.create-section {
    margin-top: 2rem;
    text-align: center;
}

.create-button {
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
    color: var(--text-color);
    border: none;
    padding: 1rem 2.5rem;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    min-width: 200px;
}

.create-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(26, 139, 127, 0.3);
}

.create-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

.button-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
}

.spinner {
    width: 1rem;
    height: 1rem;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* Navigation */
.navigation-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2rem;
}

.nav-spacer {
    flex: 1;
}

.nav-button {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}

.nav-button.primary {
    background: var(--color-primary);
    color: var(--text-color);
    border: none;
}

.nav-button.primary:hover {
    background: var(--color-primary-dark);
    transform: translateY(-1px);
}

.nav-button.secondary {
    background: transparent;
    color: var(--text-color-secondary);
    border: 1px solid rgba(26, 139, 127, 0.3);
}

.nav-button.secondary:hover {
    color: var(--text-color);
    border-color: var(--color-primary);
    background: rgba(26, 139, 127, 0.1);
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .stepper-container {
        flex-direction: column;
        gap: 2rem;
        align-items: stretch;
    }

    .stepper-item {
        flex-direction: row;
        align-items: center;
        gap: 1rem;
        text-align: left;
    }

    .step-circle {
        margin-bottom: 0;
        flex-shrink: 0;
    }

    .step-info {
        text-align: left;
        max-width: none;
        flex: 1;
    }

    .step-connector {
        display: none;
    }

    .main-title {
        font-size: 2rem;
    }

    .visibility-toggle {
        grid-template-columns: 1fr;
    }

    .topic-header {
        flex-direction: column;
        gap: 0.5rem;
    }

    .remove-topic-btn {
        align-self: flex-end;
    }
}

.step-circle.error {
    background: var(--error-color);
    border-color: var(--error-color);
    color: white;
}

.step-info.error .step-title {
    color: var(--error-color);
}

.error-icon {
    font-size: 1.2rem;
    font-weight: bold;
}

.error-indicator {
    color: var(--error-color);
    font-size: 0.75rem;
}

/* Error Summary */
.error-summary {
    background: rgba(255, 59, 48, 0.1);
    border: 1px solid rgba(255, 59, 48, 0.3);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
}

.error-summary-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.error-title {
    font-weight: 600;
    color: var(--error-color);
}

.error-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.error-item {
    display: flex;
    gap: 0.5rem;
    padding: 0.75rem;
    background: rgba(255, 59, 48, 0.05);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.error-item:hover {
    background: rgba(255, 59, 48, 0.1);
}

.error-step {
    font-weight: 600;
    color: var(--error-color);
}

.error-details {
    color: var(--text-color-secondary);
}

/* Loading overlay */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--background-color);
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
}

.loading-content {
    width: 100%;
    max-width: 500px;
    text-align: center;
    padding: 2rem;
}

/* Set explicit dimensions for the Lottie animation */
.loading-content :deep(svg) {
    width: 100% !important;
    height: auto !important;
    max-height: 300px;
}

/* Loading messages styles */
.loading-messages {
    margin-top: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.loading-message {
    font-size: 1.1rem;
    color: var(--text-color-secondary);
    font-weight: 500;
}

/* Fade transition for messages */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.8s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

</style>