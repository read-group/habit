/**
 */
var system = require("../lib/yml.system");
var yml = {};
/**
 * 工具对象，单例
 */
yml.service={};
yml.service.base=system.object.Abstract({
	ctor:function(){
		//this.dbFactory=require("../models/");
	},
	buildRtnData:function(err,content,keyLan){
		var rtn={
		   status:0,
		   content:null,
		   errMsg:null,
		   rawErr:err,
		   help:"status-0 indicate sucess,or 1 indicate fail"
		};
		if(err){
			rtn.status=1;
			rtn.errMsg=this.get18N(keyLan);
		}else{
		   	rtn.status=0;
				rtn.content=content;
		}
		return rtn;
	},
	/**
	 * code 语言编码
	 * to do 定义多语实现
	 * 按照code加载不同的多语文件数据
	 * 多语实现类按照key 返回不同的结果
	 */
	get18N:function(key,code){
		var rtn={
				auth_fail:"帐号或密码错误，请重试....",
				make_tree_fail:"树构造失败...",
				common_fail:"操作失败.",
				reg_repeat:"重复注册",
				reg_fail:"注册失败"
		}
		if(!rtn[key]){
			return key;
		}
		return rtn[key];
	}
})
module.exports = yml;
