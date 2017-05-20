var crypto=require("crypto");
var weixin=require("../../service/wx.service");
var weixinKey=require("../../service/yml.service.wxapi");
var wxpay=require("../../lib/wxpay/wxpay").wxpay;
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
	app.post('/wx/api/order',function(req,res){
		 var bizOrderId=req.body.bizOrderId;
		 var desc=req.body.desc;
		 var amount=req.body.amount * 100;
		 var actid=req.body.actid;
		 var opid=req.body.opid;
     weixinKey.service.wxapi.order(bizOrderId,desc,amount,actid,opid,function(rtnData){
			 res.json(rtnData);
		 });
	});
	//支付结果异步通知
	app.use('/api/wxpay/notify',wxpay.useWXCallback(function(msg, req, res, next){
			// 处理商户业务逻辑
			console.log("通知........-------------------------------------------");
			console.log(msg);
			bizs.service.sns.wxResultHandleForMoneyPrase(msg,req.user,function(rtnData){
				if(rtnData.status==0){
					res.success();
					//res.end();
				}else{
					res.fail();
					//res.end();
				}
			});
			// res.success() 向微信返回处理成功信息，res.fail()返回失败信息。
	}));
	//发送通知消息
	app.post('/wx/api/sendMsg',function(req,res){
		 var touser=req.body.touser;
		 var tid=req.body.tid;
		 var queryStr=req.body.queryStr;
		 var data=req.body.data;
		 weixinKey.service.wxapi.sendTmplMsg(touser,tid,queryStr,data,function(rtnData){
			 res.json(rtnData);
		 });
	});

};
