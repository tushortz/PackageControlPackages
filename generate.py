# Importing necessary modules
from urllib.request import urlopen
import os, re, six, time

# Variable decarations
target_url = "https://packagecontrol.io/browse/new"
message = "List of available Sublime text packages"
domain = "https://packagecontrol.io/packages/"
sorts = [	 
			 "0", "1", "2", "3", "4", "5", 
			 "6", "7", "8", "9", "A", "B", 
			 "C", "D", "E", "F", "G", "H", 
			 "I", "J", "K", "L", "M", "N", 
			 "O", "P", "Q", "R", "S", "T", 
			 "U", "V", "W", "X", "Y", "Z"     
		]
txt = str(urlopen(target_url).read())
current_time = time.strftime("%A %d of %B, %Y at %I:%M:%S %p")
details_link = [] 
packdict = {}
lists = []
total = 0
vall = 0

# Store all available pages number in content

content = (re.findall(r'<a href="\?page=[\'"]?([^\'" >]+)">', txt))

# Add "1" at the beginning of content list
content.insert(0, "1")

# Function to find all packages in all pages
def getpackages(num):
	'''return a dict containing all packages in all pages'''
	result = {}
	link = target_url + "?page=" + num
	txt = str(urlopen(link).read())
	content = re.findall(r'">[\'"]*([^\'">]+)</a></h3> <span class=', txt)
	
	# Convert first character always to uppercase
	for i in content:
		i = i.replace("\\xc3\\xa7", "&#xE7;").replace("\\xc3\\xaa", "&#234;").replace("%23x27;", "&#39;")
		packagename = i[0].title() + i[1:]

		# Replace any spaces with %20
		i = i.replace(" ", "%20").replace("&amp;", "%26").replace("\\xc3\\xa7", "&#xE7;").replace("#", "%23").replace("'", "&#39;").replace("\\xc3\\xaa", "&#234;").replace("&%23", "&#39;").replace("&#39;x27;", "'")

		result[packagename] = i

	return result

# Find the total packages available
for val in content:
	y = getpackages(val)
	for x in y:
		packdict[x] =  y[x]
		total +=1

# Variable to store result of sorted keys of packdict
first_item = sorted(packdict)[0]

# Create pacakges.txt and readme.md in write mode and store in respective variable
packages = open("packages.txt",'w')
readme = open("README.md",'w')

# Write some data into readme and packages
packages.write("Instruction on how to contribute to this repository can be found in `contrib.txt`\n\n")
readme.write("Instruction on how to contribute to this repository can be found in `contrib.txt` <br\>")
packages.write("\nThere are a total of %s packages available as at %s\n\n" % (total, current_time ))
readme.write("\nThere are a total of `%s` packages available as at `%s`\n\n" % (total, current_time ))
packages.write("%s \n%s \n\n" % (message,len(message) * "="))
readme.write("## %s \n\n" % (message))

# Header storing certain text
header = "---> %s" % first_item[0]

# Write the rest of the data into readme and packages.txt
for x in sorted(packdict):
	if x[0] == sorts[vall]:
		packages.write(x + "\n")

		readme.write("* [%s](%s%s) \n" % (x, domain, packdict[x]))

	elif x[0] != sorts[vall]:
		sorts[vall] = x[0]

		packages.write("\n---> " + x[0] + "\n======\n")
		readme.write("\n### " + x[0] + "\n\n")

		packages.write(x + "\n")
		readme.write("* [%s](%s%s) \n" % (x, domain, packdict[x]))

# Close files
readme.close()
packages.close()
