from subprocess import*

if __name__ == "__main__":
	Popen("clear")
	pwd = Popen(["pwd"], stdout = PIPE).stdout.read()
	print(pwd)
	filename = raw_input("Enter Filename: ")
	while True:
		try:
			fd = open(filename)
			break
		except IOError, e:
			print("File Does Not Exist")
			filename = raw_input("Enter Filename: ")
			continue
	output = pwd + "/" + filename.split("/")[-1]
	output = output.translate(None, "\n")
	out = Popen(["ln", "-s", filename, output], stdout = PIPE).stdout.read()
	print(out)
	print("Symlink Created at " + output)
	
