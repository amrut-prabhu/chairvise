<template>
  <center>
    <img :src="require('../assets/logo.png')">
    <img :src="require('../assets/title.png')">
    <div class="info">
      <h2>What is ChairVise?</h2>

      <p>Every year many academic and industry conferences are held worldwide for researchers to
      present and discuss their work. These conferences provide an important channel for exchange of
      information among researchers. </p>

      <p>The conference program ChairVise reports a summary of interesting facts e.g. acceptance and
      rejection rates, country specific contributions, of conferences that help researches mine for useful information.</p>

      <br>

      <h2>How to use ChairVise</h2>
      <ol>
        <li>Upload a conference related CSV file (or a bunch of them) to the dropbox on the left</li>
        <li>A mapping page would appear, asking for the right mapping of columns of your csv to the intended columns</li>
        <li>After mapping, visualisations would appear if the relevant visualisations exist for the combination of uploaded files</li>
      </ol>

      <br>

      <h2>Accepted CSVs</h2>
      <h3>Single File Visualisation</h3>
      <ul>
        <li>Author</li>
        <li>Submission</li>
        <li>Review</li>
        <li>Review Score</li>
      </ul>
      <h3>Multiple File Visualisation</h3>
    </div>
  </center>
</template>

<script>
export default {
  name: "Home",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: bold;
}

.info {
  text-align: left;
}

h3 {
  font-weight: normal
  font-si
}
</style>
