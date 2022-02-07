
from bs4 import BeautifulSoup

with open("/Users/newdev/Hive/Development/personal_projects/obsidian-crawler/html/50 Ecommerce Subject Lines To Drive Higher Revenue This Easter Long Weekend.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

    import wdb; wdb.set_trace()
    print(soup.find('title'))
