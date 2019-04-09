import requests
import time
import json
from requests.exceptions import RequestException
from urllib import parse
import re
import wmi

global s
s = wmi.WMI()

def parseUrl(url):
    requestURL= 'https://met.red/h/material/getCode?'

    headers = {
        'Accept':'text/javascript,application/json,*/*;q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'Content-Length':'65',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        'Host': 'met.red',
        'Origin': 'https://met.red',
        'Referer': 'https://met.red/h/material/index',
        'X-Requested-With': 'XMLHttpRequest'
     }
    cookies = {
        'UM_distinctid': '169dd8348d4415-0b3bcff9566604-454c0a2b-100200-169dd8348d5435',
        'Hm_lvt_6566ca99331702c0cf4223d9fcca30c1': '1554199562,1554357539,1554620391,1554735099',
        'CNZZDATA1274946776': '617502908-1554195801-%7C1554765528',
        'ci_session': '6e9dbf58413a16d8c833add3a2f29187a902be89',
        'Hm_lpvt_6566ca99331702c0cf4223d9fcca30c1': '1554768630'
    }

    FormData = {"type": 2, "url": url}
    # 字典转换k1=v1 & k2=v2 模式
    data = parse.urlencode(FormData)
    new = requestURL + data
    response = requests.post(new,data=data,headers=headers,cookies=cookies)
    try:
        if response.status_code == 200:
            code = json.loads(response.content)
            print( code['msg'])
            return code['data']
    except RequestException:
        return None


def getCode(code):
    requestURL= 'https://met.red/h/material/getDownloadUrl?'
    headers = {
        'Accept':'text/javascript,application/json,*/*;q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'Content-Length':'37',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        'Host': 'met.red',
        'Origin': 'https://met.red',
        'Referer': 'https://met.red/h/material/getDownload',
        'X-Requested-With': 'XMLHttpRequest'
     }
    cookies = {
        'UM_distinctid': '169dd8348d4415-0b3bcff9566604-454c0a2b-100200-169dd8348d5435',
        'Hm_lvt_6566ca99331702c0cf4223d9fcca30c1': '1554199562,1554357539,1554620391,1554735099',
        'CNZZDATA1274946776': '617502908-1554195801-%7C1554765528',
        'ci_session': '6e9dbf58413a16d8c833add3a2f29187a902be89',
        'Hm_lpvt_6566ca99331702c0cf4223d9fcca30c1': '1554768630'
    }

    FormData = {"code": code}
    # 字典转换k1=v1 & k2=v2 模式
    data = parse.urlencode(FormData)
    try:
        new = requestURL + data
        response = requests.post(new, data=data, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return json.loads(response.content)
    except RequestException:
        return None

def parseHtml(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception:
        return None

def parse_detail_page(detail):
    pattern = re.compile('<span class="pic-title fl">(.*?)</span>',re.S)
    return re.findall(pattern, detail)



def get_mainboard_info():
    mainboard=[]
    for board_id in s.Win32_BaseBoard ():
        mainboard.append(board_id.SerialNumber.strip().strip('.'))
    return mainboard


if __name__=='__main__':
    while True:
        machineCode= get_mainboard_info()
        print('您的机器码是：%s'%machineCode)
        with open('registerCode.txt',mode='a+') as f:
            readCode = f.read()
            if(readCode==''):
                inputCode = input("请输入您的注册码(纯数字)：").strip()
                pollCode = int(re.sub('\D', '', inputCode))
                newPollCode = int(re.sub('\D', '', machineCode[0])[-1:]) + 1111
                if (pollCode != newPollCode):
                    print('注册码有误，请核实')
                    continue
                else:
                    with open('registerCode.txt', 'wb') as f:
                        f.write(inputCode.encode())
                        f.close()
                    print('注册码正确')
            elif(int(readCode)==(int(re.sub('\D', '', machineCode[0])[-1:]) + 1111)):
                print('已经注册！')
            f.close()

        global downUrl
        url = input("输入素材地址（输入q退出程序）:").strip()
        if "q" in url:
            break
        content = parseHtml(url)
        title = parse_detail_page(content)[0]
        returnCode = parseUrl(url)
        print("请耐心等待一分钟！")
        time.sleep(60)
        downJson = getCode(returnCode)
        if (downJson['code'] == 1):
            print(downJson['msg'])
            time.sleep(10)
            downUrl = getCode(returnCode)['data']
        else:
            downUrl = downJson['data']
        print("\n" + '-' * 45)
        print("处理成功！")
        print('下载地址是%s'%downUrl)
        print('文件标题是%s'%title)
        print('正在为您下载')
        r = requests.get(downUrl)
        with open(title+'.zip','wb') as f:
            f.write(r.content)
            f.close()
            print("文件下载成功，在当前的目录中！")
        print("\n" + '-' * 45)