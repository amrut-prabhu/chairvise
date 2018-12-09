<template>
   <div class="hello">
       <h1> Map your columns to the relevant headers</h1>
       <li v-for="(file, index) in fileList">
           <span> {{file.name}}: </span>
           <select v-model="infoType[index]">
               <option disabled value="">Please select file type you uploaded</option>
               <option value="Review">Review</option>
                <option value="Author">Author</option>
                <option value="Submission">Submission</option>
                <option value="Review_score">Review Score</option>
            </select>
            <button v-on:click ="generateItem(file, index)"> Generate Mapping Table</button>
            <div class="MappingForm">
              <b-table :items="data[infoType[index]]">
                  <template slot="Mapping" slot-scope="row">
                        <b-form-select v-if="infoType[index]==='Review'" v-model="data[infoType[index]][row.index]['Mapping']">
                            <option disabled value="">Select your Mapping</option>
                            <option value="ReviewID">Review ID</option>
                            <option value="SubmissionID">Submission ID</option>
                            <option value="ReviewAssignID">Review Assigment ID</option>
                            <option value="Name">Reviewer Name</option>
                            <option value="FieldID">Field ID</option>
                            <option value="Comments">Review Comments</option>
                            <option value="Evaluation">Overall Evaluation</option>
                            <option value="Date">Date of review Submission</option>
                            <option value="Time">Time of review Submission</option>
                            <option value="Reco mmended">Recommended for best paper?</option>
                        </b-form-select>
                        <b-form-select v-if="infoType[index]==='Submission'" v-model="data[infoType[index]][row.index]['Mapping']">
                            <option disabled value="">Select your Mapping</option>
                            <option value="SubmissionID">Submission ID</option>
                            <option value="TrackId">Track ID</option>
                            <option value="TrackName">Track Name</option>
                            <option value="Title">Submission Title</option>
                            <option value="Authors">Authors of Submission</option>
                            <option value="Time">Time Submitted</option>
                            <option value="Update">Time Last Updated</option>
                            <option value="FormFields">Form Fields</option>
                            <option value="KeyWords">Keywords put</option>
                            <option value="Decision">Accept/Reject Decision</option>
                            <option value="Mail">Acceptance/Rejection Mail Sent or Not</option>
                            <option value="Review">Review Sent or not</option>
                            <option value="Abstract">Abstract of Submission</option>
                        </b-form-select>
                        <b-form-select v-if="infoType[index]==='Author'" v-model="data[infoType[index]][row.index]['Mapping']">
                            <option disabled value="">Select your Mapping</option>
                            <option value="SubmissionID">Submission ID</option>
                            <option value="FirstName">First Name</option>
                            <option value="LastName">Last Name</option>
                            <option value="Email">Email</option>
                            <option value="Country">Country</option>
                            <option value="Organization">Organization</option>
                            <option value="Webpage">Webpage</option>
                            <option value="PersonID">Person ID</option>
                            <option value="Corresponding">Coressponding</option>
                        </b-form-select>
                        <b-form-select v-if="infoType[index]==='Review_score'" v-model="data[infoType[index]][row.index]['Mapping']">
                            <option disabled value="">Select your Mapping</option>
                            <option value="ReviewNumber"> Review Number</option>
                            <option value="FieldNumber"> Field Number</option>
                            <option value="Score"> Score</option>
                        </b-form-select>
                    </template>
                </b-table>
            </div>
       </li>
       <select v-model="liName">
           <option disabled value="">Show next mapping table</option>
           <option value="Yes">Yes</option>
           <option value="No">No</option>
       </select>
       <el-button v-if="user != null" class="file-button" type="primary" @click="sendData(fileList)">Upload your files!</el-button>
   </div> 
</template>

<script>
import firebase from 'firebase';
import Result from '@/components/Result'
import { upload } from "@/components/Upload";
const STATUS_INITIAL = 0,
  STATUS_SAVING = 1,
  STATUS_SUCCESS = 2,
  STATUS_FAILED = 3;

