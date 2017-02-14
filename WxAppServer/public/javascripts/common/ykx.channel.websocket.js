(function(ykx){
	ykx.websocket=ykx.object.Abstract({
		ctor:function(initParams){
			this.socketUrl=initParams.socketUrl;
			this.io=initParams.io;
			this.client = this.io.connect(this.socketUrl);	
			//初始化事件
			this.init();
		},
		init:function(){
			var self=this;
			this.client.on('connect', function() {				
				self.client.on("push2browser", function(data) {				
					if(data.status==1){
						if(data.callback){
							var func=eval(data.target+"."+data.callback);
							var targetObj=eval(data.target);
							func.call(targetObj,data);
						}else{
							self.getData(data);
						}
					}else{
						self.error(data);
					}
									
				});
				//代理服务器断开监听器
				self.client.on('disconnect', function() {
					self.disConnect();
				});
				//代理服务器断开监听器
				self.client.on('error', function(err) {
					self.error();
				});
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
})(ykx)
