<template>
    <div class="library-gen-page">
        <div class="form-container" @keydown.enter="handleSubmit">
            <!-- Topic Selection -->
            <div class="libgen-create p-16 br-4" style="border: 1px solid var(--text-color); border-radius: 5px;">
                <h1 v-if="libgenRoute">Create a Course to Explore</h1>
                <div class="libgen-section">
                    <div class="form-group topic-selection">
                        <div class="libgen-title">Course name</div>
                        <div class="title-bar">
                            <input type="text" id="topicInput" ref="topicInput" v-model="topic"
                                :class="{ 'input-error': topicError || topicTypingError || topicSpaceError }"
                                placeholder="What to learn about" maxlength="100" @focus="selectInputText"
                                @paste="handlePaste" />
                        </div>
                        <!-- Error Message -->
                        <div v-if="topicError" class="error-message">
                            Please enter a topic.
                        </div>
                        <div v-if="topicTypingError" class="error-message">
                            Topic can only have spaces or letters and must be at least 4 characters long.
                        </div>
                        <div v-if="topicSpaceError" class="error-message">
                            Topic must not start or end with a space.
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
                                    :disabled="disableExtras" accept=".pdf" />
                                <div v-if="selectedFile" class="selected-file">
                                    Selected: {{ selectedFile.name }}
                                    <button class="remove-file-btn" @click="removeFile">×</button>
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
                                    <input type="text" v-model="newGroupName" placeholder="Enter unit/chapter name"
                                        :class="{ 'input-error': groupError || groupTypingError || groupSpaceError || groupEmptyError }"
                                        maxlength="40" :disabled="disableExtras" @keyup.enter="addGroup" />
                                    <button class="add-btn" @click="addGroup"
                                        :disabled="!newGroupName.trim() || groups.length >= 10 || disableExtras">
                                        Add Unit
                                    </button>
                                </div>
                                <div class="error-container">
                                    <div v-if="groupError" class="error-message">Please enter a valid unit name.</div>
                                    <div v-if="groupTypingError" class="error-message">Unit name can only have spaces or
                                        letters and must be at least 4 characters long.</div>
                                    <div v-if="groupSpaceError" class="error-message">Unit name must not start or end
                                        with a space.</div>
                                    <div v-if="groupEmptyError" class="error-message">Must have at least one Unit</div>

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
                                                    @click="removeSection(groupIndex, sectionIndex)">×</button>
                                            </div>
                                        </div>

                                        <!-- Section input for this group -->
                                        <div class="section-input-wrapper">
                                            <input type="text" v-model="group.newSectionName"
                                                placeholder="Enter section name"
                                                :class="{ 'input-error': groupNoSectionErrors[groupIndex] || groupSectionNamingErrors[groupIndex] }"
                                                maxlength="40" :disabled="group.sections.length >= 15 || disableExtras"
                                                @keyup.enter="addSection(groupIndex)" />
                                            <button class="add-btn" @click="addSection(groupIndex)"
                                                :disabled="!group.newSectionName?.trim() || group.sections.length >= 15 || disableExtras">
                                                Add Section
                                            </button>
                                        </div>
                                        <div class="error-container">
                                            <div v-if="groupNoSectionErrors[groupIndex]" class="error-message">
                                                Every Unit must have at least one section
                                            </div>
                                            <div v-if="groupSectionNamingErrors[groupIndex]" class="error-message">
                                                Section names must only have letters or spaces and must be at least 4 characters long.
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>


                            <div class="helper-text">
                                🐙 Structure your course with units/chapters and sections for better organization.
                            </div>
                            <div class="helper-text">
                                🐙 You can create up to 10 units, with up to 15 sections each.
                            </div>
                            <div class="helper-text">
                                🐙 Don't worry about adding everything now - you can add more later!
                            </div>
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
import { ref, reactive, watch, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from "axios";
import { storeToRefs } from "pinia";
import {
    useTypingEffect,
} from "@/scripts/placeholderTyping";


import { useLibGenStore } from "@/store/libGenStore";
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore } from "@/store/authStore";
import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";
import LibraryBrowser from "./LibraryBrowser.vue";


// New or modified data for groups
interface Group {
    name: string;
    sections: string[];
    newSectionName: string;
    sectionError: boolean;
}


const route = useRoute();
const router = useRouter();
const libGenStore = useLibGenStore();
const authStore = useAuthStore();
const popupStore = usePopupStore();
// New refs for groups
const groups = ref<Group[]>([]);
const groupNoSectionErrors = ref<boolean[]>([])
const groupSectionNamingErrors = ref<boolean[]>([])
const newGroupName = ref("");
const groupError = ref(false);
const groupTypingError = ref(false);
const groupSpaceError = ref(false);
const groupEmptyError = ref(false);

