var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var insertDocumentRouter = require('./routes/insertDocument');
var searchDocumentRouter = require('./routes/searchDocument');
var fuzzySearchRouter = require('./routes/fuzzySearchRouter');
var searchPublicationsRouter = require('./routes/searchPublications');
var searchCoursesRouter = require('./routes/searchCourses');
const port = 3000;
const cors = require('cors');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(cors({origin: true}));

// bodyParser
// app.use(bodyParser());
app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
})); 

app.use('/', indexRouter);
app.use('/insertDoc', insertDocumentRouter);
app.use('/searchDoc', searchDocumentRouter);
app.use('/fuzzySearch', fuzzySearchRouter);
app.use('/searchPublications', searchPublicationsRouter);
app.use('/searchCourses', searchCoursesRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

// app.listen(port, () => {
//   console.log(`App listening on port ${port}!`);
// });

module.exports = app;
