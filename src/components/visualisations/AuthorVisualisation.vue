<template>
  <div>
    <editable-header :text.sync="title"/>
    <div class="card">
      <!-- <P>
        {{authorChartIncluded}}
      </p> -->
      <bar-chart 
        id="topauthorchart" 
        ref="topauthorchart" 
        :data-input="topAuthorData" 
        :title-text="'Top Authors'"
        :xAxisLabel="'Author name'"
        :yAxisLabel="'Number of submissions'"
        class="chart"/>
      <!--using text.sync for two-way data binding to editable text child component-->
      <editable-text :text.sync="authorText"/>
      <el-select 
        v-model="authorDataLength" 
        placeholder="Select Length" 
        style="margin-top: 10px;margin-right: 40px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="authorChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <h4>World Heat Map of Submissions by Country</h4>
      <CountryHeatMap :country-data="heatMapData"/>
      <editable-text :text.sync="heatMapText"/>
    </div>
    <div class="card">
      <div 
        id="topcountrychart" 
        ref="topcountrychart">
        <hori-bar-chart 
          v-if="countryChartType=='bar'" 
          :data-input="topCountryData" 
          :title-text="'Top Countries'"
          :xAxisLabel="'Number of submissions'"
          :yAxisLabel="'Country'"
          class="chart"/>
        <pie-chart 
          v-else-if="countryChartType=='pie'" 
          :data-input="topCountryData" 
          :title-text="'Top Countries'"
          class="chart"/>
      </div>
      <editable-text :text.sync="countryText"/>
      <el-select 
        v-model="countryChartType" 
        placeholder="Select Chart" 
        style="margin-top: 20px;margin-right: 10px">
        <el-option
          v-for="item in chartOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-select 
        v-model="countryDataLength" 
        placeholder="Select Length" 
        style="margin-top: 20px;margin-right: 30px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="countryChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <div 
        id="topaffiliationchart" 
        ref="topaffiliationchart">
        <hori-bar-chart 
          v-if="affiliationChartType=='bar'" 
          :data-input="topAffiliationData" 
          :title-text="'Top Affiliations'"
          :xAxisLabel="'Number of submissions'"
          :yAxisLabel="'Organisation name'"
          class="chart"/>
        <pie-chart 
          v-else-if="affiliationChartType=='pie'" 
          :data-input="topAffiliationData" 
          :title-text="'Top Affiliations'"
          class="chart"/>
      </div>
      <editable-text :text.sync="affiliationText"/>
      <el-select 
        v-model="affiliationChartType" 
        placeholder="Select Chart"
        style="margin-top: 20px; margin-right: 10px">
        <el-option
          v-for="item in chartOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-select 
        v-model="affiliationDataLength" 
        placeholder="Select Length"
        style="margin-top: 20px;margin-right: 10px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="affiliationChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <el-button 
      type="success" 
      plain 
      style="margin-top: 10px" 
      @click="saveAuthorNew">Save as PDF</el-button>
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

import CountryHeatMap from 'vue-world-map'
import VueWordCloud from "vuewordcloud";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

import firebase from "firebase";

