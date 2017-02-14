/**
 */
//var events = require("events");
var ykx = {};
/**
 * 工具对象，单例
 */
ykx.utils = {
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
	shadowCopy:function(target,src){
		for(var k in src){
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
		
		
		//在子类调用父类对象的ctor,所以子类对象必须定义
		//ctor，避免子类不定义而再次调用父类原型对象的ctor,而导致重复调用父类ctor
		if(parent && parent.ctor){
			parent.ctor.call(child,initParams);
		}
				
		// 重写,这里解决当前对象没有定义
		var override = override || {ctor:function(){}};
		if(override && !override.ctor){
			override.ctor=function(){};
		}
		//this.deepCopy(child, override);
		that.shadowCopy(child,override);
		
		
		
		// 创建对象后初始化,只有指定执行才执行，
		if(!notExecCtor)
		  child.ctor(initParams);
		
			
		// child.ctor.apply()
		// 指向父类
		child.ubber = parent;
		return child;
	},
	/**
//	 * 删除字典内的对象的方法
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
	}
};
/**
 * 定义应用基类
 * 
 */

ykx.object = ykx.utils.extend(null,null, {
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
			child=ykx.utils.extend(null,this,null);
		}
		if(arguments.length==1){
			if(typeof arguments[0]!="object")
				throw new Error("param must be type of object");
			child=ykx.utils.extend(null,this, arguments[0]);
		}
		if(arguments.length==2){
			child=ykx.utils.extend(arguments[0],this, arguments[1]);
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
			child=ykx.utils.extend(null,this,null,true);
		}
		if(arguments.length==1){
			if(typeof arguments[0]!="object")
				throw new Error("param must be type of object");
			child=ykx.utils.extend(null,this, arguments[0],true);
		}
		if(arguments.length==2){
			child=ykx.utils.extend(arguments[0],this, arguments[1],true);
		}
		
		
		//console.log(arguments.callee.caller.toString())				
		return child
	}
});
module.exports = ykx;
