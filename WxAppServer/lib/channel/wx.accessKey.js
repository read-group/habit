var yml = {};
// 获得系统基类对象
var system = require("../yml.system");
var rest=require("../yml.rest.call");
var childproc = require('child_process');

yml.wxconfig = {
	AppID : "wx88e66f6e2bf540bd",
	Secret : "70fd2d1c13d593e50b581a7170ec98b9",
	AccessTokenUrl : "https://api.weixin.qq.com/cgi-bin/token",
}
// 定义websocket信道对象
/**
 * 这个信道需要只需要创建一个子类对象
 */
yml.accessKey = system.object.New({
	ctor : function(initParams) {
		this.restClient=rest.restClient.New();
		// 设置发送消息的接口地址
		this.agentid=5;
		this.setAccessKey(function(err,ak){
			if(err)
			  console.log(err);
		});
	},
	setAccessKey : function(cbk) {
		this.AccessKeyUrl = yml.wxconfig.AccessTokenUrl;
		this.subdata = "grant_type=client_credential&appid=" + yml.wxconfig.AppID + "&secret="
				+  yml.wxconfig.Secret;
		var that = this;
		this.restClient.setRestUrl(this.AccessKeyUrl);
		this.restClient.callGet(this.subdata,function(err, out) {
			if (err){
			 return	cbk(err);
			}

			var tokenObj = out;
			if(tokenObj.access_token){
				that.accessKey = tokenObj.access_token;
				console.log("accesskey set ok..."+that.accessKey)
				if(cbk) return cbk(null,that.accessKey);
			}else{
				if(cbk) return  cbk(err);
			}
		});
	},
	getAccessKey:function(callback,isRefresh){
		//定义是否重新去wx服务器去获取
		if(!this.accessKey){//如果不存在就去获得
			this.setAccessKey(function(err,key){
				if(err)
				   return  callback(err);
				else {
					 return callback(null,key);
				}
			});
		}else{
			if(!isRefresh)
         return callback(null,this.accessKey);
			else{
				this.setAccessKey(function(err,key){
				 if(err)
					return callback(err,null);
				 else {
					 return callback(null,key);
				 }
			 });
			}
		}
	}
});
module.exports = yml;
