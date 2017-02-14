var path     = require('path');
var express  = require('express');
var settings = require('./settings');
//var models   = require('../app/models/');

module.exports = function (app) {
  app.configure(function () {
	  console.log(__dirname);
	  app.set('port', settings.port);
	  app.set('views', settings.basepath + '/views');
	  app.set('view engine', 'ejs');
	  app.use(express.favicon());
	  app.use(express.logger('dev'));
	  app.use(express.bodyParser());
	  app.use(express.methodOverride());
    app.all('*',function (req, res, next) {
        res.header('Access-Control-Allow-Origin', 'http://mily365.com,http://www.mily365.com');
        res.header('Access-Control-Allow-Headers', 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild');
        res.header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS');
        res.header('Access-Control-Allow-Credentials', 'true');
        if (req.method == 'OPTIONS') {
          res.send(200); /让options请求快速返回/
        }
        else {
          next();
        }
　　　});
	  app.use(app.router);
	  app.use(express.static(path.join(settings.basepath, 'public')));
	// development only
	  if ('development' == app.get('env')) {
      console.log("current in develop....");
	  	app.use(express.errorHandler());
	  }
  });
};
