#!/bin/bash

if grep -qs '/home/ubuntu/backups ' /proc/mounts; then
	echo ""
else sudo mount /dev/vdb /home/ubuntu/backups
fi
