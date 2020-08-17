import random
import pymysql
import traceback
import requests
import time
from bs4 import BeautifulSoup

class DBHelper:
    def __init__(self):
        # 链接数据库
        try:
            # charset 默认是 latin1, 查询到中文会是？？
            # charset='utf8mb4' 避免有表情时插入错误
            self.__db = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='123456',
                database='men',
                charset='utf8mb4')
            self.__cur = self.__db.cursor()
        except pymysql.Error as e:
            print('链接数据库失败：', e.args[0], e.args[1])

    def insert(self, table, myDict):
        # 答案中存在表情会出错
        # 答案中存在双引号会出错，sql语句会发生歧义
        # 插入一条数据
        try:
            cols = ','.join(myDict.keys())
            values = ','.join(
                map(lambda x: '"' + str(x) + '"', myDict.values()))
            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table, cols, values)
            result = self.__cur.execute(sql)
            self.__db.commit()
        except pymysql.Error as e:
            print('插入失败：', e.args[0], e.args[1])
            # 发生错误时回滚
            # DML 语句，执行完之后，处理的数据，都会放在回滚段中（除了 SELECT 语句），
            # 等待用户进行提交（COMMIT）或者回滚 （ROLLBACK），当用户执行 COMMIT / ROLLBACK后，
            # 放在回滚段中的数据就会被删除。
            self.__db.rollback()

    def query(self, sql):
        try:
            self.__cur.execute(sql)
            result = self.__cur.fetchall()
            self.__db.commit()
            if result:
                return result
            else:
                return None
            
        except  pymysql.Error as e:
            print("数据库-查询异常", traceback.print_exc())
            
    def check_exist(self, table, record):
        try:
            sql = 'SELECT COUNT(*) FROM %s WHERE url= %s' % (table, record)
            result = self.__cur.execute(sql)
            if result > 0:
                return True
            else:
                return False
        except pymysql.Error as e:
            print('查询失败！', traceback.print_exc())
            return False
            
            
    def close(self ):
        self.__cur.close()
        self.__db.close()

UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

def constructHeaders():
    headers = {
    'User-Agent': random.choice(UserAgent_List),
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip',
    }
    return headers

def search_page_video_urls(page):
    rep = requests.get(page)
    bsoup = BeautifulSoup(rep.text, 'html.parser')
    all_divs = bsoup.findAll('div', {'class', 'thumbnail'})
    video_infos = []
    for div_ in all_divs:
        image_info = div_.find('div', {'class', 'image'})
        m_href =image_info.find('a').attrs['href']
        m_title = image_info.find('a').find('img').attrs['alt']
        m_image = image_info.find('a').find('img').attrs['data-original']
        m_duration = div_.find('div',{'class', 'marker-overlays'}).find('var', {'class','duration'}).text
        info_dict={
            'page':page,
            'title': m_title,
            'url':'http://hsex.men/' + m_href,
            'duration':m_duration,
            'image': m_image,
            'status':'0'
        }
        video_infos.append(info_dict)
    
    search_video_info(video_infos)

def search_video_info(video_infos):
    dbhelper = DBHelper()
    for video_info in video_infos:
        rep = requests.get(video_info['url'])
        bsoup = BeautifulSoup(rep.text, 'html.parser')
        video_soup = bsoup.find('div',{'classs', 'videos_box'})
        eu_video = video_soup.findAll('source')[0].attrs['src']
        cdn_video = video_soup.findAll('source')[1].attrs['src']
        video_info['eu_video_url'] = eu_video
        video_info['cdn_video_url'] = cdn_video
        dbhelper.insert('info',video_info)

for i in range(100):
    page = "http://hsex.men/top_list-" + str(i + 1) + ".htm"
    print(page)
    search_page_video_urls(page)
    time.sleep(10)