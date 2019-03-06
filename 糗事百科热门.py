import requests
import re
import json
from requests.exceptions import RequestException
import os
from urllib.parse import urlencode

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print("到头了")
        return None

def parse_one_page(html):
    pattern = re.compile('<h2>(.*?)</h2>.*?content.*?<span>(.*?)</span>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        if item:
            yield {
                '作者': item[0],
                '内容': item[1]
            }
        else:
            pass

def write_to_txt(content):
    with open('糗事百科热门笑话.txt','a',encoding='utf-8') as f:
        f.write('\n'+json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
        print("保存成功")

def main():
    s = 0
    for i in range(1, 14):
        url = 'https://www.qiushibaike.com/text/page/'+str(i)+'/'
        html = get_one_page(url)
        for item in parse_one_page(html):
            s=s+1
            print("正在保存第%d条，作者：%s"%(s,item.get("作者").translate(str.maketrans('','','\n'))))
            write_to_txt(item.get("内容").translate(str.maketrans('','','<br/>\n\u0001')))
if __name__=='__main__':
    main()