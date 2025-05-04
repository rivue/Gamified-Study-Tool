<template>
    <div v-if="!loggedIn" class="popup-overlay">
        <div v-if="loggingIn" id="loadingCloud" class="cloud-animation">☁️</div>

        <form @submit.prevent="handleSubmit" class="popup-content">
            <div class="reset-header">
                Password Reset
            </div>
            <div class="form-field">
                <label for="new-password">New Password:</label>
                <input type="password" id="new-password" name="new-password" v-model="password"
                    autocomplete="new-password" required />
            </div>
            <div class="form-field">
                <label for="confirm-password">Confirm New Password:</label>
                <input type="password" id="confirm-password" name="confirm-password" v-model="confirmPassword"
                    autocomplete="new-password" required />
            </div>
            <div v-if="passwordError" class="error-message">
                {{ passwordError }}
            </div>
            <div class="button-container">
                <input class="wrap" type="submit" id="submit" :value="buttonText" style="white-space: normal; word-wrap: break-word; text-align: center;" />
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { ref, defineProps } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps<{
    token: string
}>();

const router = useRouter();
const buttonText = ref("Submit");
const password = ref("");
const confirmPassword = ref("");
const passwordError = ref("");
const loggingIn = ref(false);
const loggedIn = ref(false);

const handleSubmit = () => {
    if (password.value !== confirmPassword.value) {
        passwordError.value = "Passwords do not match";
        buttonText.value = "Submit";
        return;
    }
    
    if (password.value.length < 8) {
        passwordError.value = "Passwords must be at least 8 characters long";
        buttonText.value = "Submit";
        return;
    }
    
    passwordError.value = "";
    buttonText.value = "Loading...";
    
    axios.post("api/reset-password", {
        token: props.token,
        new_password: password.value,
    })
    .then((response) => {
        if (response.status === 200) {
            let countdown = 5;
            buttonText.value = `Reset Successful, redirecting to login page in ${countdown}...`;
            const interval = setInterval(() => {
                countdown--;
                buttonText.value = `Reset Successful, redirecting to login page in ${countdown}...`;
                if (countdown === 0) {
                    clearInterval(interval);
                    router.push('/login');
                }
            }, 1000);
        }
    })
    .catch((error) => {
        buttonText.value = "Reset Failed";
        passwordError.value = error.response?.data.message || "An error occurred. Please try again.";
    });
};
</script>

<style scoped>
/* Styles remain unchanged */
.error-message {
    color: #ff6b6b;
    font-size: 0.9em;
    margin-bottom: 10px;
    text-align: center;
}

.button-container {
    text-align: center;
}

.inspirational-quote {
    text-align: center;
    font-style: italic;
    margin-bottom: 20px;
    color: #555;
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

.button-container {
    text-align: center;
}

.form-field {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 300px;
    width: 100%;
    margin-bottom: 16px;
    margin-left: auto;
    margin-right: auto;
}

.form-field label {
    font-size: 0.9em;
    color: var(--text-color);
    align-self: flex-start;
}

.form-field input[type="text"],
.form-field input[type="password"] {
    background-color: #00000000;
    padding: 10px;
    border: 1px solid var(--text-color);
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
}

.reset-header {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 30px;
    color: var(--text-color);
    text-align: center;
    letter-spacing: 0.5px;
    position: relative;
    padding-bottom: 10px;
}

.reset-header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 2px;
    background: var(--element-color-1);
    border-radius: 1px;
}

.popup-content {
    background-color: var(--background-color-1t);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding: 10px;
    border-radius: 8px;
    max-width: 400px;
    width: 100%;
    min-height: 300px;
}


.popup-content label {
    margin-bottom: 8px;
}

.popup-content :deep(input[type="submit"]) {
    margin-top: 8px;
    padding: 10px 15px;
    background-color: var(--element-color-1);
    color: var(--text-color);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
}

.popup-content :deep(input[type="submit"]):hover {
    background-color: var(--element-color-2);
    text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc;
}

.popup-content button {
    margin-top: 8px;
    padding: 10px 15px;
    color: var(--text-color);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.popup-content button:hover,
.popup-content button:active {
    text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc;
}


.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: var(--background-haze);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 95;
    padding: 25px;
}
</style>
