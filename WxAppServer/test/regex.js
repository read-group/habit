/**
 * 
 */

 var src = "The rain in Spain falls mainly in the plain.";
 
 //匹配单词字符，默认最大匹配，即贪婪
 var re = /\w+/g;  
 // 匹配单词字符，默认最小匹配，即懒惰，注意问号
 //var re = /\w+?/g; 
 var arr;
 while ((arr = re.exec(src)) != null)
    console.log(arr.index + "-" + arr.lastIndex + "\t" + arr);
 

 
 
/**
 * 编译替换
 * 替换是匹配时的全局替换
 */
 var str="Every man in the world! Every woman on earth!";

 patt=/man/g;
 str2=str.replace(patt,"person");
 console.log(str2);

 patt=/(wo)?man/g;
 patt.compile(patt);
 str2=str.replace(patt,"person");
 console.log(str2);

 /*
  * \{\{(.*?)\}\}
  * */
