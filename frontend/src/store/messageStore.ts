
import { defineStore } from 'pinia';
import axios from 'axios';

import eventBus from '@/eventBus';
import { usePopupStore } from "@/store/popupStore";
import { useAdsStore } from "@/store/adsStore";
import { useAuthStore } from "@/store/authStore";

type ConversationData = {
    messages: any; // Replace `any` with the actual type of `messages`
    actions: any; // Replace `any` with the actual type of `actions`
    subheading: string; // Optional property
    progress?: string | number; // Optional property, can be a string or number
};

export const useMessageStore = defineStore('messageStore', {
    state: () => ({
        messages: [],
        actions: [],
        subheading: "",
        progress: 0,
        sending: false,
    }),
    actions: {
        async updateConversation(data: ConversationData) {
            this.messages = data.messages;
            this.actions = data.actions;
            if ("subheading" in data) {
                this.subheading = data.subheading;

                if ("progress" in data) {
                    this.progress = parseFloat(data.progress as string) || 0; 
                }
            }
        },
        async fetchRecentMessages(currentPath: string) {
            const params: { lesson_id?: string; challenge_id?: string } = {};

            const apiEndpoint = "/api/chat";

            const isLesson = currentPath.includes("/lesson/");
            const isChallenge = currentPath.includes("/challenge/");

            if (isLesson) {
                params.lesson_id = currentPath.split("/").pop();
            } else if (isChallenge) {
                params.challenge_id = currentPath.split("/").pop();
            }
            axios
                .get<ConversationData>(apiEndpoint, { params })
                .then((response) => {
                    this.updateConversation(response.data);
                })
                .catch((error) => {
                    console.error(`Error fetching recent messages:`, error);
                    if (error.response && error.response.status === 401 && currentPath !== "/") {
                        const popupStore = usePopupStore();
                        popupStore.showPopup("You do not have permission to view this content.");
                    }
                });
        },
        async sendMessage(message: string, currentPath: string) {
            if (this.sending) return "not sent";

            // Sanitize input
            const sanitizeInput = (input: string) => {
                const div = document.createElement("div");
                div.textContent = input;
                return div.innerHTML;
            };
            const sanitizedMessage = sanitizeInput(message);

            if (sanitizedMessage.trim() === "") return "not sent";

            const maxMessageLength = 1000;
            if (sanitizedMessage.length > maxMessageLength) {
                const popupStore = usePopupStore();
                popupStore.showPopup("Message is too long.");
                return "not sent";
            }

            // Handle special cases
            const isLesson = currentPath.includes("/lesson/");
            const isChallenge = currentPath.includes("/challenge/");
            if (sanitizedMessage === "Leave challenge." && isChallenge) {
                return "/lessons";
            }
            if (sanitizedMessage === "Leave lesson." && isLesson) {
                return "/lessons";
            }

            // Sending logic
            this.sending = true;
            const adStore = useAdsStore();
            adStore.show();

            const formData = new FormData();
            formData.append("message", sanitizedMessage);

            if (isLesson) {
                formData.append("lesson_id", currentPath.split("/").pop() || "");
            } else if (isChallenge) {
                formData.append("challenge_id", currentPath.split("/").pop() || "");
            }

            try {
                const response = await axios.post("/api/chat", formData);
                // Handling after successful sending
                const authStore = useAuthStore();
                authStore.cloudTokens = authStore.cloudTokens +1 ;
                this.updateConversation(response.data);

                if ("redirect" in response.data) {
                    if (response.data.redirect === null) {
                        return;
                    } else {
                        return `/lesson/${response.data.redirect}`;
                    }
                }
                return response.data;
            } catch (error) {
                const popupStore = usePopupStore();
                let errorMessage = "Error sending message: ";
            
                if (axios.isAxiosError(error) && error.response) {
                    errorMessage += error.response.data?.error || `Server responded with status code ${error.response.status}`;
                } else if (axios.isAxiosError(error) && error.request) {
                    errorMessage += "No response received from server. Please check your network connection.";
                } else if (error instanceof Error) {
                    errorMessage += error.message;
                } else {
                    errorMessage += "An unknown error occurred.";
                }
            
                popupStore.showPopup(errorMessage);
            } finally {
                adStore.loaded();
                this.sending = false;
                eventBus.emit('message-recieved');
            }
        },
    },
});