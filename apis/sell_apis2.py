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

base_url = config.apps[config.env]['sell_api']
data = dict()
access_tokens = []

def create_order(sku_id=None, access_token=None):
    url = build_url(base_url=base_url, path="/api/1/pay/create_order")
    request_payload =  {
          'sku_ids': str(sku_id),
          'access_token': str(access_token),
         # 'activity':'3',
          'source':"qd_2652_activity_4"
         #  'source':"qd_2652_tk_771efd"
        }
    response = http.post(url, json=request_payload)
    if response:
        data.update(response)
        data.update(request_payload)
        print(data)

def get_orderid_detail():
    order_id = data.get("data").get("order").get("order_id")
    access_token = data.get("access_token")
    url = build_url(base_url=base_url, path=f"/api/1/pay/get_order_detail?access_token={access_token}&order_id={order_id}")
    print(url)
    response = http.get(url)
    if response:
        print(response.get("code"))
        # print(response)

def add_student(access_tokens:list):
    for access_token in access_tokens:
        sleep(1.5)
        # create_order('8179,8184','14451',access_token)
        create_order('15249',access_token)
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
    


if __name__ == "__main__":
    # 9元分班加人验证脚本
    user = User()
    fake = Faker(locale='zh-CN')
    for _ in range(1):
        user.reg([], fake.name())
    print(user.access_tokens)

    # sleep(2)
    # # access_tokens = ['13305532100_3', '18161071662_3', '18756219108_3', '18283093894_3', '18658390851_3', '15322517617_3', '18751839855_3', '15004020162_3', '13570151531_3', '18876097811_3']
    #add_student(user.access_tokens)
    # access_tokens = ["jerry3"]
    # add_student(access_tokens)
    # sleep(2)
    # db = db_utils.DBUtils()
    # uids = db.select("SELECT student_id FROM clazz_student WHERE clazz_id = 3686 and status = 1;")
    # uids = [uid[0] for uid in uids]
    # print(uids)
    # db_utils.DBUtils().pd_from_sql("SELECT * FROM clazz_student_log order by id desc limit 10;")
    
    # sleep(10)

    # clazz_id = 3680
    # uids = [10925811, 10925812, 10925813, 10925814, 10925815, 10925816, 10925817, 10925818, 10925819, 10925820]
    #  clazz_id =10800
    #  uids = [11520014]
    #  quit_clazz_by_userid(uids, clazz_id)



    #自动使用余额进行支付
    # uid = 11186057
    sku_id = 15249
    db = db_utils.DBUtils()
    uid = db.select(f"SELECT id FROM users WHERE access_token = '{user.access_tokens[0]}';")[0][0]
    print(uid)
    #余额充足
    # db_utils.DBUtils(name='payment').update(f"UPDATE sszpay_remain set user_id={uid} WHERE id  = 338 ;", commit=True)
    #余额不足
    db_utils.DBUtils(name='payment').update(f"UPDATE sszpay_remain set user_id={uid} WHERE id  = 60 ;", commit=True)

    sleep(1)
    access_token = db_utils.DBUtils().select(f"SELECT access_token FROM users WHERE id = {uid};")[0][0]
    create_order(sku_id,access_token)
    sleep(3)

    db = db_utils.DBUtils(name='payment')

    order_id = db.select(f"SELECT order_id FROM sszpay_order WHERE user_id = {uid} and p_order_id is null and product_sku_id= {sku_id};")[0][0]

    sleep(1)
    # order_id = 856545531580001
    # print(order_id)

    pay_with_remain(order_id=order_id,uid=uid)




