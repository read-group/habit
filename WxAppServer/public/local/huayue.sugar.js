/**
 * 工具对象，单例
 */
(function(window,$){
	var buzz=window.buzz;
	$huayue.sound=$huayue.object.New({
		ctor:function(){
			// Preload the sound
			// auto, metadata, none
			buzz.defaults.preload = 'auto';
			// Play the sound when ready
			// bool
			buzz.defaults.autoplay = false;
			// Loop the sound
			// bool
			buzz.defaults.loop = false;
			// value to display when a time convertion is impossible
			buzz.defaults.placeholder = '--';
			// Duration of a fading effect
			// milliseconds
			buzz.defaults.duration = 5000; 
			// Audio formats of your files
			//buzz.defaults.formats = ['ogg', 'mp3', 'aac', 'wav'];
			var that=this;
			$(document).on("pageinit",function(){
				$(document).on("click","a",function(){
					that.openSound();
				});
			});	
			this.sound=new buzz.sound("/local/sounds/btnClick.mp3");
		},
		openSound:function(){		
			
    		this.sound.play();
		}
	});

	$huayue.validor=$huayue.object.New({
		ctor:function(){
			
		},
		validate:function(selector){
			if(!$(selector).get(0).checkValidity()){
				var msg=$(selector).jqmData("validMsg");
				$(selector).attr('placeholder',msg);
				$(selector).val("");
				return false;
			}
			return true;
		},
		formValidate:function(selectorForm){
			var self=this;
			var rtn=true;
			$("input[data-valid-msg]",$(selectorForm)).each(function(i,item){			
				if(!self.validate(this)){
					rtn=false;
					return rtn;
				}	
			});
			return rtn;
		},
		validRepeat:function(reCtl,pwdctl){
			var msg=$(pwdctl).jqmData("validMsg");
			if($(reCtl).val()==$(pwdctl).val()){
				$(reCtl).attr('placeholder',msg);
				return false;
			}
			return true;
		}
	});
	$huayue.noti=$huayue.object.New({
		ctor:function(){
			var self=this;
			$(document).on("pageinit","#p1",function(){
				  //初始化每个最外层页面框架的通知插件
				self.$noti=$("#notify");
				self.$content=$("#notifyContent")
				//alert(self.$content.text());
				self.$noti.panel();
			});	
		},
		notify:function(msg){
			this.$content.text(msg);
			this.$noti.panel('open');
		}
	});
	/**
	 * 复选项目缓存处理
	 */
	$huayue.optons={};
	$huayue.optons=$huayue.object.New({
		ctor:function(){
			var self=this;
			this.cache={};	
		},
		/**
		 * 用于初始化加载时，保持和界面一致
		 */
		init:function(ns,key,item){
			var nsKey=ns+key;
			item.status=$huayue.db.status.Origin;
			this.cache[nsKey]=item;
			
		},
		/**
		 * 命名空间
		 * ns命名空间
		 */
		put:function(ns,checked,key,item){
			var nsKey=ns+key;
			if(checked){//如果选项选中
				if(!this.cache[nsKey]){//如果不存在key,就新建
					this.cache[nsKey]=item;
					item.status=$huayue.db.status.New;//表示新增
					console.log("new....");
				}else{
					this.cache[nsKey].status=$huayue.db.status.Origin;
				}
			}else{//如果选项取消了
				if(this.cache[nsKey]){//如果存在key,就设置删除状态
					if(this.cache[nsKey].status==$huayue.db.status.New){
						 delete this.cache[nsKey];
						 console.log("del....");
					}else{	   
						this.cache[nsKey].status=$huayue.db.status.Del;
					}
					
				}
			}
		},
		/**
		 * 按照命名空间获取数据集合
		 */
		get:function(ns){
			var rs=[];
			for(var k in this.cache){
				  if(k.startsWith(ns)){
					  rs.push(this.cache[k]);
				  }
			}
			return rs;
		},
		/**
		 * 清空缓存
		 * 清空指定命名空间的缓存
		 */
		clear:function(ns){
			for(var k in this.cache){
			  if(k.startsWith(ns)){
				  delete this.cache[k];
			  }
			}
		}
	});
})(window,$);

