import datetime
import requests

import bs4
from markdownify import markdownify

OBSIDIAN_DIR = '/Users/newdev/Documents/janarth-vault/crawler'
LOG_FILE = '/Users/newdev/Hive/Development/personal_projects/obsidian-crawler/error-log.txt'


def write_to_logs(message=''):
    with open(LOG_FILE, 'a') as log:
        log.write('\n\n')
        log.write(f"Logging new message at { datetime.datetime.now().strftime('%c') }")
        log.write('\n')
        log.write(message)


def download_hive_blog_post_to_md_file(url):
    request = requests.get(url)
    request.raise_for_status()

    soup = bs4.BeautifulSoup(request.text, "html.parser")
    file_name = f"{soup.find('title').text}.md"
    file_path = f"{OBSIDIAN_DIR}/{file_name}"

    try:
        """
         'x' option ensures file doesn't already exist

         However, this will be a problem if a post receives an update, bc the program
         will ignore downloading again
        """
        with open(file_path, 'x') as f:
            blog_content_div = soup.find("div", "post-content__inner")
            for html_tag in blog_content_div:
                f.write(markdownify(str(html_tag), heading_style="ATX"))
    except FileExistsError as e:
        write_to_logs(message=f"Tried to download {url}. Already exists.")


download_hive_blog_post_to_md_file(url='https://blog.hive.co/50-ecommerce-subject-lines-to-drive-higher-revenue-this-easter-long-weekend/')
