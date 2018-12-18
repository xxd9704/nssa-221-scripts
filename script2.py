import pwd, grp
from subprocess import *
import re

def getGroupNames(groups):
	return [group.gr_name for group in groups]

def getExistingGroups():
	return grp.getgrall()

def getGroupID(groupname):
	try:
		group = grp.getgrnam(groupname)
		return group.gr_gid
	except KeyError, e:
		response = Popen(["groupadd", groupname], stdout = PIPE).stdout.read()
		return grp.getgrnam(groupname).gr_gid

def makeUsername(firstname, lastname):
	if len(firstname) < 1:
		temp = lastname
	elif len(lastname) < 1:
		temp = firstname
	else:
		temp = firstname[0] + lastname
	temp = temp.lower()
	while True:
		try:
			pwd.getpwnam(temp)
			appendable = not (temp[-1].isdigit)
			if appendable:
				idx = int(re.search(r'\d+', temp).group())
				temp = temp[0:-len(str(idx))] + str(idx + 1)
			else:
				temp = temp + str(1)
		except KeyError, e:
			break
	return temp

def addUser(firstname, lastname, department, groupname):
	username = makeUsername(firstname, lastname)
	gid = getGroupID(groupname)
	shell = "/bin/bash"
	directory = "/home/" + department + "/" + username
	comment = firstname + lastname
	response = Popen(["useradd", "-m", "-d", directory, "-s", shell, "-g", str(gid), "-c", comment, username], stdout=PIPE).stdout.read()
	print(response)

if __name__ == "__main__":
	Popen("clear")
	accounts = open("Lab02_Users.csv")
	firstLine = True
	for line in accounts:
		if not firstLine:
			entry = line.split(",")
			lastname = entry[1]
			firstname = entry[2]
			department = entry[5]
			group = entry[6]
			firstname = firstname.translate(None, " \'")
			lastname = lastname.translate(None, " \'")
			department = department.translate(None, " ")
			group = group.translate(None, " \n")
			addUser(firstname, lastname, department, group)
		firstLine = False
