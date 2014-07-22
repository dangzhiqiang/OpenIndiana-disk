#!/usr/bin/bash
#
# Author: Dang Zhiqiang<c_dddd@163.com>
# Note: install disk command

chmod a+x disk.py
cp disk.py /usr/bin/disk

if [ -f /usr/bin/disk ]; then
	echo "Install disk command success"
else
	echo "Install disk command failed"
fi
