import datetime
import requests

import bs4
from markdownify import markdownify

OBSIDIAN_DIR = '/Users/newdev/Google Drive/Folders/obsidian-vaults/hive-blog-vault'
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
    try:
        request.raise_for_status()
    except requests.HTTPError as e:
        write_to_logs(message=str(e))
        return

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


def download_hive_blogs_from_card_list_view(response):
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    """
        sanity check
            - soup.select('a.js-fadein')
            - soup.select('h2.post-card__title')
        returned 9 results when on first page. assuming that this will find all blog posts
    """
    links = soup.select('a.js-fadein') or soup.select('h2.post-card__title')
    for link in links:
        link_str = link.get('href')
        if 'blog.hive.co' not in link.get('href'):
            link_str = f"https://blog.hive.co{link_str}"
        download_hive_blog_post_to_md_file(url=link_str)

# __main__
start_urls = [
    'https://blog.hive.co/tag/email-design',
    'https://blog.hive.co/tag/email-marketing',
    'https://blog.hive.co/tag/ecommerce-email',
    'https://blog.hive.co/tag/seasonal',
]

for start_url in start_urls:
    page_num = 1
    while page_num < 20:
        resp = requests.get(f"{start_url}/page/{page_num}")
        try:
            resp.raise_for_status()
            download_hive_blogs_from_card_list_view(response=resp)
        except requests.HTTPError as e:
            write_to_logs(message='Did we get to end of pages??')
            write_to_logs(message=str(e))
            break
        except Exception as e:
            write_to_logs(message='Unknown Exception')
            write_to_logs(message=str(e))

        page_num += 1
