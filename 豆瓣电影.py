import requests
import json
from requests.exceptions import RequestException
from urllib.parse import urlencode

def get_one_page(url,start,genres):
    data={
        'sort':'T',
        'range': '0,10',
        'tags':'电影',
        'start':start,
        'genres': genres
    }
    try:
        newURL = url + urlencode(data)
        response = requests.get(newURL)
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield{
                '名字': item.get('title'),
                '评分': item.get('rate'),
                '导演':item.get('directors'),
                '主演': item.get('casts'),
                '封面图': item.get('cover'),
            }

def write_to_txt(content,genres):
    with open('豆瓣'+genres+'电影排行榜.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def main():
    s = 0
    for start  in range(0,10):
        genres = "动作"
        url = 'https://movie.douban.com/j/new_search_subjects?'
        html = get_one_page(url,start*20,genres)
        for detail in parse_page_index(html):
            s = s + 1
            print("正在爬取第%d条：%s"%(s,detail))
            write_to_txt(detail,genres)
if __name__=='__main__':
    main()