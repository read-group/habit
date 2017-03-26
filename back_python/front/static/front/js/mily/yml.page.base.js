/**
 * 工具对象，单例
 */
(function(window,$){
	$yml.pageBase=$yml.object.Abstract({
		ctor:function(){
      //设置当前页面的vmDom元素的名字
      var elName=$("[data-page-root]").data("pageRoot");
			if(!elName){
				console.log("warnging...."+"请先确认正确的定义了页面vm的dom元素，page-root数据属性的定义,应用出现的第一个警告,可以忽略");
			}else{
				this.vmEleName=elName;
				console.log("page base called.....")
			};
			this.$vmPage=null;
			//
		},
		getVmEleName:function(){
			return this.vmEleName;
		},
		vmInit:function(){
			//需要子类重写，返回定义的页面vm
			if(!this.vmDef){
				console.log("warning...."+"页面没有定义vm设置方法vmDef");
				return;
			}
			var childVmDefine=this.vmDef();
			var vmPage=avalon.define(childVmDefine);
			//解决子类闭包封装了返回时的子类对象，包括当时的状态，当时还不存在$vmPage；
			//childVmDefine.$vmPage=vmPage;
			//this.$vmPage=vmPage;
			return vmPage;
		},
		vmInitAfter:function(vmMain,vmPage,paramObj,fromUrl){
			this.$vmMain=vmMain;
			this.$vmPage=vmPage;
			if(!this.pageReady){
				console.log("warnging..."+"请重写pageReady方法，需要在这个方法里写页面的业务逻辑")
			}else{
				//获取查询参数
				// var params=this.$router.$vm.navUrl.split("?");
	      // if(params.length>0){
	      //    paramObj=avalon.unparam(params[1]);
	      // }
				//注入传入的参数
				this.pageReady(paramObj,fromUrl);
			}
		}
	});
})(window,$);
