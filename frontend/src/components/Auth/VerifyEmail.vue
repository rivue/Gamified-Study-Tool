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
        <p>The verification link has expired, but we've sent a new one to your email.</p>
        <p>Please check your inbox and click the new verification link.</p>
      </div>
      <div v-else class="error">
        <h1>Verification Failed</h1>
        <p>We couldn't verify your email. The link may be invalid or expired.</p>
        <button @click="resendVerification" class="button">Resend verification email</button>
      </div>
    </div>
  </template>
  
  <script>
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
        try {
            console.log(`token: ${this.token}`); // TODO CURRENT BREAKPOINT
            const response = await fetch(`/api/confirm`, {
            // const response = await fetch(`http://localhost:5000/api/confirm`, {

                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token: this.token })
            });
          
            const data = await response.json();
            this.status = data.status;
            
            if (data.status === 'success') {
                // Set cookie or update store to reflect logged in state if needed
                // This depends on how your authentication is implemented
                setTimeout(() => {
                this.$router.push('/');
                }, 3000);
            } else if (data.message) {
                this.status = data.message;
            }
            } catch (error) {
            console.error('Verification error:', error); // TODO CURRENT BREAKPOINT
            this.status = 'error';
            } finally {
            this.loading = false;
            }
      },
      async resendVerification() {
        this.loading = true;
        try {
          const response = await fetch('/api/resend-verification', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token: this.token })
          });
          
          const data = await response.json();
          if (data.status === 'success') {
            this.status = 'resent';
          } else {
            this.status = 'error';
          }
        } catch (error) {
          console.error('Resend error:', error);
          this.status = 'error';
        } finally {
          this.loading = false;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .verification-container {
    max-width: 600px;
    margin: 50px auto;
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
  
  .loading, .success, .error {
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