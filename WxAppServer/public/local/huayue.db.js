/**
 * 工具对象，单例
 */
(function(window,$){
	$huayue.db=$huayue.object.New({
		ctor:function(){	
			this.status={
					New:"new",
					Del:"del",
					Update:"update",
					Origin:"origin"
			};
			var self=this;
			this.initData={
					users:[//冗余orgid,isChild/isHost/isNoticer/isAdmin
					          {"id":$huayue.utils.guid(),"account":"13300000000",pwd:"13381139519",nickName:"frank",role:0},
					      ],
					catalogs:[
					         {"name":"健康","items":[
					                               {name:"你今天慢跑了吗?",score:1},
					                               {name:"你今天跳绳了吗?",score:1},
					                               {name:"你今天做俯卧冲了吗?",score:1},
					                               {name:"你今天仰卧起坐了吗?",score:1},
					                               {name:"你今天还做了什么运动?",score:1},
					                             ]},
					         {"name":"阅读","items":[
					                               {name:"你今天读书了吗,有什么感想啊?",score:1},
					                               {name:"你有读书计划,并每天坚持吗?",score:1},
					                           ]},
					         {"name":"诚信","items":[
					                               {name:"你曾经答应别人在今天完成的事,兑现诺言了吗?",score:1},
					                               {name:"你今天跟爸妈说出自己真实的想法了吗?",score:1},
					                               ]},
					         {"name":"生活","items":[
					                               {name:"明天上学前的准备,现在准备好了吗?",score:1},
					                               {name:"你今天承担家里的家务了吗?",score:1},
					                               {name:"你今天保持课桌的洁净了吗?",score:1},
					                               ]},
					         {"name":"分享","items":[
					                               {name:"你今天跟同学分享过什么吗?",score:1},                          
					                               ]},
					         {"name":"宽容","items":[
					                               {name:"你能说出你不喜欢的伙伴的几个优点吗?",score:1},
					                               {name:"今天和别人闹矛盾了,你主动和好吗?",score:1},
					                               ]},
					        
					         {"name":"责任","items":[
					                               {name:"你今天把在路上产生的垃圾都送到垃圾箱了吗?",score:1},
					                               ]},
					         {"name":"感恩","items":[
					                               {name:"你今天帮助了曾经帮过你的伙伴吗?",score:1},
					                               {name:"你今天有提醒爸爸不要再抽烟了吗?",score:1},               
					                               ]},
					          {"name":"坚持","items":[
					  					                               {name:"你今天坚持反馈了吗?",score:1},
					  					                               ]},
					   
					         ]
			};
			this.dbName="little_leader";
	//		为了研发,先删除数据库,初始化数据库	
//			this.deleteDatabase(this.dbName).done(function(undefind,evt){
//				console.log("del ok....");
//				self.getDbPromise();
//			});
		},
		getDbPromise:function(){
			var self=this;
			var dbPromise=$.indexedDB(this.dbName, { 
			    // The second parameter is optional
			    "version" : 3,  // Integer version that the DB should be opened with
			    "upgrade" : function(transaction){
			        // Function called when DB is of lower version that specified in the version parameter
			        // See transaction for details on the argument
			    	var ip=transaction.objectStore("users").index("account").each(function(item){
			    		// console.log(item.value);
			    		 //return false;
			    	});
			    	transaction.objectStore("catalogs").index("name").each(function(item){
			    		 console.log(item.value);
			    		 //return false;
			    	});
			    	transaction.objectStore("issues").index("name").each(function(item){
			    		 console.log(item.value);
			    		 //return false;
			    	});
			    	self.getAll("catalogs",function(err,results){
			    		  console.log(results);
			    	});
			    	console.log("upgrade.....")
			    },
			    "schema" : {
			        "2" : function(transaction){
			            // Examples of using the transaction object
			        	console.log("2 schema defind...")
			        	/**
			        	 * =================用户预制数据
			        	 * 用户关键字段
			        	 * isAdmin 预先设置
			        	 * isChild 家长生成用户时,设置这个字段
			        	 * isHost:注册用户在家庭设置页面确认生成后,设置这个字段值为1
			        	 */
			            var userStore = transaction.createObjectStore("users",{
			            	"autoIncrement":false,
			            	"keyPath":"id"
			            });
			            userStore.createIndex("nickName",{unique:false});
			            userStore.createIndex("orgId",{unique:false,multiEntry:true});
			            userStore.createIndex("account",{unique:true,multiEntry:true});
			            $.each(self.initData.users,function(i,item){
			            	userStore.add(item);
			            });
			            /**
			             * =============================维度指标项预制数据
			             */		        
			            var catalogStore=transaction.createObjectStore("catalogs",{
			            	"autoIncrement":false,
			            	"keyPath":"id"
			            });
			            catalogStore.createIndex("name",{unique:true,multiEntry:true});
			            
			            var issueStore=transaction.createObjectStore("issues",{
			            	"autoIncrement":false,
			            	"keyPath":"id"
			            });
			            issueStore.createIndex("name",{unique:true,multiEntry:true});
			            issueStore.createIndex("cataId",{unique:false,multiEntry:false});
			            
			            $.each(self.initData.catalogs,function(i,cata){
			            	var newCata={};
			            	var cataId=$huayue.utils.guid();
			            	newCata.id=cataId;
		            	    newCata.name=cata.name;
			                catalogStore.add(newCata);
			            	$.each(cata.items,function(index,it){
			            		var issue={};
			            		var  issueId=$huayue.utils.guid();
			            		issue.id=issueId;
			            		issue.name=it.name;
			            		issue.cataId=cataId;
			            		issue.cataName=newCata.name;
			            		issue.score=it.score;
			            		issueStore.add(issue);
			            	});	            	
		               });            
			 
			        },
			        "3":function(transaction){
			        	console.log("...3")
			            /**
				            * 设置家庭组织org/群组=============org(id,nickName)
				            * ------组织id(设置人员id),-----昵称
				            * 
				            * 家庭组织人员映射表============== orgUsers(id,orgId,orgName,userId,userName)
				            * 
				            * 设置朋友表======================friends(id,fromId,fromName,toId,toName,isPass)
				            * 
				            * 
				            * 设置家庭组织指标=================homeIssues(id,orgId,catId,catName,issueId,issueName)
				            * ------id,家庭id,维度id,维度名字,指标id,指标名字
				            */
				            
				            /**
				             * 设置家庭组织org/群组=============org(id,nickName,ratioScore)
				             */
				            var orgStore=transaction.createObjectStore("orgs",{
				            	"keyPath":"id",
				            	"autoIncrement":false
				            });
				            orgStore.createIndex("nickName",{unique:true,multiEntry:true});
				            /**
				             * 家庭组织人员映射，按照组织id建立索引
				             */
				            var orgUserStore=transaction.createObjectStore("orgUsers",{
				            	"autoIncrement":false,
				            	"keyPath":"id"
				            });
				            orgUserStore.createIndex("orgId",{unique:false,multiEntry:true});
				            
				            /**
				             * 设置朋友表
				             */
				            var friendStore=transaction.createObjectStore("friends",{
				            	"autoIncrement":false,
				            	"keyPath":"id"
				            });
				            friendStore.createIndex("fromId",{unique:false,multiEntry:true});
				            friendStore.createIndex("toId",{unique:false,multiEntry:true});
				            
				            /**
				             * 设置家庭指标表
				             */
				            var homeIssueStore=transaction.createObjectStore("homeIssues",{
				            	"autoIncrement":false,
				            	"keyPath":"id"
				            });
				            homeIssueStore.createIndex("orgId",{unique:false,multiEntry:true});		            
				            /**
				             * 设置成长宝的账表
				             *  var itemData={
				            		id:null,
				            		orgId:null,
				            		userId:null,
				            		account:null,
				            		opDate:null,
				            		opType:null,	            	
				            		ratioScore:null,
				            		issueId,
				            		score,    		
				            		amount:null,
				            }
				             **/
				            var growEnsureStore=transaction.createObjectStore("growEnsure",{
				            	"autoIncrement":false,
				            	"keyPath":"id"
				            });
				            growEnsureStore.createIndex("opDate",{unique:false,multiEntry:true});
				            growEnsureStore.createIndex("orgId",{unique:false,multiEntry:true});	
				            growEnsureStore.createIndex("userId",{unique:false,multiEntry:true});	
				            growEnsureStore.createIndex("opType",{unique:false,multiEntry:true});	
				            /**
				             * 设置成长宝的内容
				             * {
				             *    id:null,
				             *    growEnsureId:null,
				             *    mime:null
				             *    data:null
				             * }
				             */
				            var growEnsureDataStore=transaction.createObjectStore("growEnsureData",{
				            	"autoIncrement":false,
				            	"keyPath":"id"
				            });
				            growEnsureDataStore.createIndex("growEnsureId",{unique:false,multiEntry:true});	
			        }
			        
			    }
			});
			dbPromise.fail(function(err,evt){
				 console.log("db fail handler.....")
			});
//			dbPromise.done(function(undefind,evt){
//				 console.log("db sucess open ok.....")
//			});
//			dbPromise.progress(function(db,evt){
//				 console.log("db  open in process.....")
//			});
			return dbPromise;
		},
		deleteDatabase:function(dbName){
		  var delePromise=	this.getDbPromise(dbName).deleteDatabase();
		  delePromise.fail(function(error, event){ 
			    /* Called when the delete is successful*/
			    error; // Reason for the error
			    console.log("del fail...."+error);
			});
		  delePromise.progress(function(db, event){ 
			    // Called when the deleting is blocked due to another transaction
			    db; // Database that is opened
			    event.type;// Indicates it is blocked, etc. 
			    console.log("delete in process.....")
			});
		  return delePromise;
		},
		/**
		 * 按照主键查询
		 */
		get:function(key,objectStoreName){
		  return	this.getDbPromise().objectStore(objectStoreName).get(key);
		},
		getByKey:function(key,objectStoreName,callback){
			var p=this.getDbPromise().objectStore(objectStoreName).get(key);
			p.done(function(result, event){
			     return callback(null,result);
			});
			p.fail(function(err,evt){
				  return callback(err,null);
			});
			
		},
		/*
		 * 按照唯一索引的指定值查询
		 */
		getByUniqueIndex:function(objectStoreName,indexName,indexValue,callback){
			var queryResult=null;
			var eachPromise=this.getDbPromise().objectStore(objectStoreName).index(indexName).each(function(item){
				if(item.value[indexName]==indexValue){
					queryResult=item.value;
					return false;
				}
			});
			eachPromise.done(function(result,evt){
					return callback(null,queryResult);
			});
			eachPromise.fail(function(err,evt){
				  return callback(err,null);
			});
		},
		/**
		 * 按照索引获取结果集
		 */
		getByIndex:function(objectStoreName,indexName,indexValue,callback){
			var queryResult=[];
			var eachPromise=this.getDbPromise().objectStore(objectStoreName).index(indexName).each(function(item){
				if(item.value[indexName]==indexValue){
					queryResult.push(item.value);	
				}else{
					return
				}
			});
			eachPromise.done(function(result,evt){
					return callback(null,queryResult);
			});
			eachPromise.fail(function(err,evt){
				  return callback(err,null);
			});
			
		},
		/**
		 * 获得指定表所有的记录
		 */
		getAll:function(objectStoreName,callback){
			var queryResult=[];
			var eachPromise=this.getDbPromise().objectStore(objectStoreName).each(function(item){
				 queryResult.push(item.value);
			});
			eachPromise.done(function(result,evt){
					return callback(null,queryResult);
			});
			eachPromise.fail(function(err,evt){
				  return callback(err,null);
			});
			
		},
		/**
		 * 新增记录
		 */
		add:function(objectStoreName,valueObj,callback){
			var obs=this.getDbPromise().objectStore(objectStoreName);
			valueObj["id"]=$huayue.utils.guid();//设置用户主键
			
			var obsPromise=obs.add(valueObj);
			obsPromise.done(function(r,evt){
				console.log("add obj ok....");
				return callback(null,valueObj);
			});
			obsPromise.fail(function(err,evt){
				console.log("add obj fail....")
				console.log(evt)
				return callback(err,null);
			});
		},
		getTransPromise:function(transcope){
			return this.getDbPromise().transaction(transcope,"readwrite");
		},
		addWithTran:function(tran,objectStoreName,valueObj,callback){
			var obs=tran.objectStore(objectStoreName);
			var obsPromise=obs.add(valueObj);
			obsPromise.done(function(r,evt){
				console.log("add obj ok....");
				return callback(null,valueObj);
			});
			obsPromise.fail(function(err,evt){
				console.log("add obj fail....")
				return callback(err,null);
			});
		},
		/**
		 * 更新记录
		 * @param tran
		 * @param objectStoreName
		 * @param valueObj
		 * @param callback
		 * @returns
		 */
		updateWithTran:function(tran,objectStoreName,valueObj,callback){
			var obs=tran.objectStore(objectStoreName);
			//先获取
			var getpromise= obs.get(valueObj.id);
			getpromise.done(function(r,evt){
				//对象浅拷贝
				$huayue.utils.deepCopy(r,valueObj)
				var obsPromise=obs.put(r);
				obsPromise.done(function(r,evt){
					console.log("update obj ok....");
					return callback(null,r);
				});
				obsPromise.fail(function(err,evt){
					console.log("update obj fail....")
					return callback(err,null);
				});
			});
			
		},
		
		/**
		 * 删除记录
		 */
		deleteWithTran:function(tran,objectStoreName,valueObj,callback){
			var obs=tran.objectStore(objectStoreName);
			var obsPromise = obs.delete(valueObj.id);
			obsPromise.done(function(r,evt){
				console.log("del obj ok....");
				return callback(null,valueObj);
			});
			obsPromise.fail(function(err,evt){
				console.log("del obj fail....")
				return callback(err,null);
			});
		},
		saveWithTran:function(tran,objectStoreName,valueObjs,callback){
			var self=this;
		    
			var loopX=function(valueObjs){
				var popObj=valueObjs.pop();
				if(popObj!=null){
					 if(popObj.status==self.status.Del){//如果是删除
					   	 self.deleteWithTran(tran,objectStoreName,popObj,function(err,r){
					   		 if(err){
					   			return callback(err,null);
					   		 }else{
					   			 return loopX(valueObjs);
					   		 }
					   	 });
					   	 
					 }
					 if(popObj.status==self.status.New){//如果是新增
						 popObj.status=self.status.Origin;
						 self.addWithTran(tran,objectStoreName,popObj,function(err,r){
							 if(err){
								 return callback(err,null);
							 }else{
								 return loopX(valueObjs);
							 }
						 });
					 }
					 if(popObj.status==self.status.Update){
						 console.log("update....");
						 console.log(popObj);
						 popObj.status=self.status.Origin;
						
						 self.updateWithTran(tran,objectStoreName,popObj,function(err,r){
							 if(err){
								 return callback(err,null);
							 }else{
								 return loopX(valueObjs);
							 }
						 });
					 }
				}else{
					return  callback(null,null);
				}	 
			};
			loopX(valueObjs);		
		}	
	});
})(window,$);
//$huayue.db.getAll("homeIssues",function(err,rs){
//	console.log(rs);
//});
//$huayue.db.getAll("growEnsure",function(err,rs){
//	console.log(rs);
//});
//$huayue.db.getAll("users",function(err,rs){
//	console.log(rs);
//});
