var yml = {};
// 获得系统基类对象
var system = require("../yml.system");
var rest=require("../yml.rest.call");
var childproc = require('child_process');

yml.wxconfig = {
	CorpID : "wx88e66f6e2bf540bd",
	Secret : "70fd2d1c13d593e50b581a7170ec98b9",
	AccessTokenUrl : "https://qyapi.weixin.qq.com/cgi-bin/gettoken",
	wxApiUrlTemplete : "{WX_API_URL}?access_token={ACCESS_TOKEN}"
}
// 定义websocket信道对象
/**
 * 这个信道需要只需要创建一个子类对象
 */
yml.wxchannel = system.object.Abstract({
	ctor : function(initParams) {
		this.restClient=rest.restClient.New();
		// 设置发送消息的接口地址
		this.agentid=5;
		this.setAccessKey(null);
	},
	setAccessKey : function(callback) {
		this.AccessKeyUrl = yml.wxconfig.AccessTokenUrl;
		this.subdata = "corpid=" + yml.wxconfig.CorpID + "&corpsecret="
				+  yml.wxconfig.Secret;
		var that = this;
		this.restClient.setRestUrl(this.AccessKeyUrl);
		this.restClient.callGet(this.subdata,function(err, out) {
			if (err)
				throw new Error(err);
			var tokenObj = out;
			if(tokenObj.access_token){
				that.accessKey = tokenObj.access_token;
				console.log("accesskey set ok...")
				callback(null);
			}else{
				callback(err);
			}
		});
	},
	setWxApiUrl:function(apiUrl){
		//设置微信要调用的微信应用接口的地址
		  var apiUrl=yml.wxconfig.wxApiUrlTemplete.replace(/\{ACCESS_TOKEN\}/g,
					that.accessKey).replace(/\{WX_API_URL\}/g,apiUrl);
			this.wxApiUrl = apiUrl;
	}
});
// console.log("dddd".replace(/d+/g,"m"));
var wxclient = yml.wxchannel.New(yml.wxconfig, {});
wxclient.setAccessKey(function(err) {
	wxclient.sendTextMsg("hello world",["wxid_9775577755611"],function(err,out){
		console.log(out);
	});
});
module.exports = yml;
