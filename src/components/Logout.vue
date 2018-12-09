<template>
  <div class="hello">
    <button @click = "logout">Logout</button>
  </div>
</template>

<script>
import firebase from "firebase";

export default {
  name: "Logout",
  methods: {
    logout: function() {
      firebase
        .auth()
        .signOut()
        .then(() => {
          this.$store.commit('clearUser');
          this.$router.replace("login");
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  /*margin: 0 10px;*/
}
a {
  color: #42b983;
}
button {
  background: #DE6262;
  padding: 10px 20px;
  font-weight: 600;
  border-radius: 22px;
  outline: 0;
  cursor: pointer;
}
</style>
