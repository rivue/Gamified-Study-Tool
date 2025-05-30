<template>
    <div class="library-gen-page p-8">
        <div class="form-container" @keydown.enter="handleSubmit">
            <div class="libgen-create p-16 br-4" style="border: 1px solid var(--text-color); border-radius: 5px;">
                <h1 v-if="libgenRoute">Create a Course to Explore</h1>
                
                <!-- Tab Navigation -->
                <Tabs v-model="currentTab" class="w-full">
                    <TabsList class="grid w-full grid-cols-3 mb-8">
                        <TabsTrigger value="basics">Course & Files</TabsTrigger>
                        <TabsTrigger value="structure">Course Structure</TabsTrigger>
                        <TabsTrigger value="settings">Settings</TabsTrigger>
                    </TabsList>

                    <!-- Tab 1: Course Name and Files -->
                    <TabsContent value="basics" class="space-y-6">
                        <div class="libgen-section">
                            <div class="form-group topic-selection">
                                <div class="libgen-title">Course name</div>
                                <div class="title-bar">
                                    <input type="text" id="topicInput" ref="topicInput" v-model="topic"
                                        :class="{ 'input-error': formattedErrors.topic?._errors?.length }"
                                        placeholder="Mrs. Frizzle's science class, Biology 272, etc..." maxlength="100"
                                        @focus="selectInputText" @paste="handlePaste" />
                                </div>
                                <div class="helper-text">🐙 Note: Course name must be 4-25 characters.</div>
                                <div v-if="formattedErrors.topic?._errors?.length" class="error-message">
                                    {{ formattedErrors.topic._errors[0] }}
                                </div>
                            </div>
                        </div>

                        <div class="libgen-section">
                            <div class="form-group file-upload">
                                <div class="libgen-title">Upload File</div>
                                <div class="file-input-container text-[var(--text-color)] border-[var(--text-color)]">
                                    <input type="file" id="fileInput" ref="fileInput" @change="handleFileUpload"
                                        :class="{ 'input-error': formattedErrors.selectedFile?._errors?.length }"
                                        :disabled="disableExtras" accept=".pdf" />
                                    <div v-if="selectedFile" class="selected-file">
                                        Selected: {{ selectedFile.name }}
                                        <button class="remove-file-btn" @click="removeFile">×</button>
                                    </div>
                                    <div v-if="formattedErrors.selectedFile?._errors?.length" class="error-message">
                                        {{ formattedErrors.selectedFile._errors[0] }}
                                    </div>
                                    <div class="helper-text">
                                        🐙 Required - PDF files only for now, max 500kb. This file will be used to generate
                                        content for your course subtopics.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </TabsContent>

                    <!-- Tab 2: Course Structure -->
                    <TabsContent value="structure" class="space-y-6">
                        <div class="libgen-section">
                            <div class="form-group course-structure">
                                <div class="libgen-title">Course Structure (Topics & Subtopics)</div>
                                <div class="helper-text mb-6">
                                    Define how your course content will be organized. Think of topics as high level concepts
                                    (like "Photosynthesis" or "Calculus Basics") and subtopics as lessons within each topic.
                                    Your uploaded file will be used to generate content for these subtopics.
                                </div>

                                <!-- Example Structure -->
                                <Card class="mb-6 bg-opacity-10 bg-gray-200">
                                    <CardContent class="p-4">
                                        <div class="text-sm mb-2"><strong>Example Structure:</strong></div>
                                        <div class="ml-2">
                                            <div><strong>Topic:</strong> "Cell Biology"</div>
                                            <div class="ml-4 mt-1"><strong>Subtopics:</strong> "Cell Membrane",
                                                "Mitochondria", "Nucleus"</div>
                                        </div>
                                    </CardContent>
                                </Card>

                                <!-- Topic Cards -->
                                <div class="topics-container space-y-4">
                                    <Card v-for="(group, groupIndex) in groups" :key="groupIndex" class="topic-card">
                                        <CardHeader class="pb-3">
                                            <div class="flex items-center justify-between">
                                                <input 
                                                    type="text" 
                                                    v-model="group.name"
                                                    placeholder="Enter topic name..."
                                                    maxlength="40"
                                                    class="topic-name-input flex-1 mr-2"
                                                    :class="{ 'input-error': formattedErrors.groups?.[groupIndex]?.name?._errors?.length }"
                                                />
                                                <button class="remove-btn" @click="removeGroup(groupIndex)">×</button>
                                            </div>
                                            <div v-if="formattedErrors.groups?.[groupIndex]?.name?._errors?.length" class="error-message">
                                                {{ formattedErrors.groups[groupIndex].name._errors[0] }}
                                            </div>
                                        </CardHeader>
                                        
                                        <CardContent class="pt-0">
                                            <!-- Subtopics -->
                                            <div class="subtopics-section">
                                                <div v-if="group.sections.length > 0" class="subtopics-list space-y-2 mb-3">
                                                    <div v-for="(section, sectionIndex) in group.sections" :key="sectionIndex"
                                                        class="subtopic-item">
                                                        <input 
                                                            type="text" 
                                                            v-model="group.sections[sectionIndex]"
                                                            placeholder="Enter subtopic name..."
                                                            maxlength="40"
                                                            class="subtopic-input flex-1"
                                                        />
                                                        <button class="remove-section-btn" @click="removeSection(groupIndex, sectionIndex)">×</button>
                                                    </div>
                                                </div>
                                                
                                                <!-- Add Subtopic Button -->
                                                <button 
                                                    class="add-subtopic-btn w-full"
                                                    @click="addSection(groupIndex)"
                                                    :disabled="group.sections.length >= 15 || disableExtras"
                                                >
                                                    + Add Subtopic
                                                </button>
                                                
                                                <div v-if="formattedErrors.groups?.[groupIndex]?.sections?._errors?.length" class="error-message mt-2">
                                                    {{ formattedErrors.groups[groupIndex].sections._errors[0] }}
                                                </div>
                                            </div>
                                        </CardContent>
                                    </Card>

                                    <!-- Add Topic Button -->
                                    <Card class="add-topic-card">
                                        <CardContent class="p-4">
                                            <button 
                                                class="add-topic-btn w-full"
                                                @click="addGroup"
                                                :disabled="groups.length >= 10 || disableExtras"
                                            >
                                                + Add Topic
                                            </button>
                                        </CardContent>
                                    </Card>
                                </div>

                                <div v-if="formattedErrors.groups?._errors?.length" class="error-message">
                                    {{ formattedErrors.groups._errors[0] }}
                                </div>

                                <div class="helper-text">
                                    🐙 You can create up to 10 topics, with up to 15 subtopics each.
                                </div>
                                <div class="helper-text">
                                    🐙 Don't worry about adding everything now - you can add more later!
                                </div>
                            </div>
                        </div>
                    </TabsContent>

                    <!-- Tab 3: Settings -->
                    <TabsContent value="settings" class="space-y-6">
                        <div class="libgen-section">
                            <div class="form-group visibility-toggle p-4">
                                <div style="font-size:0.8em; opacity:0.7; display:flex; justify-content:center; align-items:center;"
                                    class="mb-2">Visibility</div>
                                <div class="flex items-center justify-center w-full mb-3">
                                    <Tabs v-model="visibilityTab" class="w-full max-w-[400px]">
                                        <TabsList class="grid w-full grid-cols-2 p-1 py-0.5"
                                            style="background-color: rgba(var(--element-color-1-rgb), 0.5);">
                                            <TabsTrigger value="private"
                                                class="border-0 data-[state=inactive]:opacity-50 data-[state=active]:bg-[var(--element-color-1)] data-[state=active]:text-[var(--text-color)]">
                                                Private
                                            </TabsTrigger>
                                            <TabsTrigger value="public"
                                                class="border-0 data-[state=inactive]:opacity-50 data-[state=active]:bg-[var(--element-color-1)] data-[state=active]:text-[var(--text-color)]">
                                                Public
                                            </TabsTrigger>
                                        </TabsList>
                                    </Tabs>
                                </div>
                                <div class="helper-text">
                                    🐙 Public courses will appear in the course library for all users to explore.
                                </div>
                                <div class="helper-text">
                                    🐙 Private courses need a code to join.
                                </div>
                            </div>
                        </div>
                        <div class="cta-container mt-8">
                            <CtaButton :buttonText="submitButtonText" @click="handleSubmit"
                                :isSubmitting="buttonDisabled.isSubmitting || buttonDisabled.noRooms" />
                        </div>
                    </TabsContent>
                </Tabs>

                <!-- CTA Button -->
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from "axios";

