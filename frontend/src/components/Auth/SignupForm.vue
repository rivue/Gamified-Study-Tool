<template>
    <h1>Signup</h1>
    <div class="inspirational-quote">
        Stars can't shine without darkness. Your brilliant journey begins here.
    </div>
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
        <input
        type="password"
        id="new-password"
        name="new-password"
        v-model="password"
        autocomplete="new-password"
        required
        />
    </div>
    <div class="form-field">
        <label for="confirm-password">Confirm Password:</label>
        <input
        type="password"
        id="confirm-password"
        name="confirm-password"
        v-model="confirmPassword"
        autocomplete="new-password"
        required
        />
    </div>
    <div class="button-container">
      <input type="submit" id="submit" :value="buttonText" />
    </div>
  </form>
</template>
  
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { usePopupStore } from "@/store/popupStore";

const emit = defineEmits<{
  (e: 'signupSuccess'): void
}>();

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const buttonText = ref("Sign up");

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
  formData.append("new-password", password.value);

  axios.post("/api/signup", formData)
    .then((response) => {
      if (response.status === 200) {
        emit("signupSuccess");
        buttonText.value = "Sign up";
      }
    })
    .catch(error => {
      popupStore.showPopup(error.response?.data?.message || "Signup failed. Please try again.");
      buttonText.value = "Sign up";
    });
};
</script>
  
<style>
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

</style>
