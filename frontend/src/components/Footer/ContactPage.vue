<!-- ContactPage.vue -->
<template>
    <div class="page-main-container">
        <div class="page-main-section">
            <div class="contact-overlay">
                <div class="popup-content">
                    <h1>Contact / Submit feedback</h1>
                    
                    <!-- Added feedback info section -->
                    <div class="feedback-info">
                        <p><strong>Your feedback matters!</strong> All submissions are:</p>
                        <ul>
                            <li>Read by our development team</li>
                            <li>Used to prioritize new features and improvements</li>
                            <li>Stored securely and used only to enhance Rivue.ai</li>
                        </ul>
                    </div>

                    <form v-if="loggedIn" @submit.prevent="handleSubmit">
                        <textarea id="message" v-model="message" placeholder="Share your thoughts, bug reports, or feature requests here" rows="4"
                            required></textarea>

                        <input type="submit" value="Submit" />
                    </form>
                    <div v-else>Please <a href="/login">log in</a> to submit feedback and bugs.</div>
                    <br />
                    <div>
                        To reach us, join our Discord <a href="https://discord.gg/33yAcp2qDf"
                            target="_blank">community</a> or email us at <a
                            href="mailto:contact@rivue.ai?subject=Rivue.ai%20Feedback&body=Hello,%20I%20have%20some%20feedback..."><b>contact@rivue.ai</b></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import { usePopupStore } from "@/store/popupStore";
import { computed, ref } from "vue";

const message = ref("");

const authStore = useAuthStore();

const loggedIn = computed(() => authStore.loggedIn);

function handleSubmit() {
    const payload = new FormData();
    payload.append("message", message.value);

    axios
        .post("/api/feedback", payload)
        .then((response) => {
            const popupStore = usePopupStore();
            if (
                response.data &&
                response.data.message &&
                response.data.feedback_id
            ) {
                const successMessage = `${response.data.message} Your feedback ID is ${response.data.feedback_id}. Thank you for helping us improve Rivue.ai!`;
                popupStore.showPopup(successMessage);
            } else {
                popupStore.showPopup("Feedback submitted successfully! Thank you for helping us improve Rivue.ai!");
            }
            message.value = "";
        })
        .catch((error) => {
            const popupStore = usePopupStore();
            let message = "An error occurred while submitting feedback.";
            if (
                error.response &&
                error.response.data &&
                error.response.data.error
            ) {
                message = error.response.data.error;
            }
            popupStore.showPopup(message);
        });
}
</script>

<style scoped>
.contact-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: var(--background-color);
    display: flex;
    justify-content: center;
    align-items: center;
}

.popup-content {
    background-color: var(--background-color-1t);
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    max-width: 80%;
}

.popup-content div,
.popup-content form {
    width: 100%;
}

.popup-content form {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Added styles for feedback info section */
.feedback-info {
    padding: 15px;
    border-radius: 6px;
    margin-bottom: 20px;
}

.feedback-info p {
    margin: 0 0 10px 0;
    font-weight: 500;
}

.feedback-info ul {
    text-align: left;
    margin: 0;
    padding-left: 20px;
}

.feedback-info li {
    margin-bottom: 5px;
}

.popup-content label {
    margin-bottom: 8px;
}

.popup-content :deep(textarea) {
    background-color: #00000000;
    padding: 10px;
    border: 1px solid var(--text-color);
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 8px;
}

.popup-content :deep(textarea) {
    resize: vertical;
}

.popup-content :deep(input[type="submit"]) {
    margin-top: 8px;
    margin-bottom: 8px;
    padding: 10px 15px;
    background-color: var(--element-color-1);
    color: var(--text-color);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease, text-shadow 0.3s ease;
    text-align: center;
    width: auto;
    align-self: center;
}

.popup-content :deep(input[type="submit"]):hover {
    background-color: var(--element-color-2);
    text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc,
        0 0 20px #bb86fc;
}
</style>