const fb = require("../firebaseConfiguration.js");
export default {
  name: "AuthorVisualisation",
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
    CountryHeatMap,
    EditableHeader
  },
  props: ["chartData", "infoType", "inputFileName", "sessionData"],
  data: function() {
    // Create sessionId by time if doesnt already exist
    let sessionId = this.sessionData ? this.sessionData.sessionId : Date.now();

    let topAuthors = this.chartData.topAuthors;
    let topCountries = this.chartData.topCountries;
    let topAffiliations = this.chartData.topAffiliations;

    let heatMapData = {};
    let countries = this.chartData.countryCount.labels;
    let countryCount = this.chartData.countryCount.data;
    for (let i = 0; i < countries.length; i++) {
      heatMapData[countries[i]] = countryCount[i];
    }

    let chartOptions = [
      {
        value: "pie",
        label: "Pie Chart"
      },
      {
        value: "bar",
        label: "Bar Chart"
      }
    ];
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
      let authorDataLength = this.sessionData.authorDataLength;
      let countryDataLength = this.sessionData.countryDataLength;
      let affiliationDataLength = this.sessionData.affiliationDataLength;
      return {
        sessionId,
        title: this.sessionData.title,
        authorText: this.sessionData.authorText,
        countryText: this.sessionData.countryText,
        affiliationText: this.sessionData.affiliationText,
        heatMapText: this.sessionData.heatMapText,
        topAuthors,
        topCountries,
        topAffiliations,
        heatMapData,
        chartOptions,
        countryChartType: this.sessionData.countryChartType,
        affiliationChartType: this.sessionData.affiliationChartType,
        dataLengthOptions,
        authorDataLength,
        countryDataLength,
        affiliationDataLength,
        authorChartIncluded: this.sessionData.authorChartIncluded,
        countryChartIncluded: this.sessionData.countryChartIncluded,
        affiliationChartIncluded: this.sessionData.affiliationChartIncluded,
        topAuthorData: this.computeAuthorData(authorDataLength),
        topCountryData: this.computeCountryData(countryDataLength),
        topAffiliationData: this.computeAffiliationData(affiliationDataLength)
      };
    } else {
      return {
        sessionId,
        title: {
          val: "Author Info Analysis",
          edit: false,
        },
        authorText: {
          val:
            "So it's rather clear that the one with the largest number of submissions this year is: " +
            this.chartData.topAuthors.labels[0] +
            ", and all the top " +
            String(3) +
            ", putting together, contribute " +
            String(
              this.chartData.topAuthors.data.slice(0, 3).reduce(function(a, b) {
                return a + b;
              })
            ) +
            " submissions in total.",
          edit: false
        },
        countryText: {
          val:
            "And from the country information (generated from the author data), we can see that the top 1 country, in this case " +
            this.chartData.topCountries.labels[0] +
            ", has made " +
            String(
              (
                ((this.chartData.topCountries.data[0] -
                  this.chartData.topCountries.data[1]) /
                  this.chartData.topCountries.data[1]) *
                100
              ).toFixed(2)
            ) +
            "% more submission than the second-placed " +
            this.chartData.topCountries.labels[1] +
            ".",
          edit: false
        },
        affiliationText: {
          val: "Click here to add in any additional remarks.",
          edit: false
        },
        heatMapText: {
          val: "Click here to add in any additional remarks.",
          edit: false
        },
        topAuthors,
        topCountries,
        topAffiliations,
        heatMapData,
        chartOptions,
        countryChartType: "pie",
        affiliationChartType: "bar",
        dataLengthOptions,
        authorDataLength: 3,
        countryDataLength: 3,
        affiliationDataLength: 3,
        authorChartIncluded: true,
        countryChartIncluded: true,
        affiliationChartIncluded: true,
        topAuthorData: this.computeAuthorData(3),
        topCountryData: this.computeCountryData(3),
        topAffiliationData: this.computeAffiliationData(3)
      };
    }
  },
  watch: {
    authorDataLength: function(newValue, oldValue) {
      var len = newValue;
      var authorInitialText =
        "So it's rather clear that the one with the largest number of submissions this year is: " +
        this.topAuthors.labels[0] +
        ", and all the top " +
        String(len) +
        ", putting together, contribute " +
        String(
          this.topAuthors.data.slice(0, len).reduce(function(a, b) {
            return a + b;
          })
        ) +
        " submissions in total.";
      this.authorText = {
        val: authorInitialText,
        edit: false
      };
      this.topAuthorData = this.computeAuthorData(len);
    },
    countryDataLength: function(newValue, oldValue) {
      var len = newValue;
      var countryInitialText =
        "And from the country information (generated from the author data), we can see that the top 1 country, in this case " +
        this.topCountries.labels[0] +
        ", has made " +
        String(
          (
            ((this.topCountries.data[0] - this.topCountries.data[1]) /
              this.topCountries.data[1]) *
            100
          ).toFixed(2)
        ) +
        "% more submission than the second-placed " +
        this.topCountries.labels[1] +
        ".";
      this.countryText = {
        val: countryInitialText,
        edit: false
      };
      console.log("Inside the data length trigger!");
      this.topCountryData = this.computeCountryData(len);
    },
    affiliationDataLength: function(newValue, oldValue) {
      var len = newValue;
      var affiliationInitialText =
        "You may add in any additional remarks here.";
      this.affiliationText = {
        val: affiliationInitialText,
        edit: false
      };
      this.topAffiliationData = this.computeAffiliationData(len);
    }
  },
  methods: {
    saveAuthor: function() {
      // Still have this function as a reference for what has been done using the mm settings instead of pt
      let fileName = this.title.val;
      var leftMargin = Const.pdfLeftMargin;
      var rightMargin = Const.pdfRightMargin;
      var pdfInMM = Const.pdfInMM;
      var initialTopMargin = Const.pdfTopMargin;
      var doc = new jsPDF("p", "mm", "a4");
      var title = this.title.val;
      doc.setFont("Times");
      doc.setFontSize(Const.pdfTitleFontSize);
      var titleLength =
        doc.getStringUnitWidth(title) *
        Const.pdfTitleFontSize *
        Const.pdfMMPerPT;
      doc.text(
        (pdfInMM - leftMargin - rightMargin - titleLength) / 2.0 + leftMargin,
        initialTopMargin,
        title
      );
      var startingTopMargin =
        initialTopMargin + Const.pdfTitleFontSize * Const.pdfMMPerPT;
      doc.setFontSize(Const.pdfTextFontSize);

      // Attn: For the current impl, the logic is as follows:
      // 1. each page of the PDF file will contain 2 images, together with their texts
      // 2. hence, we use this numO fAddedSections to keep track of how many we have added to PDF
      // 3. so if numOfAddedSections % 2 == 1, then no need to addPage(); else if num > 0, then addPage() and reset topMargin
      var numOfAddedSections = 0;

      html2canvas(document.getElementById("topauthorchart")).then(
        authorCanvas => {
          var topMarginAfterAuthor = startingTopMargin;
          if (this.authorChartIncluded) {
            numOfAddedSections += 1;
            var authorImageData = authorCanvas.toDataURL("image/png");
            doc.addImage(
              authorImageData,
              "PNG",
              15,
              startingTopMargin,
              authorCanvas.width / 8,
              authorCanvas.height / 8
            );

            var authorTextLines = doc.splitTextToSize(
              this.authorText.val,
              pdfInMM - leftMargin - rightMargin
            );
            doc.text(
              leftMargin,
              startingTopMargin + authorCanvas.height / 8 + 10,
              authorTextLines
            );

            // Note: here pdfLineHeight is the line height considering the white space between lines
            var authorTextLinesHeight =
              Const.pdfLineHeight *
              Const.pdfTextFontSize *
              authorTextLines.length;
            topMarginAfterAuthor =
              startingTopMargin +
              authorCanvas.height / 8 +
              authorTextLinesHeight -
              5;
          }

          html2canvas(document.getElementById("topcountrychart")).then(
            countryCanvas => {
              var topMarginAfterCountry = topMarginAfterAuthor;
              if (this.countryChartIncluded) {
                numOfAddedSections += 1;
                var countryImageData = countryCanvas.toDataURL("image/png");
                doc.addImage(
                  countryImageData,
                  "PNG",
                  15,
                  topMarginAfterAuthor,
                  countryCanvas.width / 8,
                  countryCanvas.height / 8
                );

                var countryTextLines = doc.splitTextToSize(
                  this.countryText.val,
                  pdfInMM - leftMargin - rightMargin
                );
                doc.text(
                  leftMargin,
                  topMarginAfterAuthor + countryCanvas.height / 8 + 10,
                  countryTextLines
                );

                if (numOfAddedSections % 2 == 1) {
                  var countryTextLinesHeight =
                    Const.pdfLineHeight *
                    Const.pdfTextFontSize *
                    countryTextLines.length;
                  topMarginAfterCountry =
                    topMarginAfterAuthor +
                    countryCanvas.height / 8 +
                    countryTextLinesHeight -
                    5;
                }
              }

              html2canvas(document.getElementById("topaffiliationchart")).then(
                affiliationCanvas => {
                  if (this.affiliationChartIncluded) {
                    if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                      doc.addPage();
                      topMarginAfterCountry = Const.pdfTopMargin;
                    }
                    var affiliationImageData = affiliationCanvas.toDataURL(
                      "image/png"
                    );
                    doc.addImage(
                      affiliationImageData,
                      "PNG",
                      15,
                      topMarginAfterCountry,
                      affiliationCanvas.width / 8,
                      affiliationCanvas.height / 8
                    );

                    var affiliationTextLines = doc.splitTextToSize(
                      this.affiliationText.val,
                      pdfInMM - leftMargin - rightMargin
                    );
                    doc.text(
                      leftMargin,
                      topMarginAfterCountry + affiliationCanvas.height / 8 + 10,
                      affiliationTextLines
                    );
                  }

                  doc.save(fileName + ".pdf");
                }
              );
            }
          );
        }
      );
    },
    saveAuthorNew: function() {
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

      html2canvas(document.getElementById("topauthorchart")).then(
        authorCanvas => {
          var topMarginAfterAuthor = startingTopMargin;
          if (this.authorChartIncluded) {
            numOfAddedSections += 1;
            var authorImageData = authorCanvas.toDataURL("image/png");
            var authorImageWidth = Const.imageWidth;
            var authorImageHeight =
              (authorCanvas.height * authorImageWidth) / authorCanvas.width;
            doc.addImage(
              authorImageData,
              "PNG",
              leftMargin,
              startingTopMargin,
              authorImageWidth,
              authorImageHeight
            );

            var authorTextLines = doc.splitTextToSize(
              this.authorText.val,
              contentWidth
            );
            doc.text(
              leftMargin,
              startingTopMargin + authorImageHeight + 20,
              authorTextLines
            );

            // Note: here pdfLineHeight is the line height considering the white space between lines
            var authorTextLinesHeight =
              Const.pdfLineHeight *
              Const.pdfTextFontSize *
              authorTextLines.length;
            topMarginAfterAuthor =
              startingTopMargin +
              authorImageHeight +
              authorTextLinesHeight +
              30;
          }

          html2canvas(document.getElementById("topcountrychart")).then(
            countryCanvas => {
              var topMarginAfterCountry = topMarginAfterAuthor;
              if (this.countryChartIncluded) {
                numOfAddedSections += 1;
                var countryImageData = countryCanvas.toDataURL("image/png");
                var countryImageWidth = Const.imageWidth;
                var countryImageHeight =
                  (countryCanvas.height * countryImageWidth) /
                  countryCanvas.width;
                doc.addImage(
                  countryImageData,
                  "PNG",
                  leftMargin,
                  topMarginAfterAuthor,
                  countryImageWidth,
                  countryImageHeight
                );

                var countryTextLines = doc.splitTextToSize(
                  this.countryText.val,
                  contentWidth
                );
                doc.text(
                  leftMargin,
                  topMarginAfterAuthor + countryImageHeight + 20,
                  countryTextLines
                );

                if (numOfAddedSections % 2 == 1) {
                  var countryTextLinesHeight =
                    Const.pdfLineHeight *
                    Const.pdfTextFontSize *
                    countryTextLines.length;
                  topMarginAfterCountry =
                    topMarginAfterAuthor +
                    countryImageHeight +
                    countryTextLinesHeight +
                    20;
                }
              }

              html2canvas(document.getElementById("topaffiliationchart")).then(
                affiliationCanvas => {
                  if (this.affiliationChartIncluded) {
                    if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                      doc.addPage();
                      topMarginAfterCountry = Const.topMargin;
                    }
                    var affiliationImageData = affiliationCanvas.toDataURL(
                      "image/png"
                    );
                    var affiliationImageWidth = Const.imageWidth;
                    var affiliationImageHeight =
                      (affiliationCanvas.height * affiliationImageWidth) /
                      affiliationCanvas.width;
                    doc.addImage(
                      affiliationImageData,
                      "PNG",
                      leftMargin,
                      topMarginAfterCountry,
                      affiliationImageWidth,
                      affiliationImageHeight
                    );

                    var affiliationTextLines = doc.splitTextToSize(
                      this.affiliationText.val,
                      contentWidth
                    );
                    doc.text(
                      leftMargin,
                      topMarginAfterCountry + affiliationImageHeight + 20,
                      affiliationTextLines
                    );
                  }

                  doc.save(fileName + ".pdf");
                }
              );
            }
          );
        }
      );
    },
    saveSession: function() {
      console.log("SAVING SESSION");
      console.log(this.infoType);
      let thisRef = this;
      fb.database
        .ref("/" + fb.auth.currentUser.uid + "/" + this.sessionId)
        .set(
          {
            sessionId: this.sessionId,

            title: this.title,
            
            infoType: this.infoType,
            inputFileName: this.inputFileName,
            chartData: JSON.stringify(this.chartData),

            authorText: this.authorText,
            countryText: this.countryText,
            affiliationText: this.affiliationText,
            heatMapText: this.heatMapText,

            authorDataLength: this.authorDataLength,
            countryDataLength: this.countryDataLength,
            affiliationDataLength: this.affiliationDataLength,

            authorChartIncluded: this.authorChartIncluded,
            countryChartIncluded: this.countryChartIncluded,
            affiliationChartIncluded: this.affiliationChartIncluded,

            countryChartType: this.countryChartType,
            affiliationChartType: this.affiliationChartType
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
                title: "Author Visualisation session saved!",
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
    computeAuthorData: function(len) {
      // var len = this.authorDataLength;
      var scheme = this.chooseColorScheme(len);
      var topAuthorData = {
        labels: this.chartData.topAuthors.labels.slice(0, len),
        datasets: [
          {
            label: "Submission Counts",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.topAuthors.data.slice(0, len)
          }
        ]
      };
      return topAuthorData;
    },
    computeCountryData: function(len) {
      // var len = this.countryDataLength;
      var scheme = this.chooseColorScheme(len);
      var topCountryData = {
        labels: this.chartData.topCountries.labels.slice(0, len),
        datasets: [
          {
            label: "Submission Counts",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.topCountries.data.slice(0, len)
          }
        ]
      };
      console.log(topCountryData)
      return topCountryData;
    },
    computeAffiliationData: function(len) {
      // var len = this.affiliationDataLength;
      var scheme = this.chooseColorScheme(len);
      var topAffiliationData = {
        labels: this.chartData.topAffiliations.labels.slice(0, len),
        datasets: [
          {
            label: "Submission Counts",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: this.chartData.topAffiliations.data.slice(0, len)
          }
        ]
      };
      return topAffiliationData;
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

h4 {
  font-size: 14;
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
