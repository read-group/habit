var NodeCache = require( "node-cache" );
var myCache = new NodeCache({stdTTL:7});
myCache.set("hello","world");

setTimeout(function(){
  value=myCache.get("hello");
  if(value){
    console.log(value);

  }else{
    console.log("invalid");
  }
},6000);
