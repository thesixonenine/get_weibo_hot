import requests
from bs4 import BeautifulSoup
from flask import Flask
from urllib import parse


def get_baidu_hot():
    f = requests.get('http://top.baidu.com/buzz?b=1').text.encode('latin-1').decode('GBK')
    soup = BeautifulSoup(f, features="lxml")
    list_tag = soup.find(attrs={"class", "mainBody"}).find(attrs={"class", "list-table"})
    trs = list_tag.find_all('tr')
    json_str = {}
    for i in range(1, 8):
        tr = trs[i]
        if tr.get('class') is not None:
            if tr.get('class')[0] == 'item-tr':
                continue
        tds = tr.find_all('td')
        keyword = tds[1]
        word = keyword.text.replace('search', '').strip()
        json_str[word] = 'https://www.baidu.com/s?wd=' + parse.quote(word)
    return json_str.__str__()


def get_weibo_hot():
    """
    获得微博热点
    :return:
    """
    html_doc = requests.get("https://s.weibo.com/top/summary?cate=realtimehot").text
    soup = BeautifulSoup(html_doc, features="lxml")
    tags = soup.select('.td-02')
    json_str = {}
    for tag in tags:
        json_str[tag.find('a').text] = 'https://s.weibo.com' + tag.find('a')['href']
    return json_str.__str__()


# Connect to Redis
# redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


@app.route("/")
def weibo_hot_default():
    return get_weibo_hot()


@app.route("/weibo")
def weibo_hot():
    """
    微博
    :return:
    """
    return get_weibo_hot()


@app.route("/baidu")
def baidu_hot():
    return get_baidu_hot()
    # try:
    #     visits = redis.incr("counter")
    # except RedisError:
    #     visits = "<i>cannot connect to Redis, counter disabled</i>"
    #
    # html = "<h3>Hello {name}!</h3>" \
    #        "<b>Hostname:</b> {hostname}<br/>" \
    #        "<b>Visits:</b> {visits}"
    # return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)


if __name__ == "__main__":
    # 测试是否会自己构建
    # 获取微博最新的热搜及跳转链接
    # / 获取微博的最新热搜
    # /weibo 获取微博的最新热搜
    # /baidu 获取百度的最新热搜
    print("开始运行在8080端口...")
    app.run(host='0.0.0.0', port=8080)
