<template>
    <div class="library-gen-page">
      <div class="form-container" @keydown.enter="handleSubmit">
        <h1 v-if="libgenRoute">Create a Library to Explore</h1>
        <!-- Topic Selection -->
        <div class="libgen-create">
          <div class="libgen-section">
            <div class="form-group topic-selection">
              <div class="libgen-title">Course name</div>
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
          
          <!-- Hidden Sections -->
            <div class="libgen-section">
              <div class="libgen-section">
  
              <!-- File Upload Section -->
              <div class="form-group file-upload">
                <div class="libgen-title">Upload File</div>
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
              </div>
  
            <!-- Room Names Section -->
              <div class="form-group room-names">
                <div class="libgen-title">Room Names</div>
                <div class="room-input-container">
                  <div class="room-input-wrapper">
                    <input
                      type="text"
                      v-model="newRoomName"
                      placeholder="Enter room name"
                      :class="{ 'input-error': roomError }"
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
                <div v-if="roomError" class="error-message">
                    Please specify a room.
                </div>
              </div>

            </div>
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
  import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";
  import LibraryBrowser from "./LibraryBrowser.vue";3

  export default {
    name: "LibraryCreator",
    components: { CtaButton, LibraryBrowser },
    data() {
      return {
        topic: "",
        topicError: false,
        roomError: false,
        safeTopics: [
          "Innovative breakdance moves",
          "How to identify misinformation",
          "Origins of the Olympic games",
        ],
        libraryDifficulty: "",
        isSubmitting: false,
        selectedFile: null,
        newRoomName: "",
        roomNames: [],
      };
    },
    mounted() {
      this.libraryDifficulty = "Easy";
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
        return this.isSubmitting ? "Loading (~45s)" : "Explore!";
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
        this.roomNames.push(trimmedName);
        this.newRoomName = "";
        }
      },
        removeRoom(index) {
        this.roomNames.splice(index, 1);
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
          console.log("topicError")
          return;
        }
        this.topicError = false;
        if (this.roomNames.length === 0) {
          this.roomError = true;
          return;
        }
        this.roomError = true;
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

       const formData = new FormData();

        formData.append("topic", this.topic);
        formData.append("language", "English");
        formData.append("extraContext", ""); // TODO delete later (from backend and library model)
        formData.append("languageDifficulty", "Normal"); // TODO delete later (from backend and library model)
        formData.append("libraryDifficulty", this.libraryDifficulty);
        formData.append("guide", "Azalea"); // TODO delete later (from backend and library model)
        formData.append("selectedFile", this.selectedFile); // TODO textbook, could easily add support for > 1 input file later
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