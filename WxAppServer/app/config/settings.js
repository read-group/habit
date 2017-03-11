var path       = require('path');
var settings = {
  basepath       : path.normalize(path.join(__dirname, '../..')),
  user_center_url:"http://localhost:3004/api/user/",
  port       : process.env.NODE_PORT || 9406,
  database   : {
    protocol : "mysql", // or "mysql"
    query    : { pool: true },
    host     : "127.0.0.1",
    database : "convoy",
    user     : "root",
    password : "yMl@123qwe"
  },
  appId:"wx8f428820d2150a9e"

};

module.exports = settings;
