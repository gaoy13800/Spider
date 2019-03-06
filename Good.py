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
        return None

def parse_one_page(html):
    pattern = re.compile('item-title.*?href="(.*?)".*?<h3>\n            \n              (.*?)\n            \n          </h3>',re.S)
    items = re.findall(pattern,html)
    index='0kkkzz.com'
    for item in items:
        yield {
            '链接': index + item[0],
            '标题': item[1]
        }

def get_detail_page(url):
    try:
        data = {
            'ccc': '0kkkzz.com'
        }
        u = url[:36]
        newUrl = u + '?' + urlencode(data)
        response = requests.get(newUrl)
        if response.status_code == 200:
            return response.text
    except Exception:
        return None

def parse_detail_page(detail):
    '''pattern = re.compile('.*?title">(.*?)</h1>.*?1.4em">(.*?)</div>',re.S)'''
    pattern = re.compile('.*?title">(.*?)</h1>.*?1.4em">(.*?)</div>', re.S)
    items = re.findall(pattern, detail)
    for item in items:
        yield {
            '标题': item[0],
            '内容': item[1]
        }
def write_to_txt(content,title):
    if not os.path.exists('D:/小说/'):
        os.makedirs('D:/小说/')
    print("正在保存")
    with open('D:/小说/' + title+'.txt','a',encoding='utf-8') as f:
        f.write('\n'+json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
        print("保存成功")

def main(page):
    url = 'https://0kkzz.com/story/daily-ranking?page='+str(page)
    html = get_one_page(url)
    for item in parse_one_page(html):
        detail = get_detail_page(item.get('链接'))
        title =  item.get('标题')
        print(detail)
        for item in parse_detail_page(detail):
            print("下一步是保存")
            write_to_txt(item.get("内容").translate(str.maketrans('','','<br/>')),title)
if __name__=='__main__':
    main(7)
    for i in range(1,13):
        pass