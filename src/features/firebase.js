import firebase from "firebase";
const firebaseConfig = {
  apiKey: "AIzaSyBOOrOun-MX16P3gn3CSOZOqyj8f8Hpll4",
  authDomain: "snapchat-clone-152f5.firebaseapp.com",
  projectId: "snapchat-clone-152f5",
  storageBucket: "snapchat-clone-152f5.appspot.com",
  messagingSenderId: "253520943725",
  appId: "1:253520943725:web:3bdf7e17a879bc333ebd64",
};

const firebaseApp = firebase.initializeApp(firebaseConfig);
const db = firebasseApp.firestore();
const auth = firebase.auth();
const storage = firebase.storage();

const provider = new firebase.auth.GoogleAuthProvider();

export { db, auth, storage, provider };
