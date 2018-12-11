import json
import operator
import time
from urllib import parse
import re
import click
import requests
import html
start_time = time.perf_counter()
HOME_URL = "https://packagecontrol.io"
JSON_LOCATION = "/browse/new.json?page={}"
ALL_START_CHARS = set()
ALL_PACKAGES = []


def replace_string(text):
    TEXT = text.replace(
        "\\xc3\\xa7", "&#xE7;").replace(
        "'", "&#39;").replace(
        "\\xc3\\xaa", "&#234;").replace(
        "&%23", "&#39;").replace(
        "&#39;x27;", "'").replace(
        "\\xc3\\xaa", "&#234;").replace(
        "%23x27;", "&#39;")

    return TEXT


def get_total_pages():
    return get_json_content(1).get("pages", 1)


def get_json_content(page_no, node_name=None):
    url = HOME_URL + JSON_LOCATION.format(page_no)
    data = requests.get(url).json()

    if not node_name:
        return data

    return data.get(node_name)


def get_packages(page_num):
    result = get_json_content(page_num, "packages")

    packages = []

    for pack in result:
        name = pack.get("name")
        description = pack.get("description")
        url = "{HOME_URL}/packages/{name}".format(HOME_URL=HOME_URL,
                                                  name=parse.quote(name))

        packages.append({
            "name": name,
            "description": description,
            "url": url
        })

        ALL_START_CHARS.add(name[0].lower())

    return packages


metadata = get_json_content(1)
TOTAL_PAGES = metadata.get("pages", 1)
TOTAL_PACKAGES = metadata.get("total", 1)


with click.progressbar(range(1, TOTAL_PAGES+1), TOTAL_PAGES, "Downloading packages: ", show_percent=True, show_pos=True) as bar:
    for num in bar:
        packages = get_packages(num)
        ALL_PACKAGES += packages

ALL_PACKAGES.sort(key=operator.itemgetter("name"))
ALL_START_CHARS = sorted(ALL_START_CHARS)

HEADERS = """
**List of available Sublime text packages**

`{total_packages}` packages are available as at `{current_time}`

"""

total_packages = len(ALL_PACKAGES)
with click.progressbar(ALL_PACKAGES, total_packages, "Writing packages to file", show_percent=True, show_pos=True) as bar:
    with open("README.md", "w", encoding='utf-8') as f:
        f.write(HEADERS.format(
            total_packages=total_packages,
            current_time=time.strftime("%A %d of %B, %Y at %I:%M:%S %p")
        ))

        for package in bar:
            name = package.get("name", "")
            description = html.escape(package.get("description", ""))

            f.write("""[{name}]({url}) - {description}\n\n""".format(
                name=name,
                url=package.get("url"),
                description=description,
            ))

end_time = time.perf_counter()
duration = (end_time - start_time)/60

print("Execution completed in {:.2f} minutes".format(duration))
