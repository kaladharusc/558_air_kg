var express = require('express');
var router = express.Router();
var elasticSearch = require('../search_modules/search.js');

/* GET users listing. */

let send_response = (response, hits) => {
    response.send({"msg": hits});
}

router.post('/', function(req, res, next) {
  // console.log(req.body);
  let searchPattern = req.body.searchPattern.toLowerCase();
  console.log(searchPattern);
  elasticSearch.fuzzySearch(searchPattern, res, send_response);
});

module.exports = router;