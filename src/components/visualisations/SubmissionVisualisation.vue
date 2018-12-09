<template>
  <div>
    <editable-header :text.sync="title"/>
    <div class="card">
      <time-line-chart 
        id="timeserieschart" 
        ref="timeserieschart"
        :data-input="timeSeriesData" 
        :title-text="'Submission Time Series'" 
        :yAxisLabel="'Number of submissions'"
        :annotation="JCDLAnnotation"
        class="chart"/>
      <editable-text 
        :text.sync="timeseriesText" 
        style="margin-bottom: 20px;"/>
      <el-switch
        v-model="timeSeriesChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <line-chart 
        id="historicalchart" 
        ref="historicalchart" 
        :data-input="historicalAcceptanceRate"
        :title-text="'Past Years Acceptance Rates'" 
        :xAxisLabel="'Year'"
        :yAxisLabel="'Acceptance rate'"        
        class="chart"/>
      <editable-text :text.sync="historicalAcceptanceText"/>
      <el-switch
        v-model="historicalAcceptanceChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <div 
        id="acceptancechart" 
        ref="acceptancechart">
        <bar-chart-deci 
          v-if="acceptanceRateChartType=='bar'" 
          :data-input="acceptanceRateByTrackData"
          :title-text="'Acceptance Rate By Track'"
          :xAxisLabel="'Track'"
          :yAxisLabel="'Acceptance Rate'" 
          class="chart"/>
        <radar-chart 
          v-else-if="acceptanceRateChartType=='radar'" 
          :data-input="acceptanceRateByTrackData" 
          :title-text="'Acceptance Rate By Track'"
          class="chart"/>
      </div>
      <editable-text :text.sync="acceptanceRateByTrackText"/>
      <el-select 
        v-model="acceptanceRateChartType" 
        placeholder="Select Chart"
        style="margin-top: 20px; margin-right: 30px">
        <el-option
          v-for="item in chartOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="acceptanceRateByTrackChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <hori-bar-chart 
        id="topacceptedauthorchart" 
        ref="topacceptedauthorchart"
        :data-input="topAcceptedAuthorsData" 
        :title-text="'Top Accepted Authors/Contributors'" 
        :xAxisLabel="'Number of accepted papers'"
        :yAxisLabel="'Author name'"
        class="chart"/>
      <editable-text 
        :text.sync="topAcceptedAuthorsText" 
        style="margin-bottom: 20px;"/>
      <el-select 
        v-model="topAcceptedAuthorsDataLength" 
        placeholder="Select Length"
        style="margin-top: 20px;margin-right: 30px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="topAcceptedAuthorsChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <hori-bar-chart 
        id="topacceptedauthorbytrackchart" 
        ref="topacceptedauthorbytrackchart" 
        :data-input="topAcceptedAuthorsByTrackData"
        :title-text="'Top Accepted Authors By Track'" 
        :xAxisLabel="'Number of accepted papers'"
        :yAxisLabel="'Author'"
        class="chart"/>
      <editable-text 
        :text.sync="topAcceptedAuthorsByTrackText" 
        style="margin-bottom: 20px;"/>
      <el-select 
        v-model="topAcceptedAuthorsByTrackLength" 
        placeholder="Select Length"
        style="margin-top: 20px;margin-right: 10px">
        <el-option
          v-for="item in dataLengthOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-select 
        v-model="topAcceptedAuthorsSelectedTrack" 
        placeholder="Select Length"
        style="margin-top: 10px;margin-right: 30px">
        <el-option
          v-for="item in trackOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="topAcceptedAuthorsByTrackChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <!--Note: due to the constraint of the component, the style width and height must be specified-->
      <div 
        id="wordcloudall" 
        ref="wordcloudall">
        <h4>Word Cloud for All Submissions</h4>
        <vue-word-cloud 
          :words="wordCloudTotal"
          :animation-duration="50"
          :color="([, weight]) => weight > 10 ? 'Red' : weight > 5 ? 'Blue' : 'Black'"
          font-family="Arial"
          style="width: 100%;height: 200px"/>
      </div>
      <el-switch
        v-model="wordCloudAllIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <div 
        id="wordcloudaccept" 
        ref="wordcloudaccept">
        <h4>Word Cloud for Accepted Papers</h4>
        <vue-word-cloud 
          :words="acceptedWordCloud"
          :animation-duration="50"
          :color="([, weight]) => weight > 10 ? 'Red' : weight > 5 ? 'Blue' : 'Black'"
          font-family="Arial"
          style="width: 100%;height: 200px"/>
      </div>
      <el-switch
        v-model="wordCloudAcceptedIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>
    <div class="card">
      <div 
        id="wordcloudtrack" 
        ref="wordcloudtrack">
        <h4>Word Cloud for Submissions by Track</h4>

        <vue-word-cloud 
          :words="wordCloudByTrack[wordCloudSelectedTrack]"
          :animation-duration="100"
          :color="([, weight]) => weight > 10 ? 'Red' : weight > 5 ? 'Blue' : 'Black'"
          font-family="Arial"
          style="width: 100%;height: 200px"/>
      </div>
      <el-select 
        v-model="wordCloudSelectedTrack" 
        placeholder="Select Length"
        style="margin-top: 10px;margin-right: 10px">
        <el-option
          v-for="item in trackOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
      </el-select>
      <el-switch
        v-model="wordCloudByTrackIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"/>
    </div>

    <el-button 
      type="success" 
      plain 
      style="margin-top: 20px" 
      @click="saveSubmission">Save as PDF</el-button>
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
  name: "SubmissionVisualisation",
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
    EditableHeader,
  },
  props: ["chartData", "infoType", "inputFileName", "sessionData"],
  data: function() {
    // Create sessionId by time if doesnt already exist
    let sessionId = this.sessionData ? this.sessionData.sessionId : Date.now();

    let tracks = this.computeAcceptanceRateByTrack().labels;
    let acceptanceRateByTrackData = this.computeAcceptanceRateByTrack()
      .datasets[0].data;
    let acceptanceRate = this.chartData.acceptanceRate.toFixed(2);

    let trackOptions = this.getTrackInSubmission().map(function(track) {
      return { value: track, label: track };
    });
    let chartOptions = [
      {
        value: "bar",
        label: "Bar Chart"
      },
      {
        value: "radar",
        label: "Radar Chart"
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

    let wordCloudTotal = this.chartData.overallKeywordList;
    let acceptedWordCloud = this.chartData.acceptedKeywordList;
    let wordCloudByTrack = this.chartData.keywordsByTrack;

    let historicalAcceptanceRate = this.computeHistoricalAcceptanceRate();
    let timeSeriesData = this.computeTimeSeriesData();
    let JCDLAnnotation = this.computeJCDLDeadlineData();

    let topIndex = this.indexOfMax(acceptanceRateByTrackData);
    let topTrack = tracks[topIndex];
    let topValue = acceptanceRateByTrackData[topIndex] * 100;

    if (this.sessionData) {
      return {
        sessionId,
        title: this.sessionData.title,
        acceptanceRate,

        acceptanceRateSelectedTrack: this.sessionData
          .acceptanceRateSelectedTrack,
        topAcceptedAuthorsSelectedTrack: this.sessionData
          .topAcceptedAuthorsSelectedTrack,
        wordCloudSelectedTrack: this.sessionData.wordCloudSelectedTrack,

        trackOptions,
        chartOptions,
        dataLengthOptions,

        acceptanceRateChartType: this.sessionData.acceptanceRateChartType,

        wordCloudTotal,
        acceptedWordCloud,
        wordCloudByTrack,

        historicalAcceptanceRate,
        timeSeriesData,
        JCDLAnnotation,

        acceptanceRateByTrackData: this.computeAcceptanceRateByTrack(),
        topAcceptedAuthorsData: this.computeTopAcceptedAuthors(
          this.sessionData.topAcceptedAuthorsDataLength
        ),
        topAcceptedAuthorsDataLength: this.sessionData
          .topAcceptedAuthorsDataLength,

        topAcceptedAuthorsByTrackData: this.computeTopAcceptedAuthorsByTrack(
          this.sessionData.topAcceptedAuthorsDataLength,
          this.sessionData.topAcceptedAuthorsSelectedTrack
        ),
        topAcceptedAuthorsByTrackLength: this.sessionData
          .topAcceptedAuthorsByTrackLength,
        topAcceptedAuthorsByTrackChartIncluded: this.sessionData
          .topAcceptedAuthorsByTrackChartIncluded,

        timeseriesText: this.sessionData.timeseriesText,
        historicalAcceptanceText: this.sessionData.historicalAcceptanceText,
        acceptanceRateByTrackText: this.sessionData.acceptanceRateByTrackText,
        topAcceptedAuthorsText: this.sessionData.topAcceptedAuthorsText,
        topAcceptedAuthorsByTrackText: this.sessionData
          .topAcceptedAuthorsByTrackText,

        timeSeriesChartIncluded: this.sessionData.timeSeriesChartIncluded,
        historicalAcceptanceChartIncluded: this.sessionData
          .historicalAcceptanceChartIncluded,
        acceptanceRateByTrackChartIncluded: this.sessionData
          .acceptanceRateByTrackChartIncluded,
        topAcceptedAuthorsChartIncluded: this.sessionData
          .topAcceptedAuthorsChartIncluded,
        wordCloudAllIncluded: this.sessionData.wordCloudAllIncluded,
        wordCloudAcceptedIncluded: this.sessionData.wordCloudAcceptedIncluded,
        wordCloudByTrackIncluded: this.sessionData.wordCloudByTrackIncluded
      };
    } else {
      return {
        sessionId,
        title: {
          val: "Submission Info Analysis",
          edit: false,
        },
        acceptanceRate,

        acceptanceRateSelectedTrack: "Full Papers",
        topAcceptedAuthorsSelectedTrack: "Full Papers",
        wordCloudSelectedTrack: "Full Papers",

        trackOptions,
        chartOptions,
        dataLengthOptions,

        acceptanceRateChartType: "bar",

        wordCloudTotal,
        acceptedWordCloud,
        wordCloudByTrack,

        historicalAcceptanceRate,
        timeSeriesData,
        JCDLAnnotation,

        acceptanceRateByTrackData: this.computeAcceptanceRateByTrack(),
        topAcceptedAuthorsData: this.computeTopAcceptedAuthors(3),
        topAcceptedAuthorsDataLength: 3,

        topAcceptedAuthorsByTrackData: this.computeTopAcceptedAuthorsByTrack(
          3,
          "Full Papers"
        ),
        topAcceptedAuthorsByTrackLength: 3,
        topAcceptedAuthorsByTrackChartIncluded: true,

        timeseriesText: {
          val:
            "It can be identified clearly from the chart that most researchers won't submit their work until the last moment. Additionally, although some people made changes to their work after the first submission, the vast majority of people create the entry and make it the final version, since the red curve and blue curve overlaps in most of the time.",
          // val: "This is a sample text.",
          edit: false
        },
        historicalAcceptanceText: {
          val:
            "The historical data on the acceptance rate of JCDL can be found here, appending this year's data in the end. You might notice that for full papers, the rate has seen a major increase from earlier works, while there have been some fluctuations for short papers.",
          edit: false
        },
        acceptanceRateByTrackText: {
          val:
            "Then for this year's work, we can divide them into different tracks to examine the details: the track " +
            String(topTrack) +
            " has the largest acceptance rate, at around " +
            String(topValue.toFixed(2)) +
            "%. Noticeably, Doctoral Consortium and Tutorials didn't take in any entries this year.",
          edit: false
        },
        topAcceptedAuthorsText: {
          val:
            "As for the authors, congratulations to Prof. " +
            String(this.chartData.topAcceptedAuthors.names[0]) +
            " for getting " +
            String(this.chartData.topAcceptedAuthors.counts[0]) +
            " papers/projects accepted to JCDL 2018.",
          edit: false
        },
        topAcceptedAuthorsByTrackText: {
          val:
            "You may want to dig into different tracks of submissions, and here you can check out the researchers who contribute the most to the selected track.",
          edit: false
        },

        timeSeriesChartIncluded: true,
        historicalAcceptanceChartIncluded: true,
        acceptanceRateByTrackChartIncluded: true,
        topAcceptedAuthorsChartIncluded: true,
        wordCloudAllIncluded: true,
        wordCloudAcceptedIncluded: true,
        wordCloudByTrackIncluded: true
      };
    }
  },
  watch: {
    topAcceptedAuthorsDataLength: function(newValue, oldValue) {
      var len = newValue;
      this.topAcceptedAuthorsData = this.computeTopAcceptedAuthors(len);
    },
    topAcceptedAuthorsSelectedTrack: function(newValue, oldValue) {
      this.topAcceptedAuthorsByTrackData = this.computeTopAcceptedAuthorsByTrack(
        this.topAcceptedAuthorsByTrackLength,
        newValue
      );
    },
    topAcceptedAuthorsByTrackLength: function(newValue, oldValue) {
      var len = newValue;
      this.topAcceptedAuthorsByTrackData = this.computeTopAcceptedAuthorsByTrack(
        len,
        this.topAcceptedAuthorsSelectedTrack
      );
    }
  },
  methods: {
    saveSubmission: function() {
      let fileName = this.title.val;
      var leftMargin = Const.leftMargin;
      var rightMargin = Const.rightMargin;
      var initialTopMargin = Const.topMargin;
      var contentWidth = Const.contentWidth;
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

      html2canvas(document.getElementById("timeserieschart")).then(
        timeCanvas => {
          var topMarginAfterTime = startingTopMargin;
          if (this.timeSeriesChartIncluded) {
            numOfAddedSections += 1;

            var timeImageData = timeCanvas.toDataURL("image/png");
            var timeImageWidth = Const.imageWidth;
            var timeImageHeight =
              (timeCanvas.height * timeImageWidth) / timeCanvas.width;
            doc.addImage(
              timeImageData,
              "PNG",
              leftMargin,
              startingTopMargin,
              timeImageWidth,
              timeImageHeight
            );

            var timeTextLines = doc.splitTextToSize(
              this.timeseriesText.val,
              contentWidth
            );
            doc.text(
              leftMargin,
              startingTopMargin + timeImageHeight + 20,
              timeTextLines
            );

            // Note: here pdfLineHeight is the line height considering the white space between lines
            var timeTextLinesHeight =
              Const.pdfLineHeight *
              Const.pdfTextFontSize *
              timeTextLines.length;
            topMarginAfterTime =
              startingTopMargin + timeImageHeight + timeTextLinesHeight + 20;
          }

          html2canvas(document.getElementById("historicalchart")).then(
            historicalCanvas => {
              var topMarginAfterHistorical = topMarginAfterTime;
              if (this.historicalAcceptanceChartIncluded) {
                numOfAddedSections += 1;

                var historicalImageData = historicalCanvas.toDataURL(
                  "image/png"
                );
                var historicalImageWidth = Const.imageWidth;
                var historicalImageHeight =
                  (historicalCanvas.height * historicalImageWidth) /
                  historicalCanvas.width;
                doc.addImage(
                  historicalImageData,
                  "PNG",
                  leftMargin,
                  topMarginAfterTime,
                  historicalImageWidth,
                  historicalImageHeight
                );

                var historicalTextLines = doc.splitTextToSize(
                  this.historicalAcceptanceText.val,
                  contentWidth
                );
                doc.text(
                  leftMargin,
                  topMarginAfterTime + historicalImageHeight + 20,
                  historicalTextLines
                );

                if (numOfAddedSections % 2 == 1) {
                  var historicalTextLinesHeight =
                    Const.pdfLineHeight *
                    Const.pdfTextFontSize *
                    historicalTextLines.length;
                  topMarginAfterHistorical =
                    topMarginAfterTime +
                    historicalImageHeight +
                    historicalTextLinesHeight +
                    20;
                }
              }

              html2canvas(document.getElementById("acceptancechart")).then(
                acceptanceCanvas => {
                  var topMarginAfterAccept = topMarginAfterHistorical;
                  if (this.acceptanceRateByTrackChartIncluded) {
                    if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                      doc.addPage();
                      topMarginAfterHistorical = Const.topMargin;
                    }

                    numOfAddedSections += 1;
                    var acceptImageData = acceptanceCanvas.toDataURL(
                      "image/png"
                    );
                    var acceptImageWidth = Const.imageWidth;
                    var acceptImageHeight =
                      (acceptanceCanvas.height * acceptImageWidth) /
                      acceptanceCanvas.width;
                    doc.addImage(
                      acceptImageData,
                      "PNG",
                      leftMargin,
                      topMarginAfterHistorical,
                      acceptImageWidth,
                      acceptImageHeight
                    );

                    var acceptTextLines = doc.splitTextToSize(
                      this.acceptanceRateByTrackText.val,
                      contentWidth
                    );
                    doc.text(
                      leftMargin,
                      topMarginAfterHistorical + acceptImageHeight + 20,
                      acceptTextLines
                    );

                    if (numOfAddedSections % 2 == 1) {
                      var acceptanceLinesHeight =
                        Const.pdfLineHeight *
                        Const.pdfTextFontSize *
                        acceptTextLines.length;
                      topMarginAfterAccept =
                        topMarginAfterHistorical +
                        acceptImageHeight +
                        acceptanceLinesHeight +
                        20;
                    }
                  }

                  html2canvas(
                    document.getElementById("topacceptedauthorchart")
                  ).then(accAuthorCanvas => {
                    var topMarginAfterTopAccAuthors = topMarginAfterAccept;
                    if (this.topAcceptedAuthorsChartIncluded) {
                      if (
                        numOfAddedSections % 2 == 0 &&
                        numOfAddedSections > 0
                      ) {
                        doc.addPage();
                        topMarginAfterAccept = Const.topMargin;
                      }

                      numOfAddedSections += 1;
                      var accAuthorImageData = accAuthorCanvas.toDataURL(
                        "image/png"
                      );
                      var accAuthorImageWidth = Const.imageWidth;
                      var accAuthorImageHeight =
                        (accAuthorCanvas.height * accAuthorImageWidth) /
                        accAuthorCanvas.width;
                      doc.addImage(
                        accAuthorImageData,
                        "PNG",
                        leftMargin,
                        topMarginAfterAccept,
                        accAuthorImageWidth,
                        accAuthorImageHeight
                      );

                      var topAccAuthorsTextLines = doc.splitTextToSize(
                        this.topAcceptedAuthorsText.val,
                        contentWidth
                      );
                      doc.text(
                        leftMargin,
                        topMarginAfterAccept + accAuthorImageHeight + 20,
                        topAccAuthorsTextLines
                      );

                      if (numOfAddedSections % 2 == 1) {
                        var topAccAuthorsTextLinesHeight =
                          Const.pdfLineHeight *
                          Const.pdfTextFontSize *
                          topAccAuthorsTextLines.length;
                        topMarginAfterTopAccAuthors =
                          topMarginAfterAccept +
                          accAuthorImageHeight +
                          topAccAuthorsTextLinesHeight +
                          20;
                      }
                    }

                    html2canvas(
                      document.getElementById("topacceptedauthorbytrackchart")
                    ).then(accAuthorTrackCanvas => {
                      var topMarginAfterTopAccAuthorsTrack = topMarginAfterTopAccAuthors;
                      if (this.topAcceptedAuthorsByTrackChartIncluded) {
                        if (
                          numOfAddedSections % 2 == 0 &&
                          numOfAddedSections > 0
                        ) {
                          doc.addPage();
                          topMarginAfterTopAccAuthors = Const.topMargin;
                        }

                        numOfAddedSections += 1;

                        var accAuthorTrackImageData = accAuthorTrackCanvas.toDataURL(
                          "image/png"
                        );
                        var accAuthorTrackImageWidth = Const.imageWidth;
                        var accAuthorTrackImageHeight =
                          (accAuthorTrackCanvas.height *
                            accAuthorTrackImageWidth) /
                          accAuthorTrackCanvas.width;
                        doc.addImage(
                          accAuthorTrackImageData,
                          "PNG",
                          leftMargin,
                          topMarginAfterTopAccAuthors,
                          accAuthorTrackImageWidth,
                          accAuthorTrackImageHeight
                        );

                        var topAccAuthorsTrackTextLines = doc.splitTextToSize(
                          this.topAcceptedAuthorsByTrackText.val,
                          contentWidth
                        );
                        doc.text(
                          leftMargin,
                          topMarginAfterTopAccAuthors +
                            accAuthorTrackImageHeight +
                            20,
                          topAccAuthorsTrackTextLines
                        );

                        if (numOfAddedSections % 2 == 1) {
                          var topAccAuthorsTrackLinesHeight =
                            Const.pdfLineHeight *
                            Const.pdfTextFontSize *
                            topAccAuthorsTrackTextLines.length;
                          topMarginAfterTopAccAuthorsTrack =
                            topMarginAfterTopAccAuthors +
                            accAuthorTrackImageHeight +
                            topAccAuthorsTrackLinesHeight +
                            20;
                        }
                      }

                      html2canvas(document.getElementById("wordcloudall")).then(
                        wordAllCanvas => {
                          var topMarginAfterTopWordCloudAll = topMarginAfterTopAccAuthorsTrack;
                          if (this.wordCloudAllIncluded) {
                            if (
                              numOfAddedSections % 2 == 0 &&
                              numOfAddedSections > 0
                            ) {
                              doc.addPage();
                              topMarginAfterTopAccAuthorsTrack =
                                Const.topMargin;
                            }

                            numOfAddedSections += 1;

                            var wordAllImageData = wordAllCanvas.toDataURL(
                              "image/png"
                            );
                            var wordAllImageWidth = Const.imageWidth;
                            var wordAllImageHeight =
                              (wordAllCanvas.height * wordAllImageWidth) /
                              wordAllCanvas.width;
                            doc.addImage(
                              wordAllImageData,
                              "PNG",
                              leftMargin,
                              topMarginAfterTopWordCloudAll,
                              wordAllImageWidth,
                              wordAllImageHeight
                            );
                          }

                          html2canvas(document.getElementById("wordcloudtrack")).then(
                        wordTrackCanvas => {
                        var topMarginAfterTopWordCloudTrack = topMarginAfterTopWordCloudAll;
                          if (this.wordCloudByTrackIncluded) {
                            if (
                              numOfAddedSections % 2 == 0 &&
                              numOfAddedSections > 0
                            ) {
                              doc.addPage();
                              topMarginAfterTopWordCloudAll =
                                Const.topMargin;
                            }

                            numOfAddedSections += 1;

                            var wordTrackImageData = wordTrackCanvas.toDataURL(
                              "image/png"
                            );
                            var wordTrackImageWidth = Const.imageWidth;
                            var wordTrackImageHeight =
                              (wordTrackCanvas.height * wordTrackImageWidth) /
                              wordTrackCanvas.width;
                            doc.addImage(
                              wordTrackImageData,
                              "PNG",
                              leftMargin,
                              topMarginAfterTopWordCloudTrack,
                              wordTrackImageWidth,
                              wordTrackImageHeight
                            );
                          }

                        html2canvas(document.getElementById("wordcloudaccept")).then(
                        wordAcceptCanvas => {
                          if (this.wordCloudAcceptedIncluded) {
                            if (
                              numOfAddedSections % 2 == 0 &&
                              numOfAddedSections > 0
                            ) {
                              doc.addPage();
                              topMarginAfterTopWordCloudAll =
                                Const.topMargin;
                            }

                            var wordAcceptImageData = wordAcceptCanvas.toDataURL(
                              "image/png"
                            );
                            var wordAcceptImageWidth = Const.imageWidth;
                            var wordAcceptImageHeight =
                              (wordAcceptCanvas.height * wordAcceptImageWidth) /
                              wordAcceptCanvas.width;
                            doc.addImage(
                              wordAcceptImageData,
                              "PNG",
                              leftMargin,
                              topMarginAfterTopWordCloudAll,
                              wordAcceptImageWidth,
                              wordAcceptImageHeight
                            );
                          }
                          doc.save(fileName + ".pdf");
                        }
                      );
                    });
                    });
                    });
                  });
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

            acceptanceRateSelectedTrack: this.acceptanceRateSelectedTrack,
            topAcceptedAuthorsSelectedTrack: this
              .topAcceptedAuthorsSelectedTrack,
            wordCloudSelectedTrack: this.wordCloudSelectedTrack,

            acceptanceRateChartType: this.acceptanceRateChartType,

            topAcceptedAuthorsData: this.computeTopAcceptedAuthors(
              this.topAcceptedAuthorsDataLength
            ),
            topAcceptedAuthorsDataLength: this.topAcceptedAuthorsDataLength,

            topAcceptedAuthorsByTrackLength: this
              .topAcceptedAuthorsByTrackLength,
            topAcceptedAuthorsByTrackChartIncluded: this
              .topAcceptedAuthorsByTrackChartIncluded,

            timeseriesText: this.timeseriesText,
            historicalAcceptanceText: this.historicalAcceptanceText,
            acceptanceRateByTrackText: this.acceptanceRateByTrackText,
            topAcceptedAuthorsText: this.topAcceptedAuthorsText,
            topAcceptedAuthorsByTrackText: this.topAcceptedAuthorsByTrackText,

            timeSeriesChartIncluded: this.timeSeriesChartIncluded,
            historicalAcceptanceChartIncluded: this
              .historicalAcceptanceChartIncluded,
            acceptanceRateByTrackChartIncluded: this
              .acceptanceRateByTrackChartIncluded,
            topAcceptedAuthorsChartIncluded: this
              .topAcceptedAuthorsChartIncluded,
            wordCloudAllIncluded: this.wordCloudAllIncluded,
            wordCloudAcceptedIncluded: this.wordCloudAcceptedIncluded,
            wordCloudByTrackIncluded: this.wordCloudByTrackIncluded
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
                title: "Submission Visualisation session saved!",
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
    getTrackInSubmission: function() {
      return Object.keys(this.chartData.acceptanceRateByTrack);
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
    computeAcceptanceRateByTrack: function() {
      var tracks = this.getTrackInSubmission();
      var values = [];
      for (var track in tracks) {
        values.push(
          this.chartData.acceptanceRateByTrack[tracks[track]].toFixed(2)
        );
      }
      return {
        labels: tracks,
        datasets: [
          {
            label: "Acceptance Rate",
            backgroundColor: this.chooseColorScheme(10),
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: values
          }
        ]
      };
    },
    computeTopAcceptedAuthors: function(len) {
      var authors = this.chartData.topAcceptedAuthors.names.slice(0, len);
      // var authors = Object.keys(this.chartData.topAcceptedAuthors);
      var values = this.chartData.topAcceptedAuthors.counts.slice(0, len);
      var scheme = this.chooseColorScheme(len);
      // var values = authors.map(function(author) {return this.chartData.topAcceptedAuthors[author];});
      return {
        labels: authors,
        datasets: [
          {
            label: "Accepted Papers",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: values
          }
        ]
      };
    },
    computeTopAcceptedAuthorsByTrack: function(len, track) {
      var authors = this.chartData.topAuthorsByTrack[track].names.slice(0, len);
      var values = this.chartData.topAuthorsByTrack[track].counts.slice(0, len);
      var scheme = this.chooseColorScheme(len);
      return {
        labels: authors,
        datasets: [
          {
            label: "Paper Counts",
            backgroundColor: scheme,
            pointBackgroundColor: "white",
            borderWidth: 1,
            pointBorderColor: "#249EBF",
            data: values
          }
        ]
      };
    },
    computeHistoricalAcceptanceRate: function() {
      var years = this.chartData.comparableAcceptanceRate.year;
      return {
        labels: years,
        datasets: [
          {
            label: "Full Papers",
            // backgroundColor: this.chooseColorScheme(10),
            borderColor: "blue",
            fill: false,
            pointBackgroundColor: "white",
            borderWidth: 2,
            pointBorderColor: "blue",
            pointHoverRadius: 5,
            data: this.chartData.comparableAcceptanceRate["Full Papers"]
          },
          {
            label: "Short Papers",
            // backgroundColor: this.chooseColorScheme(10),
            borderColor: "red",
            fill: false,
            pointBackgroundColor: "white",
            borderWidth: 2,
            pointBorderColor: "red",
            pointHoverRadius: 5,
            data: this.chartData.comparableAcceptanceRate["Short Papers"]
          }
        ]
      };
    },
    computeTimeSeriesData: function() {
      var time = this.chartData.timeSeries.time;
      return {
        datasets: [
          {
            label: "Submit Time",
            data: this.chartData.timeSeries,
            backgroundColor: "white",
            fill: false,
            // pointBorderColor: '#249EBF',
            radius: 0,
            borderColor: "blue"
          },
          {
            label: "Last Edit Time",
            data: this.chartData.lastEditSeries,
            backgroundColor: "white",
            fill: false,
            // pointBorderColor: '#249EBF',
            radius: 0,
            borderColor: "red"
          }
        ]
      };
    },
    computeJCDLDeadlineData: function() {
      return {
        annotations: [
          {
            type: "line",
            mode: "vertical",
            scaleID: "x-axis-0",
            value: "2018-01-18",
            borderDash: [4, 4],
            borderColor: "red",
            label: {
              content: "Papers, Tutorial, and Wordshop Deadline",
              enabled: true,
              position: "top",
              xAdjust: 55,
              yAdjust: 8
            }
          },
          {
            type: "line",
            mode: "vertical",
            scaleID: "x-axis-0",
            value: "2018-02-02",
            borderDash: [4, 4],
            borderColor: "red",
            label: {
              content: "Panel, Poster, and Demo Deadline",
              enabled: true,
              position: "top",
              xAdjust: -35,
              yAdjust: 45
            }
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
