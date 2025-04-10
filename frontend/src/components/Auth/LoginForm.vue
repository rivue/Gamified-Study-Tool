<template>
    <div class="inspirational-quote">
        The stars in the universe are not just for us to see, but to remind us we can shine just as brightly. Let's continue your story.
    </div>

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
        <input
        type="password"
        id="password"
        name="password"
        v-model="password"
        autocomplete="current-password"
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
      buttonText: "Log in",
    };
  },
  methods: {
    handleSubmit() {
      this.buttonText = "Loading...";
      const formData = new FormData();
      formData.append("email", this.email);
      formData.append("password", this.password);

      axios.post("api/login", formData)
        .then(response => {
          if (response.status === 200) {
            this.$emit("loginSuccess");
          }
        })
        .catch(error => {
            console.log(error.response);
            console.log(error.response?.data);
            const popupStore = usePopupStore();
            popupStore.showPopup(error.response?.data?.message || "Login failed, please try again");
            this.buttonText = "Log in";
        });
    },
  },
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
}
.inspirational-quote {
    text-align: center;
    font-style: italic;
    margin-bottom: 20px;
    color: #555;
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