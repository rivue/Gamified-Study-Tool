<template>
    <div class="popup-overlay">
        <div v-if="loading" id="loadingCloud" class="cloud-animation">☁️</div>
        <div v-else class="popup-content">
            <div class="form-container">
                <div v-if="status === 'success'" class="success-content">
                    <div class="header-content">
                        <h1 class="title">Email Verified!</h1>
                        <p class="subtitle">Your email has been successfully verified.</p>
                        <p class="subtitle">You are now verified and can now login to use Rivue!</p>
                    </div>
                    <div class="form-actions">
                        <router-link to="/" class="login-button">Go to Login</router-link>
                    </div>
                </div>

                <div v-else class="verification-form">
                    <div class="header-content">
                        <h1 v-if="token" class="title">Verification Failed</h1>
                        <h1 v-else class="title">Resend Verification Email</h1>
                        
                        <p v-if="token" class="subtitle">We couldn't verify your email. The link may be invalid or expired.</p>
                    </div>

                    <form @submit.prevent="handleSendNewVerificationEmail">
                        <div class="form-field">
                            <label for="email">Email:</label>
                            <input type="email" id="email" name="email" v-model="email" autocomplete="email" required />
                        </div>
                        
                        <div v-if="completed && status === ''" class="completed-message">
                            If there is an unverified account associated with this email, a reset link was sent to it.
                        </div>
                        <div v-if="!completed" class="completed-message">
                            Please enter your email and click the button below to resend a verification link.
                        </div>
                        
                        <input type="submit" :value="buttonText" />
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const loading = ref(true);
const status = ref('');
const token = ref('');
const email = ref('');
const buttonText = ref('Send Verify Link');
const completed = ref(false);

onMounted(() => {
    loading.value = true;
    token.value = route.params.token as string;
    confirmEmail();
});

async function confirmEmail() {
    if (!token.value) {
        status.value = '';
        loading.value = false;
        return;
    }
    axios.post('/api/confirm', { token: token.value })
        .then((response) => {
            if (response.status === 200) {
                status.value = 'success';
            } else if (response.data && response.data.message) {
                status.value = response.data.message;
            }
        })
        .catch(() => {
        })
        .finally(() => {
            loading.value = false;
        });
}

const handleSendNewVerificationEmail = () => {
    buttonText.value = 'Loading...';
    completed.value = true;

    axios.post('api/send-verify-link', { email: email.value })
        .finally(() => {
            setTimeout(() => {
                buttonText.value = 'Send Verify Link';
            }, 750);
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
    margin-bottom: 0.5rem;
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

.form-actions {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
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
    display: block;
    margin-left: auto;
    margin-right: auto;
}

input[type="submit"]:hover {
    background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(26, 139, 127, 0.3);
}

input[type="email"] {
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

input[type="email"]:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(26, 139, 127, 0.2);
    outline: none;
}

input::placeholder {
    color: var(--text-color-secondary);
}

.login-button {
    display: inline-block;
    width: 100%;
    max-width: 300px;
    height: 44px;
    padding: 0 1.25rem;
    background: var(--button-gradient, linear-gradient(135deg, var(--color-primary), var(--color-primary-light)));
    color: var(--text-color);
    text-decoration: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
    font-weight: 600;
    font-size: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-button:hover {
    background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(26, 139, 127, 0.3);
}

.completed-message {
    max-width: 300px;
    margin: 12px auto;
    padding: 10px 16px;
    background-color: rgba(26, 139, 127, 0.1);
    border-left: 4px solid var(--color-primary);
    border-radius: 6px;
    color: var(--text-color);
    font-size: 0.9em;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
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

    input[type="submit"],
    .login-button {
        max-width: 100%;
    }
}
</style>
