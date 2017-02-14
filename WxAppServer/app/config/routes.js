var fs=require("fs");
var path=require("path");

module.exports = function (app) {
	var routePath=__dirname+"/routes";
	fs.readdir(routePath,function(err,rs){
		if(rs){
			rs.forEach(function(r){
				var func=require(routePath+"/"+r);
				func.call(null,app);
			});
		}

	});
};
