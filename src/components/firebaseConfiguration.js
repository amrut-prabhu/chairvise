import firebase from 'firebase'

var config = {
  apiKey: "AIzaSyArtfJnm9ZOzB0jJJ7SSF3Nup9RgVH8kaM",
  authDomain: "chairvize.firebaseapp.com",
  databaseURL: "https://chairvize.firebaseio.com",
  projectId: "chairvize",
  storageBucket: "chairvize.appspot.com",
  messagingSenderId: "153981757769"
};
firebase.initializeApp(config)

const database = firebase.database()
const auth = firebase.auth()
const currentUser = firebase.auth().currentUser

export{
    database,
    auth,
    currentUser,
}