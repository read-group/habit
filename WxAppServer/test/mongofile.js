var mongoose = require('mongoose');
var Schema = mongoose.Schema;
mongoose.connect('mongodb://127.0.0.1/test');
var conn = mongoose.connection;
 
var fs = require('fs');
 
var Grid = require('gridfs-stream');
Grid.mongo = mongoose.mongo;
 
conn.once('open', function () {
    console.log('open');
    var gfs = Grid(conn.db);
 
    // streaming to gridfs
    //filename to store in mongodb
    var writestream = gfs.createWriteStream({
        filename: 'mongo_file.txt'
    });
    fs.createReadStream('clear.txt').pipe(writestream);
 
    writestream.on('close', function (file) {
        // do something with `file`
        console.log(file.filename + 'Written To DB');
    });
    
  //write content to file system
    var fs_write_stream = fs.createWriteStream('write.txt');
     
    //read from mongodb
    var readstream = gfs.createReadStream({
         filename: 'mongo_file.txt'
    });
    readstream.pipe(fs_write_stream);
    fs_write_stream.on('close', function () {
         console.log('file has been written fully!');
    });
    
    
});