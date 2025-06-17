<!-- LoginSignupPopup.vue -->
<template>
    <div v-if="!loggedIn" class="popup-overlay">
        <div v-if="loggingIn" id="loadingCloud" class="cloud-animation">☁️</div>
        <div v-else class="popup-content">
            

            <transition name="fade" mode="out-in">
                <div :key="activeForm" class="form-container">
                    <LoginForm v-if="activeForm === 'login'" @loginSuccess="handleLoginSuccess" />
                    <SignupForm v-else-if="activeForm === 'signup'" @signupSuccess="handleSignupSuccess"/>
                    <SendPasswordResetEmail v-else-if="activeForm === 'passwordReset'" @resetSuccess="handleResetSuccess" />
                    <div ref="googleButton" class="google-button-container"></div>

                    <!-- Buttons under each form -->
                    <div class="form-actions">
                        <div v-if="activeForm === 'signup'">
                            <button class="toggle-btn" @click="toggleForms('login')">
                                Already have an account? <span class="underline-text">Log in</span>
                            </button>
                        </div>

                        <div v-else-if="activeForm === 'login'" class="login-actions">
                           
                            <button class="toggle-btn" @click="toggleForms('signup')">
                                Don't have an account? <span class="underline-text">Sign up</span>
                            </button>
                            <button class="toggle-btn" @click="toEmailVerificationScreen()">
                                Email not verified? <span class="underline-text">Send me a new email</span>
                            </button>
                        </div>
                    </div>
                </div>
            </transition>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import LoginForm from "./LoginForm.vue";
import SignupForm from "./SignupForm.vue";
import SendPasswordResetEmail from "./SendPasswordResetEmail.vue";
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore, UserData } from "@/store/authStore";
import { showSignupToast } from "@/utils/toasts";
import axios from 'axios';

const router = useRouter();
const route = useRoute();
const googleButton = ref<HTMLDivElement | null>(null); // Ref for the Google button container
const activeForm = ref('login');
const loggingIn = ref(false);
const authStore = useAuthStore();

// Ensure this is declared to be accessible in the global scope for the callback
declare global {
  interface Window {
    handleGoogleSignIn: (response: any) => void;
  }
}

const loggedIn = computed(() => {
    return authStore.loggedIn;
});

// Google Sign In Handler
const handleGoogleSignIn = async (response: any) => {
    loggingIn.value = true;
    try {
        const { data } = await axios.post('/api/auth/google/callback', {
           id_token: response.credential,
        });

        if (data.status === 'success') {
            authStore.login(data.user); // Assuming data.user contains the user info
            const redirectPath = route.query.redirect?.toString() || '/';
            router.push(redirectPath);
        } else {
            const popupStore = usePopupStore();
            popupStore.showPopup(data.message || 'Google Sign-In failed. Please try again.');
        }
    } catch (error) {
        console.error('Google Sign-In error:', error);
        const popupStore = usePopupStore();
        popupStore.showPopup('An error occurred during Google Sign-In. Please try again.');
    } finally {
        loggingIn.value = false;
    }
};


onMounted(async () => {
    if (loggedIn.value) {
        const popupStore = usePopupStore();
        popupStore.showPopup(
            "You are already signed in. Visit settings to log out."
        );
        router.push("/");
        return; // Exit if already logged in
    }

    // Make handleGoogleSignIn globally accessible
    window.handleGoogleSignIn = handleGoogleSignIn;

    // Wait for the next DOM update cycle to ensure googleButton.value is available
    await nextTick();

    if (googleButton.value && typeof google !== 'undefined' && google.accounts && google.accounts.id) {
        google.accounts.id.initialize({
            client_id: process.env.VUE_APP_GOOGLE_CLIENT_ID, // Ensure this is set in your .env file
            callback: window.handleGoogleSignIn,
        });
        google.accounts.id.renderButton(
            googleButton.value,
            { theme: "outline", size: "large", width: "300" } 
        );
    } else {
        console.error('Google Identity Services library not loaded or googleButton ref not found.');
    }
});

const toggleForms = (form: string) => {
    activeForm.value = form;
};

const handleLoginSuccess = async (user: UserData) => {
    authStore.login(user);
    const redirectPath = route.query.redirect?.toString() || "/";
    router.push(redirectPath);
};

const toEmailVerificationScreen = () => {
    router.push("/verify");
};

const handleSignupSuccess = (userEmail: string) => {
    router.push({name: 'Verify'});
    showSignupToast(userEmail);
};

const handleResetSuccess = () => {
    // This function was not implemented in the original code
    // Added here to satisfy the template usage
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

.form-actions {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
}

.login-actions {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
}

.popup-content :deep(input[type="submit"]) {
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
}

.popup-content :deep(input[type="submit"]):hover {
    background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(26, 139, 127, 0.3);
}

.popup-content :deep(input[type="text"]),
.popup-content :deep(input[type="email"]),
.popup-content :deep(input[type="password"]) {
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

.popup-content :deep(input[type="text"]):focus,
.popup-content :deep(input[type="email"]):focus,
.popup-content :deep(input[type="password"]):focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(26, 139, 127, 0.2);
    outline: none;
}

.popup-content :deep(input::placeholder) {
    color: var(--text-color-secondary);
}

.toggle-btn,
.forgot-password {
    background: transparent;
    color: var(--text-color-secondary);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
    text-align: center;
}

.toggle-btn:hover,
.toggle-btn:active,
.forgot-password:hover,
.forgot-password:active {
    color: var(--color-primary-light);
    background-color: rgba(26, 139, 127, 0.1);
    transform: translateY(-1px);
}

.underline-text {
    font-weight: 700;
    text-decoration: underline;
    color: var(--color-primary-light);
}

.toggle-btn:hover .underline-text,
.toggle-btn:active .underline-text,
.forgot-password:hover .underline-text,
.forgot-password:active .underline-text {
    text-decoration: none;
}

.google-button-container {
    margin-top: 1.5rem;
    width: 100%;
    max-width: 300px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
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

    .popup-content :deep(input[type="submit"]) {
        max-width: 100%;
    }

    .google-button-container {
        max-width: 100%;
    }
}
</style>
