<template>
    <h1>Password Reset</h1>
 
    <form @submit.prevent="handleSubmit">
        <div class="form-field">
            <label for="email">Email:</label>
            <input type="text" id="email" name="email" v-model="email" autocomplete="email" required />
        </div>
        <br />
        <div v-if="completed" class="completed-message">
            If there is an account associated with this email, a reset link was sent to it.
        </div>
        <div class="button-container">
            <input type="submit" id="submit" :value="buttonText" />
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

const email = ref('');
const completed = ref(false);
const buttonText = ref('Send Reset Link');

const handleSubmit = () => {
    buttonText.value = 'Loading...';
    completed.value = true;

    axios.post('api/send-reset-link', { email: email.value })
        .then((response) => {
            if (response.status === 200) {
                buttonText.value = 'Reset Link Sent';
                setTimeout(() => {
                    buttonText.value = 'Send Reset Link';
                }, 3000);
            }
        })
        .catch(() => {
            buttonText.value = 'Send Reset Link';
        });
};
</script>

<style>
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
    /* Change from flex-start to center */
    max-width: 300px;
    width: 100%;
    margin-bottom: 16px;
    /* Re-add this for spacing between fields */
    margin-left: auto;
    /* Keep these for horizontal centering */
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
    border: 1px solid var(--text-color);
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
}
.completed-message {
    max-width: 300px;
    margin: 12px auto;
    padding: 10px 16px;
    background-color: var(--background-color-1t);
    border-left: 4px solid var(--highlight-color, #bb86fc);
    border-radius: 6px;
    color: var(--text-color);
    font-size: 0.9em;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}
</style>
