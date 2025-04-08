<template>
    <div class="verification-container">
        <div v-if="loading" class="loading">
            <p>Verifying your email...</p>
        </div>
        <div v-else-if="status === 'success'" class="success">
            <h1>Email Verified!</h1>
            <p>Your email has been successfully verified.</p>
            <p>You are now logged in and ready to use Rivue!</p>
            <router-link to="/" class="button">Go to Dashboard</router-link>
        </div>
        <div v-else-if="status === 'expired_registration_token'" class="error">
            <h1>Verification Link Expired</h1>
            <p>The verification link has expired. Please click the button below to resend an email.</p>
            <p>Please click the button below to resend an email.</p>
            <button @click="resendVerification" class="button">Resend verification email</button>
        </div>
        <div v-else-if="status === 'invalid_registration_token'" class="error">
            <h1>Verification Link Invalid</h1>
            <p>The verification link is invalid. </p>
            <p>Please click the button below to resend an email.</p>
            <button @click="resendVerification" class="button">Resend verification email</button>
        </div>
        <div v-else class="error">
            <h1>Verification Failed</h1>
            <p>We couldn't verify your email. The link may be invalid or expired. </p>
            <p>Please click the button below to resend an email.</p>
            <button @click="resendVerification" class="button">Resend verification email</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            loading: true,
            status: '',
            token: ''
        };
    },
    created() {
        this.token = this.$route.params.token;
        this.verifyEmail();
    },
    methods: {
        async verifyEmail() {

            axios.post('/api/confirm', { token: this.token })
                .then((response) => {
                    if (response.status === 200) {
                        this.status = 'success';
                    } else if (response.message) {
                        this.status = response.message;
                    }
                })
                .catch(() => {
                    this.status = 'error';
                })
                .finally(() => {
                    this.loading = false;
                });

        },
        async resendVerification() {
            this.loading = true;

            axios
                .post('/api/resend-verification', { token: this.token })
                .then((response) => {
                    if (response.status === 200) {
                        this.status = 'resent';
                    } else if (response.message) {
                        this.status = 'error';
                    }
                })
                .catch(() => {
                    this.status = 'error';
                })
                .finally(() =>
                    this.loading = false
                );

        }
    }
};
</script>

<style scoped>
.verification-container {
  max-width: 600px;
  /* Change from margin: 50px auto; to these settings */
  margin: 0 auto;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  /* Keep the rest of your styles */
  padding: 30px;
  background-color: #0e0c14;
  color: #f0f8ff;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #4a148c;
}

h1 {
    color: #6a34b9;
    margin-bottom: 20px;
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
    color: #f0f8ff;
    background-color: #4a148c;
    text-decoration: none;
    border-radius: 5px;
    border: 1px solid #6a34b9;
    cursor: pointer;
}

.button:hover {
    background-color: #6a34b9;
}
</style>