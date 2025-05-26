<!-- LoginSignupPopup.vue -->
<template>
    <div v-if="!loggedIn" class="popup-overlay">
        <div v-if="loggingIn" id="loadingCloud" class="cloud-animation">☁️</div>
        <div v-else class="popup-content">
            <transition name="fade" mode="out-in">
                <div :key="activeForm">
                    <LoginForm v-if="activeForm === 'login'" @loginSuccess="handleLoginSuccess" />
                    <SignupForm v-else-if="activeForm === 'signup'" @signupSuccess="handleSignupSuccess" />
                    <SendPasswordResetEmail v-else-if="activeForm === 'passwordReset'" @resetSuccess="handleResetSuccess" />

                    <!-- Buttons under each form -->
                    <div v-if="activeForm === 'signup'">
                        <button class="toggle-btn" @click="toggleForms('login')">
                            Already have an account? <span class="underline-text">Log in</span>
                        </button>
                    </div>

                    <div v-else-if="activeForm === 'login'">
                        <button class="forgot-password" @click="toggleForms('passwordReset')">
                            Forgot your password? <span class="underline-text">Reset Here</span>
                        </button>
                        <button class="toggle-btn" @click="toggleForms('signup')">
                            Don't have an account? <span class="underline-text">Sign up</span>
                        </button>
                        <button class="toggle-btn" @click="toEmailVerificationScreen()">
                            Email not verified? <span class="underline-text">Send me a new email</span>
                        </button>
                    </div>
                </div>
            </transition>

            <div ref="googleButton"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import LoginForm from "./LoginForm.vue";
import SignupForm from "./SignupForm.vue";
import SendPasswordResetEmail from "./SendPasswordResetEmail.vue";
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore, UserData } from "@/store/authStore";

const router = useRouter();
const route = useRoute();
const googleButton = ref<HTMLDivElement | null>(null);
const activeForm = ref('login');
const loggingIn = ref(false);
const authStore = useAuthStore();

const loggedIn = computed(() => {
    return authStore.loggedIn;
});

onMounted(() => {
    // this.loadGoogleIdentityServices();
    if (loggedIn.value) {
        const popupStore = usePopupStore();
        popupStore.showPopup(
            "You are already signed in. Visit settings to log out."
        );
        router.push("/");
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

const handleSignupSuccess = () => {
    const popupStore = usePopupStore();
    popupStore.showPopup(
        "Registration email sent!\n Please click the link in the email to start your ascent."
    );
    router.push("/");
};

const handleResetSuccess = () => {
    // This function was not implemented in the original code
    // Added here to satisfy the template usage
};

// loadGoogleIdentityServices() {
//     if (window.google && window.google.accounts) {
//         this.initializeGoogleSignIn();
//     } else {
//         const script = document.createElement("script");
//         script.src = "https://accounts.google.com/gsi/client";
//         script.onload = this.initializeGoogleSignIn;
//         script.async = true;
//         script.defer = true;
//         document.head.appendChild(script);
//     }
// },

// initializeGoogleSignIn() {
//     window.google.accounts.id.initialize({
//         client_id:
//             "529262341360-9sq10od3qkro19jaavhgachkpviugfv3.apps.googleusercontent.com",
//         callback: this.handleCredentialResponse,
//     });
//     window.google.accounts.id.renderButton(this.$refs.googleButton, {
//         theme: "outline",
//         size: "large",
//     });
// },

// handleCredentialResponse(response) {
//     this.loggingIn = true;
//     this.sendTokenToBackend(response.credential);
// },
// sendTokenToBackend(id_token) {
//     axios
//         .post("/api/auth/google/callback", { id_token })
//         .then((response) => {
//             const authStore = useAuthStore();
//             authStore.login();
//             if (response.data.message === "new_user") {
//                 this.$router.push("/?awake");
//             } else {
//                 this.$router.push("/");
//             }
//         })
//         .catch((error) => {
//             console.error("Error authenticating", error);
//         })
//         .finally(() => {
//             this.loggingIn = false;
//         });
// },
</script>

<style scoped>
.form-field {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 16px;
  max-width: 250px;
  /* width: 100%; */
  margin-left: auto;
  margin-right: auto;
}

.form-field label {
  margin-bottom: 6px;
  font-size: 0.9em;
  color: var(--text-color);
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

.popup-content {
  background-color: var(--background-color-1t);
  display: flex;
  justify-content: center;  /* Horizontal center */
  align-items: center;      /* Vertical center */
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

.underline-text {
    font-weight: 700;
    text-decoration: underline;
}

.popup-content button:hover .underline-text,
.popup-content button:active .underline-text {
    text-decoration: none;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
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
</style>
