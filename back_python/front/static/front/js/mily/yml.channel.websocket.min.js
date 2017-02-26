(function(ykx){
	ykx.websocket=ykx.object.Abstract({
		ctor:function(initParams){
			this.socketUrl=initParams.socketUrl;
			this.io=initParams.io;
			this.client = this.io.connect(this.socketUrl);
			this.userId=initParams.idUser;
			//初始化事件
			this.init();
		},
		init:function(){
			var self=this;
			this.client.on('connect', function() {
           console.log("已经链接......");
					 self.client.emit("join",self.userId);
			});
				//代理服务器断开监听器
			self.client.on('disconnect', function(err) {
					self.disConnect(err);
			});
				//代理服务器断开监听器
			self.client.on('error', function(err) {
					self.error(err);
			});
		},
		/**
		 * 发送数据到服务端订阅的频道
		 */
		sendData:function(data){
			this.client.emit("cmd", data);
		},
		addListener:function(channelName,callback){
			this.client.on(channelName,callback);
		},
		/**
		 * 子类重写获取服务端的数据
		 */
		getData:function(data){

		},
		/**
		 * 子类重写进行断开处理
		 */
		disConnect:function(){
			alert('disConnect');
		},
		/**
		 * 子类重写进行通讯错误处理
		 */
		error:function(err){

		}
	});
})($yml)
