
# coding: utf-8

# # Mysql 连接对象

# In[8]:


import pymysql
import traceback

class DBHelper:
    def __init__(self):
        # 链接数据库
        try:
            # charset 默认是 latin1, 查询到中文会是？？
            # charset='utf8mb4' 避免有表情时插入错误
            self.__db = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='111111',
                database='test',
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


# # 爬取每个tag的首页地址

# In[22]:


import requests
from bs4 import BeautifulSoup

def getAllTagsFirstLink():
    tag_list = []
    html = requests.get('http://www.meizitu.com')
    html.encoding = 'gbk'
    bsoup = BeautifulSoup(html.text.strip().replace('<!--   ','').replace('-->',''), "html.parser")
    tags = bsoup.find('div',{'class': 'tags'}).findAll('a')
    dbhelper = DBHelper()
    for a in tags:
        myDict = {
            'title': a.attrs['title'],
            'url':a.attrs['href']
        }
        tag_list.append(myDict)
        #print(a.attrs['title'],a.attrs['href'])
        dbhelper.insert('t_meizitu_tags_url',myDict)
    dbhelper.close()
    return tag_list
getAllTagsFirstLink()


# # 获取当前tag的所有html地址

# In[10]:


import requests
from bs4 import BeautifulSoup
def get_tag_all_html_link(url):
    tagAllHtml = []
    tagAllHtml.append(url)
    html = requests.get(url)
    html.encoding='gbk'
    bsoup = BeautifulSoup(html.text,'html.parser').find('div',{'class','navigation'}).findAll('a')[:-2]
    if bsoup:
        for a in bsoup:
            if url.startswith('http://www.meizitu.com/a/'):
                tagAllHtml.append('http://www.meizitu.com/a/' + a.attrs['href'])
            else:
                tagAllHtml.append('http://www.meizitu.com' + a.attrs['href'])
    else:
        print('没有下一页！')
    return tagAllHtml
        
get_tag_all_html_link('http://www.meizitu.com/a/pure.html')


# # 模拟header

# In[11]:


import random
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
constructHeaders()


# # 爬取代理ip存入数据库中

# In[22]:


import requests
import re

url_proxy = 'http://www.xicidaili.com/nt/'
num = 2 #爬取页数，前两页
def ip_test(ip, headers, url_for_test='https://www.baidu.com', set_timeout=10):
    try:
        rp = requests.get(url_for_test, headers=headers, proxies={'http': ip[0] + ':' + ip[1]}, timeout = set_timeout)
        if rp.status_code == 200:
            return True
        else:
            return False
        
    except BaseException as e:
        return False
    
    
def sraw_ip(url_proxy, num,headers, url_for_test='https://www.baidu.com'):    
    ip_list = []
    dbhelper = DBHelper()
    for num_page in range (1, num +1):
        url_proxy = url_proxy + str(num_page)
        resp = requests.get(url_proxy, headers=headers, timeout = 10)
        resp.encoding = 'utf-8'
        htmlContent = resp.text
        
        pattern = re.compile('<td class="country">.*?alt="Cn" />.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>',re.S)
        iterms = re.findall(pattern, htmlContent)
        for ip in iterms:
            if ip_test(ip, headers, url_for_test):
                print('测试通过，IP地址为' + str(ip[0]) + ':' + str(ip[1]))
                ip_list.append(ip[0] + ':' + ip[1])
                myDict = {'ip':ip[0] + ':' + ip[1]}
                dbhelper.insert('t_meizitu_proxy_ip', myDict)
            else:
                print('测试失败！')
    dbhelper.close()
    return ip_list

headers = constructHeaders()
sraw_ip(url_proxy, num, headers)
    


# # 获取每个tag的所有html地址并保存

# In[14]:


def save_all_tags_html_links():
    dbhelper = DBHelper()
    html_links = []
    for tags in getAllTagsFirstLink():
        print(tags['url'])
        allinks = get_tag_all_html_link(tags['url'])
        for urlink in allinks:
            #print(tags['title'], urlink)
            myDict={'tag':tags['title'], 'html_url':urlink}
            dbhelper.insert('t_meizitu_tag_html_urls',myDict)
    dbhelper.close()
save_all_tags_html_links()


# # 获取当前page的相册链接列表

# In[15]:


