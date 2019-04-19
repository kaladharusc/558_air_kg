var elasticsearch = require("elasticsearch");
var client = new elasticsearch.Client({
  host: "localhost:9200",
  log: "trace"
});

client.ping(
  {
    requestTimeout: 30000
  },
  function(error, response, status) {
    if (error) {
      console.error("elasticsearch cluster is down!");
    } else {
      console.log("response " + response);
      console.log("status " + status);
    }
  }
);
