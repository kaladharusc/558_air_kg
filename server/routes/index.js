var elasticSearch = require('../search_modules/search.js');

var express = require('express');
var router = express.Router();

/* GET status of running elasticsearch server */
router.get('/', function(req, res, next) {
  elasticSearch.ping(res);
});

/* PUSH data to elasticsearch */

module.exports = router;
