var yml = {};
// 获得系统基类对象
var system = require("../yml.system");
var rest=require("../yml.rest.call");
var childproc = require('child_process');

yml.wxconfig = {
		//grant_type=client_credential&appid=APPID&secret=APPSECRET
	AppId:"wx8f428820d2150a9e",
	Secret : "751afbe404efaee85ba8638ceeb1dc44",
	AccessTokenPath : "https://api.weixin.qq.com/cgi-bin/token?",
	SendMsgPath : "https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token={ACCESS_TOKEN}"
}
// 定义websocket信道对象
/**
 * 这个信道需要只需要创建一个子类对象
 */
yml.wxchannel = system.object.Abstract({
	ctor : function(initParams) {
		// 启动push监听
		//this.startPushEventListen();

		this.AccessKeyUrl = initParams.AccessTokenPath;
		this.subdata = "grant_type=client_credential&appid=" + initParams.AppId + "&secret="
				+ initParams.Secret;
		this.restClient=rest.restClient.New();
		// 设置发送消息的接口地址
		this.sendMsgUrlPattern = initParams.SendMsgPath;
		this.agentid=5;
	},
	setAccessKey : function(callback) {
		var that = this;
		this.restClient.setRestUrl(this.AccessKeyUrl);
		this.restClient.callGet(this.subdata,function(err, out) {
			if (err)
				throw new Error(err);
			var tokenObj = out;
			if(tokenObj.access_token){
				that.accessKey = tokenObj.access_token;
				that.sendMsgUrl = that.sendMsgUrlPattern.replace(/\{ACCESS_TOKEN\}/g,
						that.accessKey);
				console.log("accesskey set ok...")
				callback(null);
			}else{
				callback(err);
			}


		});
	}
	,
	/**
	 * users,用户数组
	 * depts部门Id数组
	 */
	sendTextMsg : function(txtMsg,toUsersParam,callback,toDeptsParam) {
		var that = this;
		var users=toUsersParam || [];
		var depts=toDeptsParam || [];
		var toUsers=users.join("|");
		var toparts=depts.join("|");

		var txtObj ={
				     "filter":{
					      "is_to_all":false,
					   },
					   "text":{
					      "content":txtMsg
					   },
					    "msgtype":"text"
					}

		this.restClient.setRestUrl(this.sendMsgUrl);
		this.restClient.callPost(txtObj,function(err,out){
			callback(err,out);
		});
	},
	/**
	 * 创建跳转菜单
	 */
	createUrlMenu:function(url,callback){
		var createMenuUrl="https://api.weixin.qq.com/cgi-bin/menu/create?access_token={ACCESS_TOKEN}";
		createMenuUrl=createMenuUrl.replace(/\{ACCESS_TOKEN\}/g,
				this.accessKey);

		 var menuObj={
		     "button":[
		     {
						 "type":"view",
						 "name":"米粒帮助",
						 "url":url
		      },
		     {
		 		               "type":"view",
		 		               "name":"进入应用",
		 		               "url":url
		    }
		      ]

		 };
		this.restClient.setRestUrl(createMenuUrl);
		this.restClient.callPost(menuObj,function(err,out){
			callback(err,out);
		});

	},
	//删除自定义菜单
	delMenu:function(callback){
		var createMenuUrl="https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={ACCESS_TOKEN}";
		createMenuUrl=createMenuUrl.replace(/\{ACCESS_TOKEN\}/g,
				this.accessKey);
		this.restClient.setRestUrl(createMenuUrl);
		this.restClient.callGet("",function(err,out){
			callback(err,out);
		});
	}

	/**
	 * 获取所有用户信息
	 */
});
// console.log("dddd".replace(/d+/g,"m"));
var wxclient = yml.wxchannel.New(yml.wxconfig, {})

wxclient.setAccessKey(function(err) {
	//群发消息
	// wxclient.sendTextMsg("hello world",["wxid_9775577755611"],function(err,out){
	// 	console.log(out);
	// });

	//删除自定义菜单
	wxclient.delMenu(function(err,out){
		console.log(out);
	});
	//建立自定义菜单
	//wx88e66f6e2bf540bd
	//var url="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf0e81c3bee622d60&redirect_uri=http%3a%2f%2fll.yimilan.com%2ff1&response_type=code&scope=snsapi_userinfo&#wechat_redirect";
	var url="http://mily365.com";
	wxclient.createUrlMenu(url,function(err,out){
		console.log(out);
	//https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
	});


});
//ot3MKs8CHeWsTCJqRnyqux52Hrao=openid
//curl https://api.weixin.qq.com/cgi-bin/user/info?access_token=EAKYjCX8UKlIy9-VuuUDdwleWG6NQCXjWY-JB1XMLVy41Ub2k2du4KkWKT9wsb23Nye4AHJFosBpAJ5YTXc2CrgvV9StEeIRjuJEnA4VvrfxU1eLwFT-2X9RQJTZnW-aTEKiAJAYJP&openid=ot3MKs-k9VDrJE4R3j-HygRSzQEc&lang=zh_CN

module.exports = yml;
