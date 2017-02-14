
/*
 * GET home page.
 */
module.exports={
	        h1: function(req, res){
			  res.render('h1', { title: 'Express'});
			},
			h2: function(req, res){
				  res.render('h2', { title: 'Express'});
				},
		     h3: function(req, res){
					  res.render('h3', { title: 'Express'});
			},
		     h4: function(req, res){
				  res.render('h4', { title: 'Express'});
			 },
		     h5: function(req, res){
					  res.render('h5', { title: 'Express'});
			},
			 h6: function(req, res){
						  res.render('h6', { title: 'Express'});
			},
			h7: function(req, res){
				  res.render('h7', { title: 'Express'});
		   },
		   h8: function(req, res){
					  res.render('h8', { title: 'Express'});
		   },
		   h9: function(req, res){
				  res.render('h9', { title: 'Express'});
	       },
		    f1: function(req, res){
			  res.render('f1', { title: 'Express'});
			},
			f2:function(req, res){
				  res.render('f2', { title: '唠叨'});
			},
			register: function(req, res){
				  res.render('register', { title: '唠叨'});
			},
			login: function(req, res){
				  res.render('login', { title: '唠叨'});
			},
			homesettings:function(req, res){
				  res.render('homesettings', { title: '唠叨'});
			},
			settarget:function(req, res){
				  console.log(req.query.catId);
				  console.log(req.query.cataName);
				  res.render('settarget', { cataId: req.query.catId,cataName:req.query.cataName});
			},
		
			cspace:function(req, res){
				  res.render('cspace', {});
			},
			cmy:function(req, res){
				  res.render('cmy', {});
			},
			corder:function(req, res){
				  res.render('corder', {});
			},
			cshop:function(req, res){
				  res.render('cshop', {});
			},
			cadvice:function(req, res){
				  res.render('cadvice', {});
			},
			pspace:function(req, res){
				  res.render('pspace', { target: req.query.catId});
			},
			pmy:function(req, res){
				  res.render('pmy', { target: req.query.catId});
			},
			padvice:function(req, res){
				  res.render('padvice', {});
			},
			pshop:function(req, res){
				  res.render('pshop', {});
			},
			porder:function(req, res){
				  res.render('porder', {});
			},
			pinfo:function(req, res){
				  res.render('pinfo', {});
			},
			caccess:function(req, res){
				  res.render('caccess', {});
			},
			cinfo:function(req, res){
				  res.render('cinfo', {});
			},
            pspace2:function(req, res){
				  res.render('pspace2', { target: req.query.catId});
			},
}
