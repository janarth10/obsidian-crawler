'''
    Further Ideas:
    1. back link articles to a month-year page
        ie: Date Published: 2021-02-22 [[blog posts 02-2021]]
    2. list of CTAs. grep for "exercise:"? nah unreliable
    3. tag articles with name including "Mini Blog"
    # 4. remove neel nanda from blog file name
'''

import datetime
import requests
import time
import traceback

import bs4
from markdownify import markdownify
from retrying import retry


OBSIDIAN_DIR = '/Users/newdev/Google Drive/Folders/obsidian-vaults/neel-nandas-blog'
LOG_FILE = '/Users/newdev/Hive/Development/personal_projects/obsidian-crawler/error-log.txt'

BLOG_DOMAIN = 'neelnanda.io' # used to check if link is internal/external to our Obsidian vault
BLOG_CONTENT_CSS = "blog-item-content e-content"

SECOND = 1000 # retrying library uses milleseconds


def write_to_logs(message=''):
    with open(LOG_FILE, 'a') as log:
        log.write('\n\n')
        log.write(f"Logging new message at { datetime.datetime.now().strftime('%c') }")
        log.write('\n')
        log.write(message)

def is_url_from_blog(url):
    return BLOG_DOMAIN in url

@retry(wait_random_min=30 * SECOND, wait_random_max=120 * SECOND, stop_max_attempt_number=5)
def get_soup_from_url(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    return soup

def get_obsidian_file_name_from_url(url):
    soup = get_soup_from_url(url)
    filename = f"{soup.find(itemprop='headline')['content']}.md"
    filename = filename.replace('/', ' of ')
    return filename

def download_blog_post_to_md_file(url):
    if not is_url_from_blog(url):
        write_to_logs(message=f"Tried to download {url}. Does not belong to {BLOG_DOMAIN}")
        return

    file_name = get_obsidian_file_name_from_url(url=url)
    file_path = f"{OBSIDIAN_DIR}/{file_name}"

    soup = get_soup_from_url(url)

    # with open(file_path, 'x') as f: normally want to abort if file already exists
    with open(file_path, 'w') as f:
        blog_content_div = soup.find("div", BLOG_CONTENT_CSS)
        markdown_content = markdownify(str(blog_content_div), heading_style='ATX')

        # fetch data for metadata notes
        raw_date = soup.find(itemprop='datePublished')['content'] # '2020-07-18T21:35:07+0100'
        pretty_date = raw_date[:raw_date.find('T')] # '2020-07-18'
        # TODO remove duplicates - check if sets actually work here
        all_links = list(set([link.get('href') for link in blog_content_div.find_all('a')]))

        internal_links = [link for link in all_links if is_url_from_blog(link)]
        external_links = [link for link in all_links if not is_url_from_blog(link)]

        d = datetime.datetime.fromisoformat(pretty_date)
        tags = ['#published-blog-post', d.strftime('#published-%m-%Y')]
        if 'mini blog' in file_name.lower():
            tags.append('#mini-blog')

        # write metadata
        f.write(f"# Metadata of Post")
        f.write('\n')
        f.write(f"Post Description: {soup.find(itemprop='description')['content']}")
        f.write('\n')
        f.write(f"Date Published: {pretty_date}")
        f.write('\n')
        f.write(f"tags: {' '.join(tags)}")
        f.write('\n')
        f.write(f"* Internal References:")
        f.write('\n')
        for link in internal_links:
            f.write(f"    - [[{get_obsidian_file_name_from_url(url=link)}]]")
            f.write('\n')
        f.write('\n')
        f.write(f"* External References:")
        f.write('\n')
        for link in external_links:
            f.write(f"    - {markdownify(str(link), heading_style='ATX') }")
            f.write('\n')
        f.write('\n\n')

        # write post content
        f.write('# Content of Post')
        f.write('\n')
        f.write(markdown_content)

    return file_path


# # Using this to download all posts listed in one page of results
# def download_blogs_from_list_view(url):
#     soup = get_soup_from_url(url)

#     links = soup.select('a.blog-more-link')
#     for link in links:
#         link_str = link.get('href')
#         if BLOG_DOMAIN not in link.get('href'):
#             link_str = f"https://{BLOG_DOMAIN}{link_str}"

#         try:
#             download_blog_post_to_md_file(url=link_str)
#         except Exception as e:
#             write_to_logs(message=f"{link_str} failed to download")
#             write_to_logs(message=str(e))

#         time.sleep(30) # sleeping 30 seconds to avoid rate limits


# # __main__
# page_urls = [
#     'https://www.neelnanda.io/blog',
#     'https://www.neelnanda.io/?offset=1593970738240',
#     'https://www.neelnanda.io/?offset=1592213331915',
# ]

# for page_url in page_urls:
#     download_blogs_from_list_view(page_url)


# Retrying failed download urls fetched from error-log.txt
# failed_urls = [
#     'https://neelnanda.io/blog/41-helplessness',
#     'https://neelnanda.io/blog/40-help',
#     'https://neelnanda.io/blog/39-reflection',
#     'https://neelnanda.io/blog/sad',
#     'https://neelnanda.io/blog/38-slack',
#     'https://neelnanda.io/blog/37-option-paralysis',
#     'https://neelnanda.io/blog/36-aesthetics',
#     'https://neelnanda.io/blog/34-learning',
#     'https://neelnanda.io/blog/32-macro-procrastination',
#     'https://neelnanda.io/blog/31-overcoming-bias',
#     'https://neelnanda.io/blog/30-debugging-others',
#     'https://neelnanda.io/blog/post-28-on-creativity-the-joys-of-5-minute-timers',
#     'https://neelnanda.io/blog/27-retrospective',
#     'https://neelnanda.io/blog/26-accurate-self-image',
#     'https://neelnanda.io/blog/25-friendship',
#     'https://neelnanda.io/blog/mini-blog-post-23-taking-social-initiative',
#     'https://neelnanda.io/blog/mini-blog-post-22-the-8020-rule',
#     'https://neelnanda.io/blog/mini-blog-post-21-taking-the-first-step',
#     'https://neelnanda.io/blog/mini-blog-post-20-emotions-are-bayesian-evidence',
#     'https://neelnanda.io/blog/mini-blog-post-12-the-map-and-the-territory',
#     'https://neelnanda.io/blog/mini-blog-post-11-live-a-life-you-feel-excited-about'
# ]

urls = [
    'https://neelnanda.io/blog/mini-blog-post-23-taking-social-initiative',
    'https://neelnanda.io/blog/mini-blog-post-22-the-8020-rule',
    'https://neelnanda.io/blog/mini-blog-post-21-taking-the-first-step',

    'https://neelnanda.io/blog/35-standards',
    'https://neelnanda.io/blog/prioritisation',
    'https://neelnanda.io/blog/mini-blog-post-17-prioritisation-part-2-achieving-goals',
]

for failed_url in failed_urls:
    try:
        download_blog_post_to_md_file(url=failed_url)
    except Exception as e:
        write_to_logs(f"failed downloading {failed_url}\n{traceback.format_exc()}")
