<template>
    <div class="contact-page">
        <div class="header-container">
            <div class="header-content">
                <h1 class="title">Contact / Submit feedback</h1>
                <p class="subtitle">Your feedback matters! Help us improve Rivue.ai</p>
            </div>
        </div>

        <div class="feedback-info">
            <div class="info-card">
                <p class="info-title"><strong>All submissions are:</strong></p>
                <ul class="info-list">
                    <li>Read by our development team</li>
                    <li>Used to prioritize new features and improvements</li>
                    <li>Stored securely and used only to enhance Rivue.ai</li>
                </ul>
            </div>
        </div>

        <div class="form-container">
            <form @submit.prevent="handleSubmit" class="feedback-form">
                <textarea 
                    id="message" 
                    v-model="message" 
                    placeholder="Share your thoughts, bug reports, or feature requests here" 
                    rows="6"
                    required
                    class="feedback-textarea"
                ></textarea>

                <Button type="submit" class="submit-button">
                    <span class="button-text">Submit Feedback</span>
                </Button>
            </form>
        </div>

        <div class="contact-info">
            <p class="contact-text">
                To reach us, join our Discord 
                <a href="https://discord.gg/33yAcp2qDf" target="_blank" class="contact-link">community</a> 
                or email us at 
                <a href="mailto:contact@rivue.ai?subject=Rivue.ai%20Feedback&body=Hello,%20I%20have%20some%20feedback..." 
                   class="contact-link">
                    <strong>contact@rivue.ai</strong>
                </a>
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import { usePopupStore } from "@/store/popupStore";
import { computed, ref } from "vue";
import { Button } from "@/components/ui/button";

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
.contact-page {
    max-width: 800px;
    margin-top: 2rem;
    padding: 2rem;
    color: var(--text-color);
    background: var(--background-color);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(26, 139, 127, 0.2);
}

.header-container {
    margin-bottom: 2rem;
    text-align: center;
}

.header-content {
    max-width: 600px;
    margin: 0 auto;
}

.title {
    background-color: var(--text-color);
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}

.subtitle {
    font-size: 1rem;
    color: var(--text-color-secondary);
    line-height: 1.5;
}

.feedback-info {
    margin-bottom: 2rem;
}

.info-card {
    background: var(--background-color-2t);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid rgba(26, 139, 127, 0.2);
}

.info-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 1rem;
}

.info-list {
    list-style: none;
    padding: 0;
    margin: 0;
    space-y: 0.75rem;
}

.info-list li {
    position: relative;
    padding-left: 1.5rem;
    color: var(--text-color);
    line-height: 1.5;
    margin-bottom: 0.5rem;
}

.info-list li::before {
    content: "•";
    position: absolute;
    left: 0;
    color: var(--color-primary);
    font-weight: bold;
    font-size: 1.2rem;
}

.form-container {
    margin-bottom: 2rem;
}

.feedback-form {
    background: var(--background-color-1t);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 2rem;
    border: 1px solid rgba(26, 139, 127, 0.2);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.feedback-textarea {
    width: 100%;
    min-height: 120px;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid rgba(26, 139, 127, 0.3);
    background-color: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    font-size: 1rem;
    resize: vertical;
    transition: all 0.2s;
    font-family: inherit;
    line-height: 1.5;
}

.feedback-textarea::placeholder {
    color: var(--text-color-secondary);
}

.feedback-textarea:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(26, 139, 127, 0.2);
    outline: none;
}

.submit-button {
    align-self: center;
    height: 48px;
    border-radius: 8px;
    background: var(--button-gradient);
    color: var(--text-color);
    font-weight: 600;
    padding: 0 2rem;
    transition: all 0.2s;
    border: none;
    cursor: pointer;
}

.submit-button:hover:not(:disabled) {
    background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(26, 139, 127, 0.3);
}

.button-text {
    color: var(--text-color);
}

.login-prompt {
    background: var(--background-color-1t);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 2rem;
    border: 1px solid rgba(26, 139, 127, 0.2);
    text-align: center;
    margin-bottom: 2rem;
}

.login-text {
    font-size: 1.125rem;
    color: var(--text-color);
}

.login-link {
    color: var(--color-primary);
    text-decoration: none;
    font-weight: 600;
    transition: all 0.2s;
}

.login-link:hover {
    color: var(--color-primary-light);
    text-decoration: underline;
}

.contact-info {
    background: var(--background-color-1t);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid rgba(26, 139, 127, 0.2);
    text-align: center;
}

.contact-text {
    color: var(--text-color);
    line-height: 1.6;
    margin: 0;
}

.contact-link {
    color: var(--color-primary);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s;
}

.contact-link:hover {
    color: var(--color-primary-light);
    text-decoration: underline;
}

@media (max-width: 640px) {
    .contact-page {
        padding: 1.5rem;
        border-radius: 12px;
    }

    .title {
        font-size: 1.75rem;
    }

    .feedback-form {
        padding: 1.5rem;
    }

    .submit-button {
        width: 100%;
        align-self: stretch;
    }
}
</style>
