#!/bin/bash
LEO=leo
docker rm -f $LEO
docker run -d \
    --name $LEO \
    -v /home/ubuntu/Leo/logs:/var/log/leo \
    -v /home/ubuntu/Leo/myorder:/leo/order \
    leo
docker logs -f $LEO
# sleep 3
watch -n 30 tail /home/ubuntu/Leo/myorder/* /home/ubuntu/Leo/logs/*