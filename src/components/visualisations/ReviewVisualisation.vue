<template>
  <div>
    <editable-header :text.sync="title"/>
    <div class="card">
      <bar-chart 
        id="scorechart" 
        ref="scorechart" 
        :data-input="scoreDistributionData" 
        :title-text="'Score Distribution'"
        :xAxisLabel="'Weighted Review Score range'"
        :yAxisLabel="'Number of submissions'"
        class="chart"/>
      <editable-text 
        :text.sync="scoreDistributionText" 
        style="margin-bottom: 20px;"/>
      <el-switch
        v-model="scoreDistributionChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <bar-chart 
        id="recommendchart" 
        ref="recommendchart" 
        :data-input="recommendDistributionData"
        :title-text="'Recommendation Distribution'" 
        :xAxisLabel="'Weighted recommendation score range'"
        :yAxisLabel="'Number of submissions'"
        class="chart"/>
      <editable-text 
        :text.sync="recommendDistributionText" 
        style="margin-bottom: 20px;"/>
      <el-switch
        v-model="recommendDistributionChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <p>
        The mean scores and mean confidence values can be found as follows:
      </p><div 
        id="reviewtable" 
        ref="reviewtable">
        <el-table
          :data="reviewTableData"
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
      </div>
      <editable-text :text.sync="reviewTableText"/>
      <el-switch
        v-model="reviewTableIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <el-button 
      type="success" 
      plain 
      style="margin-top: 10px" 
      @click="saveReview">Save as PDF</el-button>
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

const fb = require("../firebaseConfiguration.js");

export default {
  name: "ReviewVisualisation",
  components: {
    LineChart,
    TimeLineChart,
    RadarChart,
    BarChart,
    BarChartDeci,
    HoriBarChart,
    PieChart,
    EditableText,
    [VueWordCloud.name]: VueWordCloud,
    EditableHeader
  },
  props: ["chartData", "infoType", "inputFileName", "sessionData"],
  data: function() {
    // Create sessionId by time if doesnt already exist
    let sessionId = this.sessionData ? this.sessionData.sessionId : Date.now();

    let scoreDistributionData = this.computeScoreDistributionData("score");
    let recommendDistributionData = this.computeScoreDistributionData(
      "recommend"
    );
    let reviewTableData = [
      {
        field: "Mean Score",
        value: this.chartData.meanScore.toFixed(2)
      },
      {
        field: "Mean Recommendation",
        value: this.chartData.meanRecommend.toFixed(2)
      },
      {
        field: "Mean Confidence",
        value: this.chartData.meanConfidence.toFixed(2)
      }
    ];

    let scoreRanges = scoreDistributionData.labels;
    let scoreCounts = recommendDistributionData.datasets[0].data;

    let topIndex = this.indexOfMax(scoreCounts);
    let topRange = scoreRanges[topIndex];

    let recommendCounts = recommendDistributionData.datasets[0].data;
    let firstEntryPercentage =
      (recommendCounts[0] /
        recommendCounts.reduce(function(a, b) {
          return a + b;
        })) *
      100;

    if (this.sessionData) {
      return {
        sessionId,
        title: this.sessionData.title,
        scoreDistributionData,
        recommendDistributionData,
        reviewTableData,
        scoreDistributionChartIncluded: this.sessionData
          .scoreDistributionChartIncluded,
        recommendDistributionChartIncluded: this.sessionData
          .recommendDistributionChartIncluded,
        reviewTableIncluded: this.sessionData.reviewTableIncluded,
        scoreDistributionText: this.sessionData.scoreDistributionText,
        recommendDistributionText: this.sessionData.recommendDistributionText,
        reviewTableText: this.sessionData.reviewTableText
      };
    } else {
      return {
        sessionId,
        title: {
          val: "Review Info Analysis",
          edit: false
        },
        scoreDistributionData,
        recommendDistributionData,
        reviewTableData,
        scoreDistributionChartIncluded: true,
        recommendDistributionChartIncluded: true,
        reviewTableIncluded: true,
        scoreDistributionText: {
          val:
            "Note that when considering the review scores, we are combining multiple entries at the same time: here for the overall score of each paper, we take all reviews for a particular paper, retrieve its overall score and the reviewer's confidence, then calculate the weighted average of the scores w.r.t. the confidence value, and then here it is. It's rather clear that the score range with the largest count is " +
            String(topRange) + ".",
          edit: false
        },
        recommendDistributionText: {
          val:
            "The same logic applies to the recommendation scores. Note that we use 0 to represent 'not recommended for best paper', and 1 as 'recommended for best paper', and then do a weighted average using the confidence value. It's hence also clear that the 0's takes up " +
            String(firstEntryPercentage.toFixed(2)) +
            "%.",
          edit: false
        },
        reviewTableText: {
          val:
            "The mean score and recommendation values can be found here, and you are free to add in any additional comments and remarks here.",
          edit: false
        }
      };
    }
  },
  watch: {},
  methods: {
    saveReview: function() {
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

      html2canvas(document.getElementById("scorechart")).then(scoreCanvas => {
        var topMarginAfterScore = startingTopMargin;
        if (this.scoreDistributionChartIncluded) {
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
            this.scoreDistributionText.val,
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

        html2canvas(document.getElementById("recommendchart")).then(
          recommendCanvas => {
            var topMarginAfterRecommend = topMarginAfterScore;
            if (this.recommendDistributionChartIncluded) {
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
                this.recommendDistributionText.val,
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

            html2canvas(document.getElementById("reviewtable")).then(
              tableCanvas => {
                if (this.reviewTableIncluded) {
                  if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                    doc.addPage();
                    topMarginAfterRecommend = Const.topMargin;
                  }
                  var tableImageData = tableCanvas.toDataURL("image/png");
                  var tableImageWidth = Const.imageWidth;
                  var tableImageHeight =
                    (tableCanvas.height * tableImageWidth) / tableCanvas.width;
                  doc.addImage(
                    tableImageData,
                    "PNG",
                    leftMargin,
                    topMarginAfterRecommend,
                    tableImageWidth,
                    tableImageHeight
                  );

                  var tableTextLines = doc.splitTextToSize(
                    this.reviewTableText.val,
                    contentWidth
                  );
                  doc.text(
                    leftMargin,
                    topMarginAfterRecommend + tableImageHeight + 20,
                    tableTextLines
                  );
                }

                doc.save(fileName + ".pdf");
              }
            );
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

          scoreDistributionText: this.scoreDistributionText,
          recommendDistributionText: this.recommendDistributionText,
          reviewTableText: this.reviewTableText,

          reviewTableData: this.reviewTableData,

          scoreDistributionChartIncluded: this.scoreDistributionChartIncluded,
          recommendDistributionChartIncluded: this
            .recommendDistributionChartIncluded,
          reviewTableIncluded: this.reviewTableIncluded
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
              title: "Review Visualisation session saved!",
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
    },
    computeScoreDistributionData: function(type) {
      // Type: "score" or "recommend"
      var label = type == "score" ? "Score Counts" : "Recommendation Counts";
      var rawData =
        type == "score"
          ? this.chartData.scoreDistribution
          : this.chartData.recommendDistribution;
      return {
        labels: rawData.labels,
        datasets: [
          {
            label: label,
            data: rawData.counts,
            backgroundColor: "rgba(52, 152, 219, 0.4)",
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF"
          }
        ]
      };
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
