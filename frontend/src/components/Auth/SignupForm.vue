<!-- SignupForm.vue -->
<template>
    <div class="signup-form-container">
        <h1 class="signup-title">Signup</h1>

        <form @submit.prevent="handleSubmit">
        
            <div class="flex flex-col sm:flex-row gap-4 w-full max-w-md mb-4">
                <div class="form-field flex-1">
                    <label for="first_name">First Name:</label>
                    <input
                    type="text"
                    id="first_name"
                    name="first_name"
                    v-model="firstName"
                    autocomplete="given-name"
                    />
                </div>
                <div class="form-field flex-1">
                    <label for="last_name">Last Name:</label>
                    <input
                    type="text"
                    id="last_name"
                    name="last_name"
                    v-model="lastName"
                    autocomplete="family-name"
                    />
                </div>
            </div>

        <div class="form-field">
            <label for="new-email">Email:</label>
            <input
            type="text"
            id="new-email"
            name="new-email"
            v-model="email"
            autocomplete="email"
            required
            />
        </div>
        <div class="form-field">
            <label for="username">Username: (Must be unique)</label>
            <input
            type="text"
            id="username"
            name="username"
            v-model="username"
            autocomplete="username"
            required
            />
        </div>
        <div class="form-field">
            <label for="new-password">Password:</label>
            <div class="password-input-container">
                <input
                :type="showPassword ? 'text' : 'password'"
                id="new-password"
                name="new-password"
                v-model="password"
                autocomplete="new-password"
                required
                />
                <EyeIcon 
                    class="password-toggle w-7 h-7"
                    @click="togglePasswordVisibility"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"
                    v-if="showPassword"/>
                <EyeSlashIcon 
                    class="password-toggle w-7 h-7"
                    @click="togglePasswordVisibility"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"
                    v-else/>
            </div>
        </div>
        <div class="form-field">
            <label for="confirm-password">Confirm Password:</label>
            <div class="password-input-container">
                <input
                :type="showPassword ? 'text' : 'password'"
                id="confirm-password"
                name="confirm-password"
                v-model="confirmPassword"
                autocomplete="new-password"
                required
                />
                <EyeIcon 
                    class="password-toggle w-7 h-7"
                    @click="togglePasswordVisibility"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"
                    v-if="showPassword"/>
                <EyeSlashIcon 
                    class="password-toggle w-7 h-7"
                    @click="togglePasswordVisibility"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"
                    v-else/>
            </div>
        </div>
        <div class="button-container">
          <input type="submit" id="submit" :value="buttonText" />
        </div>
      </form>
    </div>
</template>
  
<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
import { usePopupStore } from "@/store/popupStore";
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/solid';
import { maskEmailSecure } from "@/utils/general";

const emit = defineEmits<{
  (e: 'signupSuccess', email: string): void;
}>();

const email = ref("");
const username = ref("");
const firstName = ref("");
const lastName = ref("");
const password = ref("");
const confirmPassword = ref("");
const buttonText = ref("Sign up");
const showPassword = ref(false);
const googleButton = ref<HTMLDivElement | null>(null);

const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};

const handleSubmit = () => {
  buttonText.value = "Loading...";
  const popupStore = usePopupStore();
  
  if (password.value !== confirmPassword.value) {
    popupStore.showPopup("Passwords do not match!");
    buttonText.value = "Sign up";
    return;
  }

  if (password.value.length < 8) {
    popupStore.showPopup("Passwords must be longer than 8 characters!");
    buttonText.value = "Sign up";
    return;
  }
  
  const formData = new FormData();
  formData.append("new-email", email.value);
  formData.append("username", username.value);
  formData.append("first_name", firstName.value);
  formData.append("last_name", lastName.value);
  formData.append("new-password", password.value);

  axios.post("/api/signup", formData)
    .then((response) => {
      if (response.status === 200) {
        const maskedUserEmail = maskEmailSecure(email.value);
        emit("signupSuccess", maskedUserEmail);
        buttonText.value = "Sign up";
      }
    })
    .catch(error => {
      popupStore.showPopup(error.response?.data?.message || "Signup failed. Please try again.");
      buttonText.value = "Sign up";
    });
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
});
</script>
  
<style scoped>
.signup-form-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: (100vh - 10px);
}

.signup-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  color: var(--text-color);
  text-align: center;
}

.button-container {
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
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
  font-size: 16px;
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
  padding-right: 40px;
  border: 1px solid var(--text-color);
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
  font-size: 16px;
}

.password-input-container {
    position: relative;
    width: 100%;
    display: flex;
    align-items: center;
}

.password-toggle {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    z-index: 1;
}

.password-toggle:hover {
    opacity: 0.7;
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
}

/* Mobile responsive adjustments */
@media (max-width: 640px) {
  .signup-title {
    font-size: 1.75rem;
    margin-bottom: 1rem;
  }
  
  .form-field {
    max-width: 100%;
    margin-bottom: 12px;
  }
}
</style>