import re
import requests
import json
import time
import random
import traceback
import logging
import logging.config
from bs4 import BeautifulSoup

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("main")

proxies = {"http": "113.89.55.42:9999"}
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip',
}


def parser_data(data):
    if len(str(data).split("-")) > 2:
        data = str(data).split("-")[0] + "-" + str(data).split("-")[1] + "-" + str(data).split("-")[2] +  " 12:12:12"
        return data
    if len(str(data).split("-")) <= 2:
        data = str(data).split("-")[0] + "-" + str(data).split("-")[1] + "-00 12:12:12"
        return data


def make_req(payload):
    try:
        print(payload["book_title"])
        payload = {
            "id": payload["book_id"],
            "coursename": payload["book_title"],
            "coursetype": payload["book_current_class"],
            "coursestarttime": payload["book_publish_date"],
            "courseendtime": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            "coursecover": payload["book_pic"],
            "courseintro": payload["book_intro"],
            "coursestate": "ok",
            "courseprice": re.findall("\d+", str(payload["book_price"]).strip())[0],
            "catalogsort": random.randint(0, 100),
            "catalogintro": payload["book_current_class"],
            "catalogstarttime": payload["book_publish_date"],
            "catalogendtime": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            "catalogperiodtype": "A",
            "catalogtimelength": payload["book_page_count"],
            "catalogid": payload["book_ISBN"],
            "catalogname": payload["book_current_class"],
            "tagid": str(random.randint(0, 10000)),
            "tagdescn": payload["book_tags"],
            "teacherid": "tea" + str(random.randint(0, 1000)),
            "teachername": payload["author_name"],
            "teacherintro": payload["book_author_intro"]
        }
        headers2 = {'content-type': 'application/json'}
        r = requests.post(
            "http://localhost:8080/history-web/search/doc",
            data=json.dumps(payload),
            headers=headers2)

        print(r.text)
    except Exception as e:
        logger.error(traceback.print_exc())
        print(traceback.print_exc())


def book_detail(parent_class, current_class, book_title, book_link):
    try:
        book_detail_resp = requests.get(
            book_link,
            proxies=proxies,
            headers=headers,
            timeout=30)
        book_detail_soup = BeautifulSoup(book_detail_resp.text, "html.parser")

        #book_detail_soup = BeautifulSoup(
        #    open(
        #        "jieyouzahuodian.html",
        #        "r",
        #        encoding="utf-8").read(),
        #    "html.parser")

        book_info_dict = {}

        book_detail_divs = book_detail_soup.find(
            "div", {"class", "subject clearfix"}).findAll("div")
        book_detail_rating_num = book_detail_soup.find(
            "a", {"class", "rating_people"}).findAll("span")[0].text
        book_main_pic = book_detail_divs[0].find("a").attrs["href"]
        book_related_intro = book_detail_soup.find(
            "div", {
                "class", "related_info"}).findAll(
            "div", {
                "class", "intro"})[0].findAll("p")

        author_related_intro = book_detail_soup.find(
            "div", {
                "class", "related_info"}).findAll(
            "div", {
                "class", "intro"})[1].findAll("p")
        book_related_tags = book_detail_soup.findAll("a", {"class", " tag"})
        book_score = book_detail_soup.find(
            "div", {"class", "rating_self clearfix"}).findAll("strong")[0]
        book_related_info_content = ""
        author_related_info_content = ""
        book_tag_list = []
        for p in book_related_intro:
            book_related_info_content += str(p.text)
        for p in author_related_intro:
            author_related_info_content += str(p.text)
        for tag in book_related_tags:
            book_tag_list.append(str(tag.text))
        book_info_dict["book_id"] = str(book_link).split("/")[-2]
        book_info_dict['book_intro'] = book_related_info_content
        book_info_dict['book_author_intro'] = author_related_info_content
        book_info_dict['book_tags'] = book_tag_list
        book_detail_info = str(book_detail_divs[1])
        book_info_dict['book_pic'] = book_main_pic
        book_info_dict['book_rating_num'] = book_detail_rating_num
        book_info_dict['book_score'] = str(book_score.text)
        book_info_dict['book_link'] = book_link
        book_info_dict['book_parent_class'] = parent_class
        book_info_dict['book_current_class'] = current_class
        book_info_dict["book_title"] = book_title
        items = re.findall(
            re.compile(
                '<span class="pl">(.*?)</span>(.*?)(<br/>|<br>)',
                re.S),
            book_detail_info)
        print(book_detail_info)
        #print("book detail info as follow!")
        for item in items:
            if "作者" in item[0]:
                print("=========================")
                print(str(item[1]) + "")
                book_info_dict["author_name"] = str(BeautifulSoup(
                    str(item[1]), "html.parser").find("a").text).replace("\n", "").strip()
            if "出版社" in item[0]:
                book_info_dict["publish_name"] = item[1]
            if "原作名" in item[0]:
                print("******************")
                print(item[1])
                print("******************")
                book_info_dict["book_original_name"] = str(item[1])
            if "译者" in item[0]:
                book_info_dict["book_original_name"] = BeautifulSoup(
                    str(item[1]), "html.parser").find("a")
            if "出版年" in item[0]:
                book_info_dict["book_publish_date"] = parser_data(str(item[1]).strip())
            if "页数" in item[0]:
                book_info_dict["book_page_count"] = item[1]
            if "定价" in item[0]:
                book_info_dict["book_price"] = item[1]
            if "装帧" in item[0]:
                book_info_dict["book_binding"] = item[1]
            if "丛书" in item[0]:
                book_info_dict["book_books"] = str(BeautifulSoup(
                    str(item[1]), "html.parser").find("a").text)
            if "ISBN" in item[0]:
                book_info_dict["book_ISBN"] = item[1]

        #print(book_info_dict)
        make_req(book_info_dict)

        # with open("book_detail.json", 'w') as f:
        #    f.write(json.dumps(book_info_dict))
        #    f.close()
    except Exception as e:
        logger.error(book_title + book_link + str(traceback.print_exc()))
        print(book_link + book_link + str(traceback.print_exc()))


def book_list(tag_list):
    try:
        for tag in tag_list:
            time.sleep(random.randint(0, 20))
            parent_class = str(tag).split(":")[0]
            tag = str(tag).split(":")[1]
            r = requests.get("https://book.douban.com" + tag, proxies=proxies, headers=headers, timeout=30)
            soup = BeautifulSoup(r.text, "html.parser")
            books = soup.find("ul", {"class", "subject-list"}).findAll("li")
            print("books ================================================")
            logger.info(str(books))
            #print(str(books))
            for book in books:
                time.sleep(1)
                link_soup = BeautifulSoup(str(book), "html.parser").find("div", {"class","pic"})
                info_soup = BeautifulSoup(str(book), "html.parser").find("div", {"class","info"})
                book_title = BeautifulSoup(str(info_soup), "html.parser").find("a").attrs["title"]
                book_link = BeautifulSoup(str(link_soup), "html.parser").find("a").attrs["href"]
                book_detail(parent_class, tag, book_title, book_link)
    except Exception as e:
        print(traceback.print_exc())


def book_tags():
    try:
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
        book_list(tag_list)
        #print(tag_list)
    except Exception as e:
        logger.error(traceback.print_exc())
        print(traceback.print_exc())


book_tags()
#book_detail("文学", "小说", "雪落香杉树", "https://book.douban.com/subject/5431784/")
#book_detail("文学", "小说", "解忧杂货店", "https://book.douban.com/subject/25862578/")
#book_detail("文学", "小说", "我的前半生", "https://book.douban.com/subject/2230208/")
