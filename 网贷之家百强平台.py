import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
import re

def get_page_index(currentPage):
    data={
        'filter':'e3-e2',
        'show': '1',
        'sort':'3',
        'currentPage':currentPage
    }
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'deflate,br',
        'Accept-Language':'zh - CN,zh;q=0.9,en;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0(Windows NT 6.2;WOW64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/63.0.3239.132 Safari/537.36',
        'Host': 'www.wdzj.com',
        'Cookie': 'ki1e_2132_saltkey=h2kK4krN;ki1e_2132_lastvisit=1530010698;ki1e_2132_pc_size_c=0;ki1e_2132_atarget=1;uab_collina=153001429360230722473516;Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1530014294,1530066609;ki1e_2132_viewid=tid_5073606;ki1e_2132_forum_lastvisit=D_15_1530067147;ki1e_2132_sendmail=1;ki1e_2132_lastact=1530067148%09connect.php%09check;Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1530067142'
     }
    url ='https://www.wdzj.com/dangan/search?' + urlencode(data)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        print("请求错误")
        return None

def parse_one_page(html):
    pattern = re.compile('itemTitle.*?<h2><a href="/dan.*?_blank">(.*?)</a>.*? <li>(.*?)</li>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        if item:
            yield {
                '平台名称': item[0],
                '状态': item[1],
            }
        else:
            pass

def write_to_txt(content):
    with open('问题平台.txt','a',encoding='utf-8') as f:
        f.write('\n'+json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
        print("保存成功")


def main():
    s = 0
    for i in range(1, 173):
        html = get_page_index(i)
        for item in parse_one_page(html):
            s = s + 1
            print("正在保存第%d家，名称：%s，状态：%s" % (s, item.get("平台名称"),item.get("状态")))
            write_to_txt(item)
    sc = input("**************已成功保存百强平台*********")
if __name__=="__main__":
    main()