const { topics } = storeToRefs(libGenStore);

watch(
    () => groups.value.length,
    (len) => {
        groupNoSectionErrors.value = Array(len).fill(false)
    },
    { immediate: true }
)

watch(
  () => groups.value.length,
  (len) => {
    groupNoSectionErrors.value      = Array(len).fill(false);
    groupSectionNamingErrors.value  = Array(len).fill(false);
  },
  { immediate: true }
);

const typingEffectStop = ref(() => { });
const topic = ref("");
const topicError = ref(false);
const topicTypingError = ref(false);
const topicSpaceError = ref(false);
const safeTopics = ref([
    "Engineering 101",
    "Materials Science",
    "Health and Fitness",
]);
const libraryDifficulty = ref("Normal");
const buttonDisabled = ref({
    noRooms: true,
    isSubmitting: false,
});
const selectedFile = ref<File | null>(null);
const topicInput = ref<HTMLInputElement | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);


// Computed properties
const computedTopics = computed(() => {
    return topics.value.length > 0 ? topics.value : safeTopics.value;
});


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
        
        groupError.value = false;
        groupTypingError.value = !/^[a-zA-Z ]+$/.test(trimmedName) || trimmedName.length < 4;
        
        if (groupTypingError.value) {
            return;
        }
        
        groupSpaceError.value = trimmedName[0] === " " || trimmedName[trimmedName.length - 1] === " ";
        
        if (groupSpaceError.value) {
            return;
        }

        groups.value.push({
            name: trimmedName,
            sections: [],
            newSectionName: "",
            sectionError: false
        });

        buttonDisabled.value.noRooms = false;
        groupEmptyError.value = false;
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

    groupSectionNamingErrors.value[groupIndex] = false;

    if (trimmedName && group.sections.length < 15) {
        group.sectionError = false;


        // Validate section name
        const typingError = !/^[a-zA-Z ]+$/.test(trimmedName) || trimmedName.length < 4;
        const spaceError = trimmedName[0] === " " || trimmedName[trimmedName.length - 1] === " ";

        if (typingError || spaceError) {
            groupSectionNamingErrors.value[groupIndex] = true;
            return;
    }
    
    groupNoSectionErrors.value[groupIndex] = false;
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

const hasErrors = (): boolean => {

    if (!authStore.loggedIn) {
        // must login to submit
        popupStore.showPopup(
            "Please login to continue."
        );
        return true;
    }

    buttonDisabled.value.isSubmitting = true;

    if (topic.value.trim() === "") {
        topicError.value = true;
        return true;
    }

    topicError.value = false;

    topicTypingError.value = !/^[a-zA-Z ]+$/.test(topic.value) || topic.value.length < 4;

    if (topicTypingError.value) {
        return true;
    }

    topicSpaceError.value = topic.value[0] === " " || topic.value[topic.value.length - 1] === " ";
    if (topicSpaceError.value) {
        return true;
    }

    const urlPattern =
        /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)$/;
    if (urlPattern.test(topic.value)) {
        popupStore.showPopup(
            "We do not currently support links.</br>Try entering the topic of the website instead.</br>Note: This app can teach you about anything, but will not do your homework!"
        );
        return true;
    }


    // Check if there are groups and sections
    if (groups.value.length === 0) {
        groupEmptyError.value = true;
        return true;
    }

    groupEmptyError.value = false;

    groupNoSectionErrors.value = groups.value.map(g => g.sections.length === 0)

    if (groupNoSectionErrors.value.some(err => err)) {
        return true;
    }

    if (groupSectionNamingErrors.value.some(err => err)) {
        return true;
    }

    // Validate all group and section names
    for (const group of groups.value) {
        if (group.name.trim() === "" || group.sections.length === 0) {
            return true;
        }


        for (const section of group.sections) {
            if (section.trim() === "" || !/^[a-zA-Z ]+$/.test(section) ||
                section[0] === " " || section[section.length - 1] === " ") {
                return true;
            }
        }
    }

    return false;

}

const handleSubmit = () => {

    if (hasErrors()) {
        popupStore.showPopup("Please check all unit and section names.");
        buttonDisabled.value.isSubmitting = false;
        return;
    }

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
    if (computedTopics.value.length > 0 && topicInput.value) {
        const { start, stop } = useTypingEffect(topicInput.value, computedTopics.value);
        typingEffectStop.value = stop; // Store the stop function
        start();
    } else {
        //console.log("never started");
    }
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