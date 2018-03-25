import time
from selenium import webdriver

co = webdriver.ChromeOptions()
co.add_argument("log-level=3")
co.add_argument("--headless")

message = "List of available Sublime text packages"


driver = webdriver.Chrome(chrome_options=co)

page_url = "https://packagecontrol.io/browse/popular?page={0}"
driver.get(page_url.format(1))

pages_nav = driver.find_element_by_css_selector("nav.pagination")
pages = len(pages_nav.find_elements_by_tag_name("a")) + 1

all_data = []

for page in range(1, pages):
	print("scrapping page %s" % page, end=" ... ")

	URL = page_url.format(page)
	driver.get(URL)
	
	packages = driver.find_elements_by_css_selector("li.package h3")

	for package in packages:
		name = package.text
		url = package.find_element_by_tag_name('a').get_attribute("href")
		
		all_data.append((name, url))

	print("done")


total = len(all_data)
current_time = time.strftime("%A %d of %B, %Y at %I:%M:%S %p")

all_data.sort(key=lambda tup: tup[0])
unique_alphabets = []

# Create pacakges.txt and readme.md in write mode and store in respective variable
with open("README.md",'w') as f:
	f.write("## %s \n\n" % (message))
	f.write("\nThere are a total of `%s` packages available as at `%s`\n\n" % (total, current_time))
	f.write("Instruction on how to contribute to this repository can be found in `contrib.txt` <br>\n\n")

	for data in all_data:
		name, url = data 

		if name[0].upper() not in unique_alphabets:
			unique_alphabets.append(name[0].upper())
			f.write("\n## {0}\n\n".format(name[0].upper()))

		f.write("* [{0}]({1})\n".format(name, url))
		f.flush()

print("Operation Complete")
