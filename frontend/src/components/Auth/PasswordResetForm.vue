<!-- TODO: fix weird vue warn messages that come up when someone types -->
<template>
    <div class="inspirational-quote">
        The stars in the universe are not just for us to see, but to remind us we can shine just as brightly. Let's
        continue your story.
    </div>
    <form @submit.prevent="handleSubmit">
        <div class="form-field">

            <label for="email">Email:</label>
            <input type="text" id="email" name="email" v-model="email" autocomplete="email" required />
        </div>
        <br />
        <div v-if="error" class="error-message">
            There was an error sending the reset link
        </div>
        <div v-if="success" class="success-message">
            A reset link has been sent to your email
        </div>
        <div class="button-container">
            <input type="submit" id="submit" :value="buttonText" />
        </div>
    </form>
</template>

<script>

    import axios from 'axios';
  import { usePopupStore } from "@/store/popupStore";

export default {
    data() {
        return {
            email: "",
            error: false,
            success: false,
            buttonText: "Send Reset Link",
        };
    },
    methods: {
          handleSubmit() {
            this.buttonText = "Loading...";

            axios.post("api/send-reset-link", {

                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: this.email })
            })
              .then(response => {
                const data = response.data;
                console.log("response: ", data);
                if (data.status === "success") {
                  this.success = true;
                  this.buttonText = "Reset Link Sent";
                } else {
                    this.error = true;
                    this.buttonText = "Send Reset Link";
                }
              })
              .catch(error => {
                console.error("Error during login:", error);
                const popupStore = usePopupStore();
                popupStore.showPopup(error.message || "Login failed. Please try again.");
                this.buttonText = "Log in";
              });
          },
    },
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

.inspirational-quote {
    text-align: center;
    font-style: italic;
    margin-bottom: 20px;
    color: #555;
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
</style>