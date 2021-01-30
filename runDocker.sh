#!/bin/bash
LEO=leo
cd /home/ubuntu/leo
# docker-compose down
docker-compose up -d
docker-compose logs -f $LEO
# sleep 3
# watch -n 30 tail /home/ubuntu/leo/myorder/* /home/ubuntu/leo/logs/out.log  /home/ubuntu/leo/logs/order.log /home/ubuntu/leo/logs/trans.log
