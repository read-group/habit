var system = require("../yml.system");
var settings=require("../../config/settings");
var WXPay = require('weixin-pay');
var uuid = require('node-uuid');
var fs=require("fs");
yml={};
yml.wxpay=system.object.New(null,{
  ctor:function(){
    this.wp = WXPay({
         appid: settings.wxappid,
         mch_id: settings.mecid,
         partner_key: settings.seckey, //微信商户平台API密钥
         pfx: fs.readFileSync(__dirname+'/apiclient_cert.p12'), //微信商户平台证书
    });

  },
  uniOrder:function(content,cbk){
    //统一下单
      this.wp.createUnifiedOrder(content, function(err, result){
        cbk(err,result);
      });
  },
  queryOrder:function(outNo,cbk){
    this.wp.queryOrder({out_trade_no:outNo}, cbk);
  },
  getBrandWCPayRequestParams:function(content,cbk){
    this.wp.getBrandWCPayRequestParams(content,cbk);
  },
  useWXCallback:function(fn){
    return this.wp.useWXCallback(fn);
  },
  enPay:function(opts,cbk){
    this.wp.enPay(opts,cbk);
  }

})
module.exports=yml;
// //var out_trade_no:='20140703'+Math.random().toString().substr(2, 10),
// var u=uuid.v1().toString().replace(/\-/g,"");
// var ind=uuid.v1().indexOf("-");
// console.log(ind);
//  console.log(u);
// yml.wxpay.getBrandWCPayRequestParams({
//     body: '助学圈下“助”',
//     out_trade_no: u,
//     total_fee: 1,
//     spbill_create_ip: '192.168.2.210',
//     notify_url: 'http://wxpay_notify_url',
//     product_id: '1234567890',
//     openid:'ol5vCv8jx4CYlW5Ax7nuLurPTpqw'
// },function(err,r){
//   console.log(r);
// });
// yml.wxpay.queryOrder(u,function(err,r){
//   console.log(r);
// });
// yml.cache.getStringType("c",function(err,r){
//   console.log(r);
// });
