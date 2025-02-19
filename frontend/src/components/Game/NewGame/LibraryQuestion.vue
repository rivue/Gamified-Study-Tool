<template>
    <transition name="fade">
      <div v-if="questionVisible" class="question-overlay" @click="closeQuestion">
        <div class="question-backdrop">
          <!-- Close (X) button -->
          <div class="close-button" @click.stop="closeQuestion">×</div>
          <!-- Info icon moved to top right -->
          <div class="info-icon">i</div>
          <!-- Completion message when no more questions -->
          <div v-if="question === null" class="completion-message">
            Congratulations, you've completed all questions in this room!
            <!-- TODO: navigate back to home screen automatically here -->
          </div>
          <!-- Question text -->
          <div v-else class="question-content">
            <p v-html="question.text"></p>
          </div>
          <!-- Choices -->
          <div v-if="question !== null" class="choices-container">
            <div v-for="(choice, index) in question.choices" :key="index">
              <button
                :class="{
                  correct: choice === answerState.correct,
                  wrong: choice === answerState.wrong,
                  disabledButton: isDisabled
                }"
                :disabled="isDisabled"
                @click.stop="submitAnswer(choice)"
                v-html="choice"
              ></button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </template>
  
  <script>
  // Script section remains unchanged
  import { useGameStore } from "@/store/gameStore";
  
  export default {
    name: "LibraryQuestion",
    data() {
      return {
        answerState: {
          correct: null,
          wrong: null,
        },
        isDisabled: false,
      };
    },
    methods: {
      shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [array[i], array[j]] = [array[j], array[i]];
        }
      },
      submitAnswer(choice) {
        const store = useGameStore();
        const correct =
          store.factoids[store.currentQuestion].questions[0].correct_choice;
  
        if (correct === choice) {
          this.answerState.correct = choice;
          this.answerState.wrong = null;
        } else {
          this.answerState.wrong = choice;
          this.answerState.correct = null;
          this.isDisabled = true;
          setTimeout(() => {
            this.isDisabled = false;
          }, 1000);
        }
  
        setTimeout(() => {
          if (store.answerAttempt(correct === choice)) {
            this.answerState.wrong = null;
            this.answerState.correct = null;
          } else {
            this.$router.push("/login");
          }
        }, 300);
      },
      closeQuestion() {
        this.$router.push(`/knowledge/${this.$route.params.id}`);
      },
      format(content) {
        let regex;
        regex = /\*\*([^*]*?)\*\*/g;
        content = content.replace(regex, "<strong>$1</strong>");
        regex = /_([^_]*?)_|\*([^*]*?)\*/g;
        content = content.replace(regex, "<em>$1$2</em>");
        return content;
      },
    },
    computed: {
      question() {
        const store = useGameStore();
        if (store.currentQuestion === null) return null;
        const currentFactoid = store.factoids[store.currentQuestion];
  
        if (
          !currentFactoid ||
          !Array.isArray(currentFactoid.questions) ||
          currentFactoid.questions.length === 0
        ) {
          console.error("No questions available or invalid questions format");
          return null;
        }
  
        const currentQuestion = currentFactoid.questions[0];
        if (
          !currentQuestion ||
          !currentQuestion.question_text ||
          !currentQuestion.correct_choice ||
          !Array.isArray(currentQuestion.wrong_choices)
        ) {
          console.log("this is good I think - replace with actual completion message and exit out of room")
          console.error("Question structure is incomplete or invalid");
          return null;
        }
  
        const choices = [
          currentQuestion.correct_choice,
          ...currentQuestion.wrong_choices,
        ];
        this.shuffleArray(choices);
  
        return {
          text: this.format(currentQuestion.question_text),
          choices: choices.map((choice) => this.format(choice)),
        };
      },
      questionVisible() {
        const store = useGameStore();
        return store.questionVisible;
      },
    },
  };
  </script>
  
  <style scoped>
  .completion-message {
    text-align: center;
    font-size: 1.4em;
    color: var(--highlight-color);
  }
  
  .question-overlay {
    position: fixed; /* Changed from absolute to fixed */
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    z-index: 110;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5); /* Added semi-transparent background */
  }
  
  .question-backdrop {
    position: relative;
    background-color: var(--background-haze);
    padding: 2em; /* Increased padding */
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    box-shadow: 0 16px 16px var(--background-color-2t),
      0 -16px 16px var(--background-color-2t);
    width: 80%; /* Set width to 80% of viewport */
    max-width: 800px; /* Maximum width */
    min-height: 60vh; /* Minimum height */
    border-radius: 12px; /* Added rounded corners */
  }
  
  /* New close button styles */
  .close-button {
    position: absolute;
    top: 10px;
    left: 10px;
    width: 30px;
    height: 30px;
    background: rgba(255, 0, 0, 0.8);
    color: white;
    border-radius: 50%;
    text-align: center;
    line-height: 28px;
    font-size: 24px;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .close-button:hover {
    background: rgba(255, 0, 0, 1);
  }
  
  /* Moved info icon to top right */
  .info-icon {
    position: absolute;
    top: 10px;
    right: 10px; /* Changed from left to right */
    width: 30px;
    height: 30px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    text-align: center;
    line-height: 30px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .info-icon:hover {
    background: rgba(255, 255, 255, 0.5);
  }
  
  .question-content {
    text-align: center;
    width: 90%;
    padding: 30px; /* Increased padding */
    border-radius: 12px;
    background-image: linear-gradient(
      to right,
      var(--background-color-2t),
      var(--background-color-1t)
    );
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 111;
    font-size: 1.4em; /* Increased font size */
    margin: 20px 0;
  }
  
  .choices-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px; /* Increased gap */
    width: 90%;
    margin-top: 30px;
  }
  
  button {
    padding: 20px; /* Increased padding */
    width: 100%;
    height: 100%;
    border: none;
    background-color: var(--background-color-1t);
    border: 1px solid var(--background-color-2t);
    font-size: 1.2em; /* Increased font size */
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    transition: all ease 0.2s;
  }
  
  button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  }
  
  button.correct {
    background-color: green;
    color: white;
  }
  
  button.wrong {
    background-color: red;
    color: white;
  }
  
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s;
  }
  
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  
  button.disabledButton {
    pointer-events: none;
    animation: fadeDisable 1s forwards;
  }
  
  @keyframes fadeDisable {
    0% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
    100% {
      opacity: 1;
    }
  }
  
  /* Added responsive design for smaller screens */
  @media (max-width: 768px) {
    .question-backdrop {
      width: 95%;
      padding: 1em;
    }
  
    .choices-container {
      grid-template-columns: 1fr; /* Stack buttons on mobile */
    }
  
    .question-content {
      font-size: 1.2em;
    }
  
    button {
      font-size: 1em;
    }
  }
  </style>