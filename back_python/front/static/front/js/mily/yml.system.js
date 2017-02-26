/**
 * 工具对象，单例
 */
(function(window){
	var yml={};
	window.$yml=yml;
	yml.utils = {
		/**
		 * 建立命名空间的方法
		 *
		 * @param namespace
		 */
		declare : function(namespace) {
			var attrNames = namespace.split(".");
			var dicNames = {};
			var tmp = [];
			for ( var i in attrNames) {
				var keyName = attrNames[i];
				if (i == 0) {
					eval(keyName + "={}");
					tmp.push(keyName)
				} else {
					var prev = tmp.pop();
					var prevKey = prev + "['" + keyName + "']";
					prev = prevKey + "={}";
					eval(prev);
					tmp.push(prevKey);
				}
			}
		},
		deepCopy : function(child, parent) {
			var c = child, p = parent;
			c = c || {};
			for ( var i in p) {
				if (typeof p[i] === 'object') {
					c[i] = (p[i].constructor === Array) ? [] : {};
					deepCopy(c[i], p[i]);
				} else {
					c[i] = p[i];
				}
			}
			return c;

		},
		shadowCopy:function(target,src,excludePro){
			for(var k in src){
				if(k!=excludePro)
	                   target[k]=src[k];
			}
		},
		/**
		 *
		 * @param parent
		 *            继承的父类对象
		 * @param override
		 *            重写父类对象
		 * @param initParams
		 *            实例化参数 所有返回的对象都有initParams这个实例属性
		 * @returns {___anonymous_child}
		 */
		extend : function(initParams,parent, override,notExecCtor) {

			var initParams = initParams || {};
			var that=this;
			var F = function() {
				// this.ctor();
				// if(override){
				// if(!override.ctor || (override.ctor && typeof
				// override.ctor!="function")){
				// throw new Error("子类必须重写");
				// }
				// override.ctor.call(this);
				// }
				//that.shadowCopy(this,initParams);
			};
			F.prototype = parent || Object.prototype;
			var child = new F();

			// 重写,这里解决当前对象没有定义
			var override = override || {ctor:function(){}};
			if(override && !override.ctor){
				override.ctor=function(){};
			}
			//this.deepCopy(child, override);
			that.shadowCopy(child,override);

			//在子类调用父类对象的ctor,所以子类对象必须定义
			//ctor，避免子类不定义而再次调用父类原型对象的ctor,而导致重复调用父类ctor
			if(parent && parent.ctor){
				parent.ctor.call(child,initParams);
			}

			// 创建对象后初始化,只有指定执行才执行，
			if(!notExecCtor)
			  child.ctor(initParams);


			// child.ctor.apply()
			// 指向父类
			child.ubber = parent;
			return child;
		},
		/**
//		 * 删除字典内的对象的方法
		 */
		deleteElementFromDictByFilter : function(dict, todel, filter) {
			var i = 0;
			for ( var index in dict) {
				if (filter(todel, dict[index])) {
					i = index;// 记下要删除元素的索引
					// console.log(i);
				}
			}
			delete dict[i];
			return dict;
		},
		/**
		 * 删除数组内对象的方法
		 */
		deleteElementFromArrayByFilter : function(array, todel, filter) {
			var i = 0;
			for ( var index in array) {
				if (filter(todel, array[index])) {
					i = index;// 记下要删除元素的索引
					// console.log(i);
				}
			}
			array.splice(i, 1);
			return array;
		},
		guid:function()
		{
			    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
			        var r = Math.random()*16|0, v = c === 'x' ? r : (r&0x3|0x8);
			        return v.toString(16);
			    });
		},
		randNum:function(n){

		    var rnd="";

		    for(var i=0;i<n;i++)

		        rnd+=Math.floor(Math.random()*10);

		    return rnd;

		} ,
		/**
		 * 客户端获取发送到服务端的请求对象
		 *
		 */
		getClientReq:function(accesstoken,dataObj){
			return{
				accessToken:accesstoken,
				data:accesstoken
			};
		},
		/**
		 * 获取服务器端返回数据的格式化响应对象
		 */
		getServerFormatedRes:function(status,msg,data){
			return {
				status:status,
				msg:msg,
				data:data,
			}
		}

	};


	//日期格式化扩展
	Date.prototype.format = function(format) {
	    /*
	     * eg:format="yyyy-MM-dd hh:mm:ss";
	     */
	    var o = {
	        "M+" : this.getMonth() + 1, // month
	        "d+" : this.getDate(), // day
	        "h+" : this.getHours(), // hour
	        "m+" : this.getMinutes(), // minute
	        "s+" : this.getSeconds(), // second
	        "q+" : Math.floor((this.getMonth() + 3) / 3), // quarter
	        "S" : this.getMilliseconds()
	        // millisecond
	    };

	    if (/(y+)/.test(format)) {
	        format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4
	                        - RegExp.$1.length));
	    }

	    for (var k in o) {
	        if (new RegExp("(" + k + ")").test(format)) {
	            format = format.replace(RegExp.$1, RegExp.$1.length == 1
	                            ? o[k]
	                            : ("00" + o[k]).substr(("" + o[k]).length));
	        }
	    }
	    return format;
	};

	// Modal.prototype.adjustDialog = function () {
	//     var modalIsOverflowing = this.$element[0].scrollHeight > document.documentElement.clientHeight
	//
	//     this.$element.css({
	//       paddingLeft:  !this.bodyIsOverflowing && modalIsOverflowing ? this.scrollbarWidth : '',
	//       paddingRight: this.bodyIsOverflowing && !modalIsOverflowing ? this.scrollbarWidth : ''
	//     })
	//     // 是弹出框居中。。。
	//     var $modal_dialog = $(this.$element[0]).find('.modal-dialog');
	//     var m_top = ( $(window).height() - $modal_dialog.height() )/2;
	//     $modal_dialog.css({'margin': m_top + 'px auto'});
	//   }
	/**
	 * 定义应用基类
	 *
	 */

	yml.object = yml.utils.extend(null,null, {
		/**
		 * 这个方法需要被重写
		 */
		ctor : function() {
			//this.name="jy";
		},
		/**
		 * 所有子类对象必须定义ctor函数
		 */
		New : function() {
			var child=null;
			if(arguments.length>2){
				throw new Error("param number the most 2");
			}
			if(arguments.length==0){
				child=yml.utils.extend(null,null,null);
			}
			if(arguments.length==1){
				if(typeof arguments[0]!="object")
					throw new Error("param must be type of object");
				child=yml.utils.extend(null,this, arguments[0]);
			}
			if(arguments.length==2){
				child=yml.utils.extend(arguments[0],this, arguments[1]);
			}
			//console.log(arguments.callee.caller.toString())
			return child
		},
		Abstract:function(){
			var child=null;
			if(arguments.length>2){
				throw new Error("param number the most 2");
			}
			if(arguments.length==0){
				child=yml.utils.extend(null,null,null,true);
			}
			if(arguments.length==1){
				if(typeof arguments[0]!="object")
					throw new Error("param must be type of object");
				child=yml.utils.extend(null,this, arguments[0],true);
			}
			if(arguments.length==2){
				child=yml.utils.extend(arguments[0],this, arguments[1],true);
			}


			//console.log(arguments.callee.caller.toString())
			return child
		}
	});
})(window);
