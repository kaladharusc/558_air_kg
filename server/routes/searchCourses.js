var express = require('express');
var router = express.Router();
var elasticSearch = require('../search_modules/search.js');

/* GET users listing. */

let send_response = (response, hits) => {
    aggregatedCourses = []
    hits.forEach((hit) => {
        aggregatedCourses.push(...hit._source.courses)
    })
    response.send({
        "msg": aggregatedCourses
    });
}

router.post('/', function (req, res, next) {
    let searchQueryParams = req.body.searchQueryParams;
    let searchName = req.body.searchName;
    //console.log(searchQueryParams);
    elasticSearch.searchCourses(searchQueryParams, searchName, res, send_response);
});

module.exports = router;