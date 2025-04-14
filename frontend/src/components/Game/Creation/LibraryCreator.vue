<template>
    <div class="library-gen-page">
        <div class="form-container" @keydown.enter="handleSubmit">
            <h1 v-if="libgenRoute">Create a Course to Explore</h1>
            <!-- Topic Selection -->
            <div class="libgen-create">
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
                            Topic can only have spaces or letters.
                        </div>
                        <div v-if="topicSpaceError" class="error-message">
                            Topic must not start or end with a space.
                        </div>
                    </div>
                </div>

                <!-- Hidden Sections -->
                <div class="libgen-section">
                    <div class="libgen-section">

                        <!-- File Upload Section -->
                        <div class="form-group file-upload">
                            <div class="libgen-title">Upload File</div>
                            <div class="file-input-container">
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

                    <!-- Room Names Section -->
                    <div class="form-group room-names">
                        <div class="libgen-title">
                            Section Names
                        </div>
                        <div class="room-input-container">
                            <div class="room-input-wrapper">
                                <input type="text" v-model="newRoomName" placeholder="Enter section names"
                                    :class="{ 'input-error': roomError || roomTypingError || roomSpaceError }"
                                    maxlength="40" :disabled="roomNames.length >= 30 || disableExtras"
                                    @keyup.enter="addRoom" />
                                <button class="add-room-btn" @click="addRoom"
                                    :disabled="!newRoomName.trim() || roomNames.length >= 30 || disableExtras">
                                    Add
                                </button>
                            </div>
                            <div class="room-count" v-if="roomNames.length > 0">
                                {{ roomNames.length }}/30 rooms
                            </div>
                            <div class="room-chips">
                                <div v-for="(room, index) in roomNames" :key="index" class="room-chip">
                                    {{ room }}
                                    <button class="remove-room-btn" @click="removeRoom(index)">×</button>
                                </div>
                            </div>
                            <div class="helper-text">
                                🐙 Sections are how course content is divided up.
                            </div>
                            <div class="helper-text">
                                🐙 We try to make the content of each section based on its name, so if a section is named "mitosis" the content of that section is based on mitosis, etc...
                            </div>
                            <div class="helper-text">
                                🐙 Don't worry about adding all rooms or files now - you can generate more later!
                            </div>
                        </div>
                    </div>

                </div>
            </div>

            <!-- CTA Button -->
            <div class="cta-container">
                <CtaButton :buttonText="submitButtonText" @click="handleSubmit"
                    :isSubmitting="buttonDisabled.isSubmitting || buttonDisabled.noRooms" />
            </div>
            <library-browser />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from "axios";
import { storeToRefs } from "pinia";
import {
    startTypingEffect,
    stopTypingEffect,
} from "@/scripts/placeholderTyping";

import { useLibGenStore } from "@/store/libGenStore";
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore } from "@/store/authStore";
import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";
import LibraryBrowser from "./LibraryBrowser.vue";

const route = useRoute();
const router = useRouter();
const libGenStore = useLibGenStore();
const authStore = useAuthStore();
const popupStore = usePopupStore();

const { languages, topics } = storeToRefs(libGenStore);

const topic = ref("");
const topicError = ref(false);
const topicTypingError = ref(false);
const topicSpaceError = ref(false);
const roomError = ref(false);
const roomTypingError = ref(false);
const roomSpaceError = ref(false);
const safeTopics = ref([
    "Innovative breakdance moves",
    "How to identify misinformation",
    "Origins of the Olympic games",
]);
const libraryDifficulty = ref("Normal");
const buttonDisabled = ref({
    noRooms: true,
    isSubmitting: false,
});
const selectedFile = ref<File | null>(null);
const newRoomName = ref("");
const roomNames = ref<string[]>([]);
const typingInterval = ref<number | null>(null);
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

const addRoom = () => {
    const trimmedName = newRoomName.value.trim();
    if (trimmedName && roomNames.value.length < 30) {
        roomError.value = false;
        roomTypingError.value = !/^[a-zA-Z ]+$/.test(trimmedName);
        if (roomTypingError.value) {
            return;
        }
        roomSpaceError.value = trimmedName[0] === " " || trimmedName[trimmedName.length - 1] === " ";
        if (roomSpaceError.value) {
            return;
        }
        roomNames.value.push(trimmedName);
        buttonDisabled.value.noRooms = false;
        newRoomName.value = "";
    }
};

