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

base_url = config.apps[config.env]['sell_api']
sales_url = config.apps[config.env]['sales_api']

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
        print(response)
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

# 创建source
def source_batch_create(source):
    if source.startswith('qd_') and "tk" in source:
        type = 1
        source = source.replace('tk_', '')

        form_body_url = f"/m/learning_materials/download?pageType=44c19bb0a2754bd993e4607f96e927ea&activity=summer-autumn-2020-source&source={source}"
        add_forminfo(form_body_url,phone)
        print("拓客报班表单信息填写成功")

    elif source.startswith('qd_') and "activity" in source:
        type = 2
        source = source.replace('activity_', '')
        print("非拓客报班订单")
    else :
        source = source
        print("非线下渠道订单，自行创建source")
    source_split = source.split('_')
    sale_user_id = source_split[1]
    type_id = source_split[2]
    url = build_url(base_url=sales_url, path="/internal/proxy/saleasyncapi/source/v1/batch-create")
    request_payload = {
        "sourceInfoCreates": [
    {
      "saleUserId": sale_user_id,
      "type": type,
      "typeId": type_id
    }
  ]
    }
    response = http.post(url, json=request_payload)
    if response:
        print("创建source返回：",response)
    source_hash = response['data']['success_sources'][0]['source_hash']
    print("source返回：",source_hash)
    return(source)


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


    db = db_utils.DBUtils()
    uid = db.select(f"SELECT id FROM users WHERE access_token = '{user.access_tokens[0]}';")[0][0]
    # uid = 11638068
    print(uid)

    #插入预设的收货地址
    # db_utils.DBUtils(name='portal').insert(f"INSERT INTO `order_address` (`user_id`, `contact_name`, `contact_phone`, `country`, `province`, `city`, `district`, `street`, `detail`, `is_default`, `status`)VALUES('{uid}', '内部测试', '19000000099', '中国', '广东省', '广州市', '越秀区', '', '123456', 1, 1);", commit=True)
    order_address_id = get_order_address_id(uid)

    sleep(1)
    access_token = db_utils.DBUtils().select(f"SELECT access_token FROM users WHERE id = {uid};")[0][0]
    phone = db_utils.DBUtils().select(f"SELECT phone FROM users WHERE id = {uid};")[0][0]
    # sku_id = "8213"       #拓客报班商品
    # sku_id = "16239"
    # sku_id = "15019"  # 双科   15019,15043
    sku_id = "14881"  # 双科  预发  14267,14337
    # 活动课source
    # source = "qd_74702_activity_11"
    source = "qd_62464_activity_74"
    # 分销员source
    # source = "qd_4410_activity_62"
    # 拓课报班source
    # source ="qd_52828_tk_e98024"
    # source ="qd_62464_tk_901eba"
    # source = "qd_5_tk_028bc9"


    #为拓客报班订单填写表单信息


    # formurl = f"/m/learning_materials/download?pageType=44c19bb0a2754bd993e4607f96e927ea&activity=summer-autumn-2020-source&source={source}"

    source = source_batch_create(source) #使用新的source则需要创建相应source，旧source不需要创建
    if source.startswith('qd_') and "tk" in source:

        form_body_url = f"/m/learning_materials/download?pageType=44c19bb0a2754bd993e4607f96e927ea&activity=summer-autumn-2020-source&source={source}"
        add_forminfo(form_body_url,phone)
        print("拓客报班表单信息填写成功")
    order_id = create_order(sku_id, access_token, source, order_address_id)
    sleep(3)

    # db = db_utils.DBUtils(name='payment')
    # 判断sku_id是否包含逗号，包含则为双科订单，取order_cart_id去支付，否则为单科订单，取order_id去支付
    # if re.search(r',',str(sku_id)):
    #     order_id = db.select(f"SELECT distinct (order_cart_id) FROM sszpay_order WHERE user_id = {uid} and p_order_id is not null;")[0][0]
    # else:
    #     order_id = db.select(f"SELECT order_id FROM sszpay_order WHERE user_id = {uid} and p_order_id is null and product_sku_id  in({sku_id});")[0][0]
    # print(order_id)
    # sleep(1)

    # order_id = 856545531580001
    # print(order_id)

    # order_id = create_order()
    pay_with_remain(order_id=order_id, uid=uid)



