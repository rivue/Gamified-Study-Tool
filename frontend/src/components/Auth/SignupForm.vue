<template>
    <div class="inspirational-quote">
        Stars can't shine without darkness. Your brilliant journey begins here.
    </div>

  <form @submit.prevent="handleSubmit">
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
  
  <script>
import axios from 'axios';
import { usePopupStore } from "@/store/popupStore";
export default {
  data() {
    return {
      email: "",
      password: "",
      confirmPassword: "",
      buttonText: "Sign up",
    };
  },
  methods: {
    handleSubmit() {
      this.buttonText = "Loading...";
      if (this.password !== this.confirmPassword) {
        const popupStore = usePopupStore();
        popupStore.showPopup("Passwords do not match!");
        this.buttonText = "Sign up";
        return;
      }

      const formData = new FormData();
      formData.append("new-email", this.email);
      formData.append("new-password", this.password);

      axios.post("/api/signup", formData)
        .then(response => {
          const data = response.data;
          if (data.status === "success") {
            this.$emit("signupSuccess");
          } else {
            throw new Error(data.message || "Signup failed. Please try again.");
          }
        })
        .catch(error => {
          console.error('Error during signup:', error);
          const popupStore = usePopupStore();
          popupStore.showPopup(error.message || "Signup failed. Please try again.");
          this.buttonText = "Sign up";
        });
    },
  },
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
  align-self: flex-start; /* This keeps labels aligned to the left */
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
