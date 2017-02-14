module.exports = function (orm, db) {
  var CustomerRemind = db.define('crm_customer_remind',{
	id:{ type: "integer"},
	customerIds:{ type: "text"},
	frequency:{ type: "text"},
	remindDate:{ type: "date", time: false,mapsTo:'remind_date'},
	content:{ type: "text"},
	ownerId:{ type: "integer",mapsTo: 'owner_id'},	
	valid:{ type: "boolean"},
	remindSourceType:{ type: "text"}
  });
  //db.CustomerRemind=m;
};
