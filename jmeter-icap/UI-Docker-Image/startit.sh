#!/bin/bash

echo "START on `date`"

image_name="ggrig/ui-k8s-jmeter:0.01"

exec sudo docker run -d --name engine_ui --privileged -ti -e container=docker  -v /sys/fs/cgroup:/sys/fs/cgroup $image_name /usr/sbin/init