export default {
  name: 'MappingController',
  data () {
    const fb = require('@/components/firebaseConfiguration.js')
    return {
      user: fb.auth,
      data:{},
      singleData:[],
      liName:'',
      currentStatus: null,
      testChartsDataInput: null,
      infoType:[]
    };
  },
  props: ["fileList", "fieldName"],
  methods: {
    generateItem(file, idx) {
        console.log("Inside generateItem method! The file is ", file.name, 'index is', idx);
        let reader = new FileReader();
        reader.readAsText(file);
        reader.onload = (event) => {
            let csv = event.target.result;
            let allLines = csv.split(/\r\n|\n/);
            console.log("First line of csv file is", allLines[0]);
            let firstLine = allLines[0].split(',');
            console.log("The length of first line is", firstLine.length);
            let reviewMapping = ["ReviewID", "SubmissionID", "ReviewAssignID", "Name", "FieldID", "Comments", "Evaluation", "Date", "Time", "Recommended"];
            let submissionMapping = ["SubmissionID", "TrackId", "TrackName", "Title", "Authors", "Time", "Update", "FormFields", "KeyWords", "Decision", "Mail", "Review", "Abstract"];
            let authorMapping = ["SubmissionID", "FirstName", "LastName", "Email", "Country", "Organization", "Webpage", "PersonID", "Corresponding"];
            let reviewScoreMapping = ["ReviewNumber", "FieldNumber", "Score"];
            for (let i = 0; i < firstLine.length; i++) {
                if (this.infoType[idx] === "Review") {
                    this.singleData.push({column_number: i, columnName: firstLine[i], Mapping: reviewMapping[i]});
                } else if (this.infoType[idx] === "Submission") {
                    this.singleData.push({column_number: i, columnName: firstLine[i], Mapping: submissionMapping[i]});
                } else if (this.infoType[idx] === "Author"){ 
                    this.singleData.push({column_number: i, columnName: firstLine[i], Mapping: authorMapping[i]});
                } else { // Review Score
                    this.singleData.push({column_number: i, columnName: firstLine[i], Mapping: reviewScoreMapping[i]});
                }
            }
            //console.log("items are", this.singleData);
            this.data[this.infoType[idx]] = [];
            for (let i = 0; i < this.singleData.length; i++) {
                this.data[this.infoType[idx]].push(this.singleData[i]);
            }
            this.singleData = [];
        };
        
    }, 
    sendData (fileList) {
        const formData = new FormData();
        //append the files to FormData
        console.log("there are", fileList.length, "files in fileList");
        Array.from(Array(fileList.length).keys()).map(x => {
            formData.append(this.fieldName, fileList[x], this.infoType[x]);
        });
        formData.append('mappings', JSON.stringify(this.data));
       // save it
       this.save(formData, fileList);
    },
    save(formData, fileList) {
      // upload data to the server
      this.currentStatus = STATUS_SAVING;
      upload(formData)
        .then(x => {
        console.log("inside success function!")
          console.log(x);
          // this.uploadedFiles = [].concat(x);
          this.currentStatus = STATUS_SUCCESS;
          this.testChartsDataInput = x;

          var xinfoType = x.infoType;
          //console.log("info type is", infoType);
          var xinfoData = x.infoData;
          //console.log("info data is", infoData);

          var inputFileName = fileList[0].name;
          //console.log("input file name is: ", inputFileName);
          // Note: use router.push to navigate through diff pages programmatically
          this.$router.push({
            name: "Result",
            params: {
              inputFileName: inputFileName,
              chartData: xinfoData,
              infoType: xinfoType
            }
          });

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
  }
}
</script>


<style scoped>
h1, h2 {
  font-weight: normal;
}
li{
    margin-top: 10px;
}
.file-button {
    margin-top: 10px;
}
</style>