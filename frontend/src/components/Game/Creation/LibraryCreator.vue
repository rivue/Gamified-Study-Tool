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
                        <div class="libgen-title">Stepping Stone Names</div>
                        <div class="room-input-container">
                            <div class="room-input-wrapper">
                                <input type="text" v-model="newRoomName" placeholder="Enter stepping stone names"
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
                                🐙 Stepping stone = 1 lecture, textbook chapter, etc...
                            </div>
                            <div class="helper-text" v-if="roomNames.length < 30">
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

<script>
import axios from "axios";
import { mapState } from "pinia";
import {
    startTypingEffect,
    stopTypingEffect,
} from "@/scripts/placeholderTyping.js";

import { useLibGenStore } from "@/store/libGenStore.js";
import { usePopupStore } from "@/store/popupStore.js";
import { useAuthStore } from "@/store/authStore.js";
import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";
import LibraryBrowser from "./LibraryBrowser.vue"; 3

export default {
    name: "LibraryCreator",
    components: { CtaButton, LibraryBrowser },
    data() {
        return {
            topic: "",
            topicError: false,
            topicTypingError: false,
            topicSpaceError: false,
            roomError: false,
            roomTypingError: false,
            roomSpaceError: false,
            safeTopics: [
                "Innovative breakdance moves",
                "How to identify misinformation",
                "Origins of the Olympic games",
            ],
            libraryDifficulty: "",
            buttonDisabled: {
                noRooms: true,
                isSubmitting: false,
            },
            selectedFile: null,
            newRoomName: "",
            roomNames: [],
        };
    },
    mounted() {
        this.libraryDifficulty = "Normal";
        if (this.computedTopics.length > 0 && this.$refs.topicInput) {
            this.typingInterval = startTypingEffect(
                this.$refs.topicInput,
                this.computedTopics
            );
        } else {
            //console.log("never started");
        }
    },
    unmounted() {
        if (this.typingInterval) {
            stopTypingEffect(this.typingInterval);
        }
    },
    computed: {
        computedTopics() {
            return this.topics.length > 0 ? this.topics : this.safeTopics;
        },
        ...mapState(useLibGenStore, {
            languages: (state) => state.languages,
            topics: (state) => state.topics,
        }),
        libgenRoute() {
            return this.$route.path === "/library";
        },
        submitButtonText() {

            if (this.buttonDisabled.isSubmitting) {
                return "Loading (~45s)";
            }
            else if (this.buttonDisabled.noRooms) {
                return "Add at least one room to get started!";
            }
            else {
                return "Explore!";
            }
            // return this.isSubmitting ? this.isSubmitting.isEmpty ? "hi there" : "Loading (~45s)" : "Explore!";
        },
        disableExtras() {
            const authStore = useAuthStore();
            return !authStore.loggedIn;
        },
    },
    methods: {
        handlePaste(event) {
            const pastedText = event.clipboardData.getData("text");
            if (pastedText.length > 80) {
                const popupStore = usePopupStore();
                popupStore.showPopup(
                    "Briefly describe the topic you wish to learn about in up to 80 characters.</br>Add other info into the <b>Extra</b> field."
                );
            }
        },
        selectInputText(event) {
            event.target.select();
        },

        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                if (file.size > 15 * 1024 * 1024) { // 15MB limit
                    const popupStore = usePopupStore();
                    popupStore.showPopup("File size must be less than 15MB");
                    this.$refs.fileInput.value = '';
                    return;
                }
                this.selectedFile = file;
            }
        },

        removeFile() {
            this.selectedFile = null;
            this.$refs.fileInput.value = '';
        },
        addRoom() {
            const trimmedName = this.newRoomName.trim();
            if (trimmedName && this.roomNames.length < 30) {
                this.roomError = false;
                this.roomTypingError = !/^[a-zA-Z ]+$/.test(trimmedName);
                if (this.roomTypingError) {
                    return;
                }
                this.roomSpaceError = trimmedName[0] === " " || trimmedName[trimmedName.length - 1] === " ";
                if (this.roomSpaceError) {
                    return;
                }
                this.roomNames.push(trimmedName);
                this.buttonDisabled.noRooms = false;
                console.log("asd;lfkjasdf")
                this.newRoomName = "";
            }
        },
        removeRoom(index) {
            this.roomNames.splice(index, 1);
            if (this.roomNames.length === 0) {
                this.buttonDisabled.noRooms = true; // disables submit button until roomNames is not empty (must have room names to submit)
            }
        },
        handleSubmit() {
            const authStore = useAuthStore();
            if (!authStore.loggedIn) {

                // must login to submit
                const popupStore = usePopupStore();
                popupStore.showPopup(
                    "Please login to continue."
                );
                return;
            }

            if (this.topic.trim() === "") {
                this.topicError = true;
                return;
            }
            this.topicError = false;
            this.topicTypingError = !/^[a-zA-Z ]+$/.test(this.topic);
            if (this.topicTypingError) {
                return;
            }
            this.topicSpaceError = this.topic[0] === " " || this.topic[this.topic.length - 1] === " ";
            if (this.topicSpaceError) {
                console.log("topic space error");
                return;
            }

            if (this.roomNames.length === 0) {
                this.roomError = true;
                return;
            }
            for (let roomName of this.roomNames) {
                if (roomName.trim() === "") {
                    this.roomError = true;
                    return;
                }
            }
            this.roomError = false;
            this.roomTypingError = this.roomNames.some(roomName => !/^[a-zA-Z ]+$/.test(roomName));
            if (this.roomTypingError) {
                return;
            }
            this.roomSpaceError = this.roomNames.some(roomName => roomName[0] === " " || roomName[roomName.length - 1] === " ");
            if (this.roomSpaceError) {
                console.log("room space error");
                return;
            }

            const urlPattern =
                /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)$/;
            if (urlPattern.test(this.topic)) {
                const popupStore = usePopupStore();
                popupStore.showPopup(
                    "We do not currently support links.</br>Try entering the topic of the website instead.</br>Note: This app can teach you about anything, but will not do your homework!"
                );
                return;
            }

            this.buttonDisabled.isSubmitting = true;

            const formData = new FormData();

            formData.append("topic", this.topic);
            formData.append("language", "English");
            formData.append("extraContext", ""); // TODO delete later (from backend and library model)
            formData.append("languageDifficulty", "Normal"); // TODO delete later (from backend and library model)
            formData.append("libraryDifficulty", this.libraryDifficulty);
            formData.append("guide", "Azalea"); // TODO delete later (from backend and library model)
            formData.append("selectedFile", this.selectedFile);
            this.roomNames.forEach(room => formData.append("roomNames", room));
            //    formData.append("roomNames", JSON.stringify(this.roomNames));  // Convert array to string

            console.log(formData.get("selectedFile"));

            axios
                .post("/api/library/generate", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                })
                .then((response) => {

                    const libraryId = response.data.library_data.id;
                    this.$router.push(`/lessons/${libraryId}`);
                })
                .catch((error) => {
                    console.error("Error:", error);
                    if (error.response && error.response.status === 403) {
                        const popupStore = usePopupStore();
                        popupStore.showPopup(
                            "You have reached the limit.</br>Please login to continue."
                        );
                        this.$router.push("/login");
                    }
                    if (
                        error.response &&
                        error.response.status === 400 &&
                        error.response.data &&
                        error.response.data.error
                    ) {
                        const popupStore = usePopupStore();
                        popupStore.showPopup(error.response.data.error);
                    }
                })
                .finally(() => {
                    this.buttonDisabled.isSubmitting = false;
                });
        },
    },
};
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