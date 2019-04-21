var express = require('express');
var router = express.Router();
var elasticSearch = require('../search_modules/search.js');

/* GET users listing. */

let send_response = (response, hits) => {
    response.send({"msg": hits});
}

router.post('/', function(req, res, next) {
  let searchName = req.body.searchName;
  elasticSearch.searchDocument(searchName, res, send_response);
});

module.exports = router;