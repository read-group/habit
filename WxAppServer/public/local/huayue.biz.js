/**
 * 工具对象，单例
 */
(function(window,$){
	$huayue.biz={};
	$huayue.biz.user=$huayue.object.New({
		ctor:function(){
			this.session={};
			this.objectStore="users";
			this.role={
					isAdmin:0,
					isHost:1,
					isChild:2,
					isNotice:3
				
			};
		},
		/**
		 * 登录验证
		 * @param loginInfo
		 * @param callback
		 * @returns
		 */
		login:function(loginInfo,callback){
			var self=this;
			var loginInfo=loginInfo;
			console.log(loginInfo);
			$huayue.db.getByUniqueIndex(self.objectStore,"account",loginInfo.account,function(err,result){
				if(err){
					callback(err,null);
				}else{		
					 if(result && result.pwd==loginInfo.pwd){
			    		 var guid=$huayue.utils.guid();
			    		 self.session[guid]=result;//建立会话,以访问token为key
			    		 result.token=guid;
			    		 var orgId=null;
			    		 if(result.role=="2"){
			    			 orgId=result.orgId;
			    		 }
			    		 if(result.role=="1"){
			    			 orgId=result.id;
			    		 }
			    		 $huayue.db.getByKey(orgId,"orgs",function(err,r){
			    			if(r){
			    				result.org=r;
			    			}else{
			    				result.org=null;
			    			}
			    			callback(null,result);	 
			    		 });
			    		 
			    	 }else{
			    		 callback(new Error('err login'),null);
			    	 }
				}
			});   
		},
		/**
		 * 获取手机验证码
		 */
		getPhoneValidCode:function(num){
			return $huayue.utils.randNum(num);
		},
		/**
		 *注册方法成功后直接建立会话返回
		 */
		register:function(regInfo,callback){
			var self=this;
			console.log("register start...");
			if(regInfo.noticeCode && regInfo.noticeCode.trim()!="")
				regInfo.role=this.role.isNotice;//旁观者
			else{
				regInfo.role=this.role.isHost;//家长
			}
			$huayue.db.add(this.objectStore,regInfo,function(err,result){
				 var guid=$huayue.utils.guid();
				 console.log(result);
	    		 self.session[guid]=result;//建立会话,以访问token为key
	    		 result.token=guid;		 
	    		 console.log("register ok and make session.....");
	    		 callback(null,result);		 
			});
		}
	});
	/**
	 * 家庭组相关
	 */
	$huayue.biz.org=$huayue.object.New({
		ctor:function(){			
		},
		/**
		 * 初始化家庭设置的状态是新增还是更新
		 */
		initHomeSetting:function(orgId,callback){
			$huayue.db.getByKey(orgId,"orgs",function(err,r){
				if(err){
					return callback(err,null);
				}
				if(!r){
					return callback(null,0);//表示新增
				}else{
					//去获取家庭映射表
					$huayue.db.getByIndex("homeIssues","orgId",orgId,function(err,rs){					
						if(err)
							return callback(err,null);
						else
						{//对返回结果进行处理
							var rsdic={};
							$.each(rs,function(i,item){
								var catIdTmp=item.cataId;
								if(!rsdic[catIdTmp]){
									rsdic[catIdTmp]=[];
									rsdic[catIdTmp].push(item);
								}else{
									rsdic[catIdTmp].push(item);
								}
							});
							var rtn={};
							rtn["org"]=r;
							rtn["map"]=rsdic;
						
							return callback(null,rtn);
						}
					});
				}
			});
		},
		/**
		 * 当前登录人访问key,获取当前登录人
		 * nickName
		 * 孩子账户个数childNum
		 * 家长设置的指标数组(每次保存都是先删除后增)
		 */
		homeSetting:function(settingInfo,callback){
			//取出缓存在回话中的,由于调试刷新，所以直接从存储中取了
//			var token=settingInfo.accessToken;
//			var userCurrent=this.session[token];
//			var token=$.localStorage.get("accessKey");
			var user=$.localStorage.get("account");//to do 从会话里取
			//构建家庭组织信息===================
			var org={};
		
			org.id=user.id;//把注册用户的id作为注册家庭的id
			org.nickName=settingInfo.nickName;	
			org.ratioScore=settingInfo.ratioScore;
			org.status=settingInfo.status;
			//构建孩子用户信息===================
			var childNum=settingInfo.accountNum;
			var childAccounts=[];
			
			//构建组织和人员映射表===============
			var orgUsers=[];
			//把当前注册用户也加入到家庭组中,只要不是更新状态
			if(settingInfo.status!="update"){
				var currentOrgUser={};
				currentOrgUser.id=$huayue.utils.guid();
				currentOrgUser.OrgId=org.id;
				currentOrgUser.orgName=org.nickName;
				currentOrgUser.userId=user.id;
				currentOrgUser.status="new";
				//currentOrgUser.userName=user.name;以后自己设置
				orgUsers.push(currentOrgUser);
			}
			
			
			//构建家长与孩子朋友表===============
			var friends=[];
			
			//构建家庭指标表
			var homeIssures=[];
			var issues=settingInfo.issues;
			$.each(issues,function(i,issue){
				var homeIssure={};
				if(issue.status=="new")
				    homeIssure.id=$huayue.utils.guid();
				else
				    homeIssure.id=issue.orgIssureId;//在加载到客户端时绑定的
				homeIssure.orgId=org.id;
				homeIssure.cataId=issue.cataId;
				homeIssure.cataName=issue.cataName;
				homeIssure.issureId=issue.id;
				homeIssure.issureName=issue.name;		
				homeIssure.score=issue.score;	
				homeIssure.status=issue.status;
				homeIssures.push(homeIssure);
			});
			 console.log(homeIssures);
			var code=1;
			if(settingInfo.status=="update"){//如果是更新从家庭取出当前序号
				code=settingInfo.seq;
			}
			
			for(var i=0;i<childNum;i++){
				
				var childTmp={};
				var orgUser={};
				var friend={};
				childTmp.id=$huayue.utils.guid();
				//孩子的账号是注册者的手机号后顺序排号
				childTmp.account=user.account+""+(code);
				childTmp.pwd=user.account;//密码是注册者的手机号
				childTmp.role=$huayue.biz.user.role.isChild;
				childTmp.orgId=org.id;//孩子冗余的组织id默认是家庭的id,也就是家长的id
				childTmp.status="new";
				code++;
				childAccounts.push(childTmp);
				
				//记录当前孩子的序号,保存到家庭中
				org.currentChildSeq=code;
				
				orgUser.id=$huayue.utils.guid();
				orgUser.orgId=org.id;
				orgUser.orgName=org.nickName;
				orgUser.userId=childTmp.id;
				//orgUser.userName=childTmp.id;//以后自己设置
				orgUser.status="new";
				orgUsers.push(orgUser);
				
				friend.id=$huayue.utils.guid();
				friend.fromId=user.id;//当前回话用户
				//friend.fromName=
				friend.toId=childTmp.id;
				//friend.toName=
				friend.isPass=1;//表示通过同意
				friend.status="new";
				friends.push(friend);		
			}	
			//新增孩子用户、建立家庭组、建立家庭组和孩子的映射、建立朋友、建立家庭和指标的映射
			var orgInfo=null;
			var transPromise=$huayue.db.getTransPromise(["users","orgs","orgUsers","friends","homeIssues"]);
			 transPromise.progress(function(tran){//事务完成事件
					//开始传递事务对象给db,依次执行
				    //建立家庭组
				   console.log("建立或更新家庭组开始......");
				   $huayue.db.saveWithTran(tran,"orgs",[org],function(err,r){
					    if(!err){
					        console.log("建立或更新家庭组成功");
//					        alert(user);
					        orgInfo=org;//设置到客户端的缓存中，便于登录时判断是否设置过
					    }	 
					    else
					    	 console.log("建立或更新家庭组失败.....");
				   });
				   
				  /* $huayue.db.addWithTran(tran,"orgs",org,function(err,r){
					   
					   if(!err)
						     console.log("建立或更新家庭组成功.....");	
				      else
							  console.log("建立或更新家庭组失败.....");	
					  
				   });*/
				   //增加孩子用户
				   console.log("建立孩子账户开始.....");
//				   $.each(childAccounts,function(i,c){
//					   $huayue.db.addWithTran(tran,"users",c,function(err,r){
//						   if(!err)
//						     console.log("建立孩子账户成功.....");	
//						   else
//							  console.log("建立孩子账户失败.....");	
//					   });
//				   });
				   console.log(childAccounts[0]);
				   $huayue.db.saveWithTran(tran,"users",childAccounts,function(err,r){
					    if(!err)
					       console.log("建立孩子账户成功.....");
					    else
					    	 console.log("建立孩子账户失败....");
				   });
				   //建立组织人员映射表
				   console.log("组织人员映射表...");
//				   $.each(orgUsers,function(i,c){
//					   $huayue.db.addWithTran(tran,"orgUsers",c,function(err,r){
//						   if(!err)
//						       console.log("建立或更新组织人员映射成功......");		
//						   else
//							   console.log("建立或更新组织人员映射fail......");		
//					   });
//				   });
				   $huayue.db.saveWithTran(tran,"orgUsers",orgUsers,function(err,r){
					    if(!err)
					       console.log("建立或更新组织人员映射成功.....");
					    else
					    	 console.log("建立或更新组织人员映射fail......");
				   });
				   //建立朋友表
				   console.log("朋友表...");
//				   $.each(friends,function(i,c){
//					   $huayue.db.addWithTran(tran,"friends",c,function(err,r){
//						   if(!err)
//						       console.log("建立朋友表成功.....");
//						   else
//							   console.log("建立朋友表fail.....");
//					   });
//				   });
				   $huayue.db.saveWithTran(tran,"friends",friends,function(err,r){
					    if(!err)
					       console.log("建立朋友表成功......");
					    else
					    	 console.log("建立朋友表fail......");
				   });
				   //建立家庭指标表,更新更合适
				   console.log("家庭指标表...开始更新....");
				   console.log(homeIssures);
				   console.log(".....................................");
				   $huayue.db.saveWithTran(tran,"homeIssues",homeIssures,function(err,r){
					    if(!err)
					       console.log("建立或更新家庭指标表成功.....");
					    else
					    	 console.log("建立或更新家庭指标表fail.....");
				   });
//				   $.each(homeIssures,function(i,c){
//					   $huayue.db.addWithTran(tran,"homeIssues",c,function(err,r){
//						   console.log(r);					  
//					   });
//				   });
			});
			transPromise.done(function(event){//事务完成事件
				 callback(null,orgInfo);
				console.log("trans complete..............");
			});
            transPromise.fail(function(event){//事务完成事件
				 console.log("trans fail.........................");
				 console.log(event);
				 callback(event,null);
			});
			
		}
	});
	$huayue.biz.catalog=$huayue.object.New({
		ctor:function(){
			
		},
		/**
		 * 查询出所有的类别
		 */
		getCatalogs:function(callback){
			$huayue.db.getAll("catalogs",function(err,results){
				if(err){
					return callback(err,null);
				}else{
					return callback(null,results);
				}
			})
		},
		getIssues:function(callback){
			$huayue.db.getAll("issues",function(err,results){
				if(err){
					return callback(err,null);
				}else{
					return callback(null,results);
				}
			})
		},
		getIssuesByIndex:function(catId,callback){
			$huayue.db.getByIndex("issues","cataId",catId,function(err,results){
				if(err){
					return callback(err,null);
				}else{
					return callback(null,results);
				}
			});
		}
	});
	/**
	 * 家长空间
	 */
	$huayue.biz.growEnsure=$huayue.object.New({
		ctor:function(){
			//操作类型
			this.opType={
					Fill:"pfill",//充值
                    FBack:'feedback',//反馈
                    Cost:'cost'//消费
			};
			this.growAccount={
					todayFetchScore:70,
					todayFetch:70,
					cumuFill:800,
					cumuChildFetch:430,
					leftBalance:370,
					childDic:{
						
					}
			}
		},
		/**
		 * 初始化家长成长宝页面
		 * 需要准备金额数据
		 * 返回孩子
		 */
		initPSpaceGrowEnsure:function(orgId,callback){
			//获取成长宝的初始金额，填充结构
			 this.getGrowEnsureSumData(orgId,function(err,ra){
        	     if(err)
        	    	 return callback(err,null);
        	     else{
        	    	 //获取孩子的账户
        	    	 
        	    	 return callback(null,ra);
        	     }
        	    	 
	       });
		},
		/**
		 * 初始化孩子成长宝页面
		 * 返回家庭指标列表和个人成长宝数据
		 */
		initCSpaceGrowEnsure:function(orgId,childId,callback){
			var rtn={};
			var self=this;
			//先获取家庭指标列表
			$huayue.db.getByIndex("homeIssues","orgId",orgId,function(err,rs){
				if(err){
					return callback(err,null);		
				}else{
					//设置返回的家庭指标
					rtn.issues=rs;
					//按照child去获取孩子的数据，这里直接返回整个家庭的数据，方便客户端直接查看兄弟和家长数据
					self.getGrowEnsureSumData(orgId,function(err,growAccount){
						if(err){
							return callback(err,null);	
						}
						rtn.ga=growAccount;
						callback(null,rtn);
					});			
				}
			});
		},
		/**
		 * 孩子反馈方法
		 */
		feedBack:function(feedInfo,callback){
			var self=this;
			var entityFeedInfo={};
			$huayue.utils.deepCopy(entityFeedInfo,feedInfo);
			entityFeedInfo.opDate=new Date().toLocaleDateString();
			entityFeedInfo.id=$huayue.utils.guid();
			entityFeedInfo.opType=this.opType.FBack;//服务层设置
			$huayue.db.getByIndex("growEnsure","opDate",entityFeedInfo.opDate,function(err,rs){
				if(err){
					return callback(err,null);
				}else{
					console.log("===========================");
					
					if(rs && rs.length>0){
						var isValid=true;
						$.each(rs,function(i,r){
							//获取当前用户id
							var $todoTmpUsr=$.localStorage.get("account");
							if(r.issueId==entityFeedInfo.issueId && r.userId==$todoTmpUsr.id){
								isValid=false;
								return false;
							}
						});
						if(!isValid)
						     return callback("每日只能反馈一次.",null);
					}
					
					$huayue.db.add("growEnsure",entityFeedInfo,function(err,r){
							if(err){
								return callback(err,null);
							}else{
								   //获取反馈后的统计结果
			                       self.getGrowEnsureSumData(r.orgId,function(err,ra){
			                    	     if(err)
			                    	    	 return callback(err,null);
			                    	     else
			                    	    	 return callback(null,ra);
							       });
							}
						});
					
				}
			});
			
			
		},
		
		fillAmount:function(fillInfo,callback){
			var self=this;
			var entityFillInfo={};
			$huayue.utils.deepCopy(entityFillInfo,fillInfo);
			entityFillInfo.opDate=new Date().toLocaleDateString();
			entityFillInfo.id=$huayue.utils.guid();
			console.log(entityFillInfo);
			$huayue.db.add("growEnsure",entityFillInfo,function(err,r){
				if(err){
					callback(err,null);
				}else{
					   //获取充值后的统计结果
                       self.getGrowEnsureSumData(r.orgId,function(err,ra){
                    	     if(err)
                    	    	 callback(err,null);
                    	     else
                    	    	 callback(null,ra);
				       });
				}
			});
		},
		
		cost:function(fillInfo,callback){
			var self=this;
			var entityCostInfo={};
			$huayue.utils.deepCopy(entityCostInfo,fillInfo);
			entityCostInfo.opDate=new Date().toLocaleDateString();
			entityCostInfo.id=$huayue.utils.guid();
			console.log(entityCostInfo);
			$huayue.db.add("growEnsure",entityCostInfo,function(err,r){
				if(err){
					callback(err,null);
				}else{
					   //获取充值后的统计结果
                       self.getGrowEnsureSumData(r.orgId,function(err,ra){
                    	     if(err)
                    	    	 callback(err,null);
                    	     else
                    	    	 callback(null,ra);
				       });
				}
			});
		},
		
		/**
		 * 家庭成长宝的数据统计
		 */
		getTotalData:function(rs){
			var self=this;
			this.growAccount.cumuFill=0;//累积充值
			this.growAccount.todayFetchScore=0;//今日得分
			this.growAccount.todayFetch=0;//今日赢取金额
			this.growAccount.cumuChildFetch=0;//累积孩子孩子赢取
			this.growAccount.leftBalance=0;//成长宝剩余余额
			var todayStr=new Date().toLocaleDateString();
	        var childDic={};
			$.each(rs,function(i,item){			
				if(item.opType==self.opType.Fill){//如果是充值
					self.growAccount.cumuFill+=Number(item.amount);
				}
				if(item.opType==self.opType.FBack){//如果是反馈
					if(!childDic[item.userId]){
						childDic[item.userId]={
								id:item.userId,
								account:item.account,
								todayFetch:0,
								todayFetchScore:0,
								cumuFetch:0,
								cumuCost:0,
								leftBalance:0,
								issureIds:[]
						};
					}
					if(item.opDate==todayStr ){
						self.growAccount.todayFetchScore+=item.score?Number(item.score):0;
						self.growAccount.todayFetch+=item.amount?Number(item.amount):0;
						childDic[item.userId]["todayFetchScore"]+=item.score?Number(item.score):0;
						childDic[item.userId]["todayFetch"]+=item.amount?Number(item.amount):0;	
						if(item.issueId)
						    childDic[item.userId]["issureIds"].push(item.issueId);//为了更新界面的今日反馈状态
					}
					self.growAccount.cumuChildFetch+=item.amount?Number(item.amount):0;
					childDic[item.userId]["cumuFetch"]+=item.amount?Number(item.amount):0;
				}
				if(item.opType==self.opType.Cost){//如果是消费
					if(!childDic[item.userId]){
						childDic[item.userId]={
								id:item.userId,
								account:item.account,
								todayFetch:0,
								todayFetchScore:0,
								cumuFetch:0,
								cumuCost:0,
								leftBalance:0,
								issureIds:[]
						};
					}
					childDic[item.userId]["cumuCost"]+=item.amount?Number(item.amount):0;
				}
			});
			this.growAccount.leftBalance=this.growAccount.cumuFill-this.growAccount.cumuChildFetch;
		    for(var k in childDic){
		    	var child=childDic[k];
		    	child.leftBalance=child.cumuFetch-child.cumuCost;
		    }
		    this.growAccount.childDic=childDic;
			return this.growAccount;
		}
		,
		/**
		 * 获取成长保的统计数据
		 */
		getGrowEnsureSumData:function(orgId,callback){
			var self=this;
			//求家庭累积充值,按照家庭查询出结果集合
			$huayue.db.getByIndex("growEnsure","orgId",orgId,function(err,rs){
				if(err){
					return callback(err,null);
				}else{
					//求出总投入
					var  growAccount= self.getTotalData(rs);		
					
					//查询出所有孩子,遍历每个孩子如果不在成长保里，就初始化一个值到成长保返回值
					$huayue.db.getByIndex("users","orgId",orgId,function(err,us){
						if(err){
							return callback(err,null);
						}else{
							$.each(us,function(i,u){
								if(u.role=="2"){//如果是孩子
									if(!growAccount.childDic[u.id]){//如果不存在，赋予一个初始值
										growAccount.childDic[u.id]={
												id:u.id,
												account:u.account,
												todayFetch:0,
												todayFetchScore:0,
												cumuFetch:0,
												cumuCost:0,
												leftBalance:0
										};
									}
									
								}
							});
							console.log(growAccount);
							return callback(null,growAccount);		
						}
					});

				}
			});
			
		}
	});
})(window,$);
var user=  $.localStorage.get("account");
//console.log(user.id);
$huayue.biz.org.initHomeSetting("3937e69b-8dd7-4a24-9ac3-d8d467f616ca",function(err,r){
	console.log(r);
});
