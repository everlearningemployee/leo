#!/bin/bash
conda activate Leo
nohup python Leo.py &
ps -ef | grep Leo
sleep 3
watch -n 30 tail nohup.out LeoOrder.json order.log

