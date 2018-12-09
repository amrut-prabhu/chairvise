<template>
  <div class="hello">
    <AuthorVisualisation 
      v-if="infoType === 'author'" 
      :chart-data="chartData" 
      :info-type="infoType"
      :input-file-name="inputFileName" 
      :session-data="sessionData"/>

    <SubmissionVisualisation 
      v-else-if="infoType === 'submission'" 
      :chart-data="chartData" 
      :info-type="infoType"
      :input-file-name="inputFileName" 
      :session-data="sessionData"/>

    <ReviewVisualisation 
      v-else-if="infoType === 'review'" 
      :chart-data="chartData" 
      :info-type="infoType"
      :input-file-name="inputFileName" 
      :session-data="sessionData"/>

    <AuthorAndReviewVisualisation 
      v-else-if="infoType === 'author&review'" 
      :chart-data="chartData" 
      :info-type="infoType"
      :input-file-name="inputFileName" 
      :session-data="sessionData"/>

    <AuthorAndSubmissionVisualisation 
      v-else-if="infoType === 'author&submission'" 
      :chart-data="chartData" 
      :info-type="infoType"
      :input-file-name="inputFileName" 
      :session-data="sessionData"/>

    <SubmissionAndReviewVisualisation 
      v-else-if="infoType === 'submission&Review'" 
      :chart-data="chartData" 
      :info-type="infoType"
      :input-file-name="inputFileName" 
      :session-data="sessionData"/> <!--End of Submission and Review Component-->

    <ReviewScoreVisualisation 
      v-else-if="infoType === 'reviewScore'" 
      :chart-data="chartData" 
      :info-type="infoType"
      :input-file-name="inputFileName" 
      :session-data="sessionData"/>

    <NoVisualisation 
      v-else
      :chart-data="chartData" 
      :info-type="infoType"
      :input-file-name="inputFileName" 
      :session-data="sessionData"/>
  </div>
</template>

<script>
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

import NoVisualisation from "@/components/visualisations/NoVisualisation";

import AuthorVisualisation from "@/components/visualisations/AuthorVisualisation";
import SubmissionVisualisation from "@/components/visualisations/SubmissionVisualisation";
import ReviewVisualisation from "@/components/visualisations/ReviewVisualisation";
import ReviewScoreVisualisation from "@/components/visualisations/ReviewScoreVisualisation";

import AuthorAndReviewVisualisation from "@/components/visualisations/AuthorAndReviewVisualisation";
import AuthorAndSubmissionVisualisation from "@/components/visualisations/AuthorAndSubmissionVisualisation";
import SubmissionAndReviewVisualisation from "@/components/visualisations/SubmissionAndReviewVisualisation";

export default {
  name: "Chart",
  components: {
    AuthorVisualisation,
    SubmissionVisualisation,
    ReviewVisualisation,
    ReviewScoreVisualisation,
    AuthorAndReviewVisualisation,
    AuthorAndSubmissionVisualisation,
    SubmissionAndReviewVisualisation,
    NoVisualisation
  },
  props: ["chartData", "infoType", "inputFileName", "sessionData"],
  data: function() {
    console.log("type: " + this.infoType)
    return {};
  },
  methods: {
    saveToPdf: function() {
      let fileName = "Visual Analysis";
      var leftMargin = 15;
      var rightMargin = 15;
      var pdfInMM = 210;
      var doc = new jsPDF("p", "mm", "a4");
      // doc.text("Hello World", 10, 10);
      var lines = doc.splitTextToSize(
        this.authorText.val,
        pdfInMM - leftMargin - rightMargin
      );
      doc.text(leftMargin, 20, lines);
      html2canvas(document.getElementById("testpdf")).then(canvas => {
        var imageData = canvas.toDataURL("image/png");
        doc.addImage(
          imageData,
          "PNG",
          15,
          50,
          canvas.width / 8,
          canvas.height / 8
        );

        doc.save(fileName + ".pdf");
      });
    },
    computeTopWordClouds: function(wordCountMap) {
      var wordsSorted = Object.keys(wordCountMap)
        .sort(function(a, b) {
          return wordCountMap[b] - wordCountMap[a];
        })
        .slice(0, 20);
      var topWordCloud = {};
      wordsSorted.forEach(function(word) {
        topWordCloud[word] = wordCountMap[word];
      });
      return topWordCloud;
    }
  },
  beforeRouteUpdate(to, from, next) {
    next();
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