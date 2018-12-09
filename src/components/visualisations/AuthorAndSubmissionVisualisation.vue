<template>
  <div>
    <editable-header :text.sync="title"/>
    <div class="card">
      <div 
        id="topAccepteddCountries" 
        ref="topAccepteddCountries">
        <bar-chart 
          :data-input="topAcceptedCountriesData" 
          :title-text="'Top Accepted Countries'"
          :x-axis-label="'Country'"
          :y-axis-label="'Accepted paper count'"
          class="chart"/>
      </div>
      <editable-text :text.sync="topAcceptedCountriesText"/>
      <el-select 
        v-model="topAcceptedCountriesDataLength" 
        placeholder="Select Length"
        style="margin-top: 20px;margin-right: 10px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="topAcceptedCountriesChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>

    <div class="card">
      <div 
        id="topRejectedCountries" 
        ref="topRejectedCountries">
        <bar-chart 
          :data-input="topRejectedCountriesData" 
          :title-text="'Top Rejected Countries'"
          :x-axis-label="'Country'"
          :y-axis-label="'Rejected paper count'"
          class="chart"/>
      </div>
      <editable-text :text.sync="topRejectedCountriesText"/>
      <el-select 
        v-model="topRejectedCountriesDataLength" 
        placeholder="Select Length"
        style="margin-top: 20px;margin-right: 10px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="topRejectedCountriesChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>

     <div class="card">
      <div 
        id="topAcceptedOrganisations" 
        ref="topAcceptedOrganisations">
        <bar-chart 
          :data-input="topAcceptedOrganisationsData" 
          :title-text="'Top Accepted Organisations'"
          :x-axis-label="'Organisation'"
          :y-axis-label="'Accepted paper count'"
          class="chart"/>
      </div>
      <editable-text :text.sync="topAcceptedOrganisationsText"/>
      <el-select 
        v-model="topAcceptedOrganisationsDataLength" 
        placeholder="Select Length"
        style="margin-top: 20px;margin-right: 10px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="topAcceptedOrganisationsChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>

    <div class="card">
      <div 
        id="topRejectedOrganisations" 
        ref="topRejectedOrganisations">
        <bar-chart 
          :data-input="topRejectedOrganisationsData" 
          :title-text="'Top Rejected Organisations'"
          :x-axis-label="'Organisation'"
          :y-axis-label="'Rejected paper count'"
          class="chart"/>
      </div>
      <editable-text :text.sync="topRejectedOrganisationsText"/>
      <el-select 
        v-model="topRejectedOrganisationsDataLength" 
        placeholder="Select Length"
        style="margin-top: 20px;margin-right: 10px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="topRejectedOrganisationsChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>

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
  name: "AuthorAndSubmissionVisualisation",
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
    // parsedResult['topAcceptedOrganisations'] = acceptedOrg
	// parsedResult['topRejectedOrganisations'] = rejectedOrg

	// parsedResult['topAcceptedCountries'] = acceptedCountry
    // parsedResult['topRejectedCountries'] = rejectedCountry
    let topAcceptedOrganisations = this.chartData.topAcceptedOrganisations;
    let topRejectedOrganisations = this.chartData.topRejectedOrganisations;
    let topAcceptedCountries = this.chartData.topAcceptedCountries;
    let topRejectedCountries = this.chartData.topRejectedCountries;

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
      let topAcceptedCountriesDataLength = this.sessionData.topAcceptedCountriesDataLength;
      let topAcceptedOrganisationsDataLength = this.sessionData.topAcceptedOrganisationsDataLength;
      let topRejectedCountriesDataLength = this.sessionData.topRejectedCountriesDataLength;
      let topRejectedOrganisationsDataLength = this.sessionData.topRejectedOrganisationsDataLength;
      return {
        sessionId,
        title: this.sessionData.title,

        dataLengthOptions,

        topAcceptedCountriesDataLength,
        topAcceptedCountriesData: this.computeTopAcceptedCountriesData(topAcceptedCountriesDataLength),
        topAcceptedCountriesChartIncluded: this.sessionData.topAcceptedCountriesChartIncluded,
        topAcceptedCountriesText: this.sessionData.topAcceptedCountriesText,

        topRejectedCountriesDataLength,
        topRejectedCountriesData: this.computeTopRejectedCountriesData(topRejectedCountriesDataLength),
        topRejectedCountriesChartIncluded: this.sessionData.topRejectedCountriesChartIncluded,
        topRejectedCountriesText: this.sessionData.topRejectedCountriesText,
        
        topAcceptedOrganisationsDataLength,
        topAcceptedOrganisationsData: this.computeTopAcceptedOrganisationData(topAcceptedOrganisationsDataLength),
        topAcceptedOrganisationsChartIncluded: this.sessionData.topAcceptedOrganisationsChartIncluded,
        topAcceptedOrganisationsText: this.sessionData.topAcceptedOrganisationsText,

        topRejectedOrganisationsDataLength,
        topRejectedOrganisationsData: this.computeTopRejectedOrganisationData(topRejectedOrganisationsDataLength),
        topRejectedOrganisationsChartIncluded: this.sessionData.topRejectedOrganisationsChartIncluded,
        topRejectedOrganisationsText: this.sessionData.topRejectedOrganisationsText,

      };
    } else {
      return {
        sessionId,
        title: {
          val: "Author & Submission Info Analysis",
          edit: false
        },

        dataLengthOptions,

        topAcceptedCountriesDataLength: 3,
        topAcceptedCountriesData: this.computeTopAcceptedCountriesData(3),
        topAcceptedCountriesChartIncluded: true,
        topAcceptedCountriesText: {
          val: "Insert text here",
          edit: false
        },

        topAcceptedOrganisationsDataLength: 3,
        topAcceptedOrganisationsData: this.computeTopAcceptedOrganisationData(3),
        topAcceptedOrganisationsChartIncluded: true,
        topAcceptedOrganisationsText: {
          val: "Insert text here",
          edit: false
        },

        topRejectedCountriesDataLength: 3,
        topRejectedCountriesData: this.computeTopRejectedCountriesData(3),
        topRejectedCountriesChartIncluded: true,
        topRejectedCountriesText: {
          val: "Insert text here",
          edit: false
        },

        topRejectedOrganisationsDataLength: 3,
        topRejectedOrganisationsData: this.computeTopRejectedOrganisationData(3),
        topRejectedOrganisationsChartIncluded: true,
        topRejectedOrganisationsText: {
          val: "Insert text here",
          edit: false
        }
      };
    }
  },
  watch: {
    topAcceptedCountriesDataLength: function(newValue, oldValue) {
      var len = newValue;
      this.topCountriesData = this.computeTopAcceptedCountriesData(len);
    },
    topAcceptedOrganisationsDataLength: function(newValue, oldValue) {
      var len = newValue;
      this.bestPaperAuthorsData = this.computeTopAcceptedOrganisationData(len);
    },
    topRejectedCountriesDataLength: function(newValue, oldValue) {
      var len = newValue;
      this.topCountriesData = this.computeTopRejectedCountriesData(len);
    },
    topRejectedOrganisationsDataLength: function(newValue, oldValue) {
      var len = newValue;
      this.bestPaperAuthorsData = this.computeTopRejectedOrganisationData(len);
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

            topRejectedCountriesDataLength: this.topRejectedCountriesDataLength,
            topRejectedCountriesText: this.topRejectedCountriesText,
            topRejectedCountriesChartIncluded: this.topRejectedCountriesChartIncluded,

            topRejectedOrganisationsDataLength: this.topRejectedOrganisationsDataLength,
            topRejectedOrganisationsText: this.topRejectedOrganisationsText,
            topRejectedOrganisationsChartIncluded: this.topRejectedOrganisationsChartIncluded,

            topAcceptedCountriesDataLength: this.topAcceptedCountriesDataLength,
            topAcceptedCountriesText: this.topAcceptedCountriesText,
            topAcceptedCountriesChartIncluded: this.topAcceptedCountriesChartIncluded,

            topAcceptedOrganisationsDataLength: this.topAcceptedOrganisationsDataLength,
            topAcceptedOrganisationsText: this.topAcceptedOrganisationsText,
            topAcceptedOrganisationsChartIncluded: this.topAcceptedOrganisationsChartIncluded,

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
                title: "Author and Submission Visualisation session saved!",
                type: "success",
                message: "Go to History Page to resume previous sessions.",
                duration: 2500
              });
            }
          }
        );
    },
    computeTopAcceptedCountriesData: function(len) {
      let scheme = this.chooseColorScheme(len);
      let topAcceptedCountriesData = {
        labels: this.chartData.topAcceptedCountries.slice(0, len).map(arr => arr[0]),
        datasets: [
          {
            label: "Top Accepted Countries",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.topAcceptedCountries.slice(0, len).map(arr => arr[1])
          }
        ]
      };
      return topAcceptedCountriesData;
    },
    computeTopRejectedCountriesData: function(len) {
      let scheme = this.chooseColorScheme(len);
      let topRejectedCountriesData = {
        labels: this.chartData.topRejectedCountries.slice(0, len).map(arr => arr[0]),
        datasets: [
          {
            label: "Top Rejected Countries",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.topRejectedCountries.slice(0, len).map(arr => arr[1])
          }
        ]
      };
      return topRejectedCountriesData;
    },
    computeTopAcceptedOrganisationData: function(len) {
      let scheme = this.chooseColorScheme(len);
      let topAcceptedOrganisationsData = {
        labels: this.chartData.topAcceptedOrganisations
          .slice(0, len)
          .map(arr => arr[0]),
        datasets: [
          {
            label: "Top Accepted Organisations",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.topAcceptedOrganisations
              .slice(0, len)
              .map(arr => arr[1])
          }
        ]
      };
      return topAcceptedOrganisationsData;
    },
   computeTopRejectedOrganisationData: function(len) {
      let scheme = this.chooseColorScheme(len);
      let topRejectedOrganisationsData = {
        labels: this.chartData.topRejectedOrganisations
          .slice(0, len)
          .map(arr => arr[0]),
        datasets: [
          {
            label: "Top Rejected Organisations",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.topRejectedOrganisations
              .slice(0, len)
              .map(arr => arr[1])
          }
        ]
      };
      return topRejectedOrganisationsData;
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
