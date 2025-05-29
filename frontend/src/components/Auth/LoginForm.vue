<template>
    <h1>Login</h1>

    <form @submit.prevent="handleSubmit">
        <div class="form-field">
            <label for="email">Email:</label>
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
            <label for="password">Password:</label>
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
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"v-if="showPassword"/>
                <EyeSlashIcon 
                    type="button"
                    class="password-toggle w-7 h-7"
                    @click="togglePasswordVisibility"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'" v-else/>
            </div>
        </div>
        <div class="button-container">
            <input type="submit" id="submit" :disabled="isSubmitting" :value="buttonText" />
        </div>
    </form>
</template>
    
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { usePopupStore } from "@/store/popupStore";
import { UserData } from "@/store/authStore";
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/solid';
 

const emit = defineEmits<{
    (e: 'loginSuccess', user: UserData): void
}>();

const email = ref("");
const password = ref("");
const buttonText = ref("Log in");
const isSubmitting = ref(false);
const showPassword = ref(false);

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
</script>

<style>
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
</style>