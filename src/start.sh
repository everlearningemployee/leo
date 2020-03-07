#!/bin/bash
conda activate Leo
nohup python Leo.py &
watch -n 30 tail nohup.out LeoOrder.json order.log

