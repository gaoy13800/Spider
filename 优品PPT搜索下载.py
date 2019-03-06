import requests
import re
import json
from requests.exceptions import RequestException
import os
from urllib.parse import urlencode
import sys
import time

def get_one_page(keyWord,size):
    try:
        data = {
            'keyword': keyWord,
            'searchtype': 'titlekeyword',
            'kwtype': 1,
            'pagesize': size,
            'PageNo': 1,
        }
        url = 'http://www.ypppt.com/p/search.php?' + urlencode(data)
        response = requests.get(url)
        if response.status_code == 200:
            r = response.text

        return r
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<li>.*?img_preview.*?src="(.*?)".*?href="(.*?)".*?_blank"(.*?).*?red.*?>(.*?)</font>(.*?)</a>.*?left">(.*?)</span><span class="right">(.*?)</span>.*?</li>',re.S)
    items = re.findall(pattern,html)
    if(items.__len__()==0):
        print("抱歉，暂无符合您需要的资源")
    else:
        index = 'http://www.ypppt.com'
        for item in items:
            yield {
                '封面图链接':index + item[0],
                '文章链接': index + item[1],
                '标题': item[2]+item[3]+item[4],
                '时间': item[5],
                '浏览量': item[6]
            }

def get_detail_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            r = response.text
            a = r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
        return a
    except Exception:
        return None

def parse_detail_page(detail):
    pattern = re.compile('<h1>(.*?)</h1>.*?分类：</i>(.*?)</li>.*?大小：</i>(.*?)</li>.*?<div class="button">.*?<a href="(.*?)".*?down-button',re.S)
    items = re.findall(pattern, detail)
    for item in items:
        yield {
            '标题': item[0],
            '分类': item[1],
            '大小': item[2],
            '下载链接': item[3]
        }

def write_to_file(downUrl,title,classify,imgUrl):
    if 'youpinppt' not in downUrl:
        newurl = 'http://www.ypppt.com'+ downUrl
        r = requests.get(newurl)
        i = requests.get(imgUrl)
        if not os.path.exists('D:/PPT/'  +'/'+ title):
            os.makedirs('D:/PPT/'  + '/'+title)
        with open('D:/PPT/' +'/'  + title+'/'+ title+'.rar', "wb") as f:
            f.write(r.content)
            f.close()
        with open('D:/PPT/'  + '/'+ title+'/' + title + '.jpg', "wb") as k:
            k.write(i.content)
            k.close()

        print("\n****************正在下载：%s\n" %(title))
    else:
        r = requests.get(downUrl)
        i = requests.get(imgUrl)
        if not os.path.exists('D:/PPT/'  +'/' + title):
            os.makedirs('D:/PPT/'  + '/' +title)
        with open('D:/PPT/' +'/'+ title+'/' + title+'.rar', "wb") as f:
            f.write(r.content)
            f.close()
        with open('D:/PPT/'  + '/'+ title+'/' + title + '.jpg', "wb") as k:
            k.write(i.content)
            k.close()
        print("\n****************正在下载：%s\n" %(title))

def write_to_txt(content,keyWord):
    with open(keyWord+'PPT下载链接.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def main(keyWord,size):
        html = get_one_page(keyWord,size)
        for item in parse_one_page(html):
            detail = get_detail_page(item.get('文章链接'))
            imgUrl = item.get('封面图链接')
            for item in parse_detail_page(detail):
                downUrl = write_to_file(item.get('下载链接'), item.get('标题'), item.get('分类'), imgUrl)
                write_to_txt(item,keyWord)
            errorCode = input("\n*************************执行完毕**************************************\n")


if __name__=='__main__':
    print("*********************精美PPT模版自动下载程序****************************")
    print("*                                                                     *")
    print("*                          By QiYu                                    *")
    print("*                                                                     *")
    print("******************下载文件将会保存在D盘PPT目录***************************\n")
    code = input("请输入授权码：")
    if (code == '6666'):
        print("\n**********************授权码正确****************************************\n")
        keyWord = input("请输入您要下载的关键字：")
        size = input("请输入您要下载数量：")
        main(keyWord,size)
    else:
        errorCode = input("\n*******************授权码有误，请核对后再试******************************\n")