<template>
    <form @submit.prevent="handleSubmit">
      <label for="email">Email:</label>
      <input
        type="text"
        id="email"
        name="email"
        v-model="email"
        autocomplete="email"
        required
      />
      <br />
      <div class="button-container">
        <input type="submit" id="submit" :value="buttonText" />
      </div>
    </form>
  </template>
    
    <script>

//     import axios from 'axios';
//   import { usePopupStore } from "@/store/popupStore";
  
  export default {
    data() {
      return {
        email: "",
        password: "",
        buttonText: "Send Reset Link",
      };
    },
    methods: {
    //   handleSubmit() {
    //     this.buttonText = "Loading...";
    //     const formData = new FormData();
    //     formData.append("email", this.email);
    //     formData.append("password", this.password);
  
    //     axios.post("api/login", formData)
    //       .then(response => {
    //         const data = response.data;
    //         if (data.status === "success") {
    //           this.$emit("loginSuccess");
    //         } else {
    //           throw new Error("Login failed. Please try again.");
    //         }
    //       })
    //       .catch(error => {
    //         console.error("Error during login:", error);
    //         const popupStore = usePopupStore();
    //         popupStore.showPopup(error.message || "Login failed. Please try again.");
    //         this.buttonText = "Log in";
    //       });
    //   },
    },
  };
  </script>
    
    <style>
  .button-container {
    text-align: center;
  }
  </style>