// src/store/gameStore.js
import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import { usePopupStore } from "@/store/popupStore.js";
import { useUserStatsStore } from "@/store/userStatsStore";

export const useGameStore = defineStore("gameStore", {
    state: () => ({
        libraryId: null,
        roomStates: {},
        currentRoom: null,
        nextRooms: [],
        factoids: [],
        currentQuestion: 0,
        answeredQuestions: [],
        incorrectQuestionAnswers: [],
        questionVisible: false,
        factoidVisible: null,
        finalTest: false,
        score: 0,
        multiplier: 5,
        showStart: true,
        showNext: false,
        completed: false,
        tutorial: true,
        clicks: 0,
        context: null,
        difficulty: null,
        guide: null,
        imageUrl: null,
        language: null,
        languageDifficulty: null,
        libraryTopic: null,
        likes: 0,
        timer: null,
        timeSpent: 0,
        timerActive: false,
        bestTime: 0,
        completion: 0,
        noGeneratedRooms: false,
        libraryError: false,
    }),
    actions: {
        setId(libraryId) {
            this.resetGameState();
            this.libraryId = libraryId;
        },
        startGame() {
            if (this.timeSpent !== 0) {
                this.hideGameInfo();
                return;
            }
            this.showStart = false;
            this.openRoom(this.libraryTopic);
        },
        hideGameInfo() {
            this.showStart = false;
            this.questionVisible = true;
            this.factoidVisible = null;
        },
        showGameInfo() {
            this.showStart = true;
            this.questionVisible = false;
            this.factoidVisible = null;
        },
        toggleFactoid() {
            if (this.showStart || this.showNext) return;
            if (this.factoidVisible == null) {
                this.questionVisible = false;
                this.factoidVisible = this.currentQuestion;
            } else {
                this.factoidVisible = null;
                this.questionVisible = true;
            }
        },
        answerAttempt(correct) {
            if (correct) {
                this.score += this.multiplier;
                this.multiplier += 1;
                this.currentQuestion += 1;
                if (this.currentQuestion === 2 && !this.finalTest) {
                    console.log("TODO") // TODO this is just a placeholder
                   
                } else if (this.currentQuestion === 2) { // && this.finalTest) {
                    this.questionVisible = false;
                    this.factoidVisible = null;
                    this.endGame();
                    this.completed = true;
                    return true;
                }
            } else {
                const currentFactoid = this.factoids[this.currentQuestion];
                if (!this.incorrectQuestionAnswers.includes(currentFactoid)) {
                    this.incorrectQuestionAnswers.push(currentFactoid);
                }
                if (this.incorrectQuestionAnswers.length >= 4) {
                    const newRoomName = "Revision room " + (Object.keys(this.roomStates).length + 1);
                    if (!this.roomStates[newRoomName]) {
                        // this.roomNames.push(newRoomName);
                        this.roomStates[newRoomName] = {
                            state: 2,
                            factoids: this.incorrectQuestionAnswers.slice()
                        };
                    }
                    this.incorrectQuestionAnswers = [];
                }
                this.multiplier = Math.round(5 + Math.sqrt(Math.max(0, this.multiplier - 5)));
            }
            return true;
        },
        async fetchLibraryDetails(libraryId, roomNameThing) {
            
            this.setId(libraryId);
            
            try {
                const response = await axios.get(`/api/library/${libraryId}`, {params: {library_topic: roomNameThing}});

                // do loadName first in case factoid doesn't exist
                console.log("response: ", response);
                if (response.data.status === "success") {
                    if (response.data.data === null) {
                        // if for some reason roomNameThing is null
                        this.libraryError = true;
                        console.error("Failed to fetch library details", response);
                        return;
                    }
                    const data = response.data.data;
                    this.score = data.score || 0;
                    this.bestTime = data.best_time || 0;
                    this.completion = data.completion || 0;
                    this.clicks = data.clicks || 0;
                    this.context = data.context || null;
                    this.difficulty = data.difficulty || "Normal";
                    this.guide = data.guide || null;
                    this.imageUrl = data.image_url || null;
                    this.language = data.language || "English";
                    this.languageDifficulty = data.language_difficulty || "Normal";
                    // this.libraryTopic = data.library_topic || null;
                    this.libraryTopic = roomNameThing;
                    // console.log("roomNameThing: ", roomNameThing);
                    this.likes = data.likes || 0;
                    this.userId = data.user_id || null;
                    this.tutorial = data.tutorial || false;
                    this.roomStates = {};
                    this.roomStates[this.libraryTopic] = {
                        state: 2,
                        factoids: response.data.room_data.factoids || []
                    };
                    
                    // if (this.tutorial) {
                    //     const popupStore = usePopupStore();
                    //     popupStore.showLibraryInstructions();
                    // }
                    
                } else {
                    this.libraryError = true;
                    console.error("Failed to fetch library details", response);

                }
            } catch (error) {
                this.libraryError = true;
                console.error("Error fetching library details:", error);
            }
        },
        async loadRoom(room_name) {
            try {
                if (this.roomStates[room_name].state !== 1) {
                    console.error(`Trying to load ${room_name} in state ${this.roomStates[room_name].state}.`);
                    return;
                }
                const response = await axios.post("/api/library/room", {
                    libraryId: this.libraryId,
                    subtopic: room_name
                });
                console.log("roomname: ", room_name, "library topic: " , this.libraryTopic)
                if (response.data.status === "success") {
                    this.roomStates[room_name].state = 2;
                    this.roomStates[room_name].factoids = response.data.data.factoids;
                } else {
                    console.error(`Failed to unlock room ${room_name}: ${response.data.message}`);
                    this.roomStates[room_name].state = 0; // forgot what state means, I'm just trying to throw an error message in NextRoomscomponent
                    if (response.data.status === 403) {
                        const popupStore = usePopupStore();
                        popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                        return false;
                    }
                }
            } catch (error) {
                if (error.response && error.response.status === 403) {
                    console.log(error.response);
                    const popupStore = usePopupStore();
                    popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                    return false;
                }
                console.error("Error unlocking room:", error);
            }
            return true;
        },
        openRoom(room_name) {
            if (this.roomStates[room_name].state < 2) {
                console.error(`Opening unloaded room ${room_name}`);
                return;
            }
            this.showNext = false;
            this.currentRoom = room_name;
            this.factoids = this.roomStates[room_name].factoids;
            this.currentQuestion = 0;
            const authStore = useAuthStore();
            authStore.cloudTokens += 1;
            this.questionVisible = true;
            this.roomStates[room_name].state = 3;
            if (room_name === "Final Test Room") {
                this.finalTest = true;
                this.factoids = this.factoids.map(factoid => {
                    return {
                        ...factoid,
                        text: "No cheating lol"
                    };
                });
            }
        },
        endGame() {
            const userStatsStore = useUserStatsStore();
            userStatsStore.resetStats();
            const completedRooms = Object.keys(this.roomStates).filter(
                roomName => this.roomStates[roomName].state === 3
            );
            let data = {
                libraryId: this.libraryId,
                score: this.score,
                time: 500,
                completed: completedRooms
            };
            axios
                .post(`/api/library/end`, data)
                .then(response => {
                    if (response.data.status === "success") {
                        this.completed = true;
                    } else {
                        console.error("Failed to end game:", response.data.message);
                    }
                })
                .catch(error => {
                    console.error("Error sending game end data:", error);
                });
        },
        resetGameState() {
            this.libraryId = null;
            this.roomStates = {};
            this.currentRoom = null;
            this.nextRooms = [];
            this.factoids = [];
            this.currentQuestion = 0;
            this.answeredQuestions = [];
            this.incorrectQuestionAnswers = [];
            this.questionVisible = false;
            this.factoidVisible = null;
            this.score = 0;
            this.multiplier = 5;
            this.showStart = true;
            this.showNext = false;
            this.completed = false;
            this.clicks = 0;
            this.context = null;
            this.difficulty = null;
            this.guide = null;
            this.imageUrl = null;
            this.language = null;
            this.languageDifficulty = null;
            this.libraryTopic = null;
            this.likes = 0;
            this.bestTime = 0;
            this.completion = 0;
            this.noGeneratedRooms = false;
        }
    }
});
