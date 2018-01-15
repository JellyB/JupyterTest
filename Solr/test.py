import urllib.parse
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("main")
tags = ['<a class="tag" href="/tag/小说">小说</a>,\
<a class="tag" href="/tag/随笔">随笔</a>,\
<a class="tag" href="/tag/日本文学">日本文学</a>,\
<a class="tag" href="/tag/散文">散文</a>,\
<a class="tag" href="/tag/诗歌">诗歌</a>,\
<a class="tag" href="/tag/童话">童话</a>,\
<a class="tag" href="/tag/名著">名著</a>,\
<a class="tag" href="/tag/港台">港台</a>']

for tag in tags:
    print(tag)
    #print(urllib.parse.urlencode(str(tag)))


def parser_data(data):
    if len(str(data).split("-")) > 2:
        data = str(data).split("-")[0] + "-" + str(data).split("-")[1] + "-" + str(data).split("-")[2] +  " 12:12:12"
        return data
    if len(str(data).split("-")) <= 2:
        data = str(data).split("-")[0] + "-" + str(data).split("-")[1] + "-00 12:12:12"
        return data

data = "2017-2-7"
logger.error(parser_data(data))