var Wx= require("../lib/channel/wx.event");
var ak=require("../lib/channel/wx.accessKey");
var rest=require("../lib/yml.rest.call");
var settings=require("../config/settings");
var weixin=new Wx();
weixin.token = 'token';
// 监听文本消息
weixin.textMsg(function(msg) {
    console.log("textMsg received");
    console.log(JSON.stringify(msg));
    var resMsg = {};
    switch (msg.content) {
        case "文本" :
            // 返回文本消息
            resMsg = {
                fromUserName : msg.toUserName,
                toUserName : msg.fromUserName,
                msgType : "text",
                content : "这是文本回复",
                funcFlag : 0
            };
            break;

        case "音乐" :
            // 返回音乐消息
            resMsg = {
                fromUserName : msg.toUserName,
                toUserName : msg.fromUserName,
                msgType : "music",
                title : "音乐标题",
                description : "音乐描述",
                musicUrl : "音乐url",
                HQMusicUrl : "高质量音乐url",
                funcFlag : 0
            };
            break;

        case "图文" :

            var articles = [];
            articles[0] = {
                title : "PHP依赖管理工具Composer入门",
                description : "PHP依赖管理工具Composer入门",
                picUrl : "http://weizhifeng.net/images/tech/composer.png",
                url : "http://weizhifeng.net/manage-php-dependency-with-composer.html"
            };

            articles[1] = {
                title : "八月西湖",
                description : "八月西湖",
                picUrl : "http://weizhifeng.net/images/poem/bayuexihu.jpg",
                url : "http://weizhifeng.net/bayuexihu.html"
            };

            articles[2] = {
                title : "「翻译」Redis协议",
                description : "「翻译」Redis协议",
                picUrl : "http://weizhifeng.net/images/tech/redis.png",
                url : "http://weizhifeng.net/redis-protocol.html"
            };

            // 返回图文消息
            resMsg = {
                fromUserName : msg.toUserName,
                toUserName : msg.fromUserName,
                msgType : "news",
                articles : articles,
                funcFlag : 0
            }
    }

    weixin.sendMsg(resMsg);
});

// 监听图片消息
weixin.imageMsg(function(msg) {
    console.log("imageMsg received");
    console.log(JSON.stringify(msg));
});

// 监听位置消息
weixin.locationMsg(function(msg) {
    console.log("locationMsg received");
    console.log(JSON.stringify(msg));
});

// 监听链接消息
weixin.urlMsg(function(msg) {
    console.log("urlMsg received");
    console.log(JSON.stringify(msg));
});
var restClient=rest.restClient.New();
//设置获取
function getUserInfo(openid,cbk){
  restClient=rest.restClient.New();
  restClient.setRestUrl("https://api.weixin.qq.com/cgi-bin/user/info");
  ak.accessKey.getAccessKey(function(err,key){
    if(err){
      return cbk(err);
    }else {
      var data="access_token={ACCESS_TOKEN}&openid={OPENID}&lang=zh_CN"
      .replace(/\{ACCESS_TOKEN\}/g, key).replace(/\{OPENID\}/g,openid);
       return restClient.callGet(data,cbk);
    }
  });
}
// 监听事件消息
weixin.eventMsg(function(msg) {
  if(msg.event=="subscribe" || msg.eventKey=="hostLogin"){
    var articles = [];
    articles[0] = {
        title : "帮助家长陪伴孩子习惯养成",
        description : "六步玩转小小领袖,详见<使用指南>。很多时候，孩子缺的是陪伴和关注，小小领袖让更多的家长朋友来关注孩子,陪伴孩子一起坚持...",
        picUrl : "http://wx.yimilan.com/images/ok.jpg",
        url : "http://mily365.com/?noticeKey="+msg.fromUserName,
        //url : "http://ll.yimilan.com/help/sixstep.html"
    };
    var resMsg = {
        fromUserName : msg.toUserName,
        toUserName : msg.fromUserName,
        msgType : "news",
        articles : articles,
        funcFlag : 0
    };
    weixin.sendMsg(resMsg);
    //获取用户的具体信息，并保存到
    getUserInfo(msg.fromUserName,function(err,rs) {
      //注册微信信息到用户中心
      rs["appId"]=settings.appId;
      restClient.setRestUrl(settings.user_center_url+"reg");
      restClient.callPost({wxInfo:rs},function(err,out){
         console.log(out);

      });
    });
  }else{
    //发送空串回微信服务器
    weixin.res.send("");
  }
});

//获取用户信息
module.exports=weixin;
// var x={ subscribe: 1,
//   openid: 'ot3MKs-k9VDrJE4R3j-HygRSzQEn',
//   nickname: '蒋勇',
//   sex: 1,
//   language: 'zh_CN',
//   city: '海淀',
//   province: '北京',
//   country: '中国',
//   headimgurl: 'http://wx.qlogo.cn/mmopen/SdoNic3lybgnpAb372gibTGLtQ5Hx44tbFZHiajOicbicL5Ls4XLQRDAI6zzLOa4ia2bX2zssib0cEZuCIwKNkhecHLCGNLYl3mDrTq/0',
//   subscribe_time: 1460528560,
//   unionid: 'okCtTsxIjxqRzT-gpy1tMxesBH8E',
//   remark: '',
//   groupid: 0 };
// restClient.setRestUrl(settings.user_center_url+"reg");
// restClient.callPost(x,function(err,out){
//    console.log(out);
//
// });
