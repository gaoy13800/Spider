import requests
import random
import os
from PIL import Image

import urllib3
urllib3.disable_warnings()
def get_Verifynum(url):
	global session
	r= session.get("https://www.shangxueba.com/ask/VerifyCode2.aspx",verify=False)
	with open('temp.jpg','wb+') as f:
		f.write(r.content)
	image=Image.open('temp.jpg')
	image.show()
	Verifynum=input("\n输入验证码:")
	image.close()
	os.remove("temp.jpg")
	return Verifynum
def verifyfirst(Verifynum):
	global session
	data={
			"Verify": Verifynum,
			"action": "CheckVerify",
		}
	session.post("https://www.shangxueba.com/ask/ajax/GetZuiJia.aspx",data=data)
def get_ans_html(Verifynum,dataid):
	global session
	data={
		"phone":"",
		"dataid": dataid,
		"action": "submitVerify",
		"siteid": "1001",
		"Verify": Verifynum,
	}
	r=session.post("https://www.shangxueba.com/ask/ajax/GetZuiJia.aspx",data=data)
	return r.text
def write(html_data):
	html="""
	<html>
	<head>
	</head>
	<body>
	<hr>
	<div style="width:600px;margin:0 auto">
	%s
	</div>
	
	</body>
	</html>

	"""%(html_data)
	with open("anser.html","w+",encoding="ANSI") as f:
		f.write(html)

if __name__ == '__main__':
	global session
	while True:
		session = requests.session()
		session.headers.update({"X-Forwarded-For":"%d.%d.%d.%d"%(random.randint(120,125),random.randint(1,200),random.randint(1,200),random.randint(1,200))})
		print("=========================闲鱼商家c***qy7客户专享版本=======================\n")
		print("最好不要放在系统盘或桌面，因为需要创建html文件来保存答案，系统盘可能需要权限\n")
		url = input("输入您要查看的网址，输入q结束本程序：")
		url = url.strip()
		if "q"in url :
			break
		if "html" not in url or "https" not in url:
			print("url 格式不对")
			continue
		dataid=url.split("/")[-1].replace(r".html","")
		verifynum = get_Verifynum(url)
		verifyfirst(verifynum)
		html=get_ans_html(verifynum,dataid)
		write(html)
		print("\n\n答案获取成功！！\n\n在本程序同一个目录生成的的anser.html中查看\n\n============================运行结束=====================================\n")