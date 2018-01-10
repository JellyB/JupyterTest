import db
import user_agent
import re
import requests

url_proxy = 'http://www.xicidaili.com/nt/'
num = 2  # 爬取页数，前两页
table_name = 't_meizitu_proxy_ip'


def get_random_ip():
    sql = ''
    dbhelper = db.HELper()


def ip_test(ip, headers, url_for_test='https://www.baidu.com', set_timeout=10):
    try:
        rp = requests.get(
            url_for_test,
            headers=headers,
            proxies={
                'http': ip[0] + ':' + ip[1]},
            timeout=set_timeout)
        if rp.status_code == 200:
            return True
        else:
            return False

    except BaseException as e:
        return False


def scrawl_ip(url_proxy, num, headers, url_for_test='https://www.baidu.com'):
    ip_list = []
    dbhelper = db.DBHelper()
    for num_page in range(1, num + 1):
        url_proxy = url_proxy + str(num_page)
        resp = requests.get(url_proxy, headers=headers, timeout=10)
        resp.encoding = 'utf-8'
        html_content = resp.text

        pattern = re.compile(
            '<td class="country">.*?alt="Cn" />.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>',
            re.S)
        iterms = re.findall(pattern, html_content)
        for ip in iterms:
            if ip_test(ip, headers, url_for_test):
                print('测试通过，IP地址为' + str(ip[0]) + ':' + str(ip[1]))
                ip_list.append(ip[0] + ':' + ip[1])
                my_dict = {'ip': ip[0] + ':' + ip[1]}
                if dbhelper.check_exist(table_name, my_dict):
                    continue
                dbhelper.insert(table_name, my_dict)
            else:
                print('测试失败！')
    dbhelper.close()
    return ip_list


headers = user_agent.constructHeaders()
scrawl_ip(url_proxy, num, headers)
