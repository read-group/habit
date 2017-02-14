var yml = {};
// 获得系统基类对象
var system = require("../yml.system");
var rest=require("../yml.rest.call");
var settings=require("../../config/settings");
/**
 * 这个信道需要只需要创建一个子类对象
 */
yml.socketiochannel = system.object.Abstract({
	ctor : function(initParams) {
			this.cacheClients = {};
			this.session={};//内存会话存储
			this.idMapAccessKey={};
			this.restClient=rest.restClient.New();
			this.server = initParams.server;

			// 建立双工通信服务
			this.io = require('socket.io')(this.server);
			//调用父类对象的开始监听PUSH事件**********************
			//this.startPushEventListen();
			//***********************************************
			var that = this;
			this.io.on('connection', function(client) {
				console.log("connections..............");
				client.on("join", function(data) {// data是登陆者的Id
					that.cacheClients[data] = client;
				    console.log(429+'join...................');
				    client.emit("push2browser", 'ok'+data);
				});
				// 接受来自客户端的命令
				client.on("cmd", function(data) {// data是登陆者的Id
					if(data.cmd!="auth"){//身份检查
						if(data.keyAccess){
							if(!that.session[data.keyAccess]){
								//返回身份无效或会话过期，需要重新认证
								var d={status:-1,errMsg:"身份无效或会话过期，请重新登录"};
								that.sendData(client,d);
								return;
							}
						}else{
							//返回身份无效或会话过期，需要重新认证
							var d={status:-1,errMsg:"身份无效或会话过期，请重新登录"};
							that.sendData(client,d);
							return;
						}
					}
					console.log("from client cmd:" + JSON.stringify(data));
					that.handleCmd(client,data);

				});
				// 错误处理
				client.on("error", function(err) {
					console.log("error happened............................"
							+ err);
					that.cacheClients = system.utils
							.deleteElementFromDictByFilter(that.cacheClients,
									client, function(toDel, each) {
										return toDel == each;
									});
				});
				client.on("disconnect", function(err) {
					console.log("disconnect happened............................"
							+ err);
					that.cacheClients = system.utils
							.deleteElementFromDictByFilter(that.cacheClients,
									client, function(toDel, each) {
										return toDel == each;
									});
				});
			});
	},
	sendData:function(client,data){
		client.emit("push2browser",data);
	},
	/**
	 * 修饰返回的结果
	 * input是从客户端来的数据
	 * out是要返回的数据
	 */
	decrateRtnData:function(err,input,out){
		var out=out||{status:1}
		if(err){
			out.status=0;
			out.rawErr=err;
		}
		out.callback=input.callback;
		out.target=input.target;
		return out;
	},
	buildChatMsg:function(input){
		var out={};
		var toAccessKey=this.idMapAccessKey[input.content.to];
		if(this.session[toAccessKey]){
			out.status=1;
			out.from=input.content.from;
			out.to=input.content.to;
			out.fromName=this.session[input.keyAccess].name;
			out.toName=this.session[toAccessKey].name;
			out.content=input.content.txt;
		}else{//对方不在线
			out.status=-2;
			out.errMsg="对方不在线";
		}

		return this.decrateRtnData(null,input,out);
	},
	handleCmd:function(client,data){
		var self=this;
		if(data.cmd=="auth"){//如果是认证

			this.restClient.setRestUrl(settings.user_center_url+data.cmd);
			this.restClient.callPost(data.content,function(err,out){
				console.log(out);
				var rtn=self.decrateRtnData(err,data,out);
				if(rtn.status==1){//表示认证通过,如果通过,那么用户的id为key建立客户socket缓存
					self.cacheClients[rtn.content.id] = client;
					self.session[rtn.content.keyAccess]=rtn.content;
					//建立一个认证的用户的id与key的映射
					self.idMapAccessKey[rtn.content.id]=rtn.content.keyAccess;
				}
				self.sendData(client,rtn);

			});
		}
		if(data.cmd=="logout"){
			if(self.session[data.keyAccess]){
				self.cacheClients[self.session[data.keyAccess].id] = null;
				self.session[data.keyAccess]=null;
			}
			var rtn=self.decrateRtnData(null,data,null);
			self.sendData(client,rtn);
		}
		if(data.cmd=="reconnect"){
			if(self.session[data.keyAccess]){
				self.cacheClients[self.session[data.keyAccess].id] = client;
				//self.session[data.keyAccess]=null;
			}
			var rtn=self.decrateRtnData(null,data,null);
			self.sendData(client,rtn);
		}
		if(data.cmd=="org"){

			this.restClient.setRestUrl(settings.user_center_url+data.cmd);
			this.restClient.callPost(data.content||{},function(err,out){
				var rtn=self.decrateRtnData(err,data,out)
				self.sendData(client,rtn);
			});
		}
		if(data.cmd=="emps"){

			this.restClient.setRestUrl(settings.user_center_url+data.cmd);
			this.restClient.callPost(data.content,function(err,out){
				var rtn=self.decrateRtnData(err,data,out)
				self.sendData(client,rtn);
			});
		}
		if(data.cmd=="chat"){
			var toClient=this.cacheClients[data.content.to];
			var toMsg=this.buildChatMsg(data);
			if(toClient){
				  console.log("xxxxxxxxxxxxxxxxxxx");
				  console.log(toMsg);
				  this.sendData(toClient,toMsg);
			}
			else{
				  this.sendData(client,toMsg);
			}
			//需要把消息持久化到数据库，持久化ok后，在回调里发送到目标客户
//			this.restClient.setRestUrl(settings.user_center_url+data.cmd);
//			this.restClient.callPost(data.content,function(err,out){
//				var rtn=self.decrateRtnData(err,data,out)
//				self.sendData(client,rtn);
//			});
		}
	}
});
module.exports = yml;