import { usePopupStore } from "@/store/popupStore";
import { useAuthStore } from "@/store/authStore";
import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader } from "@/components/ui/card";


// New or modified data for groups
interface Group {
    name: string;
    sections: string[];
    newSectionName: string;
    sectionError: boolean;
    isEditing?: boolean;
    editingName?: string;
}
import { z } from "zod";

// Define schemas for your form
const sectionSchema = z.string()
    .min(4, "Subtopic names must be at least 4 characters")
    .max(25, "Subtopic names must be at most 25 characters")
    .refine(val => !val.startsWith(" ") && !val.endsWith(" "),
        "Subtopic names must not start or end with a space");

const groupSchema = z.object({
    name: z.string()
        .min(4, "Topic names must be at least 4 characters")
        .max(25, "Topic names must be at most 25 characters")
        .refine(val => !val.startsWith(" ") && !val.endsWith(" "),
            "Topic names must not start or end with a space"),
    sections: z.array(z.string())
        .min(1, "Every Topic must have at least one section")
        .superRefine((sections, ctx) => {
            // Check for length issues first
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

            // Check for whitespace
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

            // Check duplicates within a topic
            if (sections.length !== new Set(sections.map(s => s.toLowerCase())).size) {
                ctx.addIssue({
                    code: z.ZodIssueCode.custom,
                    message: "Duplicate subtopic names are not allowed within a topic"
                });
            }
        })
});

