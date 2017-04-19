#!/bin/bash
#杀死进程
netstat -tnlup | grep uwsgi | awk '{print $7}' | cut -d '/' -f1 | xargs   kill -9
netstat -tnlup | grep node | awk '{print $7}' | cut -d '/' -f1 | xargs   kill -9
#启动uwsgi
/mnt/s/penv/bin/uwsgi --ini /mnt/s/mygit/habit/back_python/uwsgi.ini &

#启动node
# nohup node /mnt/s/mygit/habit/WxAppServer/wxApp.js & >/dev/null
#删除会话文件
/etc/init.d/redis-server stop
rm -rf /mnt/d/redis-data/dump.rdb
/etc/init.d/redis-server start

# nohup node /yimilan/node/nodeapp/Seed/Platform/WxAppServer/wxApp.js & >/dev/null
# nohup node /yimilan/node/nodeapp/Seed/Platform/UserCenter/uc.js & >/dev/null
# nohup node /yimilan/node/nodeapp/Seed/LittleLeader/leaderApp.js & >/dev/null
