/**
 * Module dependencies.
 */
var http = require('http');
var express = require('express');
var setttings=require("./app/config/settings");
var environment = require('./app/config/environment');
var routes = require('./app/config/routes');
var app = express();
// all environments
environment(app);//初始化环境
routes(app);//初始化路由

var server = http.createServer(app);
//console.log(process.env.NODE_ENV);
if (!module.parent) {
	server.listen(setttings.port, function() {
		console.log('http server listening on port ' + setttings.port);
	});
}
module.exports = app;
