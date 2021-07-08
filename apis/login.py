import requests
import json

url = "http://salemanager.uae.shensz.local/salemanagerapi/api/1/auth/login"
headers = {'Accept': 'application/json, text/plain, */*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Content-Length': '73',
           'Content-Type': 'application/json',
           'Host': 'salemanager.uae.shensz.local',
           'Origin': 'http://salemanager.uae.shensz.local',
           'Referer': 'http://salemanager.uae.shensz.local/salemanager/login?from=http%3A%2F%2Fsalemanager.uae.shensz.local%2Fsalemanager%2Flogin%2FresetPwd',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
           }
data = {"account":"13201234567",
        "password":"a123456",
        "serial_number":"A0000001"}

response =requests.post(url,headers =headers,data =json.dumps(data))
print(response.text)
print(response.cookies)