// Create schema for the entire form
const formSchema = z.object({
    topic: z.string()
        .min(4, "Course name must be at least 4 characters")
        .max(25, "Course name must be at most 25 characters")
        .refine(val => !val.startsWith(" ") && !val.endsWith(" "),
            "Course name must not start or end with a space"),
    visibility: z.boolean(),
    selectedFile: z.instanceof(File, { message: "Must have at least one file - we wouldn't know what to generate!" }),
    groups: z.array(groupSchema)
        .min(1, "Must have at least one Topic")
        .refine(
            groups => {
                const names = groups.map(g => g.name.toLowerCase());
                return names.length === new Set(names).size;
            },
            "Duplicate topic names are not allowed"
        )
});
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const popupStore = usePopupStore();
// New refs for groups
const groups = ref<Group[]>([]);
const typingEffectStop = ref(() => { });
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

const libgenRoute = computed(() => {
    return route.path === "/create";
});

const submitButtonText = computed(() => {
    if (buttonDisabled.value.isSubmitting) {
        return "Loading (~60s)";
    }
    else if (buttonDisabled.value.noRooms) {
        return "Add at least one Topic to generate a course";
    }
    else {
        return "Generate Course";
    }
});

const disableExtras = computed(() => {
    return !authStore.loggedIn;
});

// Methods for group management
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

// Methods for section management
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

// Methods
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
        if (file.size > 15 * 1024 * 1024) { // 15MB limit
            popupStore.showPopup("File size must be less than 15MB");
            if (fileInput.value) fileInput.value.value = '';
            return;
        }
        selectedFile.value = file;
    }
};

const removeFile = () => {
    selectedFile.value = null;
    if (fileInput.value) fileInput.value.value = '';
};

// Helper function to count total sections across all groups
const getTotalSectionCount = () => {
    return groups.value.reduce((total, group) => total + group.sections.length, 0);
};

const resetErrors = () => {
    formattedErrors.value = {} as any
};

function validateForm(data: unknown) {
    resetErrors()
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

async function handleSubmit() {
    buttonDisabled.value.isSubmitting = true;

    const payload = {
        topic: topic.value,
        visibility: isPublic.value,
        selectedFile: selectedFile.value,
        groups: groups.value.map(g => ({
            name: g.name,
            sections: g.sections.filter(s => s.trim() !== "") // Filter out empty sections
        })).filter(g => g.name.trim() !== "") // Filter out groups with empty names
    }

    if (!validateForm(payload)) {
        buttonDisabled.value.isSubmitting = false;
        return
    }

    // Flatten groups and sections into the format expected by your API
    const formData = new FormData();

    if (selectedFile.value) {
        formData.append("selectedFile", selectedFile.value);
    }

    // Add group structure data
    payload.groups.forEach((group, index) => {
        formData.append(`groupNames[${index}]`, group.name);
        group.sections.forEach(section => {
            formData.append(`groupSections[${index}][]`, section);
        });
    });

    formData.append("topic", topic.value);
    formData.append("language", "English");
    formData.append("extraContext", ""); // TODO delete later (from backend and library model)
    formData.append("languageDifficulty", "Normal"); // TODO delete later (from backend and library model)
    formData.append("libraryDifficulty", libraryDifficulty.value);
    formData.append("guide", "Azalea"); // TODO delete later (from backend and library model)
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
        });
};

