<template>
  <div>
    <editable-header :text.sync="title"/>
    <div class="card">
      <div 
        id="topcountrieschart" 
        ref="topcountrieschart">
        <hori-bar-chart 
          :data-input="topCountriesData" 
          :title-text="'Top Countries'"
          :x-axis-label="'Average Score'"
          :y-axis-label="'Country'"
          class="chart"/>
      </div>
      <editable-text :text.sync="topCountriesText"/>
      <el-select 
        v-model="topCountriesDataLength" 
        placeholder="Select Length"
        style="margin-top: 20px;margin-right: 10px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="topCountriesChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>

    <div class="card">
      <div 
        id="toporganisationschart" 
        ref="toporganisationschart">
        <hori-bar-chart 
          :data-input="topOrganisationsData" 
          :title-text="'Top Countries'"
          :x-axis-label="'Average Score'"
          :y-axis-label="'Organisation'"
          class="chart"/>
      </div>
      <editable-text :text.sync="topOrganisationsText"/>
      <el-select 
        v-model="topOrganisationsDataLength" 
        placeholder="Select Length"
        style="margin-top: 20px;margin-right: 10px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="topOrganisationsChartIncluded"
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
  name: "AuthorAndReviewVisualisation",
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

    let countryScores = this.chartData.countryScores;
    let organisationScores = this.chartData.organisationScores;
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
      let topCountriesDataLength = this.sessionData.topCountriesDataLength;
      let topOrganisationsDataLength = this.sessionData
        .topOrganisationsDataLength;
      return {
        sessionId,
        title: this.sessionData.title,

        dataLengthOptions,

        topCountriesDataLength,
        topCountriesData: this.computeTopCountriesData(topCountriesDataLength),
        topCountriesChartIncluded: this.sessionData.topCountriesChartIncluded,
        topCountriesText: this.sessionData.topCountriesText,

        topOrganisationsDataLength,
        topOrganisationsData: this.computeTopOrganisationData(
          topOrganisationsDataLength
        ),
        topOrganisationsChartIncluded: this.sessionData
          .topOrganisationsChartIncluded,
        topOrganisationsText: this.sessionData.topOrganisationsText
      };
    } else {
      return {
        sessionId,
        title: {
          val: "Author & Review Info Analysis",
          edit: false
        },

        dataLengthOptions,

        topCountriesDataLength: 3,
        topCountriesData: this.computeTopCountriesData(3),
        topCountriesChartIncluded: true,
        topCountriesText: {
          val: "Click here to insert text",
          edit: false
        },

        topOrganisationsDataLength: 3,
        topOrganisationsData: this.computeTopOrganisationData(3),
        topOrganisationsChartIncluded: true,
        topOrganisationsText: {
          val: "Click here to insert text",
          edit: false
        }
      };
    }
  },
  watch: {
    topCountriesDataLength: function(newValue, oldValue) {
      var len = newValue;
      this.topCountriesData = this.computeTopCountriesData(len);
    },
    topOrganisationsDataLength: function(newValue, oldValue) {
      var len = newValue;
      this.bestPaperAuthorsData = this.computeTopOrganisationData(len);
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

      html2canvas(document.getElementById("topcountrieschart")).then(
        scoreCanvas => {
          var topMarginAfterScore = startingTopMargin;
          if (this.topCountriesChartIncluded) {
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
              this.topCountriesText.val,
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

          html2canvas(document.getElementById("toporganisationschart")).then(
            recommendCanvas => {
              var topMarginAfterRecommend = topMarginAfterScore;
              if (this.topOrganisationsChartIncluded) {
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
                  this.topOrganisationsText.val,
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
      fb.database
        .ref("/" + this.$store.getters.getUser.uid + "/" + this.sessionId)
        .set(
          {
            sessionId: this.sessionId,
            title: this.title,

            infoType: this.infoType,
            inputFileName: this.inputFileName,
            chartData: JSON.stringify(this.chartData),

            topCountriesDataLength: this.topCountriesDataLength,
            topCountriesText: this.topCountriesText,
            topCountriesChartIncluded: this.topCountriesChartIncluded,

            topOrganisationsDataLength: this.topOrganisationsDataLength,
            topOrganisationsText: this.topOrganisationsText,
            topOrganisationsChartIncluded: this.topOrganisationsChartIncluded,

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
                title: "Author and Review Visualisation session saved!",
                type: "success",
                message: "Go to History Page to resume previous sessions.",
                duration: 2500
              });
            }
          }
        );
    },
    computeTopCountriesData: function(len) {
      let scheme = this.chooseColorScheme(len);
      let topCountriesData = {
        labels: this.chartData.countryScores.slice(0, len).map(arr => arr[0]),
        datasets: [
          {
            label: "Top Countries",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.countryScores.slice(0, len).map(arr => arr[1])
          }
        ]
      };
      return topCountriesData;
    },
    computeTopOrganisationData: function(len) {
      let scheme = this.chooseColorScheme(len);
      let topOrganisationsData = {
        labels: this.chartData.organisationScores
          .slice(0, len)
          .map(arr => arr[0]),
        datasets: [
          {
            label: "Top Organisations",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.organisationScores
              .slice(0, len)
              .map(arr => arr[1])
          }
        ]
      };
      return topOrganisationsData;
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
