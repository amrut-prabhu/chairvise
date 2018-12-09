<template>
  <div>
    <editable-header :text.sync="title"/>
    <div class="card">
      <!-- <P>
        {{authorChartIncluded}}
      </p> -->
      <bar-chart 
        id="authorScoreschart" 
        ref="authorScoreschart" 
        :data-input="authorScoresData" 
        :title-text="'Top Author Scores'"
        :xAxisLabel="'Author name'"
        :yAxisLabel="'Average weighted Score'"
        class="chart"/>
      <!--using text.sync for two-way data binding to editable text child component-->
      <editable-text :text.sync="authorScoresText"/>
      <el-select 
        v-model="authorScoresDataLength" 
        placeholder="Select Length" 
        style="margin-top: 10px;margin-right: 40px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="authorScoresChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <!-- <P>
        {{authorChartIncluded}}
      </p> -->
      <bar-chart 
        id="bestPaperAuthorsChart" 
        ref="bestPaperAuthorsChart" 
        :data-input="bestPaperAuthorsData" 
        :title-text="'Authors with most recommendations for Best Paper '"
        :xAxisLabel="'Authors'"
        :yAxisLabel="'Number of recommended papers'"
        class="chart"/>
      <!--using text.sync for two-way data binding to editable text child component-->
      <editable-text :text.sync="bestPaperAuthorText"/>
      <el-select 
        v-model="bestPaperAuthorsDataLength" 
        placeholder="Select Length" 
        style="margin-top: 10px;margin-right: 40px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="bestPaperAuthorsChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <el-button 
      type="success" 
      plain 
      style="margin-top: 10px" 
      @click="saveAsPDF">Save as PDF</el-button>
    <el-button 
      type="Info" 
      plain 
      style="margin-top: 10px" 
      @click="saveSession">Save Session</el-button>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart";
import TimeLineChart from "@/components/charts/TimeLineChart";
import RadarChart from "@/components/charts/RadarChart";
import BarChart from "@/components/charts/BarChart";
import BarChartDeci from "@/components/charts/BarChartDeci";
import HoriBarChart from "@/components/charts/HoriBarChart";
import PieChart from "@/components/charts/PieChart";

import EditableText from "@/components/EditableText";
import EditableHeader from "@/components/EditableHeader";

import Const from "../Const";

import VueWordCloud from "vuewordcloud";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

import firebase from "firebase";

