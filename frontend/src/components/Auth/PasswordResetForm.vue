<template>
    <div v-if="!loggedIn" class="popup-overlay">
        <div v-if="loggingIn" id="loadingCloud" class="cloud-animation">☁️</div>
        <div v-else class="popup-content">
            <div class="header-content">
                <h1 class="title">Password Reset</h1>
                <p class="subtitle">Enter your new password below</p>
            </div>

            <form @submit.prevent="handleSubmit" class="form-container">
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
                    <input type="submit" id="submit" :value="buttonText" />
                </div>
            </form>
        </div>
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

.popup-content {
    background: var(--background-color);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(26, 139, 127, 0.2);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding: 2rem;
    max-width: 450px;
    width: 100%;
    min-height: 400px;
    color: var(--text-color);
}

.header-content {
    text-align: center;
    margin-bottom: 2rem;
}

.title {
    background-color: var(--text-color);
    font-size: 2rem;
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
    text-align: center;
}

.form-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.form-field {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 16px;
    max-width: 300px;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
}

.form-field label {
    margin-bottom: 6px;
    font-size: 0.9em;
    color: var(--text-color);
}

.button-container {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 1rem;
}

.error-message {
    color: #ff6b6b;
    font-size: 0.9em;
    margin-bottom: 10px;
    text-align: center;
    width: 100%;
}

input[type="submit"] {
    width: 100%;
    max-width: 300px;
    height: 44px;
    margin-top: 8px;
    padding: 0 1.25rem;
    background: var(--button-gradient, linear-gradient(135deg, var(--color-primary), var(--color-primary-light)));
    color: var(--text-color);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
    font-weight: 600;
    font-size: 1rem;
    white-space: normal;
    word-wrap: break-word;
}

input[type="submit"]:hover {
    background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(26, 139, 127, 0.3);
}

input[type="password"] {
    width: 100%;
    height: 44px;
    padding: 0 1rem;
    border-radius: 8px;
    border: 1px solid rgba(26, 139, 127, 0.3);
    background-color: rgba(26, 139, 127, 0.1);
    color: var(--text-color);
    font-size: 1rem;
    transition: all 0.2s;
}

input[type="password"]:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(26, 139, 127, 0.2);
    outline: none;
}

input[type="password"]::placeholder {
    color: var(--text-color-secondary);
}

@keyframes cloudMove {
    0% {
        opacity: 0;
        transform: translateX(-25vw) translateY(-2vh);
    }

    25% {
        transform: translateX(-12.5vw) translateY(2vh);
    }

    50% {
        opacity: 1;
        transform: translateX(0vw) translateY(-2vh);
    }

    75% {
        transform: translateX(12.5vw) translateY(2vh);
    }

    100% {
        opacity: 0;
        transform: translateX(25vw) translateY(-2vh);
    }
}

.cloud-animation {
    font-size: 3em;
    position: absolute;
    top: 40%;
    left: 50%;
    animation: cloudMove 3s linear infinite;
}

@media (max-width: 640px) {
    .popup-content {
        padding: 1.5rem;
        border-radius: 12px;
        max-width: 350px;
        min-height: 350px;
    }

    .title {
        font-size: 1.75rem;
    }

    .form-field {
        max-width: 100%;
    }

    input[type="submit"] {
        max-width: 100%;
    }
}
</style>
