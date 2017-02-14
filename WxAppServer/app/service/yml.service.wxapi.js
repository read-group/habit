/**
 */
var weixinKey=require("../lib/channel/wx.accessKey");
var services = require("./yml.service.base");
var rest=require("../lib/yml.rest.call");
var ak=require("../lib/channel/wx.accessKey");
var uuid=require("node-uuid");
var settings=require("../config/settings");
var ffmpeg = require('fluent-ffmpeg');
var yml = {};
yml.service={};
/**
 * 习惯业务对象，单例
 */
yml.service.wxapi=services.service.base.New({
	ctor:function(){
		 this.restClient=rest.restClient.New();
		 this.host="http://wx.yimilan.com/";
		 this.folder="wxdownload/";
		 this.audioFolder="audio/";
		 this.imgFolder="img/";
	},
	getJsApiConfig:function(url,cbk){
		var self=this;
		weixinKey.accessKey.getAccessKey(function(){
				weixinKey.accessKey.getJsApiConfig(url,function(err,c){
				  var rtnData=self.buildRtnData(err, c, "获取js调用配置失败");
 	 			  return cbk(rtnData);
			});
		});

	},
	getAccessKey:function(cbk){
		var self=this;
		weixinKey.accessKey.getAccessKey(function(err,rtn){
			 var rtnData=self.buildRtnData(err, rtn, "获取js调用配置失败")
			 return cbk(rtnData);
		});
	},
	downloadFile:function(mediaId,type,cbk){
		var that=this;
		//获取访问key类型
		ak.accessKey.getAccessKey(function(err,key){
			 if(!err){
				 var url="http://file.api.weixin.qq.com/cgi-bin/media/get?access_token={ACCESS_TOKEN}\\&media_id={MEDIA_ID}";
				 var handledUrl=url.replace(/\{ACCESS_TOKEN}/g, key).replace(/\{MEDIA_ID\}/g, mediaId);
				 that.restClient.setRestUrl(handledUrl);
				 //动态生成一个文件名称
				 var fileName=uuid.v1();
				 var filePathName=null;
				 if(type=="img"){
					 filePathName=settings.basepath+"/public/wxdownload/"+that.imgFolder+fileName;
				 }
				 if(type=="audio"){
					 filePathName=settings.basepath+"/public/wxdownload/"+that.audioFolder+fileName;
				 }
				 that.restClient.callDownLoad(filePathName,function(err,out){
					 var rtnData=that.buildRtnData(err, out, "获取js调用配置失败");
					 console.log("下载文件.......................");
					 console.log(rtnData);
					 if(!err){
						 if(type=="img"){
						   rtnData.resUrl=that.host+that.folder+that.imgFolder+fileName;
							 return cbk(rtnData);
					   }
						 if(type=="audio"){
							 var inputFile=filePathName;
							 var outputFile=filePathName+".mp3"
							//  ffmpeg(inputFile).output(outputFile).audioFilters([
							// 	 {filter: 'volume',options: '3'},{filter:'silencedetect',options:'n=-50dB:d=5'}])
							// 	 .on('end', function(stdout, stderr) {
							//      rtnData.resUrl=that.host+that.folder+that.audioFolder+fileName+".mp3";
							// 		 return cbk(rtnData);
							//    }).on('error',function(err){
							// 		 rtnData.resUrl="转换出错";
							// 		 return cbk(rtnData);
							// 	 }).run();
							 ffmpeg(inputFile).output(outputFile).audioFilters('volume=2')
								 .on('end', function(stdout, stderr) {
							     rtnData.resUrl=that.host+that.folder+that.audioFolder+fileName+".mp3";
									 return cbk(rtnData);
							   }).on('error',function(err){
									 console.log(err);
									 rtnData.resUrl="转换出错";
									 return cbk(rtnData);
								 }).run();
						 }
					 }else {
					 	  return cbk(rtnData);
					 }

				 });

			 }else{
				 var rtnData=that.buildRtnData(err, null, "下载文件失败.");
				 return cbk(rtnData);
			 }
		});

	}
});
module.exports = yml;
///yimilan/node/nodeapp/Seed/Platform/TransDeamon/ffmpeg302
// var u={
// 	idOrg:"878dc130-04fd-11e6-ad98-3fe90a9788b1"
// }
// yml.service.habit.cats(u,function(rs){
// 	rs.content.forEach(function(r){
// 		console.log(r.name);
// 	});
// });
//   yml.service.habit.byCat('86ae5120-0512-11e6-86ca-f908682f3732',function(rs){
//
// 	rs.content.forEach(function(r){
// 		console.log(r.name);
// 	});
// });
//

// var url="http://file.api.weixin.qq.com/cgi-bin/media/get?access_token={ACCESS_TOKEN}&media_id={MEDIA_ID}";
// var handledUrl=url.replace(/\{ACCESS_TOKEN}/g, "ccc").replace(/\{MEDIA_ID\}/g, "ddd");
// console.log(handledUrl);
