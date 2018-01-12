import requests
from bs4 import BeautifulSoup

headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': 'gzip',
    }
def book_detail(book_link):
    book_detail_resp = requests.get(book_link, headers=headers, timeout=30)
    book_detail_soup = BeautifulSoup(book_detail_resp.text, "html.parser")
    book_tag_soup = book_detail_soup.find(
        "div", {"class", "subject clearfix"}).findAll("div")
    book_main_pic = book_tag_soup[0].find("a").attrs["href"]
    # print(book_tag_soup[1])
    book_info_spans = book_tag_soup[1].findAll("span")
    book_info_dict = {}
    if "[" in book_tag_soup[1].find("a").text:
        book_info_dict["author"] = book_tag_soup[1].find("a").text.split(
            " ")[0].strip() + book_tag_soup[1].find("a").text.split(" ")[1].strip()
    else:
        book_info_dict["author"] = book_tag_soup[1].find("a").text.strip()


book_detail("https://book.douban.com/subject/25862578/")
