# -*- coding: utf-8 -*-



import requests
import asyncio
import aiohttp
import re
from exceptions import ParamsError




absolute_http_url_regexp = re.compile(r"^https?://", re.I)

def get(url):
    response = requests.get(url)
    if response.status_code == 200:
        if response.json()['code'] == 0:
            return response.json()
        else:
            print('[REQUEST FAIL]{}\nresponse:{}'.format(url, response.json()))
    else:
        print('[REQUEST ERROR]{}, \nstatus code:{}'.format(url, response.status_code))


def post(url, json: dict = None, data: str = None):
    if json:
        response = requests.post(url, json=json)
    else:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, headers=headers, data=data.encode('utf-8'))
    if response.status_code == 200:
        if response.json()['code'] == 0:
            return response.json()
        else:
            print('[REQUEST FAIL]{}\nbody:{}\nresponse:{}'.format(url, json if json else data, response.json()))
    else:
        print('[REQUEST ERROR]{}, \nstatus code:{}'.format(url, response.status_code))

def delete(url):
    response = requests.delete(url)
    if response.status_code == 200:
        if response.json()['code'] == 0:
            return response.json()
        else:
            print('[REQUEST FAIL]{}\nresponse:{}'.format(url, response.json()))
    else:
        print('[REQUEST ERROR]{}, \nstatus code:{}'.format(url, response.status_code))

def build_url(base_url, path):
    if absolute_http_url_regexp.match(path):
        return path
    elif base_url:
        return "{}/{}".format(base_url.rstrip("/"), path.lstrip("/"))
    else:
        raise ParamsError("base url missed!")

# async def get(url):
#     print('start')
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             print(await response.text())
#     print('end')
#
#
# async def run():
#     tasks = []
#     for i in range(1, 100):
#
#         tasks.append(asyncio.ensure_future(get('http://courseapi.uae.shensz.local')))
#     await asyncio.wait(tasks)
#
#
if __name__ == '__main__':
    test = build_url(None,"kkkk")
    # print(test)