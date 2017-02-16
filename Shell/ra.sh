#!/bin/bash
#杀死node进程
netstat -tnlup | grep uwsgi | awk '{print $7}' | cut -d '/' -f1 | xargs   kill -9

#启动uwsgi
uwsgi --ini /mnt/s/mygit/habit/back_python/uwsgi.ini
#删除会话文件
/etc/init.d/redis-server stop
#rm -rf /var/lib/redis/dump.rdb
/etc/init.d/redis-server start

# nohup node /yimilan/node/nodeapp/Seed/Platform/WxAppServer/wxApp.js & >/dev/null
# nohup node /yimilan/node/nodeapp/Seed/Platform/UserCenter/uc.js & >/dev/null
# nohup node /yimilan/node/nodeapp/Seed/LittleLeader/leaderApp.js & >/dev/null
