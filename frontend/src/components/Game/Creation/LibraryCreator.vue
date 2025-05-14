<template>
    <div class="library-gen-page p-8">
        <div class="form-container" @keydown.enter="handleSubmit">

            <!-- Topic Selection -->
            <div class="libgen-create p-16 br-4" style="border: 1px solid var(--text-color); border-radius: 5px;">
                <h1 v-if="libgenRoute">Create a Course to Explore</h1>
                <div class="libgen-section">
                    <div class="form-group topic-selection">

                        <div class="libgen-title">Course name</div>
                        <div class="title-bar">
                            <input type="text" id="topicInput" ref="topicInput" v-model="topic"
                                :class="{ 'input-error': formattedErrors.topic?._errors?.length }"
                                placeholder="Mrs. Frizzle's science class, Biology 272, etc..." maxlength="100"
                                @focus="selectInputText" @paste="handlePaste" />
                        </div>
                        <div v-if="formattedErrors.topic?._errors?.length" class="error-message">
                            {{ formattedErrors.topic._errors[0] }}
                        </div>
                    </div>
                </div>

                <div class="libgen-section">
                    <div class="libgen-section">

                        <!-- File Upload Section -->
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
                                    🐙 Only accepting .pdf files that are 500kb or less for now - we're still building!
                                </div>
                            </div>
                        </div>
                    </div>


                    <!-- Room Names Section with Groups -->
                    <div class="form-group room-names">
                        <div class="libgen-title">
                            Course Structure
                        </div>
                        <div class="room-input-container">
                            <!-- Group controls -->
                            <div class="group-controls">

                                <div class="group-input-wrapper">
                                    <input type="text" v-model="newGroupName" placeholder="Exam 1, Exam 2, etc..."
                                        maxlength="40" :disabled="disableExtras" @keyup.enter="addGroup" />
                                    <button class="add-btn" @click="addGroup"
                                        :disabled="!newGroupName.trim() || groups.length >= 10 || disableExtras">
                                        Add Unit
                                    </button>
                                </div>

                                <div v-if="formattedErrors.groups?._errors?.length" class="error-message">
                                    {{ formattedErrors.groups._errors[0] }}
                                </div>
                            </div>

                            <!-- Groups list -->
                            <div class="groups-container">
                                <div v-for="(group, groupIndex) in groups" :key="groupIndex" class="group-item">

                                    <div class="group-header">
                                        <div class="group-title">{{ group.name }}</div>
                                        <div class="group-actions">
                                            <span class="section-count">{{ group.sections.length }} sections</span>
                                            <button class="remove-btn" @click="removeGroup(groupIndex)">×</button>
                                        </div>
                                    </div>


                                    <!-- Sections for this group -->
                                    <div class="group-sections">
                                        <div class="section-chips">
                                            <div v-for="(section, sectionIndex) in group.sections" :key="sectionIndex"
                                                class="section-chip">
                                                {{ section }}
                                                <button class="remove-section-btn"
                                                @click="removeSection(groupIndex, sectionIndex)">×
                                            </button>
                                            </div>
                                        </div>

                                        <!-- Section input for this group -->
                                        <div class="section-input-wrapper">
                                            <input type="text" v-model="group.newSectionName"
                                                placeholder="Mitosis, Derivative Rule, etc..." maxlength="40"
                                                :disabled="group.sections.length >= 15 || disableExtras"
                                                :class="{ 'input-error': formattedErrors.groups?.[groupIndex]?.sections?._errors?.length }"
                                                @keyup.enter="addSection(groupIndex)" />
                                            <button class="add-btn" @click="addSection(groupIndex)"
                                                :disabled="!group.newSectionName?.trim() || group.sections.length >= 15 || disableExtras">
                                                Add Section
                                            </button>
                                        </div>
                                        <div v-if="formattedErrors.groups?.[groupIndex]?.name?._errors?.length"
                                            class="error-message">
                                            {{ formattedErrors.groups[groupIndex].name._errors[0] }}
                                        </div>

                                        <div v-if="formattedErrors.groups?.[groupIndex]?.sections?._errors?.length"
                                            class="error-message">
                                            {{ formattedErrors.groups[groupIndex].sections._errors[0] }}
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="helper-text">
                            🐙 You can create up to 10 units, with up to 15 sections each.
                        </div>
                        <div class="helper-text">
                            🐙 Don't worry about adding everything now - you can add more later!
                        </div>
                    </div>
                </div>

                <!-- Public/Private Toggle -->
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

                <!-- CTA Button -->
                <div class="cta-container">
                    <CtaButton :buttonText="submitButtonText" @click="handleSubmit"
                        :isSubmitting="buttonDisabled.isSubmitting || buttonDisabled.noRooms" />
                </div>
            </div>
            <library-browser />
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
import LibraryBrowser from "./LibraryBrowser.vue";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

