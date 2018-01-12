import re
import requests
from bs4 import BeautifulSoup
import os

proxies = {"http": "113.89.55.42:9999"}
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip',
}


def book_detail(book_link):
    # book_detail_resp = requests.get(book_link, proxies=proxies, headers=headers,timeout = 30)
    book_detail_resp = requests.get(book_link, proxies=proxies, headers=headers, timeout=30)


    book_detail_soup = BeautifulSoup(open("jieyouzahuodian.html", "r", encoding="utf-8").read(), "html.parser")
    book_tag_soup = book_detail_soup.find("div", {"class", "subject clearfix"}).findAll("div")
    book_main_pic = book_tag_soup[0].find("a").attrs["href"]
    book_detail_info = str(book_tag_soup[1])
    book_info_dict = {}
    #book_info_dict["author"] = str(book_tag_soup[1].findAll("a")[0].text).replace("\n", "").strip()

    items = re.findall(re.compile('<span class="pl">(.*?):</span>(.*?)(<br/>|<br>)', re.S), book_detail_info)
    print(book_detail_info)
    print("=====================")
    for item in items:
        if "作者" in item[0]:
            book_info_dict["author_name"] = str(BeautifulSoup(str(item[1]), "html.parser").find("a").text).replace("\n", "").strip()
        if "出版社" in item[0]:
            book_info_dict["publish_name"] = item[1]
        if "原作名" in item[0]:
            book_info_dict["original_name"] = item[1]
        if "译者" in item[0]:
            book_info_dict["original_name"] = BeautifulSoup(str(item[1]), "html.parser").find("a")
        if "出版年" in item[0]:
            book_info_dict["publish_date"] = item[1]
        if "页数" in item[0]:
            book_info_dict["page_count"] = item[1]
        if "定价" in item[0]:
            book_info_dict["price"] = item[1]
        if "装帧" in item[0]:
            book_info_dict["binding"] = item[1]
        if "丛书" in item[0]:
            book_info_dict["books"] = str(BeautifulSoup(str(item[1]), "html.parser").find("a").text)
        if "ISBN" in item[0]:
            book_info_dict["ISBN"] = item[1]




    print(book_info_dict)



book_detail("https://book.douban.com/subject/25862578/")