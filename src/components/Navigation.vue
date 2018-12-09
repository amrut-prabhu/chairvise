<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <button 
      class="navbar-toggler" 
      type="button" 
      data-toggle="collapse" 
      data-target="#navbarSupportedContent" 
      aria-controls="navbarSupportedContent" 
      aria-expanded="false" 
      aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"/>
    </button>
    <div 
      id="navbarSupportedContent" 
      class="collapse navbar-collapse">
      <ul class="navbar-nav mr-auto"> 
        <li class="nav-item active">
          <router-link to="/">
            <a 
              v-if="isLoggedIn" 
              class="nav-link">Home <span class="sr-only">(current)</span></a>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/History">
            <a 
              v-if="isLoggedIn" 
              class="nav-link disabled" 
              href="#">History</a>
          </router-link>
        </li>
      </ul>
      <span v-if="isLoggedIn">
        <vue-avatar 
          :username="displayName" 
          :src="photoUrl"/></span>
      <LogOut v-if="isLoggedIn"/>
    </div>
  </nav>
</template>

<script>
import LogOut from "./Logout";

export default {
  name: "Navigation",
  components: {
    LogOut
  },
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    },
    displayName: function() {
      let displayName = this.$store.getters.getUser.displayName;
      return displayName ? displayName : this.$store.getters.getUser.email;
    },
    photoUrl: function() {
      return this.$store.getters.getUser.photoURL;
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}

.vue-avatar-enter-active {
  animation: vue-avatar-in 0.8s;
}

.vue-avatar-leave-active {
  animation: vue-avatar-in reverse;
}
</style>
