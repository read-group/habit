#!/bin/bash
/*
*远程拷贝命令
*/

//先打包压缩，然后把打包压缩的结果上传到远程服务器
export curDir="$(cwd)";
export dirInputName=$1;
export filePath=curDir+$dirInputName;
tar -czvf $dirInputName+".tar.gz" $filePath;
