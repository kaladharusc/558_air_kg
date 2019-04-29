var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client({
    host: 'localhost:9200',
    log: 'trace'
});

var exports = module.exports = {}

exports.ping = function (outResponse) {
    client.ping({
        requestTimeout: 3000,
    }, function (error, response, status) {
        if (error) {
            console.error("Elasticsearch cluster is down !");
            outResponse.send({
                "msg": "Elasticsearch cluster is down !"
            });
        } else {
            console.log("Response " + response);
            console.log("Status " + status);
            outResponse.send({
                "msg": `${response} : ${status}`
            });
        }
    });
}

exports.insertDocument = function (request, outResponse) {
    client.index({
        index: 'person',
        id: 1,
        type: 'doc',
        body: request
    }, function (error, response, status) {
        if (error) {
            outResponse.send({
                "msg": "Document could not be inserted !"
            });
        } else {
            // console.log("Response " + response);
            // console.log("Status " + status);
            outResponse.send({
                "msg": `${response} : ${status}`
            });
        }
    });
}

exports.fuzzySearch = function (searchPattern, res_object, callback) {
    client.search({
        index: 'research_doc',
        type: 'research_information',
        body: {
            query: {
                wildcard: {
                    person: `${searchPattern}*`
                }
            }
        }
    }).then(function (response) {
        var hits = response.hits.hits.map(ele => ele["_source"]["person"]);
        callback(res_object, hits);
    }, function (error) {
        callback(res_object, "");
        console.trace(error.message);
    });
}

exports.searchDocument = function (searchName, res_object, callback) {
    client.search({
        index: 'research_doc',
        type: 'research_information',
        body: {
            query: {
                match: {
                    person: searchName
                }
            }
        }
    }).then(function (response) {
        var hits = response.hits.hits;
        callback(res_object, hits);
    }, function (error) {
        // callback(error.message);
        console.trace(error.message);
    })
}

exports.searchPublications = function (searchQueryParams, searchName, res_object, callback) {

    client.search({
        index: 'research_doc',
        type: 'research_information',
        body: {
            _source: ["papers"],
            query: {
                match: {
                    person: searchName
                },
                regexp: {
                    "corpus.domain": searchQueryParams
                }
            }
        }
    }).then(function (response) {
        var hits = response.hits.hits;
        callback(res_object, hits);
    }, function (error) {
        // callback(error.message);
        console.trace(error.message);
    })

}

exports.searchCourses = function (searchQueryParams, searchName, res_object, callback) {

    client.search({
        index: 'research_doc',
        type: 'research_information',
        body: {
            _source: ["courses"],
            query: {
                match: {
                    person: searchName
                },
                regexp: {
                    "corpus.domain": searchQueryParams
                }
            }
        }
    }).then(function (response) {
        var hits = response.hits.hits;
        callback(res_object, hits);
    }, function (error) {
        // callback(error.message);
        console.trace(error.message);
    })

}