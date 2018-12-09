<template>
  <div class = "sign-up">
    <p> Create a new account!</p>
    <input 
      v-model = "email" 
      type = "text" 
      placeholder="Email"><br>
    <input 
      v-model = "password" 
      type = "password" 
      placeholder="Password"><br>
    <button @click ="signUp">Sign Up</button>
    <span> Return to <router-link to="/">Login</router-link>.</span>
  </div>
</template>

<script>
import firebase from "firebase";

export default {
  name: "Signup",
  data: function() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    signUp: function() {
      firebase
        .auth()
        .createUserWithEmailAndPassword(this.email, this.password)
        .then(
          result => {
            this.$store.commit("setUser", result.user);
            result
            this.$router.replace("home");
          },
          err => {
            alert(err.message);
          }
        );
    }
  }
};
</script>

<style scoped>
.signUp {
  margin-top: 40px;
}
input {
  margin: 10px 0;
  width: 20%;
  padding: 15px;
}
button {
  padding: 10px 20px;
  color: white;
  font-weight: bold;
  border-radius: 22px;
  outline: 0;
  cursor: pointer;
}
span {
  display: block;
  margin-top: 20px;
  font-size: 11px;
}
</style>
