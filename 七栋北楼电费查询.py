# Author: Qiyu
from urllib import request
from urllib import parse
import json

print("-----------------------七栋电费查询By QY--------------------------\n")
num = input("输入您的寝室号（例如7B302）：")
if num[0:2] == '7B':
    url = "http://pay.nit.edu.cn/Pay/CheckRoom"
    values = {"buildname": "7B_2_0_76", "roomname": num, "json": "true"}
    header = {"Accept": "application/json, text/javascript, */*", "Connection": "keep-alive",
              "Content-Type": "application/x-www-form-urlencoded",
              "Cookie": "ASP.NET_SessionId=lkiaiaezi1bzu515mic1zhk5", "Host": "pay.nit.edu.cn",
              "Origin": "http://pay.nit.edu.cn", "Referer": "http://pay.nit.edu.cn/pay/electricity_fee/11",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"}
    data = parse.urlencode(values).encode(encoding='UTF8')
    req = request.Request(url, data, header)  # 生成页面请求的完整数据
    response = request.urlopen(req)  # 发送页面请求
    result = json.loads(response.read())
    print("\n-----------------------------查询--------------------------------\n")
    print("%s剩余电量为:%s\n" % (num, result["msg"].split(',')[-2]))  # 获取服务器返回的页面信息
    num = input("-----------------------------成功--------------------------------")
elif num[0:2] == '3B':
    url = "http://pay.nit.edu.cn/Pay/CheckRoom"
    values = {"buildname": "3B_2_0_72", "roomname": num, "json": "true"}
    header = {"Accept": "application/json, text/javascript, */*", "Connection": "keep-alive",
              "Content-Type": "application/x-www-form-urlencoded",
              "Cookie": "ASP.NET_SessionId=lkiaiaezi1bzu515mic1zhk5", "Host": "pay.nit.edu.cn",
              "Origin": "http://pay.nit.edu.cn", "Referer": "http://pay.nit.edu.cn/pay/electricity_fee/11",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"}
    data = parse.urlencode(values).encode(encoding='UTF8')
    req = request.Request(url, data, header)  # 生成页面请求的完整数据
    response = request.urlopen(req)  # 发送页面请求
    result = json.loads(response.read())
    print("\n-----------------------------查询--------------------------------\n")
    print("%s剩余电量为:%s\n" % (num, result["msg"].split(',')[-2]))  # 获取服务器返回的页面信息
    num = input("-----------------------------成功--------------------------------")
elif num[0:2] == '7A':
    url = "http://pay.nit.edu.cn/Pay/CheckRoom"
    values = {"buildname": "7A_2_0_7", "roomname": num, "json": "true"}
    header = {"Accept": "application/json, text/javascript, */*", "Connection": "keep-alive",
              "Content-Type": "application/x-www-form-urlencoded",
              "Cookie": "ASP.NET_SessionId=lkiaiaezi1bzu515mic1zhk5", "Host": "pay.nit.edu.cn",
              "Origin": "http://pay.nit.edu.cn", "Referer": "http://pay.nit.edu.cn/pay/electricity_fee/11",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"}
    data = parse.urlencode(values).encode(encoding='UTF8')
    req = request.Request(url, data, header)  # 生成页面请求的完整数据
    response = request.urlopen(req)  # 发送页面请求
    result = json.loads(response.read())
    print("\n-----------------------------查询--------------------------------\n")
    print("%s剩余电量为:%s\n" % (num, result["msg"].split(',')[-2]))  # 获取服务器返回的页面信息
    num = input("-----------------------------成功--------------------------------")
else:
    num = input("--------------------您输入的寝室号有误，请重新运行--------------------")