// New or modified data for groups
interface Group {
    name: string;
    sections: string[];
    newSectionName: string;
    sectionError: boolean;
}
import { z } from "zod";

// Define schemas for your form
const sectionSchema = z.string()
    .min(4, "Section names must be at least 4 characters")
    .max(25, "Section names must be at most 25 characters")
    .refine(val => !val.startsWith(" ") && !val.endsWith(" "),
        "Section names must not start or end with a space");

const groupSchema = z.object({
    name: z.string()
        .min(4, "Unit names must be at least 4 characters")
        .max(25, "Unit names must be at most 25 characters")
        .refine(val => !val.startsWith(" ") && !val.endsWith(" "),
            "Unit names must not start or end with a space"),
    sections: z.array(z.string())
        .min(1, "Every Unit must have at least one section")
        .superRefine((sections, ctx) => {
            // Check for length issues first
            const lengthIssues = sections.some(
                section => section.length < 4 || section.length > 25
            );
            
            if (lengthIssues) {
                ctx.addIssue({
                    code: z.ZodIssueCode.custom,
                    message: "All section names must be between 4 and 25 characters"
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
                    message: "Section names must not start or end with a space"
                });
                return;
            }
            
            // Check duplicates within a unit
            if (sections.length !== new Set(sections.map(s => s.toLowerCase())).size) {
                ctx.addIssue({
                    code: z.ZodIssueCode.custom,
                    message: "Duplicate section names are not allowed within a unit"
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
    selectedFile: z.instanceof(File, { message: "Must have at least one file" }),
    groups: z.array(groupSchema)
        .min(1, "Must have at least one Unit")
        .refine(
            groups => {
                const names = groups.map(g => g.name.toLowerCase());
                return names.length === new Set(names).size;
            },
            "Duplicate unit names are not allowed"
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
const newGroupName = ref("");

const libgenRoute = computed(() => {
    return route.path === "/library";
});

const submitButtonText = computed(() => {
    if (buttonDisabled.value.isSubmitting) {
        return "Loading (~45s)";
    }
    else if (buttonDisabled.value.noRooms) {
        return "Add at least one room to get started!";
    }
    else {
        return "Explore!";
    }
    // return isSubmitting ? isSubmitting.isEmpty ? "hi there" : "Loading (~45s)" : "Explore!";
});


const disableExtras = computed(() => {
    return !authStore.loggedIn;
});

// Methods for group management
const addGroup = () => {

    const trimmedName = newGroupName.value.trim();

    if (trimmedName && groups.value.length < 10) {

        groups.value.push({
            name: trimmedName,
            sections: [],
            newSectionName: "",
            sectionError: false
        });

        buttonDisabled.value.noRooms = false;
        newGroupName.value = "";
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
    const trimmedName = group.newSectionName.trim();

    if (trimmedName && group.sections.length < 15) {

        group.sections.push(trimmedName);
        group.newSectionName = "";
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

    const payload = {
        topic: topic.value,
        visibility: isPublic.value,
        selectedFile: selectedFile.value,
        groups: groups.value.map(g => ({
            name: g.name,
            sections: g.sections
        }))
    }

    if (!validateForm(payload)) return

    // Flatten groups and sections into the format expected by your API
    const formData = new FormData();

    if (selectedFile.value) {
        formData.append("selectedFile", selectedFile.value);
    }

    // Add group structure data
    groups.value.forEach((group, index) => {
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
    /* Align content at the top */
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
    color: red;
    font-size: 1em;
    margin-top: 0.5em;
}


.option {
    background: #00000000;
    opacity: 0.8;
    color: var(--highlight-color);
}


input[type="text"]::placeholder {
    color: var(--text-color);
    opacity: 0.65;
}


.input {
    margin-left: 2px;
    margin-right: 2px;
}

.form-container input[type="text"] {
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid var(--text-color);
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
}

select {
    padding: 10px;
    border: 1px solid var(--element-color-1);
}

input[type="text"] {
    padding: 8px;
    /* background: var(--background-color-1t); */
}

.cta-container {
    display: block;
    width: fit-content;
    margin: 1em auto 0;
}


.toggle-button {
    margin-left: 0;
    color: var(--text-color);
    opacity: 0.7;
    background: none;
    border: none;
    font-size: 0.8em;
    cursor: pointer;
}


.file-upload {
    margin-bottom: 2em;
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


.room-input-container {
    display: flex;
    flex-direction: column;
    gap: 0.5em;
    margin-bottom: 1em;
}


.room-input-wrapper {
    display: flex;
    gap: 0.5em;
}


.room-input-wrapper input {
    flex-grow: 1;
}


.add-room-btn {
    padding: 8px 16px;
    background-color: var(--element-color-1);
    border: none;
    border-radius: 4px;
    color: var(--text-color);
    cursor: pointer;
}


.add-room-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}


.room-count {
    font-size: 0.8em;
    opacity: 0.7;
    text-align: right;
}

.remove-room-btn {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    padding: 0;
    font-size: 1.2em;
    opacity: 0.7;
    display: flex;
    align-items: center;
    justify-content: center;
}

.remove-room-btn:hover {
    opacity: 1;
}

.helper-text {
    font-size: 0.8em;
    opacity: 0.7;
    margin-top: 0.5em;
    text-align: center;
    color: var(--text-color);
}


/* New styles for groups */
.group-controls {
    margin-bottom: 16px;
}


.section-heading {
    font-size: 0.9em;
    font-weight: 600;
    margin-bottom: 8px;
    color: var(--text-color);
}


.group-input-wrapper {
    display: flex;
    gap: 0.5em;
}

.group-input-wrapper input {
    flex-grow: 1;
}

.add-btn {
    padding: 8px 16px;
    background-color: var(--element-color-1);
    border: none;
    border-radius: 4px;
    color: var(--text-color);
    cursor: pointer;
    white-space: no-wrap;
}

.add-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.error-container {
    margin-top: 4px;
}

.groups-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 16px;
}


.group-item {
    border: 1px solid var(--text-color);
    border-radius: 8px;
    padding: 12px;
}


.group-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}


.group-title {
    font-weight: 600;
    font-size: 1em;
}


.group-actions {
    display: flex;
    align-items: center;
    gap: 12px;
}


.section-count {
    font-size: 0.8em;
    opacity: 0.7;
}


.remove-btn {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    font-size: 1.2em;
    opacity: 0.7;
    display: flex;
    align-items: center;
    justify-content: center;
}


.remove-btn:hover {
    opacity: 1;
}


.group-sections {
    display: flex;
    flex-direction: column;
    gap: 12px;
}


.section-input-wrapper {
    display: flex;
    gap: 0.5em;
    border: var(--text-color);
}


.section-input-wrapper input {
    flex-grow: 1;
}


.section-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 8px;
}


.section-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    background-color: var(--element-color-1);
    border-radius: 16px;
    font-size: 0.85em;
}


.remove-section-btn {
    background: none;
    border: none;
    color: var(--text-color);
    cursor: pointer;
    padding: 0;
    font-size: 1.1em;
    opacity: 0.7;
    display: flex;
    align-items: center;
    justify-content: center;
}


.remove-section-btn:hover {
    opacity: 1;
}
</style>