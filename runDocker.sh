#!/bin/bash
LEO=leo
docker rm -f $LEO
docker run -d \
    --rm \
    --name $LEO \
    -v /home/ubuntu/leo/logs:/var/log/leo \
    -v /home/ubuntu/leo/myorder:/leo/order \
    leo
docker logs -f $LEO
# sleep 3
# watch -n 30 tail /home/ubuntu/leo/myorder/* /home/ubuntu/leo/logs/out.log  /home/ubuntu/leo/logs/order.log /home/ubuntu/leo/logs/trans.log
