import datetime
import requests

import bs4
from markdownify import markdownify

OBSIDIAN_DIR = '/Users/newdev/Documents/Folders/obsidian-vaults/hive-blog-vault'
LOG_FILE = '/Users/newdev/Hive/Development/personal_projects/obsidian-crawler/error-log.txt'


def write_to_logs(message=''):
    with open(LOG_FILE, 'a') as log:
        log.write('\n\n')
        log.write(f"Logging new message at { datetime.datetime.now().strftime('%c') }")
        log.write('\n')
        log.write(message)


def download_hive_blog_post_to_md_file(url):
    if 'blog.hive.co' not in url:
        write_to_logs(message=f"Tried to download {url}. Does not belong to Hive Blog")
        return

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
            f.write(f"[Original Link]({url})")
            f.write("\n\n")
            blog_content_div = soup.find("div", "post-content__inner")
            for html_tag in blog_content_div:
                if type(html_tag) == bs4.element.NavigableString:
                    f.write(markdownify(str(html_tag), heading_style="ATX"))
                elif html_tag.name == 'a' and 'blog.hive.co' in html_tag.get('href'):
                    write_to_logs(message=f"individual a_tag: {html_tag.get('href')}")
                    f.write(f"[[{download_hive_blog_post_to_md_file(url=html_tag.get('href'))}]]")
                    f.write("\n")
                else:
                    for a_tag in html_tag.select('a'):
                        write_to_logs(message=f"nested a_tag: {a_tag.get('href')}")
                        if a_tag.name == 'a' and 'blog.hive.co' in a_tag.get('href'):
                            f.write(f"[[{download_hive_blog_post_to_md_file(url=a_tag.get('href'))}]]")
                            f.write("\n")
                    f.write(markdownify(str(html_tag), heading_style="ATX"))
    except FileExistsError as e:
        write_to_logs(message=f"Tried to download {url}. Already exists.")

    return file_name


download_hive_blog_post_to_md_file(url='https://blog.hive.co/50-ecommerce-subject-lines-to-drive-higher-revenue-this-easter-long-weekend/')


# def bfs_crawl():
#     """
#         Using breadth first search to download all blog posts in the Hive Blog "graph"

#         TODO
#         - where to start? Is there a way to get a list of all articles? If so don't need to BFS
#         - need to replace "markdownify(str(a_tag), heading_style="ATX")" with [[<filename>]]. so that my
#             obsidian files link to eachother
#     """

#     # for fucks just want to pseudo the BFS algo

#     urls_queue = []
#     for post_url in urls_queue:
#         # define this fn within 'bfs_crawl' so that it can add new urls to que
#         download_hive_blog_post_to_md_file(post_url)
