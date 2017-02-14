var crypto=require("crypto");
var weixin=require("../../service/wx.service");
module.exports = function (app) {
	/*微信事件处理*/
	// config

	// 接入验证
	app.get('/', function(req, res) {
	    // 签名成功
	    if (weixin.checkSignature(req)) {
	        res.send(200, req.query.echostr);
	    } else {
	        res.send(200, 'fail');
	    }
	});
	// Start
	app.post('/', function(req, res) {

	    // loop
	    weixin.loop(req, res);

	});
};
