var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client({
    host: 'localhost:9200',
    log: 'trace'
});

var exports = module.exports = {}

exports.ping = function(outResponse) {
    client.ping({
        requestTimeout: 3000,
    }, function(error, response, status) {
        if (error) {
            console.error("Elasticsearch cluster is down !");
            outResponse.send({"msg": "Elasticsearch cluster is down !"});
        } else {
            console.log("Response " + response);
            console.log("Status " + status);
            outResponse.send({"msg": `${response} : ${status}`});
        }
    });
}

exports.search = function(searchData, callback) {
    client.search({
        index: 'bank',
        type: 'account',
        body: {
            query: {
                match: {address: searchData.searchTerm}
            }
        }
    }).then(function(response) {
        var hits = response.hits.hits;
        callback(hits);
    }, function(error) {
        callback(error.message);
        console.trace(error.message);
    })
}