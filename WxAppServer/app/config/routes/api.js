var crypto=require("crypto");
var weixin=require("../../service/wx.service");
var weixinKey=require("../../service/yml.service.wxapi");
module.exports = function (app) {
	app.post('/wx/api/jsConfig', function(req, res) {
		 var url=req.body.url;
		 weixinKey.service.wxapi.getJsApiConfig(url,function(rtnData){
			 res.json(rtnData);
		 });
	});
	app.post('/wx/api/getAccessKey', function(req, res) {
		 var url=req.body.url;
		 weixinKey.service.wxapi.getAccessKey(function(rtnData){
			 res.json(rtnData);
		 });
	});
	app.post('/wx/api/download',function(req,res){
		 var mediaid=req.body.mediaId;
		 var type=req.body.type;
     weixinKey.service.wxapi.downloadFile(mediaid,type,function(rtnData){
			 res.json(rtnData);
		 });
	});
};
