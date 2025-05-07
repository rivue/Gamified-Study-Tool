// tate
// rc/store/gameStore.js
import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import { usePopupStore } from "@/store/popupStore";
import { useUserStatsStore } from "@/store/userStatsStore";

const DEFAULT_SECTIONID_VALUE = -1000;

export const useGameStore = defineStore("gameStore", {
    state: () => ({
        userStateData: null,
        libraryId: null as string | null,
        roomStates: {} as Record<string, { state: number; factoids: any[] }>,
        currentRoom: null as string | null,
        nextRooms: [],
        factoids: [] as any[],
        currentQuestion: 0,
        answeredQuestions: [],
        incorrectQuestionAnswers: [] as any[],
        questionVisible: false,
        factoidVisible: null as any,
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
        libraryTopic: null as string | null,
        likes: 0,
        timer: null,
        timeSpent: 0,
        timerActive: false,
        bestTime: 0,
        completion: 0,
        noGeneratedRooms: false,
        libraryError: false,
        sectionId: DEFAULT_SECTIONID_VALUE as number,
    }),
    actions: {
        setSectionId(sectionId: number) {
            this.sectionId = sectionId;
        },
        setId(libraryId: string) {
            this.resetGameState();
            this.libraryId = libraryId;
        },
        startGame() {
            if (this.timeSpent !== 0) {
                this.hideGameInfo();
                return;
            }
            this.showStart = false;
            if (this.libraryTopic !== null) {
                this.openRoom(this.libraryTopic);
            }
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
        answerAttempt(correct: boolean) {
            if (correct) {
                this.score += this.multiplier;
                this.multiplier += 1;
                this.currentQuestion += 1;
                if (this.currentQuestion === this.factoids.length) { // && this.finalTest) {
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
        async fetchLibraryDetails(libraryId: string, roomNameThing: string) {

            let sectionid = DEFAULT_SECTIONID_VALUE;

            if (this.sectionId) {
                const sectionid = this.sectionId
            }

            this.libraryError = false;
            this.setId(libraryId);

            if (sectionid !== DEFAULT_SECTIONID_VALUE) {
                this.setSectionId(sectionid);
            }
            
            try {
                const response = await axios.get(`/api/library/${libraryId}`, {params: {library_topic: roomNameThing}});

                // do loadName first in case factoid doesn't exist
                if (response.data.status === "success") {
                    if (response.data.data === null && response.data.room_data === null) {
                        // if for some reason roomNameThing is null
                        this.libraryError = true;
                        console.error("Failed to fetch library details", response);
                        return;
                    }
                    const data = response.data.data;
                    this.userStateData = response.data.room_data;
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
                    // console.debug("roomNameThing: ", roomNameThing);
                    this.likes = data.likes || 0;
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

                }
            } catch (error) {
                if (axios.isCancel(error)) {
                    this.libraryError = true;
                } else {
                    this.libraryError = true;
                }
            }
        },
        async loadRoom(room_name: string) {
            try {
                if (this.roomStates[room_name].state !== 1) {
                    return;
                }
                const formdata = new FormData();
                formdata.append("libraryId", this.libraryId || "");
                formdata.append("subtopic", room_name);
                const response = await axios.post("/api/library/room", formdata);
                
                // const response = await axios.post("/api/library/room", {
                //     libraryId: this.libraryId,
                //     subtopic: room_name
                // });

                if (response.data.status === "success") {
                    this.roomStates[room_name].state = 2;
                    this.roomStates[room_name].factoids = response.data.data.factoids;

                } else {
                    this.roomStates[room_name].state = 0; // forgot what state means, I'm just trying to throw an error message in NextRoomscomponent
                    if (response.data.status === 403) {
                        const popupStore = usePopupStore();
                        popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                        return false;
                    }
                }
            } catch (error) {
                if (axios.isAxiosError(error) && error.response?.status === 403) {
                    const popupStore = usePopupStore();
                    popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                    return false;
                } else if (error instanceof Error) {
                    console.error("Error unlocking room:", error.message);
                } else {
                    console.error("Unknown Error unlocking room:", error);
                }
            }
            return true;
        },
        openRoom(room_name: string) {
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
                this.factoids = this.factoids.map((factoid: any) => {
                    return {
                        ...factoid,
                        text: "No cheating lol"
                    };
                });
            }
        },
        endGame() {
            if (this.incorrectQuestionAnswers.length > 3) {
                return;
            }
            const userStatsStore = useUserStatsStore();
            userStatsStore.resetStats();

            // const completedRooms = Object.keys(this.roomStates).filter(
                // roomName => this.roomStates[roomName].state === 3
            // );

            let data = {
                libraryId: this.libraryId,
                sectionId: this.sectionId,
                
                // libraryId: this.libraryId,
                // score: this.score,
                // time: 500,
                // completed: completedRooms
            };
            axios
                .post(`/api/library/end`, data)
                .then(response => {
                    if (response.data.status === "success") {
                        this.completed = true;
                        this.setSectionId(DEFAULT_SECTIONID_VALUE);
                    } else {
                        console.error("Failed to end game:", response.data.message);
                    }
                })
                .catch(error => {
                    console.error("Error sending game end data:", error);
                });
        },
        resetGameState() {
            this.userStateData = null;
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
