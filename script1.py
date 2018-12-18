from subprocess import *

def pingTest(server):
	response = Popen(["ping", server, "-c", "3"], stdout=PIPE).stdout.read()
	for line in response.split("\n"):
		if line[0:3] == "3 p":
			if line[23] != "0":
				return True
	return False
					
def findDNSServers():
	conf = open("/etc/resolv.conf", "r")
	rejectLine = False
	servers = []
	for line in conf:
		if line[0:10] == "nameserver":
			servers.append(line.split()[1])
	return servers

def pingDNSServers():
	servers = findDNSServers()
	pingables = []
	for server in servers:
		if pingTest(server):
			pingables.append(server)
	return server

def findGateway():
	response = Popen(["ip", "route"], stdout=PIPE).stdout.read()
	firstLine = response.split("\n")[0]
	if (firstLine[0:11] == "default via"):
		return firstLine.split()[2]
	return False

def pingGateway():
	server = findGateway()
	if (server):
		return pingTest(server)
	return False

def pingRemote():
	return pingTest("8.8.8.8")

if __name__ == "__main__":
	Popen("clear")
	print("The test has begun.")
	print("Default Gateway: " + findGateway());
	result = "Success" if pingGateway() else "Failure"
	print("Gateway Connection: " + result)
	result = "Success" if pingRemote() else "Failure"
	print("Remote Connection: " + result)
	result = "Success" if pingDNSServers() else "Failure"
	print("Name Resolution: " + result)
	print("The test has finished.")
