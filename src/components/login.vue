<template>
  <section class="login-block">
    <div class="container">
      <div class="row">
        <div class="col-md-4 login-sec">
          <h2 class="text-center">Login</h2>
          <form class="login-form">
            <input 
              v-model="email" 
              type="text" 
              placeholder="Email"><br>
            <input 
              v-model="password" 
              type="password" 
              placeholder="Password"><br>

            <div class="form-check">
              <button 
                type="submit"
                class="btn btn-login" 
                @click="signIn">Login</button>
            </div>
            <div @click="googleSignIn" >
              <img
                class="googlebutton"
              >
            </div>
            <p>Don't have an account?
              <router-link to="/signup">Create one!</router-link>
            </p>
          </form>
        </div>
        <div class="col-md-8 banner-sec">
          <div 
            class="carousel-inner" 
            role="listbox">
            <div>
              <img 
                class="d-block img-fluid" 
                src="https://static.pexels.com/photos/33972/pexels-photo.jpg" 
                alt="First slide">
              <div class="carousel-caption d-none d-md-block">
                <div class="banner-text">
                  <h2>This is ChairVize</h2>
                  <p>ChairVise reports a summary of interesting facts e.g. acceptance and rejection rates, country specific contributions, of conferences that help researches mine for useful information.</p>
                </div>	
              </div>
            </div>
          </div>	   	    
        </div>
      </div>
  </div>  </section>

</template>

<script>
import firebase from "firebase";

let provider = new firebase.auth.GoogleAuthProvider();

export default {
  name: "Login",
  data: function() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    googleSignIn: function() {
      firebase
        .auth()
        .signInWithPopup(provider)
        .then(result => {
          // This gives you a Google Access Token. You can use it to access the Google API.
          // The signed-in user info.
          let user = result.user;
          this.$store.commit("setUser", user);
          this.$router.push({
            name: "Home"
          });
        })
        .catch(function(error) {
          // Handle Errors here.
          let errorCode = error.code;
          let errorMessage = error.message;
          // The email of the user's account used.
          let email = error.email;
          console.log("Cannot log in with: " + email);
          console.log("Error Code: " + errorCode);
          console.log(errorMessage);
        });
    },
    signIn: function() {
      firebase
        .auth()
        .signInWithEmailAndPassword(this.email, this.password)
        .then(
          result => {
            this.$store.commit("setUser", result.user);
            this.$router.push({
              name: "Home"
            });
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
@import url("//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css");

.login {
  margin-top: 40px;
}

input {
  margin: 10px 0;
  width: 100%;
  padding: 15px;
}

button {
  padding: 10px 20px;
  font-weight: bold;
  border-radius: 22px;
  outline: 0;
  cursor: pointer;
}

p {
  margin-top: 40px;
  font-size: 13px;
}

p a {
  text-decoration: underline;
  cursor: pointer;
}

.googlebutton {
  content: url("../assets/google_signin_buttons/1x/btn_google_signin_dark_normal_web.png");
  margin-top: 20px;
}

.googlebutton:hover {
  content: url("../assets/google_signin_buttons/1x/btn_google_signin_dark_focus_web.png");
  cursor: pointer;
}

.googlebutton:active {
  content: url("../assets/google_signin_buttons/1x/btn_google_signin_dark_pressed_web.png");
}

.login-block {
  float: left;
  width: 100%;
  padding: 50px 0;
}

.banner-sec {
  background: url(https://static.pexels.com/photos/33972/pexels-photo.jpg)
    no-repeat left bottom;
  background-size: cover;
  min-height: 500px;
  border-radius: 0 10px 10px 0;
  padding: 0;
}
.container {
  background: #fff;
  border-radius: 10px;
  box-shadow: 15px 20px 0px rgba(0, 0, 0, 0.1);
}
.carousel-inner {
  border-radius: 0 10px 10px 0;
}
.carousel-caption {
  text-align: left;
  left: 5%;
}
.login-sec {
  padding: 50px 30px;
  position: relative;
}
.login-sec .copy-text {
  position: absolute;
  width: 80%;
  bottom: 20px;
  font-size: 13px;
  text-align: center;
}
.login-sec .copy-text i {
  color: #feb58a;
}
.login-sec .copy-text a {
  color: #e36262;
}
.login-sec h2 {
  margin-bottom: 30px;
  font-weight: 800;
  font-size: 30px;
  color: #de6262;
}
.login-sec h2:after {
  content: " ";
  width: 100px;
  height: 5px;
  background: #feb58a;
  display: block;
  margin-top: 20px;
  border-radius: 3px;
  margin-left: auto;
  margin-right: auto;
}
.btn-login {
  background: #de6262;
  color: #fff;
  font-weight: 600;
}
.banner-text {
  width: 70%;
  position: absolute;
  bottom: 40px;
  padding-left: 20px;
}
.banner-text h2 {
  color: #fff;
  font-weight: 600;
}
.banner-text h2:after {
  content: " ";
  width: 100px;
  height: 5px;
  background: #fff;
  display: block;
  margin-top: 20px;
  border-radius: 3px;
}
.banner-text p {
  color: #000;
  font-weight: bold;
}
</style>
