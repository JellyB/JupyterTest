import requests
import db
import time
import traceback
import user_agent
import os
from bs4 import BeautifulSoup


def get_all_tags_first_link():
    tag_list = []
    html = requests.get('http://www.mzitu.com')
    html.encoding = 'gbk'
    bsoup = BeautifulSoup(
        html.text.strip().replace(
            '<!--   ',
            '').replace(
            '-->',
            ''),
        "html.parser")
    tags = bsoup.find('div', {'class': 'tags'}).findAll('a')
    dbhelper = db.DBHelper()
    for a in tags:
        myDict = {
            'title': a.attrs['title'],
            'url': a.attrs['href']
        }
        tag_list.append(myDict)
        # print(a.attrs['title'],a.attrs['href'])
        dbhelper.insert('t_meizitu_tags_url', myDict)
    dbhelper.close()
    return tag_list


def get_tag_all_html_link(url):
    tagAllHtml = []
    tagAllHtml.append(url)
    html = requests.get(url)
    html.encoding = 'gbk'
    bsoup = BeautifulSoup(html.text, 'html.parser').find(
        'div', {'class', 'navigation'}).findAll('a')[:-2]
    if bsoup:
        for a in bsoup:
            if url.startswith('http://www.meizitu.com/a/'):
                tagAllHtml.append(
                    'http://www.meizitu.com/a/' +
                    a.attrs['href'])
            else:
                tagAllHtml.append('http://www.meizitu.com' + a.attrs['href'])
    else:
        print('没有下一页！')
    return tagAllHtml


def save_all_tags_html_links():
    dbhelper = db.DBHelper()
    html_links = []
    for tags in get_all_tags_first_link():
        print(tags['url'])
        allinks = get_tag_all_html_link(tags['url'])
        for urlink in allinks:
            print(tags['title'], urlink)
            myDict = {'tag': tags['title'], 'html_url': urlink}
            dbhelper.insert('t_meizitu_tag_html_urls', myDict)
    dbhelper.close()


def get_current_page_albums(page):
    current_page_albums = []
    rep = requests.get(page)
    rep.encoding = 'gb2312'
    bsoup = BeautifulSoup(rep.text, 'html.parser')
    album_list = bsoup.find(
        'ul', {'class', 'wp-list clearfix'}).findAll('li', {'class', 'wp-item'})
    for album in album_list:
        album_link = album.find('h3', {'class', 'tit'}).find('a').attrs['href']
        current_page_albums.append(album_link)
    return current_page_albums


def get_current_album_title_imgs(current_page_albums_links, tag_path):
    try:
        for link in current_page_albums_links:
            rep = requests.get(link)
            rep.encoding = 'gb2312'
            bsoup = BeautifulSoup(rep.text, 'html.parser')
            imgs = bsoup.find('div', {'class', 'postContent'}).find(
                'p').findAll('img')
            album_title = bsoup.find(
                'div', {'class', 'metaRight'}).find('a').text
            download_album(tag_path, imgs, album_title)
            time.sleep(5)
    except BaseException as e:
        print('获取每个相册图片 & 标题异常！', traceback.print_exc())


#current_page_albums_links = ['http://www.meizitu.com/a/5529.html', 'http://www.meizitu.com/a/5527.html']

#get_current_album_title_imgs(current_page_albums_links, 'F:\Meizitu\90后')


def download_album(tag_path, imgs, album_title):
    headers = user_agent.constructHeaders()
    for img in imgs:
        time.sleep(2)
        album_title = format_text(album_title)
        img_src = img.attrs['src']
        title = format_text(img.attrs['alt']) + img_src.split('/')[-1]
        if title.startswith('妹子图微信'):
            continue
        else:
            try:
                if not os.path.exists(os.path.join(tag_path, album_title)):
                    os.makedirs(os.path.join(tag_path, album_title))
                os.chdir(tag_path + "\\" + album_title)
                exists = os.path.exists(album_title)
                if not exists:
                    try:
                        img_html = requests.get(
                            img_src, headers=headers, stream=True, timeout=30, verify=True)
                        with open(title + '.jpg', 'wb') as f:
                            f.write(img_html.content)
                            f.close()
                            print(title + " download successfully!")
                    except BaseException as e:
                        print('图片下载失败--！', e)
            except BaseException as e2:
                print('相册文件构建失败！', str(e2))
                continue

# 对名字进行处理，如果包含下属字符，则直接剔除该字符


def format_text(text):
    text = text.strip()
    for i in ['\\', '/', ':', '*', '?', '"', '<', '>', '!', '|']:
        while i in text:
            text = text.replace(i, '')
    return text


def create_tags_dir(base_url):
    dbhelper = db.DBHelper()
    sql = 'SELECT title from t_meizitu_tags_url where scrawl_flag != "1" ORDER BY title asc'
    result = dbhelper.query(sql)
    try:
        if result:
            # 遍历数据库中的每个tag
            for tag in result:
                print(
                    '==========================正在爬取=====================' +
                    tag[0])
                if not os.path.exists(os.path.join(base_url, tag[0])):
                    os.makedirs(os.path.join(base_url, tag[0]))
                os.chdir(base_url + '\\' + tag[0])
                sql_tag = 'SELECT html_url FROM t_meizitu_tag_html_urls WHERE tag =' + \
                    "'" + tag[0] + "'" + ' ORDER BY html_url asc'
                result_tag = dbhelper.query(sql_tag)
                if not result_tag:
                    print("%s 下没有发现url！", tag)
                else:
                    # 处理当前tag的 当前页面 里的相册
                    for page in result_tag:
                        # 获得当前页面的 相册链接地址列表
                        current_page_albums_links = get_current_page_albums(
                            page[0])
                        # 获取单个相册中图片url 链接地址及 相册名称
                        get_current_album_title_imgs(
                            current_page_albums_links, base_url + '\\' + tag[0])

        else:
            print("查询异常！")
    except BaseException as e:
        print('操作异常：', e)
    finally:
        dbhelper.close()


create_tags_dir('F:\\Meizitu')
