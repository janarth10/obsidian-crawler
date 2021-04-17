import requests
import bs4
from markdownify import markdownify

OBSIDIAN_DIR = '/Users/newdev/Documents/janarth-vault/crawler'


def download_hive_blog_post_to_md_file(url):
    request = requests.get(url)
    request.raise_for_status()

    soup = bs4.BeautifulSoup(request.text, "html.parser")
    file_name = f"{soup.find('title').text}.md"
    file_path = f"{OBSIDIAN_DIR}/{file_name}"

    # JPTODO should check if this file exists already. bc if it does
    #   idw append more content to it
    with open(file_path, 'a') as f:
        blog_content_div = soup.find("div", "post-content__inner")
        for html_tag in blog_content_div:
            f.write(markdownify(str(html_tag), heading_style="ATX"))

download_hive_blog_post_to_md_file(url='https://blog.hive.co/50-ecommerce-subject-lines-to-drive-higher-revenue-this-easter-long-weekend/')
