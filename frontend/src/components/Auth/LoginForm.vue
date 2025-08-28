<template>
    <div class="header-content">
        <h1 class="title">Welcome Back</h1>
        <p class="subtitle">Sign in to continue your learning journey</p>
    </div>
    <form @submit.prevent="handleSubmit">
        <div class="form-field">
            <label for="email">Email</label>
            <input
                type="text"
                id="email"
                name="email"
                v-model="email"
                autocomplete="email"
                required
            />
        </div>
        <div class="form-field">
            <div class="password-label-container">
                <label for="password">Password</label>
                <button type="button" class="forgot-password-link" @click="toggleForms('passwordReset')">
                    Forgot password?
                </button>
            </div>
            <div class="password-input-container">
                <input
                    :type="showPassword ? 'text' : 'password'"
                    id="password"
                    name="password"
                    v-model="password"
                    autocomplete="current-password"
                    required
                />
                <EyeIcon 
                    type="button"
                    class="password-toggle w-7 h-7"
                    @click="togglePasswordVisibility"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"
                    v-if="showPassword"/>
                <EyeSlashIcon 
                    type="button"
                    class="password-toggle w-7 h-7"
                    @click="togglePasswordVisibility"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'" 
                    v-else/>
            </div>
        </div>
        <div class="button-container">
            <input type="submit" id="submit" :disabled="isSubmitting" :value="buttonText" />
        </div>
    </form>
    
    <div class="divider-container">
        <div class="divider-line"></div>
        <span class="divider-text">or</span>
        <div class="divider-line"></div>
    </div>
    
    <div class="google-button-container">
        <div ref="googleButton" class="google-button"></div>
    </div>

</template>
    
<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
import { usePopupStore } from "@/store/popupStore";
import { UserData } from "@/store/authStore";
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/solid';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from "@/store/authStore";

const props = defineProps<{
    toggleForms: (form: string) => void
}>();

const emit = defineEmits<{
    (e: 'loginSuccess', user: UserData): void
}>();

const email = ref("");
const password = ref("");
const buttonText = ref("Login");
const isSubmitting = ref(false);
const showPassword = ref(false);
const googleButton = ref<HTMLDivElement | null>(null);

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};

const handleSubmit = () => {
    if (!email.value || !password.value) {
        const popupStore = usePopupStore();
        popupStore.showPopup("Email and password are required.");
        return;
    }
    
    buttonText.value = "Loading...";
    isSubmitting.value = true;

    const formData = new FormData();
    formData.append("email", email.value);
    formData.append("password", password.value);
    formData.append("timezone", Intl.DateTimeFormat().resolvedOptions().timeZone);

    axios.post("api/login", formData)
        .then(response => {
            if (response.status === 200) {
                console.log(response)
                const user: UserData = {
                    id: response.data.user.id,
                    username: response.data.user.email,
                    firstName: response.data.user.first_name,
                    lastName: response.data.user.last_name,
                    current_streak: response.data.user.current_streak,
                    highest_streak: response.data.user.highest_streak,
                }
                emit("loginSuccess", user);
            }
        })
        .catch(error => {
            const popupStore = usePopupStore();
            popupStore.showPopup(error.response?.data?.message || "Login failed, please try again");
        })
        .finally(() => {
            buttonText.value = "Log in";
            isSubmitting.value = false;
        });
};

const handleGoogleSignIn = async (response: any) => {
    const popupStore = usePopupStore();
    try {
        const { data } = await axios.post('/api/auth/google/callback', {
           id_token: response.credential,
        });

        if (data.status === 'success') {
            authStore.login(data.user);
            const redirectPath = route.query.redirect?.toString() || '/';
            router.push(redirectPath);
        } else {
            popupStore.showPopup('Google Sign-In failed. Please try again.');
        }
    } catch (error: any) {
        const popupStore = usePopupStore();
        const errorMessage = 'An error occurred during Google Sign-In. Please try again.';
        popupStore.showPopup(errorMessage);
    }
};

onMounted(async () => {
    // Wait for the next DOM update cycle to ensure googleButton.value is available
    await nextTick();

    if (googleButton.value && typeof google !== 'undefined' && google.accounts && google.accounts.id) {
        google.accounts.id.renderButton(
            googleButton.value,
            { theme: "outline", size: "large", width: "300" } 
        );
    } else {
        console.error('Google Identity Services library not loaded or googleButton ref not found.');
    }

    // Load Google Sign-In
    if (typeof window !== 'undefined' && window.google) {
        await nextTick();
        if (googleButton.value) {
            window.google.accounts.id.initialize({
                client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
                callback: handleGoogleSignIn,
            });
            
            window.google.accounts.id.renderButton(googleButton.value, {
                theme: 'outline',
                size: 'large',
                width: 300,
                text: 'signin_with'
            });
        }
    }
});
</script>

<style>
.header-content {
    text-align: center;
    margin-bottom: 2rem;
}
form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

.button-container {
    text-align: center;
    background-color: transparent;
    border: none;
}

.form-field {
    display: flex;
    flex-direction: column;
    align-items: center; /* Change from flex-start to center */
    max-width: 300px;
    width: 100%;
    margin-bottom: 16px; /* Re-add this for spacing between fields */
    margin-left: auto; /* Keep these for horizontal centering */
    margin-right: auto;
}

.form-field label {
    font-size: 0.9em;
    color: var(--text-color);
}

.form-field input[type="text"],
.form-field input[type="password"] {
    background-color: #00000000;
    padding: 10px;
    padding-right: 40px; /* Add space for the icon */
    border: 1px solid var(--text-color);
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
}
.password-toggle {
    position: absolute;
    right: 10px; /* Position from the right edge */
    top: 50%;
    transform: translateY(-50%); /* Center vertically */
    cursor: pointer;
    z-index: 1;
}
.password-input-container {
    position: relative;
    width: 100%;
    display: flex;
    align-items: center;
}

.password-toggle:hover {
    opacity: 0.7;
}

.password-label-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 6px;
}

.forgot-password-link {
    background: none;
    border: none;
    color: var(--color-primary-light);
    font-size: 0.8rem;
    cursor: pointer;
    text-decoration: underline;
    padding: 0;
}

.forgot-password-link:hover {
    color: var(--color-primary);
    text-decoration: none;
}

.divider-container {
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 300px;
    margin: 1.5rem 0 1rem 0;
}

.divider-line {
    flex: 1;
    height: 1px;
    background-color: var(--text-color-secondary);
    opacity: 0.3;
}

.divider-text {
    margin: 0 1rem;
    font-size: 0.875rem;
    color: var(--text-color-secondary);
    white-space: nowrap;
}

.google-button-container {
    width: 100%;
    max-width: 300px;
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
}

</style>