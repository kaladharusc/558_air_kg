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

exports.insertDocument = function (request, outResponse) {
    client.index({
        index: 'person',
        id: 1,
        type: 'doc',
        body: request
    }, function(error, response, status) {
        if (error) {
            outResponse.send({"msg": "Document could not be inserted !"});
        } else {
            // console.log("Response " + response);
            // console.log("Status " + status);
            outResponse.send({"msg": `${response} : ${status}`});
        }           
    });
}

exports.searchDocument = function(searchName, res_object, callback) {
    client.search({
        index: 'person',
        type: 'doc',
        body: {
            query: {
                match: {name: searchName}
            }
        }
    }).then(function(response) {
        var hits = response.hits.hits;
        callback(res_object, hits);
    }, function(error) {
        // callback(error.message);
        console.trace(error.message);
    })
}