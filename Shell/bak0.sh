#!/bin/bash
mysqldump -uroot -pviathink@520612 schoolerp | gzip >  /mnt/d/bak/mysql/$(date '+%Y-%m-%d_%H:%M:%S').schoolerpsql.gz
