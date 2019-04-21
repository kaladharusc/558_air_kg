var express = require('express');
var router = express.Router();
var elasticSearch = require('../search_modules/search.js');

/* GET users listing. */
router.post('/', function(req, res, next) {
  elasticSearch.insertDocument(req.body, res);
});

module.exports = router;