import requests
from bs4 import BeautifulSoup
def get_current_page_albums(page):
    current_page_albums = []
    rep = requests.get(page)
    rep.encoding = 'gb2312'
    bsoup = BeautifulSoup(rep.text, 'html.parser')
    album_list = bsoup.find('ul', {'class', 'wp-list clearfix'}).findAll('li', {'class', 'wp-item'})
    for album in album_list:
        album_link = album.find('h3',{'class', 'tit'}).find('a').attrs['href']
        current_page_albums.append(album_link)
    return current_page_albums
    


# # 获取当前相册的图片链接及标题

# In[18]:


import requests
import time
import traceback
from bs4 import BeautifulSoup

def get_current_album_title_imgs(current_page_albums_links, tag_path):
    try:
        for link in current_page_albums_links:
            rep = requests.get(link)
            rep.encoding = 'gb2312'
            bsoup = BeautifulSoup(rep.text, 'html.parser')
            imgs = bsoup.find('div', {'class', 'postContent'}).find('p').findAll('img')
            album_title = bsoup.find('div',{'class', 'metaRight'}).find('a').text
            download_album(tag_path, imgs, album_title)
            time.sleep(5)
    except BaseException as e:
        print('获取每个相册图片 & 标题异常！', traceback.print_exc())
        
current_page_albums_links = ['http://www.meizitu.com/a/3668.html', 'http://www.meizitu.com/a/5527.html']
        
get_current_album_title_imgs(current_page_albums_links, '/home/jelly/Meizitu')
    


# # 创建相应的相册，并下载相册

# In[1]:


import os
def download_album(tag_path, imgs, album_title):
    headers = constructHeaders()
    for img in imgs:
        album_title = format_text(album_title)
        img_src = img.attrs['src']
        title = format_text(img.attrs['alt']) + img_src.split('/')[-1]
        if title.startswith('妹子图微信'):
            continue
        else:
            try:
                if not os.path.exists(os.path.join(tag_path, album_title)):
                    os.makedirs(os.path.join(tag_path, album_title))
                os.chdir(tag_path + "/" + album_title)
                exists = os.path.exists(album_title)
                if not exists:               
                    try:
                        img_html = requests.get(img_src, headers=headers, stream=True, timeout=30, verify=True)
                        with open(title + '.jpg', 'wb') as f:                        
                            f.write(img_html.content)
                            f.close()
                            print(title + " download successfully!")
                    except BaseException as e:
                        print('图片下载失败--！', e)
            except BaseException as e2:
                print('相册文件构建失败！', str(e2))
                continue
            
            
    


# # 文本格式化

# In[17]:


#对名字进行处理，如果包含下属字符，则直接剔除该字符
def format_text(text):
    text = text.strip()
    for i in ['\\', '/', ':', '*', '?', '"', '<', '>', '!', '|']:
        while i in text:
            text = text.replace(i, '')
    return text
    


# In[21]:


import traceback
def test():
    try:
        sql = 'SELECT title,scrawl_flag from t_meizitu_tags_url where scrawl_flag !="1" ORDER BY title asc'
        dbhelper = DBHelper()
        result = dbhelper.query(sql)
        print(result)
    except BaseException as e:
         print(e, traceback.print_exc())
test()


# # Main  根据tag创建本地文件夹下载图片

# In[ ]:


import os
def  create_tags_dir(base_url):
    dbhelper = DBHelper()
    sql = 'SELECT title from t_meizitu_tags_url where scrawl_flag != "1" ORDER BY title asc'
    result = dbhelper.query(sql)
    try:
        if result:
            #遍历数据库中的每个tag
            for tag in result:
                if not os.path.exists(os.path.join(base_url, tag[0])):
                    os.makedirs(os.path.join(base_url, tag[0]))
                os.chdir(base_url + '/' + tag[0])
                sql_tag = 'SELECT html_url FROM t_meizitu_tag_html_urls WHERE tag =' + "'" + tag[0] + "'" + ' ORDER BY html_url asc'
                result_tag = dbhelper.query(sql_tag)
                if not result_tag:
                    print("%s 下没有发现url！", tag)
                else:
                    #处理当前tag的 当前页面 里的相册
                    for page in result_tag:
                        #获得当前页面的 相册链接地址列表
                        current_page_albums_links = get_current_page_albums(page[0])
                        #获取单个相册中图片url 链接地址及 相册名称
                        get_current_album_title_imgs(current_page_albums_links, base_url + '/' + tag[0])                    
                        
                        
        else:
            print("查询异常！")
    except BaseException as e:
        print('操作异常：',e)
    finally:
        dbhelper.close()    
            
    
create_tags_dir('/home/jelly/Meizitu')

