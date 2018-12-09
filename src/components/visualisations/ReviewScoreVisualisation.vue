<template>
  <div>
    <editable-header :text.sync="title"/>
    <div class="card">
      <p>
        Mean scores & confidence
      </p>
      <div
        id="scoretable" 
        ref="scoretable">
        <el-table
          :data="scoreTableData"
          stripe
          style="width: 70%;margin-top:10px;margin-bottom: 10px">
          <el-table-column
            prop="field"
            label="Field"
            width="180"/>
          <el-table-column
            prop="value"
            label="Value"
            width="180"/>
        </el-table>
        <editable-text :text.sync="statsTableText"/>
      </div>
      <el-switch
        v-model="scoreTableIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <div
        id="yesChart" 
        ref="yesChart">
        <pie-chart 
          :data-input="yesData" 
          :title-text="'Yes Statistics'"
          class="chart"/>
        <editable-text :text.sync="yesChartText"/>
      </div>
      <el-switch
        v-model="yesChartIncluded"
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

import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import EditableText from "@/components/EditableText";
import EditableHeader from "@/components/EditableHeader";

import Const from "../Const";

const fb = require("../firebaseConfiguration.js");
import VueWordCloud from "vuewordcloud";

export default {
  name: "ReviewScoreVisualisation",
  components: {
    LineChart,
    TimeLineChart,
    RadarChart,
    BarChart,
    BarChartDeci,
    HoriBarChart,
    PieChart,
    EditableText,
    html2canvas,
    jsPDF,
    EditableHeader
  },
  props: ["chartData", "infoType", "inputFileName", "sessionData"],
  data: function() {
    // Create sessionId by time if doesnt already exist
    let sessionId = this.sessionData ? this.sessionData.sessionId : Date.now();

    let msg = "Review Score Analysis";
    let scheme = this.chooseColorScheme(2);
    let yesPercentage = this.chartData.yesPercentage.toFixed(2);
    let meanScore = this.chartData.meanScore;
    let meanConfidence = this.chartData.meanConfidence;
    let totalReview = this.chartData.totalReview;
    let scoreTableData = [
      {
        field: "Mean Score",
        value: meanScore.toFixed(2)
      },
      {
        field: "Mean Confidence",
        value: meanConfidence.toFixed(2)
      }
    ];
    let totalYes = Math.round(yesPercentage * totalReview);
    let yesData = {
      labels: ["Yes", "No"],
      datasets: [
        {
          label: "Yes Statistics",
          backgroundColor: scheme,
          pointBackgroundColor: "white",
          borderWidth: 1,
          pointBorderColor: "#249EBF",
          data: [totalYes, totalReview - totalYes]
        }
      ]
    };
    return {
      title: this.sessionData
        ? this.sessionData.title
        : {
            val: "Review Score Info Analysis",
            edit: false
          },
      sessionId,
      msg,
      yesPercentage,
      meanScore,
      meanConfidence,
      scoreTableData,
      yesData,
      totalReview,
      statsTableText: this.sessionData
        ? this.sessionData.statsTableText
        : {
            val: "The mean scores and mean confidence values is shown above",
            edit: false
          },
      yesChartText: this.sessionData
        ? this.sessionData.yesChartText
        : {
            val:
              "The chart above shows the number the total number of reviews receiving yes and no respectively. " +
              "Only " +
              totalYes +
              " reviews gave a yes ouf of a total of " +
              totalReview +
              " reviews.",
            edit: false
          },
      scoreTableIncluded: this.sessionData
        ? this.sessionData.scoreTableIncluded
        : true,
      yesChartIncluded: this.sessionData
        ? this.sessionData.yesChartIncluded
        : true
    };
  },
  watch: {},
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

      html2canvas(document.getElementById("scoretable")).then(scoreCanvas => {
        var topMarginAfterScore = startingTopMargin;
        if (this.scoreTableIncluded) {
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
            this.statsTableText.val,
            contentWidth
          );
          doc.text(
            leftMargin,
            startingTopMargin + scoreImageHeight + 20,
            scoreTextLines
          );

          var scoreTextHeight =
            Const.pdfLineHeight * Const.pdfTextFontSize * scoreTextLines.length;
          var topMarginAfterScore =
            startingTopMargin + scoreImageHeight + scoreTextHeight + 20;
        }

        html2canvas(document.getElementById("yesChart")).then(
          recommendCanvas => {
            var topMarginAfterRecommend = topMarginAfterScore;
            if (this.yesChartIncluded) {
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
                this.yesChartText.val,
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
      });
    },
    saveSession: function() {
      let thisRef = this;
      fb.database.ref("/" + fb.auth.currentUser.uid + "/" + this.sessionId).set(
        {
          sessionId: this.sessionId,
          title: this.title,

          infoType: this.infoType,
          inputFileName: this.inputFileName,
          chartData: JSON.stringify(this.chartData),

          statsTableText: this.statsTableText,
          yesChartText: this.yesChartText,

          scoreTableIncluded: this.scoreTableIncluded,
          yesChartIncluded: this.yesChartIncluded
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
              title: "Review Score Visualisation session saved!",
              type: "success",
              message: "Go to History Page to resume previous sessions.",
              duration: 2500
            });
          }
        }
      );
    },
    chooseColorScheme: function(len) {
      switch (len) {
        case 2:
          return Const.colorScheme2;
        case 3:
          return Const.colorScheme3;
        case 5:
          return Const.colorScheme5;
        default:
          return Const.colorScheme10;
      }
    },
    savePdf: function() {
      let fileName = "Review Score Visual Analysis";
      var leftMargin = Const.leftMargin;
      var rightMargin = Const.rightMargin;
      var contentWidth = Const.contentWidth;
      var initialTopMargin = Const.topMargin;
      var doc = new jsPDF("p", "pt");
      var title = "Review Score Visual Analysis";
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

      html2canvas(document.getElementById("scoretable")).then(scoreCanvas => {
        var topMarginAfterScore = startingTopMargin;
        if (this.scoreTableIncluded) {
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
            this.statsTableText.val,
            contentWidth
          );
          doc.text(
            leftMargin,
            startingTopMargin + scoreImageHeight + 20,
            scoreTextLines
          );

          var scoreTextHeight =
            Const.pdfLineHeight * Const.pdfTextFontSize * scoreTextLines.length;
          var topMarginAfterScore =
            startingTopMargin + scoreImageHeight + scoreTextHeight + 20;
        }

        html2canvas(document.getElementById("yeschart")).then(yesCanvas => {
          var topMarginAfterRecommend = topMarginAfterScore;
          if (this.yesChartIncluded) {
            numOfAddedSections += 1;
            var yesImageData = yesCanvas.toDataURL("image/png");
            var yesImageWidth = Const.imageWidth;
            var yesImageHeight =
              (yesCanvas.height * yesImageWidth) / yesCanvas.width;
            doc.addImage(
              yesImageData,
              "PNG",
              leftMargin,
              topMarginAfterScore,
              yesImageWidth,
              yesImageHeight
            );

            var recommendTextLines = doc.splitTextToSize(
              this.yesChartText.val,
              contentWidth
            );
            doc.text(
              leftMargin,
              topMarginAfterScore + yesImageHeight + 20,
              recommendTextLines
            );

            if (numOfAddedSections % 2 == 1) {
              var recommendTextLinesHeight =
                Const.pdfLineHeight *
                Const.pdfTextFontSize *
                recommendTextLines.length;
              topMarginAfterRecommend =
                topMarginAfterScore +
                yesImageHeight +
                recommendTextLinesHeight +
                20;
            }
          }

          doc.save(fileName + ".pdf");
        });
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
p {
  font-weight: bold;
}

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
