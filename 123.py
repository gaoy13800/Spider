import requests
from bs4 import BeautifulSoup

def get_verifynum(i): # 网址的验证码逻辑是先去这个网址获取验证码图片，提交计算结果到另外一个网址进行验证。
    url =[]
    title =[]
    try:
        s = requests.session()
        data1 = {
            "username": "15666666666",
            "password": "15666666666",
        }
        header = {
            "Accept": "*/*",
            "Connection": "keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36","X-Requested-With":"XMLHttpRequest"
                  }
        cookies = {'PHPSESSID': 'pnhope6f2bjn7h2vafqdouj931'}
        a= s.post("http://www.gguuy.top/admin.php?s=/admin/public/login.html", headers=header,data=data1,cookies=cookies,verify=False).text # 核查验证码正确性

        url1 ='http://www.gguuy.top/admin.php?s=/admin/con/edit/id/'+i+'.html'
        header = {"Accept": "application/json, text/javascript, */*", "Connection": "keep-alive","User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36","X-Requested-With":"XMLHttpRequest"}
        respose = s.get(url1,headers=header,cookies=cookies)
        if respose.status_code == 200:
            soup = BeautifulSoup(respose.text, "html.parser")
            title1 = soup.find('input',attrs={"name": "title"})['value']  # 抓取平台名字
            src = soup.find('input', attrs={"name": "src"})['value']  # 抓取url
            if title1=='':
                pass
            else:
                if 'baidu' not in src and 'weixin' not in src:
                    string = title1+'-'+url1
                    return string
                else:
                    pass
    except Exception:
        return None



def main():
    url = []
    j=1
    for i in range (300,1000):
        url1 = get_verifynum(str(i))
        if url1:
            with open('lianjie.txt', 'a+', encoding='utf-8') as f:
                f.write(url1+ '\n')
                f.close()
            print("第%s条数据"%j)
            j=j+1
if __name__=='__main__':
    main()