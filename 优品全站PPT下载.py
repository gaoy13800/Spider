import requests
import re
import json
from requests.exceptions import RequestException
import os

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            r = response.text
            a = r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
        return a
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<li>.*?img_preview.*?src="(.*?)".*?href="(.*?)".*?p-title.*?>(.*?)</a>.*?left">(.*?)</span><span class="right">(.*?)</span>.*?</li>',re.S)
    items = re.findall(pattern,html)
    index = 'http://www.ypppt.com'
    for item in items:
        yield {
            '封面图链接':index + item[0],
            '文章链接': index + item[1],
            '标题': item[2],
            '属性': item[3],
            '浏览量': item[4]
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
            '下载页面链接': item[3]
        }

def get_down_page(detail):
    pattern = re.compile('.*?<div class="de">.*?<h1>(.*?)</h1>.*?分类：</i>(.*?)</li>.*?大小：</i>(.*?)</li>.*?<ul class="down clear">.*?<li><a href="(.*?)">下载地址1.*?',re.S)
    items = re.findall(pattern, detail)
    for item in items:
        yield {
            '标题': item[0],
            '分类': item[1],
            '大小': item[2],
            '下载链接': item[3]
        }
def get_detail_down(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            r = response.text
            #a = r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
        return  r
    except Exception:
        return None

def write_to_file(downUrl,title,classify,imgUrl):
    if 'youpinppt' not in downUrl:
        newurl = 'http://www.ypppt.com'+ downUrl
        r = requests.get(newurl)
        i = requests.get(imgUrl)
        if not os.path.exists('D:/PPT/' + classify +'/'+ title):
            os.makedirs('D:/PPT/' + classify + '/'+title)
        with open('D:/PPT/'+ classify +'/'  + title+'/'+ title+'.rar', "wb") as f:
            f.write(r.content)
            f.close()
        with open('D:/PPT/' + classify + '/'+ title+'/'  + '预览图'+'.jpg', "wb") as k:
            k.write(i.content)
            k.close()
        print("****************正在下载：%s\n" %(title))
    else:
        r = requests.get(downUrl)
        i = requests.get(imgUrl)
        if not os.path.exists('D:/PPT/' + classify +'/' + title):
            os.makedirs('D:/PPT/' + classify + '/' +title)
        with open('D:/PPT/'+ classify +'/'+ title+'/' + title+'.rar', "wb") as f:
            f.write(r.content)
            f.close()
        with open('D:/PPT/' + classify + '/'+ title+'/'  + '预览图'+'.jpg', "wb") as k:
            k.write(i.content)
            k.close()
        print("****************正在下载：%s\n" %(title))

def write_to_txt(content):
    with open('PPT下载链接.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def main(list):
    if list == 1 :
        url='http://www.ypppt.com/moban/'
        html = get_one_page(url)
        for item in parse_one_page(html):
            detail = get_detail_page(item.get('文章链接'))
            imgUrl = item.get('封面图链接')
            for item1 in parse_detail_page(detail):
                get_detail = get_detail_down('http://www.ypppt.com'+item1.get('下载页面链接'))
                for page in get_down_page(get_detail):
                    downUrl = write_to_file(page.get('下载链接'), page.get('标题').split('-')[0].strip(),page.get('分类'),imgUrl)
                    write_to_txt(item)

    else:
        url = 'http://www.ypppt.com/moban/'+'list-'+ str(list) + '.html'
        html = get_one_page(url)
        for item in parse_one_page(html):
            detail = get_detail_page(item.get('文章链接'))
            imgUrl = item.get('封面图链接')
            for item1 in parse_detail_page(detail):
                get_detail = get_detail_down('http://www.ypppt.com'+item1.get('下载页面链接'))
                for page in get_down_page(get_detail):
                    downUrl = write_to_file(page.get('下载链接'), page.get('标题').split('-')[0].strip(),page.get('分类'),imgUrl)
                    write_to_txt(item)

if __name__=='__main__':
    print("*********************精美PPT模版自动下载程序****************************")
    print("*                                                                     *")
    print("*                          By QiYu                                    *")
    print("*                                                                     *")
    print("******************下载文件将会保存在D盘PPT目录***************************\n")
    code = input("请输入授权码：")
    if(code == '6666'):
        print("\n*******************授权码正确，现在开始下载******************************\n")
        for i in range(1,102):
            main(i)
    else:
        errorCode = input("\n*******************授权码有误，请核对后再试******************************\n")