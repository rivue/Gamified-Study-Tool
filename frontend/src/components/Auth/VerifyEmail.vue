<template>
    <div class="verification-container p-8">
        <div v-if="loading" class="loading">
            <p>Loading...</p>
        </div>
        <div v-else>

            <div v-if="status === 'success'" class="success">
                <h1>Email Verified!</h1>
                <p>Your email has been successfully verified.</p>
                <p>You are now logged in and ready to use Rivue!</p>
                <router-link to="/" class="button">Go to Dashboard</router-link>
            </div>
            <div v-else class="success">


                <div v-if="token">
                    <h1>Verification Failed</h1>
                    <p> We couldn't verify your email. The link may be invalid or expired.</p>
                </div>

                <h1 v-if="!token">Resend Verification Email</h1>

                <form @submit.prevent="handleSendNewVerificationEmail">
                    <br/>
                    <div class="form-field">
                        <label for="email">Email:</label>
                        <input type="text" id="email" name="email" v-model="email" autocomplete="email" required />
                    </div>
                    <div v-if="completed && status === ''" class="completed-message">
                        If there is an unverified account associated with this email, a reset link was sent to it.
                    </div>
                    <div v-if="!completed" class="completed-message">Please enter your email and click the button below to resend a verification link.</div>
                    <div class="button-containered py-2 px-4 text-md">
                        <input type="submit" id="submit" :value="buttonText" />
                    </div>
                </form>
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

<style>
.button-containered {
    text-align: center;
    border-radius: 6px;
    background-color: var(--color-primary)
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
}

.form-field label {
    display: flex;
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

.verification-container {
    max-width: 600px;
    margin: 0 auto;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: var(--background-color-1t);
    color: #f0f8ff;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #f0f8ff;
}

.loading,
.success,
.error {
    padding: 20px;
}

.button {
    display: inline-block;
    padding: 10px 20px;
    margin-top: 20px;
    color: var(--text-color);
    background-color: var(--element-color-1);
    text-decoration: none;
    border-radius: 5px;
    cursor: pointer;
}

.verification-container .error-message {
    color: #ff4d4f;
    /* Red color for error */
    font-size: 1em;
    margin: 10px 0;
    text-align: center;
    font-weight: bold;
}

/* Update the form-field label to align it to the left */
.form-field label {
    display: block;
    /* Change to block for proper alignment */
    font-size: 0.9em;
    color: var(--text-color);
    text-align: left;
    /* Align text to the left */
    width: 100%;
    /* Ensure it spans the width of the form field */
    margin-bottom: 5px;
    /* Add some spacing below the label */
}
</style>
