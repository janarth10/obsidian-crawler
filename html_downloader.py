import requests
import sys

import bs4


HTML_FILE_DIR = '/Users/newdev/Hive/Development/personal_projects/obsidian-crawler/html'

# getting command line argument
url = str(sys.argv[1])

# downloading request html
request = requests.get(url)
request.raise_for_status()

# using bs4 to find title of webpage for file name
soup = bs4.BeautifulSoup(request.text, "html.parser")
file_name = f"{soup.find('title').text}.html"
file_path = f"{HTML_FILE_DIR}/{file_name}"

# write request into html file
with open(file_path, 'x') as f:
    f.write(request.text)


