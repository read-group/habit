var fs=require("fs");
var csv = require('node-csv');
var model=require("../models");
var lines=0;

//行处理器
function LineHandler(dbparam,lineParam,ownidParam){
	this.db=dbparam;
	this.lineArray=lineParam.split(",");
	this.ownerId=ownidParam;
}
LineHandler.prototype.handle=function(){
	var ownid=this.ownerId;
	var phone=this.lineArray[3];
	var plateNumber=this.lineArray[4];
	var memo=this.lineArray[5];
	if(!memo) memo="";
	var customerId=null;
	console.log(ownid+":"+phone+":"+plateNumber+":"+memo);
	//按照车牌号去更新owner_id,如果为空，按照电话号码去更新
	var updateSql="update  convoy.crm_customer set owner_id="+ownid+",lastTrackDate='"+"2015-07-29 14:33:11"+"',";
	updateSql+="lastTrackType='followUp',content='"+memo+"'"+ " where ";
	var selectSql="select id from convoy.crm_customer where ";
	var that=this;
	if(plateNumber && plateNumber!="" && plateNumber!="\N"){
		updateSql+=" plate_number='"+plateNumber+"'";
		//console.log(updateSql);	
		this.db.driver.execQuery(updateSql,function(err,data){
			if(err) console.log(err);
			console.log(updateSql);
		});
		selectSql+=" plate_number='"+plateNumber+"'";
	    if(memo && memo!=""){
	    	this.db.driver.execQuery(selectSql,function(err,data){
				if(err) console.log(err);
				if(data && data.length>0){
					var curId=data[0].id;
					var insertSql="insert into convoy.crm_customer_track ";
					insertSql+="(customer_id, track_date, track_mode, track_type,";
					insertSql+=	"content,progress,"; 
					insertSql+=	"idCreator, creator, createTime, idUpdator) VALUES ( ";
					insertSql+=""+curId+",'"+"2015-07-29 14:33:11"+"','"+"phone"+"','"+"followUp"+"','"+memo+"',"+"0"+",";
					insertSql+=""+"429"+",'"+"蒋勇"+"','"+"2015-07-29 14:33:11"+"',"+"429"+")";
					//console.log(insertSql);
					that.db.driver.execQuery(insertSql,function(err,data){
						if(err) console.log(err);	
						console.log(insertSql);
					});
				}
				
			    	//查询出客户id
			    
				
			});
	    }
				
	}else if(phone &&  phone!=""){
		updateSql+=" mobile='"+phone+"'";
		//console.log(updateSql);
		this.db.driver.execQuery(updateSql,function(err,data){
			if(err) console.log(err);
			console.log(updateSql);
		});
		selectSql+=" mobile='"+phone+"'";
		this.db.driver.execQuery(selectSql,function(err,data){
			if(err) console.log(err);
			if(data && data.length>0){
				var curId=data[0].id;
				var insertSql="insert into convoy.crm_customer_track ";
				insertSql+="(customer_id, track_date, track_mode, track_type,";
				insertSql+=	"content, progress,"; 
				insertSql+=	"idCreator, creator, createTime, idUpdator) VALUES ( ";
				insertSql+=""+curId+",'"+"2015-07-29 14:33:11"+"','"+"phone"+"','"+"followUp"+"','"+memo+"',"+"0"+",";
				insertSql+=""+"429"+",'"+"蒋勇"+"','"+"2015-07-29 14:33:11"+"',"+"429"+")";
				
				that.db.driver.execQuery(insertSql,function(err,data){
					if(err) console.log(err);	
					console.log(insertSql);
				});
			}
			
		    	//查询出客户id		
		});
	}
}


function FileHandler(f,dbparam){
	this.file=f;	
	this.pathname="./initCrm/"+f;
	this.db=dbparam;
}
FileHandler.prototype.handle=function(){
	//查询出当前文件名对应的owner_id
	var ownerName =this.file.split("-")[0];
	var that=this;
	this.db.driver.execQuery("SELECT id FROM convoy.sys_permission_employee where name like '%"+ownerName+"%' and disabled=0"
   // var p1="'"+ownerName+"'"
	//this.db.driver.execQuery("SELECT id FROM convoy.sys_permission_employee where name like ? and disabled=0",[p1]
	,function(err,data){
		if(err)
			console.log(err);
		var ownerId=data[0].id;
		console.log(that.pathname);
		var d=fs.readFileSync(that.pathname,"utf-8");
		var lines=d.split("\n");
		//调用行处理器，来处理行数据，更新客户信息和添加一条跟进
		for(var i=1;i<lines.length;i++){
			var line=lines[i];
			var lineHanler=new LineHandler(that.db,line,ownerId);
			lineHanler.handle();
		}
		
		
		
	});
}
//csv.each('./initCrm/7-31董雷雷-所有客户统计表转CRM库.csv').on('data', function(data) {
//	  lines++;
//	  console.log(data[1]);
//	}).on('end', function() {
//	  console.log(lines + ' lines parsed');
//	})
model(function(err,db){
	if(err)
		console.log("fail");
//	db.driver.execQuery(
//			  "SELECT user.??, user.?? FROM user WHERE user.?? LIKE ? AND user.?? > ?",
//			  ['id', 'name', 'name', 'john', 'id', 55],
//			  function (err, data) { ... }
//			)
	fs.readdir("./initCrm", function(err, files){
		files.forEach(function(f){
			var fileHandler=new FileHandler(f,db);
			fileHandler.handle();
		});
	});


});
//var d= fs.readFileSync("./initCrm/7-31李素敏-所有客户统计表转CRM库.csv","utf-8");
//d.split("\n").forEach(function(line){
//	console.log(d);
//});





////	//console.log();
//	
//});
//var d= fs.readFileSync("./clear.txt",'utf-8');
//var carNos= d.split("\n")
//carNos.forEach(function(c){
//	console.log(c);
//});