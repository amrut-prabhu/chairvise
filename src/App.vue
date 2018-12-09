<template>
  <center>
    <Navigation v-if="user"/>
    <div 
      id="app" 
      style="width:100%;">
      <el-container id="main">
        <el-aside 
          v-if="user != null" 
          style="width:25%;">
          <div style="margin:20px"/>
          <center id="upload">
            <form 
              v-if="isInitial || isSaving || isSuccess" 
              enctype="multipart/form-data" 
              novalidate>
              <!--The type multipart/form-data is important, otherwise Django will not accept-->
              <h2 v-if="user != null" >Upload File(s) Here</h2>
              <div 
                v-if="user != null" 
                class="dropbox">
                <input 
                  :name="uploadFieldName" 
                  :disable="isSaving" 
                  type="file" 
                  multiple 
                  accept=".csv" 
                  class="input-file" 
                  @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length">
                <p 
                  v-if="isInitial || isSuccess" 
                  style="margin-bottom:0px;padding-top:120px;font-size:18px">
                  Drag your file(s) here to begin<br> or click to browse
                </p>
                <p v-if="isSaving">
                  Uploading {{ fileCount }} files...
                </p>
              </div>
            </form>
          </center>
        </el-aside>
        <el-container>
          <el-main>
            <center>
              <router-view :key="$route.fullPath"/>
            </center>
          </el-main>
        </el-container>
      </el-container>
    </div>
  </center>
</template>

<script>
import { upload } from "./components/Upload";
import router from "./router";
import Navigation from "./components/Navigation";
import Logout from "./components/Logout";
import firebase from "firebase";
import MappingController from "./components/MappingController"

const STATUS_INITIAL = 0,
  STATUS_SAVING = 1,
  STATUS_SUCCESS = 2,
  STATUS_FAILED = 3;

export default {
  name: "App",
  components: {
    Navigation,
    Logout,
    MappingController
  },
  props: ["fileList"],
  data() {
    return {
      uploadedFiles: [],
      uploadError: null,
      currentStatus: null,
      uploadFieldName: "file",
      testChartsDataInput: null,
      uploadedFileNames: "",
      options: [
        {
          value: "author",
          label: "Author File"
        },
        {
          value: "submission",
          label: "Submission File"
        },
        {
          value: "review",
          label: "Review File"
        }
      ]
    };
  },
  computed: {
    user: function() {
      return this.$store.getters.getUser;
    },
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isSaving() {
      return this.currentStatus === STATUS_SAVING;
    },
    isSuccess() {
      return this.currentStatus === STATUS_SUCCESS;
    },
    isFailed() {
      return this.currentStatus === STATUS_FAILED;
    }
  },
  mounted() {
    this.reset();
  },
  beforeUpdate() {},
  methods: {
    startHacking() {
      this.$notify({
        title: "It works!",
        type: "success",
        message:
          "We've laid the ground work for you. It's time for you to build something epic!",
        duration: 2500
      });
    },
    reset() {
      // reset form to initial state
      this.currentStatus = STATUS_INITIAL;
      this.uploadedFiles = [];
      this.uploadError = null;
    },
    save(formData) {
      // upload data to the server
      this.currentStatus = STATUS_SAVING;
      upload(formData)
        .then(x => {
          // console.log("inside success function!")
          console.log(x);
          // this.uploadedFiles = [].concat(x);
          this.currentStatus = STATUS_SUCCESS;
          this.testChartsDataInput = x;

          var infoType = x.infoType;
          console.log("info type is", infoType);
          var infoData = x.infoData;
          
          var nameArray = document
            .querySelector(".input-file")
            .value.split("\\");
          var inputFileName = nameArray[nameArray.length - 1];
          var nameArray = document
            .querySelector(".input-file")
            .value.split("\\");
          var inputFileName = nameArray[nameArray.length - 1];
          
          router.push({
            name: "Result",
            params: {
              inputFileName: this.uploadedFileNames,
              chartData: infoData,
              infoType: infoType
            }
          });

          this.uploadedFileNames = "";

          // Note: adding the below code to make sure that reuploading the same file will give you sth
          // Can consider changing this and the same code in catch block to finally();
          document.querySelector(".input-file").value = "";
        })
        .catch(err => {
          this.uploadError = err.response;
          this.currentStatus = STATUS_FAILED;
          document.querySelector(".input-file").value = "";
        });
    },
    filesChange(fieldName, fileList) {
      console.log("Inside App.vue filesChange method! ");
      //console.log(document.querySelector(".input-file").value.split("\\"));
      // handle file changes
      console.log("File name is ", fileList[0].name);
      const formData = new FormData();
      if (!fileList.length) return;
      console.log("The first element in fileList is",fileList[0]);
      router.push ({
        name: "MappingController",
        params: {
          fieldName: fieldName,
          fileList: fileList
        }
      });
      /*
      // append the files to FormData
      Array.from(Array(fileList.length).keys()).map(x => {
        formData.append(fieldName, fileList[x], fileList[x].name);

        if (this.uploadedFileNames == "") {
          this.uploadedFileNames = fileList[x].name;
        } else {
          this.uploadedFileNames += "&" + fileList[x].name;
        }
      });

      // save it
      console.log("form Data is ", formData);
      this.save(formData);
      */
    }
  }
};
</script>

<style>
.dropbox {
  outline: 2px dashed grey; /* the dash box */
  outline-offset: -10px;
  background: lightcyan;
  color: dimgray;
  margin-bottom: 5%;
  margin-top: 5%;
  height: 300px; /* minimum height */
  width: 90%;
  position: relative;
  cursor: pointer;
}

.input-file {
  opacity: 0; /* invisible but it's there! */
  width: 100%;
  height: 100%;
  position: absolute;
  cursor: pointer;
  left: 0; /*put this otherwise the input box will shift by half of the parent width */
}

.dropbox:hover {
  background: lightblue; /* when mouse over to the drop zone, change color */
}

.dropbox p {
  font-size: 0.5em;
  text-align: center;
  padding: 50px 0;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  margin-bottom: 0px;
}

#main {
  margin-bottom: 10px;
}

.el-header,
.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
  margin-bottom: 5px;
}

.el-aside {
  background: #de6262; /* fallback for old browsers */
  background: -webkit-linear-gradient(
    to bottom,
    #ffb88c,
    #de6262
  ); /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(
    to bottom,
    #ffb88c,
    #de6262
  ); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
  color: #333;
  color: #333;
  text-align: center;
  line-height: 30px;
  margin-right: 5px;
}

.el-main {
  background: #de6262; /* fallback for old browsers */
  background: -webkit-linear-gradient(
    to bottom,
    #ffb88c,
    #de6262
  ); /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(
    to bottom,
    #ffb88c,
    #de6262
  ); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
  color: #333;
  height: 800px;
  /*text-align: center;*/
  /*line-height: 450px;*/
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

.logo-img {
  display: inline-block;
  width: 3%;
  padding: none;
}

.title-img {
  display: inline-block;
  height: 50px;
  padding-left: 5px;
  padding-right: 5px;
}

.file-button {
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 5px;
  padding-right: 5px;
}
</style>
