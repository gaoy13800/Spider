import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
def get_one_page(url):
    try:
        header = {"Accept": "application/json, text/javascript, */*", "Connection": "keep-alive","User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36","X-Requested-With":"XMLHttpRequest"}
        respose = requests.get(url,headers=header)
        if respose.status_code == 200:
            return respose.text
        return None
    except Exception:
        return None

def paesr_one_page(html):
    pattern = re.compile('<dd>.*?board-index-.*?">(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            '排名':item[0],
            '封面图': item[1],
            '电影名': item[2],
            '主演': item[3].strip()[3:],
            '上映时间': item[4].strip()[5:],
            '评分': item[5]+item[6]
        }

def write_to_file(content):
    with open('猫眼电影Top100.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url = "http://maoyan.com/board/4?offset="+str(offset)
    html = get_one_page(url)
    for item in paesr_one_page(html):
        print(item)
        write_to_file(item)

if __name__=='__main__':
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])