// Lifecycle hooks
onMounted(() => {
    libraryDifficulty.value = "Normal";
});

onUnmounted(() => {
    typingEffectStop.value();
});
</script>

<style scoped>
.library-gen-page {
    display: flex;
    justify-content: flex-start;
    display: flex;
    flex-direction: column;
    width: 100%;
}

.libgen-section {
    width: 100%;
}

.form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    width: 100%;
    max-width: 1000px;
    margin: 0 auto;
    padding: 1em;
}

.libgen-create {
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin: 0 auto;
    background: var(--background-color-1t);
}

.form-group {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-bottom: 1em;
}

.libgen-title {
    margin-left: 1em;
    margin-bottom: -0.125em;
    font-size: 0.8em;
    opacity: 0.7;
}

.title-bar {
    display: flex;
    flex-direction: row;
    align-items: baseline;
}

.input-error {
    border-color: red;
}

.error-message {
    color: var(--error-color);
    font-size: 1em;
    margin-top: 0.5em;
}

input[type="text"]::placeholder {
    color: var(--text-color);
    opacity: 0.65;
}

.form-container input[type="text"] {
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid var(--text-color);
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
    padding: 8px;
}

.cta-container {
    display: block;
    width: fit-content;
    margin: 1em auto 0;
}

.file-input-container {
    display: flex;
    flex-direction: column;
    gap: 0.5em;
}

.file-input-container input[type="file"] {
    padding: 8px;
    border: 1px solid var(--text-color);
    border-radius: 4px;
    background-color: rgb(0, 0, 0, 0);
}

.selected-file {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5em;
    border-radius: 4px;
    font-size: 0.9em;
    border: 1px solid var(--text-color);
}

.remove-file-btn {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    padding: 0 0.5em;
    font-size: 1.2em;
    opacity: 0.7;
}

.remove-file-btn:hover {
    opacity: 1;
}

.helper-text {
    font-weight: bold;
    font-size: 0.9em;
    margin-top: 0.5em;
    text-align: center;
    color: var(--text-color);
}

/* New card-based styles */
.topics-container {
    max-width: 100%;
}

.topic-card {
    border: 1px solid var(--text-color);
    background: var(--background-color-1);
}

.topic-name-input {
    background-color: transparent;
    border: 1px solid rgba(var(--text-color-rgb), 0.3);
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 1.1em;
    font-weight: 600;
}

.topic-name-input:focus {
    outline: none;
    border-color: var(--element-color-1);
}

.remove-btn {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    font-size: 1.2em;
    opacity: 0.7;
    padding: 4px 8px;
    border-radius: 4px;
}

.remove-btn:hover {
    opacity: 1;
    background-color: rgba(255, 0, 0, 0.1);
}

.subtopic-item {
    display: flex;
    align-items: center;
    gap: 8px;
}

.subtopic-input {
    background-color: transparent;
    border: 1px solid rgba(var(--text-color-rgb), 0.3);
    border-radius: 4px;
    padding: 6px 10px;
}

.subtopic-input:focus {
    outline: none;
    border-color: var(--element-color-1);
}

.remove-section-btn {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    font-size: 1.1em;
    opacity: 0.7;
    padding: 2px 6px;
    border-radius: 4px;
    flex-shrink: 0;
}

.remove-section-btn:hover {
    opacity: 1;
    background-color: rgba(255, 0, 0, 0.1);
}

.add-subtopic-btn {
    background: var(--element-color-1);
    border: 1px solid rgba(var(--text-color-rgb), 0.3);
    color: var(--text-color);
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.add-subtopic-btn:hover:not(:disabled) {
    background: rgba(var(--element-color-1-rgb), 0.8);
}

.add-subtopic-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.add-topic-card {
    border: 2px dashed rgba(var(--text-color-rgb), 0.3);
    background: transparent;
}

.add-topic-btn {
    background: transparent;
    border: none;
    color: var(--text-color);
    padding: 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1.1em;
    opacity: 0.7;
    transition: opacity 0.2s;
}

.add-topic-btn:hover:not(:disabled) {
    opacity: 1;
    background: rgba(var(--element-color-1-rgb), 0.1);
}

.add-topic-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}
</style>
