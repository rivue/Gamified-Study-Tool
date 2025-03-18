// store/libGenStore.js
import { defineStore } from 'pinia';

export const useLibGenStore = defineStore('libGenStore', {
  state: () => ({
    languages: [
      "English", "Arabic", "Bengali", "Chinese", "Czech", "Danish",
      "Dutch", "Finnish", "French", "German", "Greek", "Hebrew",
      "Hindi", "Hungarian", "Indonesian", "Italian", "Japanese",
      "Korean", "Malay", "Norwegian", "Polish", "Portuguese",
      "Romanian", "Russian", "Spanish", "Swedish", "Thai",
      "Turkish", "Ukrainian", "Vietnamese"
    ],
    "topics": [
      "Biochemistry",
      "Communication",
      "Genetic Engineering",
      "Orbital Mechanics",
      "History of the Internet",
      "Quantum Computing",
      "Ancient Civilizations",
      "Neural Networks",
      "Renewable Energy Systems",
      "Elementary Education",
      "Internet of Things",
      "Dark Matter",
      "Nanotechnology",
      "Biotechnology",
      "Machine Learning",
      "Artificial Intelligence",
      "Climate Change and Global Warming",
      "Psychological Effects of Social Media",
      "Exploring the Deep Ocean",
      "Computer Architechture",
      "Human-Computer Interaction",
      "Biohacking and Human Enhancement",
      "Global Pandemics",
      "The Future of Space Colonization",
      "Blockchain in Industries",
      "Environmental Science",
      "Immunology",
      "Physiology",
      "Green Innovations for Sustainability",
      "Fluid Mechanics",
      "Animals and Their Habitats",
      "Anesthesiology",
      "Pollination",
      "Understanding Weather",
      "History of Famous Inventions",
      "Neuroscience",
      "Linear Algebra",
      "Introduction to Calculus",
      "Physics",
      "AP Human Geography",
      "Philosophy",
      "Classical Literature",
      "Microeconomics",
      "Introduction to Psychology",
      "Biology",
      "Music Theory"
    ]
  }),
  getters: {
    filteredLanguages: (state) => (searchTerm) => {
      if (!searchTerm) {
        return state.languages;
      }
      return state.languages.filter((lang) =>
        lang.toLowerCase().includes(searchTerm.toLowerCase())
      );
    },
    filteredTopics: (state) => (searchTerm) => {
      if (!searchTerm) {
        return state.topics;
      }
      return state.topics.filter((topic) =>
        topic.toLowerCase().includes(searchTerm.toLowerCase())
      );
    },
  },
});
