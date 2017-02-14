var yml = {};
// 获得系统基类对象
var system = require("./yml.system");
var childproc = require('child_process');
/**
 * 这个信道需要只需要创建一个子类对象
 */
yml.restClient = system.object.Abstract({
	ctor : function(initParams) {

		this.cmdGetPattern = "curl {-G} -k  -d '{data}' {url}";
		this.cmdPostPattern="curl  -k -H 'Content-type: application/json'  -d '{data}' {url}";
		this.cmdDownLoadFilePattern="curl -G -o {fileName} {url}";
	},
	setRestUrl:function(restUrl){
		this.restUrl=restUrl;
	},
	FetchGetCmd : function(subData, url) {
		// console.log(this.cmdPattern);
		var cmd = this.cmdGetPattern.replace(/\{\-G\}/g, "-G").replace(
				/\{data\}/g, subData).replace(/\{url\}/g, url);
		return cmd;
	},
	FetchPostCmd : function(subData, url) {
		var data=JSON.stringify(subData);
		var cmd= this.cmdPostPattern.replace(/\{data\}/g,
				data).replace(/\{url\}/g, url);
		return cmd;
	},
	FetchDownLoadCmd : function(fname,url) {
		// console.log(this.cmdPattern);
		var cmd = this.cmdDownLoadFilePattern.replace(/\{fileName\}/g, fname).replace(
				/\{url\}/g, url);
		console.log("download cmd ========================");
		console.log(cmd);
		console.log("download cmd ========================");
		return cmd;
	},
	exec:function(cmd, callback) {
		childproc.exec(cmd, function(err,out){
			if(err){
			  return	callback(err);
			}
			else{
				var jsonData=JSON.parse(out);
				return callback(null,jsonData);
			}
		});
	},
	exec2:function(cmd, callback) {
		childproc.exec(cmd, function(err,out){
			var jsonData=null;
			if(err){
			  return	callback(err);
			}
			else{
				try{
					jsonData=JSON.parse(out);
				}catch(e){
					return callback(null,out);
				}
				return callback(null,jsonData);
			}
	   });
  },
	callGet:function(data,callback) {
      var cmd=this.FetchGetCmd(data,this.restUrl);
      this.exec(cmd,callback);
	},
	callPost:function(data,callback){
	  var cmd=this.FetchPostCmd(data,this.restUrl);
	  this.exec(cmd,callback);
	},
	callDownLoad:function(fname,callback){
		var cmd=this.FetchDownLoadCmd(fname,this.restUrl);
		this.exec2(cmd,callback);
	}
});
module.exports = yml;
// var initParams={
// 		restUrl:"https://api.weixin.qq.com/cgi-bin/user/info"
// };
// var restClient= yml.restClient.New(initParams,{
// 	ctor:function(){
// 	}
// });
//restClient.callPost({loginName:'jiangyong',pwd:'520612'},function(err,out){
//	console.log(out);
//});

// restClient.callGet("access_token=EAKYjCX8UKlIy9-VuuUDdwleWG6NQCXjWY-JB1XMLVy41Ub2k2du4KkWKT9wsb23Nye4AHJFosBpAJ5YTXc2CrgvV9StEeIRjuJEnA4VvrfxU1eLwFT-2X9RQJTZnW-aTEKiAJAYJP&openid=ot3MKs-k9VDrJE4R3j-HygRSzQEc&lang=zh_CN",
// 		function(err,out){
// 	console.log(out);
// })