const removeRoom = (index: number) => {
    roomNames.value.splice(index, 1);
    if (roomNames.value.length === 0) {
        buttonDisabled.value.noRooms = true; // disables submit button until roomNames is not empty (must have room names to submit)
    }
};

const handleSubmit = () => {
    if (!authStore.loggedIn) {
        // must login to submit
        popupStore.showPopup(
            "Please login to continue."
        );
        return;
    }

    if (topic.value.trim() === "") {
        topicError.value = true;
        return;
    }
    topicError.value = false;
    topicTypingError.value = !/^[a-zA-Z ]+$/.test(topic.value);
    if (topicTypingError.value) {
        return;
    }
    topicSpaceError.value = topic.value[0] === " " || topic.value[topic.value.length - 1] === " ";
    if (topicSpaceError.value) {
        return;
    }

    if (roomNames.value.length === 0) {
        roomError.value = true;
        return;
    }
    for (let roomName of roomNames.value) {
        if (roomName.trim() === "") {
            roomError.value = true;
            return;
        }
    }
    roomError.value = false;
    roomTypingError.value = roomNames.value.some(roomName => !/^[a-zA-Z ]+$/.test(roomName));
    if (roomTypingError.value) {
        return;
    }
    roomSpaceError.value = roomNames.value.some(roomName => roomName[0] === " " || roomName[roomName.length - 1] === " ");
    if (roomSpaceError.value) {
        return;
    }

    const urlPattern =
        /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)$/;
    if (urlPattern.test(topic.value)) {
        popupStore.showPopup(
            "We do not currently support links.</br>Try entering the topic of the website instead.</br>Note: This app can teach you about anything, but will not do your homework!"
        );
        return;
    }

    buttonDisabled.value.isSubmitting = true;

    const formData = new FormData();

    formData.append("topic", topic.value);
    formData.append("language", "English");
    formData.append("extraContext", ""); // TODO delete later (from backend and library model)
    formData.append("languageDifficulty", "Normal"); // TODO delete later (from backend and library model)
    formData.append("libraryDifficulty", libraryDifficulty.value);
    formData.append("guide", "Azalea"); // TODO delete later (from backend and library model)
    if (selectedFile.value) {
        formData.append("selectedFile", selectedFile.value);
    }
    roomNames.value.forEach(room => formData.append("roomNames", room));

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
        typingInterval.value = startTypingEffect(
            topicInput.value,
            computedTopics.value
        );
    } else {
        //console.log("never started");
    }
});

onUnmounted(() => {
    if (typingInterval.value) {
        stopTypingEffect(typingInterval.value);
    }
});
</script>

<style scoped>
.library-gen-page {
    display: flex;
    justify-content: flex-start;  /* Align content at the top */
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
    max-width: 720px;
    margin: 0 auto;
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
    font-size: 0.8em;
    margin-top: 0.5em;
}

.option {
    background: #00000000;
    opacity: 0.8;
    color: var(--highlight-color);
}

input[type="text"]::placeholder {
    color: var(--highlight-color);
}

.input {
    background-color: var(--background-color);
    margin-left: 2px;
    margin-right: 2px;
}

.form-container input[type="text"] {
    background-color: var(--background-color);
    border: 1px solid var(--element-color-1);
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
}

.cta-container {
    width: 100%;
    max-width: 720px;
    margin: 0 auto;
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
    border: 1px solid var(--element-color-1);
    border-radius: 4px;
    background-color: var(--background-color);
}

.selected-file {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5em;
    background-color: var(--background-color);
    border: 1px solid var(--element-color-1);
    border-radius: 4px;
    font-size: 0.9em;
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

.room-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5em;
}

.room-chip {
    display: flex;
    align-items: center;
    gap: 0.5em;
    padding: 4px 8px;
    background-color: var(--element-color-1);
    border-radius: 16px;
    font-size: 0.9em;
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
</style>