const fb = require("../firebaseConfiguration.js");
export default {
  name: "SubmissionAndReviewVisualisation",
  components: {
    LineChart,
    TimeLineChart,
    RadarChart,
    BarChart,
    BarChartDeci,
    HoriBarChart,
    PieChart,
    EditableText,
    EditableHeader,
    [VueWordCloud.name]: VueWordCloud
  },
  props: ["chartData", "infoType", "inputFileName", "sessionData"],
  data: function() {
    // Create sessionId by time if doesnt already exist
    let sessionId = this.sessionData ? this.sessionData.sessionId : Date.now();

    let recommendedKeywordListData = this.chartData.recommendedKeywordList;
    let recommendedKeywordMapData = this.chartData.recommendedKeywordMap;

    let dataLengthOptions = [
      {
        value: 3,
        label: "3"
      },
      {
        value: 5,
        label: "5"
      },
      {
        value: 10,
        label: "10"
      }
    ];
    if (this.sessionData) {
      let authorScoresDataLength = this.sessionData.authorScoresDataLength;
      let bestPaperAuthorsDataLength = this.sessionData
        .bestPaperAuthorsDataLength;

      return {
        sessionId,
        title: this.sessionData.title,

        authorScoresDataLength,
        authorScoresData: this.computeAuthorScoresData(authorScoresDataLength),
        authorScoresText: this.sessionData.authorScoresText,
        authorScoresChartIncluded: this.sessionData.authorScoresChartIncluded,

        bestPaperAuthorsDataLength,
        bestPaperAuthorsData: this.computeBestPaperAuthorData(
          bestPaperAuthorsDataLength
        ),
        bestPaperAuthorText: this.sessionData.bestPaperAuthorText,
        bestPaperAuthorsChartIncluded: this.sessionData
          .bestPaperAuthorsChartIncluded,

        dataLengthOptions
      };
    } else {
      return {
        sessionId,
        title: {
          val: "Submission and Review Info Analysis",
          edit: false
        },

        authorScoresData: this.computeAuthorScoresData(3),
        authorScoresDataLength: 3,
        authorScoresText: {
          val: "Click to Insert text here",
          edit: false
        },
        authorScoresChartIncluded: true,

        bestPaperAuthorsData: this.computeBestPaperAuthorData(3),
        bestPaperAuthorsDataLength: 3,
        bestPaperAuthorText: {
          val: "Click to Insert text here",
          edit: false
        },
        bestPaperAuthorsChartIncluded: true,

        dataLengthOptions
      };
    }
  },
  watch: {
    authorScoresDataLength: function(newValue, oldValue) {
      var len = newValue;
      this.authorScoresData = this.computeAuthorScoresData(len);
    },
    bestPaperAuthorsDataLength: function(newValue, oldValue) {
      var len = newValue;
      this.bestPaperAuthorsData = this.computeBestPaperAuthorData(len);
    }
  },
  methods: {
    saveAsPDF: function() {
      let fileName = this.title.val;
      var leftMargin = Const.leftMargin;
      var rightMargin = Const.rightMargin;
      var contentWidth = Const.contentWidth;
      var initialTopMargin = Const.topMargin;
      var doc = new jsPDF("p", "pt");
      var title = this.title.val;
      doc.setFont("Times");
      doc.setFontSize(Const.pdfTitleFontSize);
      var titleLength = doc.getStringUnitWidth(title) * Const.pdfTitleFontSize;
      doc.text(
        (contentWidth - titleLength) / 2.0 + leftMargin,
        initialTopMargin,
        title
      );
      var startingTopMargin = initialTopMargin + Const.pdfTitleFontSize;
      doc.setFontSize(Const.pdfTextFontSize);

      var numOfAddedSections = 0;

      html2canvas(document.getElementById("authorScoreschart")).then(
        scoreCanvas => {
          var topMarginAfterScore = startingTopMargin;
          if (this.authorScoresChartIncluded) {
            numOfAddedSections += 1;

            var scoreImageData = scoreCanvas.toDataURL("image/png");
            var scoreImageWidth = Const.imageWidth;
            var scoreImageHeight =
              (scoreCanvas.height * scoreImageWidth) / scoreCanvas.width;
            doc.addImage(
              scoreImageData,
              "PNG",
              leftMargin,
              startingTopMargin,
              scoreImageWidth,
              scoreImageHeight
            );

            var scoreTextLines = doc.splitTextToSize(
              this.authorScoresText.val,
              contentWidth
            );
            doc.text(
              leftMargin,
              startingTopMargin + scoreImageHeight + 20,
              scoreTextLines
            );

            var scoreTextHeight =
              Const.pdfLineHeight *
              Const.pdfTextFontSize *
              scoreTextLines.length;
            var topMarginAfterScore =
              startingTopMargin + scoreImageHeight + scoreTextHeight + 20;
          }

          html2canvas(document.getElementById("bestPaperAuthorsChart")).then(
            recommendCanvas => {
              var topMarginAfterRecommend = topMarginAfterScore;
              if (this.bestPaperAuthorsChartIncluded) {
                numOfAddedSections += 1;
                var recommendImageData = recommendCanvas.toDataURL("image/png");
                var recommendImageWidth = Const.imageWidth;
                var recommendImageHeight =
                  (recommendCanvas.height * recommendImageWidth) /
                  recommendCanvas.width;
                doc.addImage(
                  recommendImageData,
                  "PNG",
                  leftMargin,
                  topMarginAfterScore,
                  recommendImageWidth,
                  recommendImageHeight
                );

                var recommendTextLines = doc.splitTextToSize(
                  this.bestPaperAuthorText.val,
                  contentWidth
                );
                doc.text(
                  leftMargin,
                  topMarginAfterScore + recommendImageHeight + 20,
                  recommendTextLines
                );

                if (numOfAddedSections % 2 == 1) {
                  var recommendTextLinesHeight =
                    Const.pdfLineHeight *
                    Const.pdfTextFontSize *
                    recommendTextLines.length;
                  topMarginAfterRecommend =
                    topMarginAfterScore +
                    recommendImageHeight +
                    recommendTextLinesHeight +
                    20;
                }
              }
              doc.save(fileName + ".pdf");
            }
          );
        }
      );
    },
    saveSession: function() {
      let thisRef = this;
      console.log(this.authorScoresData);
      fb.database
        .ref("/" + this.$store.getters.getUser.uid + "/" + this.sessionId)
        .set(
          {
            sessionId: this.sessionId,
            title: this.title,

            infoType: this.infoType,
            inputFileName: this.inputFileName,
            chartData: JSON.stringify(this.chartData),

            authorScoresDataLength: this.authorScoresDataLength,
            authorScoresText: this.authorScoresText,
            authorScoresChartIncluded: this.authorScoresChartIncluded,

            bestPaperAuthorsDataLength: this.bestPaperAuthorsDataLength,
            bestPaperAuthorText: this.bestPaperAuthorText,
            bestPaperAuthorsChartIncluded: this.bestPaperAuthorsChartIncluded,

            dataLengthOptions: this.dataLengthOptions
          },
          function(error) {
            if (error) {
              thisRef.$notify({
                title: "Saving error!",
                type: "error",
                message:
                  "There was an error saving the session. Check your internet connection.",
                duration: 2500
              });
            } else {
              thisRef.$notify({
                title: "Submission and Review Visualisation session saved!",
                type: "success",
                message: "Go to History Page to resume previous sessions.",
                duration: 2500
              });
            }
          }
        );
    },
    computeAuthorScoresData: function(len) {
      let scheme = this.chooseColorScheme(len);
      let authorScoresData = {
        labels: this.chartData.authorScores.slice(0, len).map(arr => arr[0]),
        datasets: [
          {
            label: "Score",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.authorScores.slice(0, len).map(arr => arr[1])
          }
        ]
      };
      return authorScoresData;
    },
    computeBestPaperAuthorData: function(len) {
      let scheme = this.chooseColorScheme(len);
      let bestPaperAuthorsData = {
        labels: this.chartData.bestPaperAuthors
          .slice(0, len)
          .map(arr => arr[0]),
        datasets: [
          {
            label: "Number of Best Paper Nominations",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.bestPaperAuthors
              .slice(0, len)
              .map(arr => arr[1])
          }
        ]
      };
      return bestPaperAuthorsData;
    },
    chooseColorScheme: function(len) {
      switch (len) {
        case 3:
          return Const.colorScheme3;
        case 5:
          return Const.colorScheme5;
        default:
          return Const.colorScheme10;
      }
    },
    indexOfMax: function(arr) {
      if (arr.length === 0) {
        return -1;
      }

      var max = arr[0];
      var maxIndex = 0;

      for (var i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
          maxIndex = i;
          max = arr[i];
        }
      }

      return maxIndex;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.chart {
  margin-bottom: 10px;
  margin-top: 10px;
}

.line {
  float: left;
}

.center-line {
  float: center;
}

h1,
h2 {
  font-weight: normal;
}

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

.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}

* {
  box-sizing: border-box;
}

body {
  font-family: Arial, Helvetica, sans-serif;
}

/* Float four columns side by side */
.column {
  float: left;
  width: 25%;
  padding: 0 10px;
}

/* Float two columns side by side */
.cardcolumn {
  float: left;
  width: 50%;
  padding: 0 10px;
}

/* Remove extra left and right margins, due to padding in columns */
.row {
  margin: 0 -5px;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

/* Style the counter cards */
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  padding: 16px;
  text-align: center;
  transition: 0.3s;
  border-radius: 5px;
  background-color: #f1f1f1;
  margin-bottom: 12px;
}

/* Responsive columns - one column layout (vertical) on small screens */
@media screen and (max-width: 600px) {
  .column {
    width: 100%;
    display: block;
    margin-bottom: 20px;
  }
}
</style>