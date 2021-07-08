#!/usr/bin/env python
# -*- coding:UTF-8 -*-


# DESCRIPTION:

import config
from utils import http_utils as http
from utils.utils import build_url, query_json
from utils import db_utils, str_utils
from controllers.renewal_controller import Renewal
from controllers.user_controller_v2 import User
from time import sleep
from faker import Faker
import re
from flask import Flask, request, jsonify

base_url = config.apps[config.env]['sell_api']

data = dict()
access_tokens = []

def create_order(sku_id=None, access_token=None, source=None, order_address_id=None):
    url = build_url(base_url=base_url, path="/api/1/pay/create_order")
    request_payload =  {
          'sku_ids': sku_id,
          #'sku_ids': str(sku_id),
          'access_token': str(access_token),
         # 'activity':'3',
          'source': source,
        #  'source':"qd_2652_tk_771efd"
          'order_address_id': order_address_id
        }
    response = http.post(url, json=request_payload)
    if response:
        data.update(response)
        data.update(request_payload)
        print(data)
    order_id = response.get('data').get("order").get("order_id")
    print("订单id=", order_id)
    return order_id

def get_orderid_detail():
    order_id = data.get("data").get("order").get("order_id")
    access_token = data.get("access_token")
    url = build_url(base_url=base_url, path=f"/sellapi/1/pay/get_order_detail?access_token={access_token}&order_id={order_id}")
    print(url)
    response = http.get(url)
    if response:
        print(response.get("code"))
        # print(response)

def add_forminfo(form_body_url=None,form_body_phone=None):
    url = build_url(base_url=base_url, path="/sellapi/1/config/h5/form")
    request_payload = {
    "url": form_body_url,
    "configType": "44c19bb0a2754bd993e4607f96e927ea",
    "formValues": [
        {
            "key": "name",
            "value": "张三",
            "type": "input",
            "label": "学生姓名"
        },
        {
            "key": "school",
            "value": "越秀小学",
            "type": "input",
            "label": "在读学校"
        },
        {
            "key": "clazz",
            "value": "三年一班",
            "type": "input",
            "label": "班级"
        },
        {
            "key": "phone",
            "value": form_body_phone,
            "type": "phone",
            "label": "报名手机号码（请填写家长联系电话）"
        }
    ],
    "openid": "",
    "unionid": "",
    "openApi": "http://saleapi.uae.shensz.local/sale/api/1/toker/form_submit"
        }
    response = http.post(url, json=request_payload)
    if response:
        data.update(response)
        data.update(request_payload)
        print(data)

#获取收获地址的id
def get_order_address_id(uid):
    db = db_utils.DBUtils()
    # 查询地址的id
    order_address_id = db.select(f"SELECT id FROM  `order_address`  where user_id = {uid};")[0][0]
    # sql2 = """SELECT id FROM  `order_address`  where user_id='${user_id}'"""
    # sql2 = str_utils.custom_replace(sql2, user_id=user_id)
    # result = db_utils.select(sql2)
    # order_address_id = result[0][0]
    print("order_address_id=",order_address_id)
    return order_address_id

def add_student(access_tokens:list):
    for access_token in access_tokens:
        sleep(1.5)
        # create_order('8179,8184','14451',access_token)
        create_order(str(sku_id),access_token)
        get_orderid_detail()  

def quit_clazz_by_userid(uids, clazz_id):
    test = Renewal()
    for uid in uids:
        # 获取orderID
        order_id = str_utils.int2list(test.get_order_id_from_payment(uid,clazz_id))
        # 退课
        test.quit_clazz(order_id)
        
# 使用余额进行支付
def pay_with_remain(order_id=None, uid=None):
    db = db_utils.DBUtils()
    access_token = db.select(f"SELECT access_token FROM users WHERE id = {uid};")[0][0]
    url = build_url(base_url=base_url, path=f"/sellapi/1/pay/create_order_payment?access_token={access_token}")
    request_payload  = f'order_id={order_id}&channel=remainpay&device_info=APP'
    response = http.post(url, data=request_payload)
    print(response)
    


app = Flask(__name__)
@app.route('/createorder', methods=['get', 'post'])

def get_data():
    sku_id = request.json.get("sku_id")
    source = request.json.get("source")
    print(sku_id)
    user = User()
    fake = Faker(locale='zh-CN')
    for _ in range(1):
        user.reg([], fake.name())
    print(user.access_tokens)
    db = db_utils.DBUtils()
    uid = db.select(f"SELECT id FROM users WHERE access_token = '{user.access_tokens[0]}';")[0][0]
    print(uid)
    order_address_id = get_order_address_id(uid)

    sleep(1)
    access_token = db_utils.DBUtils().select(f"SELECT access_token FROM users WHERE id = {uid};")[0][0]
    phone = db_utils.DBUtils().select(f"SELECT phone FROM users WHERE id = {uid};")[0][0]

    order_id = create_order(sku_id,access_token,source,order_address_id)
    sleep(3)
    pay_with_remain(order_id=order_id,uid=uid)
    #为拓客报班订单填写表单信息
    if "tk" in source:
        form_body_url = f"/m/learning_materials/download?pageType=44c19bb0a2754bd993e4607f96e927ea&activity=summer-autumn-2020-source&source={source}"
        add_forminfo(form_body_url,phone)
        print("拓客报班表单信息填写成功")
        return("拓客报班订单支付成功")
    elif "," in sku_id:
        print("非拓客报班订单")
        return ("双科联报订单支付成功")
    else:
        return ("单科订单支付成功")
    # formurl = f"/m/learning_materials/download?pageType=44c19bb0a2754bd993e4607f96e927ea&activity=summer-autumn-2020-source&source={source}"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

