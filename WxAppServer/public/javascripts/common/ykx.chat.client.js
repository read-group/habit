(function($, ykx) {
	$(function() {	
		ykx.controllers={};
		ykx.getControllerByTag=function(tag){
			return ykx.controllers[tag];
		};
		//通信客户端
		var initParams = {
				"socketUrl" : "http://10.17.4.229:3000",
				"io" : io
			};		
		ykx.chatClient = ykx.websocket.New(initParams, {
			ctor : function() {
				this.msgTypes=["txt","img","audio","video"];
				this.user=null;
			},	
			
			/**
			 * 子类重写获取服务端的数据
			 */
			getData : function(data) {
				
			},
			/**
			 * 子类重写进行断开处理
			 * 说明服务出现异常
			 * 则清理掉客户端的cookie
			 */
			disConnect : function(err) {
				$.messager.alert("提示",err);
				ykx.loginController.clearAccessKey();
				ykx.loginController.setInitState();
				
			},
			/**
			 * 子类重写进行通讯错误处理
			 */
			error : function(data) {	
				if(data.status==-1){//说明身份无效过期或未登录，需要验证身份
					ykx.loginController.clearAccessKey();
					ykx.loginController.setInitState();
					return;
				}
				if(data.status==-2){
					$.messager.alert("提示",data.errMsg);
					return;
				}
				$.messager.alert("提示",data.errMsg);
			}
		});
		/**
		 * 控制器基类
		 */
		ykx.controllerBase=ykx.object.Abstract({
			ctor:function(){
				ykx.controllers[this.getTag()]=this;
				this.initControls();
				this.initEvents();
				this.setInitState();
			},
			getTag:function(){
				this.tag="";
				return this.tag;
			},
			initControls:function(){
				
			},
			initEvents:function(){
				
			},
			setInitState:function(){
				
			},
			/**
			 * 构造要发送的数据
			 */
			buildDataToSend : function(cmd, content, callback) {
				var self=this;
				var data = {
					"keyAccess":null,
					"cmd" : cmd,
					"content" : content,
					"callback" : callback,
					"target":self.getTag(),
				};
				if(ykx.chatClient.user && ykx.chatClient.user.keyAccess){
					data.keyAccess=ykx.chatClient.user.keyAccess;
				}
				return data;
			}
		});		
		/**
		 * 消息面板控制器
		 */
		
		ykx.msgPanelController=ykx.controllerBase.New({
			ctor:function(){			
				this.from=null;
				this.to=null;
			},
			/**
			 * 构造
			 */
			buildChatMsg:function(txtMsg){
				if(this.from==this.to || !this.to){
					$.messager.alert("提示","请选择要发送消息的目标人员.");
					ykx.findTabController.$findTab.tabs("select",1);
					return null;
				}
				var msg={
					from:this.from,
					to:this.to,
					txt:txtMsg
					
				};
				var dataToSend=this.buildDataToSend("chat",msg,"chatReply");
				return dataToSend;
			},
			getTag:function(){
				this.tag="ykx.msgPanelController";
				return this.tag;
			},
			/**
			 * 关联要处理的UIyuan s
			 */
			initControls:function(){
				var self=this;
				this.$btnSend=$("#btnSendMsg");
				this.$txtMsg=$("#txtMsg");
				this.$tabsMsgType=$("#tabsMsgType");
				this.$hintRight = $("[name='chatMsgRight']");	
				this.$hintLeft = $("[name='chatMsgLeft']");	
				this.$chatTabs=$("#chatList");
				/*this.$hintRight.tooltip({
				    position: 'right',
				    content: '<span style="color:#fff">This is the tooltip message.</span>',
				    onShow: function(){
				    	$(this).tooltip('tip').css({
				            backgroundColor: '#666',
				            
				            borderColor: '#666'
				        });
				    }
				});
				this.$hintRight.tooltip('show');
				this.$hintRight.off("mouseenter");
				this.$hintRight.off("mouseleave");
				
				this.$hintLeft.tooltip({
				    position: 'left',
				    content: '<span style="color:#fff">This is the tooltip message.</span>',
				    onShow: function(){
				    	$(this).tooltip('tip').css({
				            backgroundColor: '#666',
				            borderColor: '#666'
				        });
				    }
				});
				this.$hintLeft.tooltip('show');
				this.$hintLeft.off("mouseenter");
				this.$hintLeft.off("mouseleave");*/
			},
			/**
			 * 挂载事件
			 */
			initEvents:function(){
				var self=this;
				this.msgType=ykx.chatClient.msgTypes[0];
				this.$tabsMsgType.tabs({
					onSelect:function(t,i){
						self.msgType=ykx.chatClient.msgTypes[i];
						//alert(self.msgType);
					}
				});
				this.$btnSend.click(function(){
                    if(ykx.loginController && ykx.loginController.user && ykx.loginController.user.keyAccess){
                    	if(self.msgType==ykx.chatClient.msgTypes[0]){//表示文本消息
    						var txtMsg=$.trim(self.$txtMsg.val());
    						if(txtMsg==""){
    							$.messager.alert("提示","请输入要发送的文本消息...");
    							return;
    						}
    						var dataToSend=self.buildChatMsg(txtMsg);
    						if(dataToSend!=null)
    						   ykx.chatClient.sendData(dataToSend);
    					}
                    }else{
                    	$.removeCookie("user");
    					window.location.reload();
                    }			
				});
				
			},
			buildMsgToolTip:function(container,fromName,msgContent){
				var $div=$("<div style='padding:10px'></div>");
				var $msgHtml=$("<a  href='javascript:void(0)'>"+fromName+"</a>");
				$div.append($msgHtml);
				$(container).append($div);
				$msgHtml.tooltip({
					position:"right",
					content:msgContent,
					onShow: function(){
				        $(this).tooltip('tip').css({
				            backgroundColor: '#666',
				            borderColor: '#666'
				        });
				    }
				});
				$msgHtml.tooltip('show');
			},
			chatReply:function(data){
				//alert(JSON.stringify(data));
				var fromName=data.fromName;
				var msgContent=data.content;
				var from=data.from;
				var divId="#"+from;
				var someTab= this.$chatTabs.tabs('getTab',fromName);
				if(!someTab){//只要不存在添加来访tab
					this.$chatTabs.tabs('add',{
						title:fromName,
						content:"<div id='"+from+"'></div>",
						closable:true,
					});                      
					//var msgHtml="<a tag='x' href='javascript:void(0)' style='display:block'  title='"+msgContent+"'>"+fromName+"</a>";					
				    this.buildMsgToolTip(divId,fromName,msgContent);
					
				}else{
					this.buildMsgToolTip(divId,fromName,msgContent);
				}
			}
			
		});
	
		
		/**
		 * 发现页签控制器
		 */
		ykx.findTabController=ykx.controllerBase.New({
			ctor:function(){},
			getTag:function(){
				this.tag="ykx.findTabController";
				return this.tag;
			},
			/**
			 * 关联要处理的UIyuan s
			 */
			initControls:function(){
				this.$findTab = $("#findTab");
				
			},
			/**
			 * 挂载事件
			 */
			initEvents:function(){
				this.$findTab.tabs({
					onSelect:function(t,i){
						if(i==1){				
							if(ykx.loginController.user){						
								ykx.orgController.selectNode(ykx.loginController.user.id);
								//ykx.loginController.loadData();
							}
							  
						}
					}
				});
				
			},
			
		});
		/**
		 * 组织树控制器
		 */
		ykx.orgController=ykx.controllerBase.New({
			getTag:function(){
				this.tag="ykx.orgController";
				return this.tag;
			},
			/**
			 * 关联要处理的UIyuan s
			 */
			initControls:function(){
				this.$orgData=$("#orgData");
				this.$searchbox=$("#searchbox");
				this.root=null;
			},
			/**
			 * 挂载事件
			 */
			initEvents:function(){
				var self=this;
				
				this.$orgData.tree({
					onSelect:function(node){
						if(node.attributes.isEmp){
							ykx.msgPanelController.from=ykx.chatClient.user.id;
							ykx.msgPanelController.to=node.id;				
						}
					}
				});
				this.$searchbox.searchbox({
				    searcher:function(value,name){
				    	self.$orgData.tree('doFilter', value);
				    	//self.$orgData.tree('doFilter', '');
				    	var nodeRoot=self.$orgData.tree('find',self.root.id);
				    	self.$orgData.tree('expandAll',nodeRoot.target);
				    }
				});
			},
			loadData:function(){
				var dataToSend = this.buildDataToSend("org", null,
				"orgReply");
	         	ykx.chatClient.sendData(dataToSend);
			},
			selectNode:function(id){
				var node = this.$orgData.tree('find', id);
				var pnode=this.$orgData.tree('find', node.attributes.idParent);		
				this.$orgData.tree('expandTo', pnode.target);
//				//选中
//				this.$orgData.tree('select', nodeParent.target);
			},
			orgReply:function(data){
				//alert(JSON.stringify(data.content));
				this.$orgData.tree({
					data:[data.content]
				});
				this.root=data.content;
			}
		});		
		/**
		 * 登陆控制器
		 */
		ykx.loginController=ykx.controllerBase.New({
			ctor:function(){
				$.cookie.json = true;
				this.isAuth=false;
			},
			getTag:function(){
				this.tag="ykx.loginController";
				return this.tag;
			},
			/**
			 * 关联要处理的UIyuan s
			 */
			initControls:function(){
				this.$otherInfo = $("#otherInfo");
				this.$btnLogin = $("#btnLogin");
				this.$btnExit=$("#btnExit");
				this.$txtLoginName = $("#loginName");
				this.$txtPwd = $("#pwd");
				this.$frmPerson = $("#frmPerson");
				this.$loginTr=$("#loginTr");
				this.$pwdTr=$("#pwdTr");
				
			    			
			},
			clearAccessKey:function(){
				$.removeCookie("user");
			},
			//初次加载或登录成功或刷新时回调用这个方法
			setInitState:function(isLogin){
				$.cookie.json = true;
				if (!$.cookie("user")) {// 未登录那么就显示登录，隐藏其它信息
					this.isAuth=false;
					ykx.getControllerByTag("ykx.findTabController").$findTab.tabs('select', 2);
					this.showLogin();
					this.hideOther();

				} else {		
					// 从cookie中取出用户信息
					this.user = $.cookie("user");	
					this.isAuth=true;	
					ykx.chatClient.user=this.user;	
					
					//如果已经存在了cookie,说明是刷新
					//如果是刷新则重新按照访问key建立客户端链接缓存
					if(!isLogin)
					{
						var dataToSend = this.buildDataToSend("reconnect", null,"reconnectReply");
					    ykx.chatClient.sendData(dataToSend);
					  
					}else{
						  this.loadForm();
					}
					
				}
			},
			loadForm:function(){
				// 更新我表单
				this.$frmPerson.form('load',this.user);
				this.showOther();
				this.hideLogin();	
				//加载组织数据
				ykx.orgController.loadData();
			},
			reconnectReply:function(data){
				this.loadForm();
			},
			/**
			 * 挂载事件
			 */
			initEvents:function(){
				var self = this;
				this.$btnLogin.click(function() {				
					var loginName = $.trim(self.$txtLoginName.val());
					var pwd =$.trim(self.$txtPwd.val());
					if(loginName!="" && pwd!=""){
						var content = {};
						content.loginName = loginName;
						content.pwd = pwd;
						var dataToSend = self.buildDataToSend("auth", content,
								"authReply");
						//通讯客户端
						ykx.chatClient.sendData(dataToSend);
					}					
				});
				//退出会话
				this.$btnExit.click(function(){
					var dataToSend = self.buildDataToSend("logout", null,
					"logoutReply");
		         	ykx.chatClient.sendData(dataToSend);
												
				});
				this.$frmPerson.keydown(function(e){
					if(e.keyCode==13){
						if(!self.isAuth)
						   self.$btnLogin.trigger("click");
					}
				});
			},
			logoutReply:function(data){
				$.removeCookie("user");
				window.location.reload();
			},
			hideLogin:function(){
				this.$loginTr.attr("style", "display:none");
				this.$pwdTr.attr("style", "display:none");
			},
			showLogin:function(){
				this.$txtLoginName.val("");		
				this.$txtPwd.val("");			
				this.$loginTr.attr("style", "display:");
				this.$pwdTr.attr("style", "display:");
			},
			showOther:function(){
				this.$otherInfo.attr("style", "display:");
			},
			hideOther:function(){
				this.$otherInfo.attr("style", "display:none");
			},
			/**
			 * 登陆认证回复
			 */
			authReply : function(data) {
				if (data.status == 1) {
                    this.$frmPerson.form('load',data.content);
                    $.cookie("user",data.content);
                    //登录成功后，刷新发现面板
                    this.setInitState(true);		
				}else{
					this.showLogin();
					this.hideOther();
					$.messager.alert("提示",data.errMsg);
					$.removeCookie("user");
				}
			}
		});	
		
		
	});
})(jQuery, ykx)
