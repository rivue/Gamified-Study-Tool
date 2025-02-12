<template>
    <div class="library-gen-page">
      <div class="form-container" @keydown.enter="handleSubmit">
        <h1 v-if="libgenRoute">Create a Library to Explore</h1>
        <!-- Topic Selection -->
        <div class="libgen-create">
          <div class="libgen-section">
            <div class="form-group topic-selection">
              <div class="libgen-title">Topic (What To Learn About)</div>
              <div class="title-bar">
                <input
                  type="text"
                  id="topicInput"
                  ref="topicInput"
                  v-model="topic"
                  :class="{ 'input-error': topicError }"
                  placeholder="What to learn about"
                  maxlength="100"
                  @focus="selectInputText"
                  @paste="handlePaste"
                />
                <button class="randomize-btn" @click="randomizeTopic">🎲</button>
              </div>
              <!-- Error Message -->
              <div v-if="topicError" class="error-message">
                Please enter a topic.
              </div>
            </div>
  
            <div class="form-group difficulty-buttons">
              <div class="button-container">
                <button
                  v-for="level in difficultyLevels"
                  :key="level"
                  :class="{ selected: libraryDifficulty === level }"
                  @click="libraryDifficulty = level"
                  class="difficulty-button"
                >
                  {{ level }}
                </button>
              </div>
            </div>
          </div>
  
          <!-- Toggle Button -->
          <div class="libgen-section">
            <div class="toggle-button-container">
              <button class="toggle-button" @click="toggleDetails">
                <span v-if="!showDetails">▼ Additional options</span>
              </button>
            </div>
          </div>
  
          <!-- Hidden Sections -->
          <transition name="fade">
            <div class="libgen-section" v-if="showDetails">
              <div class="libgen-section">
  
                <!-- Guide -->
                <div class="form-group tutor-button">
                  <div class="libgen-title">Tutor</div>
                  <MenuButton class="tutor-button-button" :label="currentMentorName" @click="changeMentor" />
                </div>
  
              <!-- File Upload Section -->
              <div class="form-group file-upload">
                <div class="libgen-title">Upload File (Optional)</div>
                <div class="file-input-container">
                  <input
                    type="file"
                    id="fileInput"
                    ref="fileInput"
                    @change="handleFileUpload"
                    :disabled="disableExtras"
                    accept=".txt,.pdf,.doc,.docx"
                  />
                  <div v-if="selectedFile" class="selected-file">
                    Selected: {{ selectedFile.name }}
                    <button class="remove-file-btn" @click="removeFile">×</button>
                  </div>
                </div>
              </div>
                <!-- Language -->
                <div class="form-group language-picker">
                  <div class="libgen-title">Language</div>
                  <select id="languageSelect" v-model="language">
                    <option
                      v-for="language in languages"
                      :key="language"
                      :value="language"
                    >
                      {{ language }}
                    </option>
                  </select>
                </div>
                <div class="form-group difficulty-buttons">
                  <div class="button-container">
                    <button
                      v-for="level in difficultyLevels"
                      :key="level"
                      :class="{ selected: languageDifficulty === level }"
                      @click="languageDifficulty = level"
                      class="difficulty-button"
                    >
                      {{ level }}
                    </button>
                  </div>
                </div>
              </div>
  
              <!-- Optional Extra Context -->
              <div class="form-group extra-context">
                <div class="libgen-title">Extra</div>
                <input
                  type="text"
                  id="extraContext"
                  v-model="extraContext"
                  :placeholder="
                    disableExtras ? 'Login to enable' : 'Optional context...'
                  "
                  :disabled="disableExtras"
                />

                 <!-- Room Names Section -->
              <div class="form-group room-names">
                <div class="libgen-title">Room Names (Optional)</div>
                <div class="room-input-container">
                  <div class="room-input-wrapper">
                    <input
                      type="text"
                      v-model="newRoomName"
                      placeholder="Enter room name"
                      maxlength="40"
                      :disabled="roomNames.length >= 30 || disableExtras"
                      @keyup.enter="addRoom"
                    />
                    <button 
                      class="add-room-btn"
                      @click="addRoom"
                      :disabled="!newRoomName.trim() || roomNames.length >= 30 || disableExtras"
                    >
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
                </div>
              </div>

              </div>
            </div>
          </transition>
        </div>
        <!-- CTA Button -->
        <div class="cta-container">
          <CtaButton
            :buttonText="submitButtonText"
            @click="handleSubmit"
            :isSubmitting="isSubmitting"
          />
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
  import { useMentorStore } from "@/store/mentorStore";
  import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";
  import MenuButton from "@/components/Menus/MenuButton.vue";
  import LibraryBrowser from "./LibraryBrowser.vue";3

  export default {
    name: "LibraryCreator",
    components: { CtaButton, LibraryBrowser, MenuButton },
    data() {
      return {
        topic: "",
        topicError: false,
        safeTopics: [
          "Innovative breakdance moves",
          "How to identify misinformation",
          "Origins of the Olympic games",
        ],
        language: "",
        extraContext: "",
        languageDifficulty: "",
        libraryDifficulty: "",
        difficultyLevels: ["Easy", "Normal", "Hard"],
        showDetails: false,
        isSubmitting: false,
        newRoomName: "",
        roomNames: [],
      };
    },
    mounted() {
      this.fetchCurrentMentor();
      this.language = "English";
      this.libraryDifficulty = "Easy";
      this.languageDifficulty = "Normal";
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
        return this.isSubmitting ? "Loading (~10s)" : "Explore!";
      },
      disableExtras() {
        const authStore = useAuthStore();
        return !authStore.loggedIn;
      },
      currentMentorName() {
        const mentorStore = useMentorStore();
        return mentorStore.currentMentor;
      },
    },
    methods: {
      async fetchCurrentMentor() {
        const mentorStore = useMentorStore();
        mentorStore.getCurrentMentorName();
      },
      changeMentor() {
        const mentorStore = useMentorStore();
        mentorStore.show();
        console.log("showins")
      },
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
        this.readFileContent(file);
      }
    },

    removeFile() {
      this.selectedFile = null;
      this.fileContent = null;
      this.$refs.fileInput.value = '';
    },

    readFileContent(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.fileContent = e.target.result;
      };
      reader.readAsText(file);
    },
       addRoom() {
      const trimmedName = this.newRoomName.trim();
      if (trimmedName && this.roomNames.length < 30) {
        this.roomNames.push(trimmedName);
        this.newRoomName = "";
      }
    },
    removeRoom(index) {
      this.roomNames.splice(index, 1);
    },
      handleSubmit() {
        if (this.topic.trim() === "") {
          this.topicError = true;
          return;
        }
        this.topicError = false;
        const urlPattern =
          /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)$/;
        if (urlPattern.test(this.topic)) {
          const popupStore = usePopupStore();
          popupStore.showPopup(
            "We do not currently support links.</br>Try entering the topic of the website instead.</br>Note: This app can teach you about anything, but will not do your homework!"
          );
          return;
        }
        this.isSubmitting = true;
        const postData = {
          topic: this.topic,
          language: this.language,
          extraContext: this.extraContext,
          languageDifficulty: this.languageDifficulty,
          libraryDifficulty: this.libraryDifficulty,
          guide: this.currentMentorName,
          selectedFile: null,
          // fileContent: null,
          fileContent: this.fileContent,
          roomNames: this.roomNames
        };
       
        axios
          .post("/api/library/generate", postData)
          .then((response) => {
            
            const libraryId = response.data.library_data.id;
            this.$router.push(`/library/${libraryId}`);
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
            this.isSubmitting = false;
          });
      },
      randomizeTopic() {
        const randomIndex = Math.floor(Math.random() * this.topics.length);
        this.topic = this.topics[randomIndex];
      },
      toggleDetails() {
        this.showDetails = !this.showDetails;
      },
    },
  };
  </script>
  
  <style scoped>
  .library-gen-page {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
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
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    width: 100%;
    max-width: 720px;
    margin: 0 auto;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    width: 100%;
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
  
  .randomize-btn {
    padding: 0 0.25em;
    font-size: 1.5em;
    background: #00000000;
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
  
  .language-picker select {
    background-color: var(--background-color);
  }
  
  .cta-container {
    margin-top: 2em;
    margin-bottom: 1em;
  }
  
  .button-container {
    display: flex;
    justify-content: space-around;
    flex-direction: row;
    width: 100%;
    margin-bottom: 1em;
    margin-top: 0.25;
  }
  .difficulty-button {
    background: none;
    border: none;
    padding: 0.5em 1em;
    color: var(--highlight-color);
    font-size: 1em;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .difficulty-button.selected {
    color: var(--text-color);
    transform: scale(1.1);
    font-weight: bold;
  }
  
  .extra-context input {
    width: 100%;
  }
  
  .extra-context {
    display: flex;
    flex-direction: column;
  }
  
  .toggle-button-container {
    display: flex;
    align-content: left;
    margin-top: -0.5em;
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
  
  .tutor-button{
    margin-bottom:2em;
  }
  
  .tutor-button-button{
    margin:0 auto;
  }
  
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s;
  }
  
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
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
</style>