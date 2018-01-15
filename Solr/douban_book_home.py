import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
import random
proxies = {"http": "113.89.55.42:9999"}
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip',
}

def book_tags():

    #book_tags_soup = BeautifulSoup(open("tag_list.html", "r", encoding="utf-8").read(), "html.parser")
    book_tags_soup = BeautifulSoup(
        requests.get("https://book.douban.com/",  proxies=proxies, headers=headers, timeout=30).text,
        "html.parser")
    #print(str(book_tags_soup))
    book_tags_ul = book_tags_soup.find(
        "ul", {"class", "hot-tags-col5 s"}).findAll("ul")
    tag_list = []
    for ul in book_tags_ul:
        parent_tag = BeautifulSoup(str(ul), "html.parser").find("li", {"class", "tag_title"}).text
        for a in BeautifulSoup(str(ul), "html.parser").findAll("a"):
            if "view" not in a.attrs["href"]:
                tag_list.append(str(parent_tag).replace("\n", "").strip() + ":" + a.attrs["href"])

    #return tag_list
    print(tag_list)


#book_tags()

def parser_data(data):
    if len(str(data).split("-")) >= 2:
        data = str(data).split("-")[0] + "-" + str(data).split("-")[1] + "-00 12:12:12"
        return data
    else:
        data = str(data).split("-")[0] + str(data).split("-")[1] + "-00 12:12:12"
        return data

    data = "2016-5-1"
    print(parser_data(data))

#book_link = 'https://book.douban.com/subject/2230208/'
#price = " 22.00元"
#print(re.findall("\d+", str(price).strip())[0])
#print(str(book_link).split("/")[-2])
#print(random.randint(0, 100))
data = "2016-5-1"
print(parser_data(data))
