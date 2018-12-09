<template>
  <div class="history">
    <h1>Saved Sessions</h1>
    <ul id="history-list">
      <li v-for="session in sessionList">
        <div class="sessionBox" >
          <div class="column">
            <span class="session-header">Title: </span> <span>{{ session.title.val }}</span>
            <br>
            <span class="session-header">InfoType: </span> <span>{{ session.infoType }}</span>
            <br>
            <span class="session-header">Upload Time: </span> <span>{{ getFormattedDate(session.sessionId) }}</span>
            <br>
          </div>
          <div class="column">
            <el-button 
              type="success"
              @click="loadSession(session)">
              Load Session
            </el-button>
            <el-button 
              type="danger"
              @click="deleteSession(session)">
              Delete Session
            </el-button>
          </div>
        </div>
        <br>
      </li>
    </ul>
    <div v-if="sessionList.length === 0">
      <h2>Oops. It appears you don't have any sessions saved.
      Save your sessions by pressing the 'Save Session' button at the bottom of the visualisation.
      </h2>
      <img :src="require('../assets/save_session_demo.png')">
    </div>
  </div>
</template>

<script>
const fb = require("./firebaseConfiguration.js");
const moment = require("moment");

export default {
  name: "History",
  data: function() {
    let sessionList = [];
    let dataBaseRef = null;
    fb.auth.onAuthStateChanged(user => {
      dataBaseRef = fb.database.ref(user.uid);
      dataBaseRef.on("value", snapshot => {
        let sessions = snapshot.val();
        sessionList.splice(0, sessionList.length);
        for (let sessionKey in sessions) {
          sessionList.unshift(sessions[sessionKey]);
        }
      });
    });
    return {
      sessionList
    };
  },
  methods: {
    getFormattedDate: function(time) {
      return moment(time).format("Do MMMM YYYY, h:mm:ss a");
    },
    loadSession: function(session) {
      this.$router.push({
        name: "Result",
        params: {
          inputFileName: session.inputFileName,
          chartData: JSON.parse(session.chartData),
          infoType: session.infoType,
          sessionData: session
        }
      });
    },
    deleteSession: function(session) {
      fb.auth.onAuthStateChanged(user => {
        let dataBaseRef = fb.database.ref(user.uid + "/" + session.sessionId);
        dataBaseRef.remove();
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
a {
  color: #42b983;
}
button {
  padding: 10px 20px;
  color: white;
  font-weight: bold;
  border-radius: 22px;
  outline: 0;
  cursor: pointer;
}

div .sessionBox {
  border: 1px solid black;
  text-align: left;
  padding: 22px;
  border-radius: 22px;
  background-color: #8cd3ff;
  overflow: hidden;
}

span {
  font-size: 1.1em;
}

.session-header {
  font-size: 1.2em;
  font-weight: bold;
}

.column {
  float: left;
  width: 50%;
}
</style>
