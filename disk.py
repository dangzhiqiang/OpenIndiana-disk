#!/usr/bin/python
# Filename: disk.py
# Author: Dang Zhiqiang<c_dddd@163.com>

import re
import getopt
import sys
from subprocess import Popen, PIPE


def __pipeopen(command):
	return Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True, close_fds=True)


def disk_is_free(disk):
	assert disk != ""

	cmd = "zpool create -n tmp_dzq_1s0k %s" % disk
	proc = __pipeopen(cmd)
	proc.wait()
	ret_code = proc.returncode

	return ret_code


def get_zpool_name_list():
	retval = []

	cmd = "zpool list -H -o name"
	proc = __pipeopen(cmd)
	stdout, stderr = proc.communicate()
	ret_code = proc.returncode
	if ret_code != 0:
		print("[ERROR] - get zpool name list error: %s", stderr.split("\n")[0])
		return 1

	retval = stdout.split("\n")
	retval.pop()

	return retval


def get_disk_list():
	disks = []
	zpool_list = []

	cmd = "iostat -xn"
	proc = __pipeopen(cmd)
	stdout, stderr = proc.communicate()
	ret_code = proc.returncode
	if ret_code != 0:
		print("[ERROR] - get disk list error: %s", stderr.split("\n")[0])
		return disks

	zpool_list = get_zpool_name_list()

	for record in stdout.split("\n"):
		found = False

		ret = re.split(" +", record.lstrip())
		if len(ret) < 11:
			continue
		elif ret[0] == "r/s":
			continue

		fake_disk = ret[10]
		if fake_disk in zpool_list:
			found = True

		if found:
			continue
		else:
			disks.append(fake_disk)

	return disks


# return: diskinfo
# 	diskinfo may contain then following keys:
# 	"Soft Errors|Hard Errors|Transport Errors"\
# 	"|Model|Vendor|Product|Revision|Serial No|Size"\
# 	"|Media Error|Device Not Ready|No Device"\
# 	"|Recoverable|Illegal Request"\
# 	"|Predictive Failure Analysis"
def get_disk_info(disk):
	diskinfo = {}

	cmd = "iostat -Er %s" % disk
	proc = __pipeopen(cmd)
	stdout, stderr = proc.communicate()
	ret_code = proc.returncode
	if ret_code != 0:
		print("[ERROR] - get disk \'%s\' info error: %s" %\
		    (disk, stderr.split("\n")[0]))
		return diskinfo
	
	diskinfo_tmp = stdout.replace("\n", ",")
	diskinfo_new = re.split(",+", diskinfo_tmp)

	diskinfo["Alias"] = diskinfo_new[0].strip()

	for record in diskinfo_new[1:]:
		if len(record) == 0:
			continue

		ret = record.split(":")
		diskinfo[ret[0]] = ret[1].strip()

	disk_size = diskinfo.get("Size", "unknow")
	if disk_size != "unknow":
		diskinfo["Size"] = disk_size.split(" ")[0]
	else:
		diskinfo["Size"] = "unknow"

	return diskinfo

	
def disk_list():
	disks = []

	disks = get_disk_list()
	if len(disks) == 0:
		print("[ERROR] - List disk info error")
		return 1

	print("{0:23} {1:7} {2:10} {3:17} {4:16} {5:12} {6:6}".format(\
	    "DEVICE", "ALISA", "VENDOR", "PRODUCT", "SERIALNO", "SIZE", "FREE"))

	for disk in disks:
		disk_free = "no"

		if disk_is_free(disk) == 0:
			disk_free = "yes"

		diskinfo = get_disk_info(disk)
		if len(diskinfo) == 0:
			continue

		print("{0:23} {1:7} {2:10} {3:17} {4:16} {5:12} {6:6}".format(\
		    disk,
		    diskinfo.get("Alias", "unknow"),
		    diskinfo.get("Vendor", "unknow"), 
		    diskinfo.get("Product", "unknow"),
		    diskinfo.get("Serial No", "unknow"), 
		    diskinfo.get("Size", "unknow"),
		    disk_free))

	return 0


def usage(command):
	print '''\
Usage:
	%s                # List disk info
	%s -h or --help   # Show this help info
Note:
	This command will list disk info in current system, include below message:

	DEVICE:
		Display device names in descriptive format. For example: cXtYdZ
	ALISA:
		Device Name
	VENDOR: 
		Vendor Name 
	PRODUCT: 
		Product ID
	SERIALNO: 
		Serial No.
	SIZE: 
		Size of this device
	FREE: 
		Is free or not, value(yes, no)\
''' % (command, command)


if __name__ == '__main__':
	if len(sys.argv) > 2:
		print "Usage ERROR!"
		usage(sys.argv[0])
		exit(1)
	elif len(sys.argv) == 2:
		if sys.argv[1] == "--help" or sys.argv[1] == "-h":
			usage(sys.argv[0])
			exit(0)
		else:
			print "Arguments ERROR!"
			usage(sys.argv[0])
			exit(1)
	else:
		disk_list()

