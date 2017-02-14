var yml = {};
// 获得系统基类对象
var system = require("../yml.system");
var rest=require("../yml.rest.call");
var childproc = require('child_process');
var NodeCache = require("node-cache");
var sha1 = require('sha1');

yml.wxconfig = {
	AppID : "wx8041b1a0fca56fba",
	Secret : "774b973ca5cfafb61d402d03442cd23f",
	AccessTokenUrl : "https://api.weixin.qq.com/cgi-bin/token",
	noncestr:'Wm3WZYTPz0wzccnW',
	ticketUrl:'https://api.weixin.qq.com/cgi-bin/ticket/getticket',
	cache_duration:1000*60*60*1
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
		this.cache=new NodeCache({stdTTL:800});
		this.getAccessKey(function(err,ak){
			if(err)
			  console.log(err);
		});
	},
	getAccessKey : function(cbk) {
		if(this.cache.get("accessKey")){
			console.log("hit accessKey cache.....");
			return cbk(null,this.cache.get("accessKey"));
		}else{
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
					that.cache.set('accessKey',tokenObj.access_token);  //加入缓存
					console.log("accesskey set ok..."+that.cache.get("accessKey"));
					if(cbk) return cbk(null,that.cache.get("accessKey"));
				}else{
					if(cbk) return  cbk(err);
				}
			});
		}
	},
	getJsApiConfig:function(url,cbk){
		var noncestr = yml.wxconfig.noncestr,
			 timestamp = Math.floor(Date.now()/1000); //精确到秒
			 var cacheUrl= this.cache.get('url');
			 var isSameUrl=(cacheUrl==url);
			 if(this.cache.get('ticket') && isSameUrl){
					 var jsapi_ticket = this.cache.get('ticket');
					 var sign1=sha1('jsapi_ticket=' + jsapi_ticket + '&noncestr=' + noncestr + '&timestamp=' + timestamp + '&url=' + url);
					 console.log("cache------------------------"+sign1);
					 return cbk(null,{
							 nonceStr:noncestr,
							 timestamp:timestamp,
							 url:url,
							 jsapi_ticket:jsapi_ticket,
							 signature:sign1
					 });
	      }else{
					var that = this;
					this.restClient.setRestUrl(yml.wxconfig.ticketUrl);
					var subdata='access_token='+ this.cache.get('accessKey') + '&type=jsapi';
					this.restClient.callGet(subdata,function(err, out){
						if(err){
							return cbk(err,null);
						}else{
							that.cache.set('ticket',out.ticket);  //加入缓存
							that.cache.set('url',url);
							var str='jsapi_ticket=' + that.cache.get("ticket") + '&noncestr=' + noncestr + '&timestamp=' + timestamp + '&url=' + url;
							var sign2=sha1(str);
							console.log("new------------------------"+str);
							console.log("new------------------------"+sign2);
							return  cbk(null,{
                            nonceStr:noncestr,
                            timestamp:timestamp,
                            url:url,
                            jsapi_ticket:that.cache.get("ticket"),
                            signature:sign2
                        });
						}
					});
				}
	}
});
module.exports = yml;
// yml.accessKey.getAccessKey(function(){
// 		yml.accessKey.getJsApiConfig("http://ll.yimilan.com/app/grain/addChild.html",function(err,c){
// 		 if(err){
// 			 console.log(err);
// 		 }
// 		 else{
// 				 console.log(yml.accessKey.cache.get("accessKey"));
// 				 console.log(yml.accessKey.cache.get("ticket"));
// 		}
//
// 	});
// });
// str="jsapi_ticket=sM4AOVdWfPE4DxkXGEs8VPLv_N3a4_D2mRl5uoM4XX-Coj7Hep4p2bMFQ4Luvv2XrqcUINDy8yMcp1dIO_3QR&noncestr=Wm3WZYTPz0wzccnW&timestamp=1461298039&url=http://ll.yimilan.com/app/home/main.html"
// var x=sha1(str);
// console.log("========================");
// console.log(x)
