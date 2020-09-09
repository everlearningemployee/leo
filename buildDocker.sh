#!/bin/bash
docker build \
    --no-cache=false \
    --force-rm=true \
    -t leo \
    .
