import platform
import socket
from subprocess import*
import glob
import re
import os
from collections import OrderedDict

def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo=OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

def cpuinfo():
    cpuinfo=OrderedDict()
    procinfo=OrderedDict()
    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs=nprocs+1
                # Reset
                procinfo=OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''            
    return cpuinfo


dev_pattern = ['sd.*','mmcblk*']

def storageSize(device):
    nr_sectors = open(device+'/size').read().rstrip('\n')
    sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')
    return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)

def printStorageDevices():
    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                print("Storage " + device + " Size: " + str(storageSize(device)))


if __name__ == "__main__":
	Popen("clear")
	uname = platform.uname()
	fqdn = uname[1]
	ipa = socket.gethostname()
	print("System Report for " + fqdn + " (" + ipa + ")")
	time = uname[3][7:]
	print("Generated at " + time)
	uptime = Popen(["uptime"], stdout = PIPE).stdout.read().split(",")[0].split(" ")[4]
	print("Uptime: " + uptime)
	print("System: " + uname[1] + " " + uname[2])
	printStorageDevices()
	cpuinfo = cpuinfo()
	print("CPU: " + cpuinfo[cpuinfo.keys()[0]]["model name"])
	mem = meminfo()
	print("Total Memory: " + mem["MemTotal"])
	print("Free Memory: " + mem["MemFree"])
