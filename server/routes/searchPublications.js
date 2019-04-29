var express = require('express');
var router = express.Router();
var elasticSearch = require('../search_modules/search.js');

/* GET users listing. */

let send_response = (response, hits) => {
    aggregatedPublications = []
    hits.forEach((hit) => {
        aggregatedPublications.push(...hit._source.papers)
    })
    response.send({"msg": aggregatedPublications});
}

router.post('/', function(req, res, next) {
  let searchQueryParams = req.body.searchQueryParams;
  let searchName = req.body.searchName;
  //console.log(searchQueryParams);
  elasticSearch.searchPublications(searchQueryParams, searchName, res, send_response);
});

module.exports = router;