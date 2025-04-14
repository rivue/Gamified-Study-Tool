<template>
    <div class="quiz-container">
      <div
        v-for="(question, index) in questions"
        :key="index"
        :class="['quiz-question', { 'disabled-question': quizSubmitted }]"
      >
        <p>{{ question.text }}</p>
        <div v-if="isMultipleChoice(question)" class="choices">
          <label
            v-for="(choice, choiceIndex) in question.choices"
            :key="`q-${index}-choice-${choiceIndex}`"
            :class="{
              'selected-choice': userAnswers[index] === choice,
              'unselected-choice': userAnswers[index] !== choice,
              'disabled-choice': quizSubmitted,
            }"
          >
            <input
              type="radio"
              :name="`question-${index}`"
              :value="choice"
              v-model="userAnswers[index]"
              class="quiz-radio"
              :disabled="quizSubmitted"
            />
            <span :class="getRadioDotClass(index, choice)"></span>
            {{ choice }}
          </label>
        </div>
        <div v-else class="true-false">
          <label
            v-for="choice in ['True', 'False']"
            :key="`q-${index}-${choice}`"
            :class="{
              'selected-choice': userAnswers[index] === choice,
              'unselected-choice': userAnswers[index] !== choice,
              'disabled-choice': quizSubmitted,
            }"
          >
            <input
              type="radio"
              :name="`question-${index}`"
              :value="choice"
              v-model="userAnswers[index]"
              class="quiz-radio"
              :disabled="quizSubmitted"
            />
            <span :class="getRadioDotClass(index, choice)"></span>
            {{ choice }}
          </label>
        </div>
      </div>
    </div>
    <div v-if="isScore" class="score-display">
      <p class="centered-score">Quiz score: {{ scoreText }}%</p>
    </div>
    <button
      v-else
      @click="submitQuiz"
      :disabled="!isFormValid() || quizSubmitted"
    >
      {{ submitText }}
    </button>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, watch, onUnmounted } from 'vue';
  import { useInputStore } from "@/store/inputStore";
  import { useMessageStore } from "@/store/messageStore";
  import { useRouter } from 'vue-router';
  
  // Types
  interface QuestionResult {
    userAnswer: string;
    isCorrect: boolean;
  }
  
  interface Question {
    text: string;
    choices?: string[];
    type: 'multiple-choice' | 'true-false';
    correctAnswer: string | boolean;
  }
  
  interface QuizData {
    [key: string]: {
      text: string;
      correct_choice?: string;
      wrong_choices?: string[];
      answer?: boolean;
    };
  }
  
  interface QuizResult {
    score: number;
    answers: (string | null)[];
  }
  
  // Props
  const props = defineProps<{
    rawQuizData: string;
  }>();
  
  // State
  const questions = ref<Question[]>([]);
  const userAnswers = ref<(string | null)[]>([]);
  const submitText = ref('Submit');
  const quizSubmitted = ref(false);
  const isScore = ref(false);
  const scoreText = ref('');
  
  // Store
  const inputStore = useInputStore();
  const messageStore = useMessageStore();
  const router = useRouter();
  
  // Computed
  const isAnyOptionSelected = computed(() => {
    return userAnswers.value.some((answer) => answer !== null);
  });
  
  const questionResults = computed(() => {
    return questions.value.map((question, index) => {
      const userAnswer = userAnswers.value[index];
      const userAnswerStr = userAnswer !== null ? userAnswer.toString().toLowerCase() : '';
      const correctAnswerStr = question.correctAnswer.toString().toLowerCase();
      const isCorrect = userAnswerStr === correctAnswerStr;
      return { userAnswer: userAnswerStr, isCorrect } as QuestionResult;
    });
  });
  
  const sending = computed(() => {
    return messageStore.sending;
  });
  
  // Methods
  const isMultipleChoice = (question: Question): boolean => {
    return question.type === 'multiple-choice';
  };
  
  const isFormValid = (): boolean => {
    return userAnswers.value.every((answer) => answer !== null);
  };
  
  const parseQuizQuestions = (content: string): void => {
    let extractedAnswers: QuizResult | null = null;
    const contentParts = content.split(' | ');
    
    if (contentParts.length >= 2) {
      try {
        extractedAnswers = JSON.parse(contentParts[0]) as QuizResult;
        if (extractedAnswers && extractedAnswers.score && extractedAnswers.answers) {
          isScore.value = true;
          scoreText.value = extractedAnswers.score.toString();
          quizSubmitted.value = true;
        } else {
          throw new Error('Invalid quiz data format');
        }
  
        content = contentParts[1];
      } catch (e) {
        console.error('Error parsing quiz data:', e);
      }
    } else {
      inputStore.hide();
    }
  
    let quizData: QuizData;
    try {
      quizData = JSON.parse(content) as QuizData;
    } catch (e) {
      console.error('Error parsing quiz content:', e);
      return;
    }
  
    questions.value = Object.keys(quizData).map((key, index) => {
      const questionObj = quizData[key];
      userAnswers.value[index] = quizSubmitted.value && extractedAnswers
        ? extractedAnswers.answers[index]
        : null;
        
      const hasWrongChoices = 'wrong_choices' in questionObj;
  
      if (hasWrongChoices && questionObj.wrong_choices) {
        let choices = [
          questionObj.correct_choice as string,
          ...questionObj.wrong_choices,
        ];
        shuffleArray(choices);
        return {
          text: questionObj.text,
          choices: choices,
          correctAnswer: questionObj.correct_choice as string,
          type: 'multiple-choice',
        } as Question;
      } else {
        return {
          text: questionObj.text,
          correctAnswer: questionObj.answer as boolean,
          type: 'true-false',
        } as Question;
      }
    });
  };
  
  const shuffleArray = (array: string[]): void => {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  };
  
  const checkAnswers = async (): Promise<void> => {
    let correctCount = 0;
    
    questions.value.forEach((question, index) => {
      let userAnswer = typeof userAnswers.value[index] === 'boolean'
        ? userAnswers.value[index]?.toString()
        : userAnswers.value[index];
        
      let correctAnswer = typeof question.correctAnswer === 'boolean'
        ? question.correctAnswer.toString()
        : question.correctAnswer as string;
  
      if (question.type === 'true-false' && userAnswer) {
        userAnswer = userAnswer.toLowerCase();
        correctAnswer = correctAnswer.toLowerCase();
      }
  
      if (userAnswer === correctAnswer) {
        correctCount++;
      }
    });
  
    const scorePercentage = Math.round(
      (correctCount / questions.value.length) * 100
    );
    
    const jsonData: QuizResult = {
      score: scorePercentage,
      answers: userAnswers.value,
    };
    
    const routePath = router.currentRoute.value.path;
    const response = await messageStore.sendMessage(
      JSON.stringify(jsonData),
      routePath
    );
  
    if (!response || response === 'not sent') {
      console.error('No response or message not sent');
      return;
    } else {
      submitText.value = 'Finished';
      quizSubmitted.value = true;
      if (scorePercentage !== 100) {
        inputStore.show();
      }
    }
  };
  
  const submitQuiz = (): void => {
    if (!quizSubmitted.value) {
      submitText.value = 'Checking answers...';
      checkAnswers();
    }
  };
  
  const getRadioDotClass = (questionIndex: number, choice: string): Record<string, boolean> => {
    const isSubmitted = quizSubmitted.value;
    const isSelected = userAnswers.value[questionIndex] === choice;
    const result = questionResults.value[questionIndex];
    
    if (isSubmitted) {
      if (isSelected) {
        return {
          'radio-dot': true,
          'correct-choice': result.isCorrect,
          'incorrect-choice': !result.isCorrect,
        };
      } else {
        return {
          'radio-dot': true,
          'default-dot': true,
        };
      }
    } else {
      return {
        'radio-dot': true,
        'selected-not-submitted': isSelected,
        'default-dot': !isSelected,
      };
    }
  };
  
  // Lifecycle hooks
  watch(() => props.rawQuizData, (newValue) => {
    if (newValue) {
      parseQuizQuestions(newValue);
    }
  }, { immediate: true });
  
  onUnmounted(() => {
    inputStore.show('unmount');
  });
  </script>
  
  <style scoped>
  .quiz-container {
    position: relative;
    overflow: hidden;
    margin-top: 1rem;
    padding: 0.5rem;
    width: 100%;
    max-width: 100%;
    transition: all 0.3s ease-in-out;
    border-top-right-radius: 10px;
    border-top-left-radius: 10px;
    word-wrap: break-word;
    text-align: left;
  }
  
  .quiz-question {
    margin-bottom: 20px;
    border-bottom: 1px solid var(--element-color-1);
  }
  
  .quiz-question p {
    margin-bottom: 10px;
    font-weight: 700;
  }
  .choices label,
  .true-false label {
    display: block;
    position: relative;
    padding-left: 35px;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 0.9rem;
    user-select: none;
  }
  
  .quiz-radio {
    position: absolute;
    opacity: 0;
    cursor: pointer;
  }
  
  .selected-choice {
    transition: opacity 0.3s;
    opacity: 1;
  }
  
  .unselected-choice {
    transition: opacity 0.3s;
    opacity: 0.8;
  }
  
  button {
    background-color: #4caf50;
    color: var(--text-color);
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  button:hover:not(:disabled) {
    background-color: #45a049;
  }
  
  .disabled-question {
    opacity: 0.8;
    pointer-events: none;
  }
  
  .disabled-choice {
    cursor: not-allowed;
  }
  
  .score-display .centered-score {
    text-align: center;
    font-size: 24px;
  }
  
  .radio-dot {
    position: absolute;
    top: 0;
    left: 0;
    height: 25px;
    width: 25px;
    border-radius: 50%;
    background-color: var(--text-color);
    transition: background-color 0.3s;
  }
  
  .selected-not-submitted {
    background-color: var(--element-color-1);
  }
  
  .correct-choice {
    background-color: #4caf50;
  }
  
  .incorrect-choice {
    background-color: #f44336;
  }
  
  .default-dot {
    background-color: var(--text-color);
  }
  </style>