#!/usr/bin/env python
# -*- coding:UTF-8 -*-


# DESCRIPTION:


# vscode解决包路径问题
# import sys,os
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
# sys.path.append(BASE_DIR)


import config
from time import sleep
from utils import http_utils as http
from utils import db_utils
from utils.time_utils import time_delta, time_format
from controllers import renewal_controller


portal_api = config.apps[config.env]['portal_api']
sell_api = config.apps[config.env]['sell_api']


def create_clazz(name: str, year: int, grade: list, mentor_id: int, clazz_type: int,
                 start_time: str, stop_time: str, time_type: int, time_text: str, level: int,
                 star_count: int, tags: list, time_seq: int, is_staff: int, master_student_limit: int,
                 time_type_detail: list
                 ):
    url = portal_api + '/api/1/clazz/create_clazz?access_token=zf'
    request_payload = {
        'clazzId': 0,
        'name': name,
        'year': year,
        'grade': grade,
        'mentorId': mentor_id,
        'type': clazz_type,
        'startTime': start_time,
        'stopTime': stop_time,
        'timeType': time_type,
        'timeText': time_text,
        'level': level,
        'startCount': star_count,
        'tags': tags,
        'timeSeq': time_seq,
        'isStaff': is_staff,
        'masterStudentLimit': master_student_limit,
        'timeTypeDetail': time_type_detail
    }
    response = http.post(url, json=request_payload)
    if response:
        clazz_id = response['data']['clazzId']
        print('[CREATE CLAZZ SUCCESS]clazz_id:{}'.format(clazz_id))
        return clazz_id


def create_clazz_plan(title: str, clazz_plan_type: int, start_time: str, stop_time: str, seq: int, clazz_id: int):
    url = portal_api + '/api/1/clazz/create_clazz_plan?access_token=zf'
    # huangguangjie
    request_payload = {
        'title': title,
        'type': clazz_plan_type,
        'startTime': start_time,
        'stopTime': stop_time,
        'seq': seq,
        'clazzId': clazz_id
    }
    response = http.post(url, json=request_payload)
    if response:
        clazz_plan_id = response['data']['clazzPlanId']
        print('[CREATE CLAZZ_PLAN SUCCESS]{}'.format(response['data']))
        return clazz_plan_id



# 创建小班
def create_team(clazz_id: int, team_level: int=1, is_old_team: int=0, name: str='',  team_name: str='') -> int:
    url = portal_api + '/api/1/clazz/create_team?access_token=zf'
    request_payload = {
        "name": name,
        "teamLevel": team_level,
        "isOldTeam": is_old_team,
        "clazzId": clazz_id,
        "teamName": team_name
    }
    response = http.post(url, json=request_payload)
    if response:
        team_id = response['data']['teamId']
        print('[CREATE TEAM SUCCESS]{}'.format(response['data']))
        return team_id


# 创建商品并上架
def create_product(product_title: str, price: float, clazz_id : int ):
    url = portal_api + '/api/1/clazz/create_product?access_token=zf'
    request_payload = {
        "title":product_title,
        "price":price,
        "skuNum":-1,
        "deliveryType":2,
        "teamLevel":1,
        # "saleStartAt":null,
        # "saleEndAt":null,
        "hideMall":0,
        "status":1,
        "clazzId":clazz_id
    }
    response = http.post(url, json=request_payload)
    if response:
        print(response)
        sku_id = response['data']['skuId']
        return sku_id

# 删除商品库存控制
def clear_stock(sku_id: str):
    # sku_ids = int(sku_id)
    db = db_utils.DBUtils(name='payment')
    stock_ids = db.select(f"SELECT ss.id FROM sszpay_product sp LEFT JOIN sszpay_stock_product ssp ON sp.sku_id = ssp.sku_id LEFT JOIN sszpay_stock ss ON ssp.stock_id = ss.id WHERE sp.sku_id = {sku_id} AND ss.status = 1 AND ssp.status = 1 and ss.type = 3;")
    print(stock_ids)
    a = 0
    for _ in range(len(stock_ids)):
        stock_id = stock_ids[a][0]
        url = portal_api + f'/api/1/stock/{stock_id}?access_token=zf'
        http.delete(url)
        a = a + 1
    print(sku_id + "商品库存控制删除成功")


# 内部报班优化
def apply_clazz_student_nice(uid: int,clazz_id: int):
    url = portal_api + '/api/1/clazz/apply_clazz_for_individual?access_token=zf'
    request_payload = {}
    renewal = renewal_controller.Renewal()
    if clazz_id:
        sku_id = db_utils.DBUtils(name='payment').select("select sku_id from sszpay_product_attr where attr_key = 'clazz_ids' and attr_value = {} and status = 1;".format(clazz_id))[0][0]
    # 判断是int转成map对象方便后续转list（int）的情况
    if isinstance(uid,int):
        uid = map(int, str(uid).split(" "))
    team_id = renewal.get_team_id(clazz_id)
    request_payload['student_ids'] = list(uid)
    request_payload['clazz_id'] = clazz_id
    request_payload['sku_id'] = sku_id
    request_payload['team_id'] = team_id
    data = {"team_level":1,"reason":"1","is_staff":0,"apply_by":"ids"}
    request_payload.update(data)
    response = http.post(url, json=request_payload)
    if response:
        msg = response["msg"]
        print('[APPLY CLAZZ SUCCESS]{}'.format(response['data']))


# 审批绿色通道
def create_exchange_clazz(reason_type: int, to_sku_id: int, to_team_id: int, order_id: int):
    url = portal_api + '/api/1/dingtalk_approve/create_exchange_clazz?access_token=zf'
    request_payload = {
        "reasonType":reason_type,
        "toSkuId":to_sku_id,
        "toTeamId":to_team_id,
        "reason":"test",
        "reasonImgUrls":["https://static.guorou.net/course-static/df9c42b1083d47c3a9ff8ed671270606.jpg"],
        "orderId":order_id
    }
    request_payload["isGreen"] = True
    response = http.post(url, json=request_payload)
    if response:
        print(response)


# 发起退课
def create_clazz_quit(order_id: int):
    url = portal_api + '/api/1/clazz_quit/create_clazz_quit?access_token=zf'
    request_payload = {
        'orderId': order_id,
        'quitType': 1,
        'applyAmount': 0,
        'applyReason': '你猜',
        'reason': '你猜',
        'reasonImgUrls': ['https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1579165013&di=33423a6be2b157ff31c693900cc1dfd7&src=http://b-ssl.duitang.com/uploads/item/201606/14/20160614224510_HwyZv.thumb.700_0.jpeg',],
    }
    response = http.post(url, json=request_payload)
    if response:
        print(response)

# 同意退课
def create_quit_approval_finish(approval_code: int):
    url = portal_api + '/api/1/clazz_quit/approval/finish?access_token=zf'
    request_payload = {
        'approval_code': approval_code,
        'result': 'AGREE',
    }
    response = http.post(url, json=request_payload)
    if response:
        print(response)

# 调小班不走审批直接调接口
def change_team(student_id: int, clazz_id: int, team_id: int ):
    url = portal_api + '/api/1/clazz/change_team?access_token=zf'
    
    request_payload = {
        'student_id': student_id,
        'clazz_id': clazz_id,
        'team_id': team_id
    }
    response = http.post(url, json=request_payload)
    if response:
        print(response)

# 调班主任
def exchange_team_master(team_id: int, from_master_id: int, to_master_id: int):
    url = portal_api + '/api/1/clazz/exchange_team_master?access_token=zf'
    request_payload = {
        'team_id': team_id,
        'to_master_id': to_master_id,
        'from_master_id': from_master_id,
    }
    response = http.post(url, json=request_payload)
    if response:
        print(response)

# 不走审批调账号
def exchange_order_user(order_id: int, to_user_id: int):
    url = portal_api + '/api/1/pay/exchange_order_user?access_token=zf'
    request_payload = {
        'order_id': order_id,
        'user_id': to_user_id,
    }
    response = http.post(url, json=request_payload)
    if response:
        print(response)

# 调课程
def exchange_clazz(uid: int, clazz_id: int, to_clazz_id: int,is_temp: bool, team_id= None):
    renewal = renewal_controller.Renewal()
    order_id = renewal.get_order_id_from_payment(uid, clazz_id)
    sku_id = renewal.get_sku_id(to_clazz_id)
    if not team_id:
        team_id = renewal.get_team_id(to_clazz_id)
    url = portal_api + '/api/1/pay/exchange_order?access_token=zf'
    request_payload = {
        'order_id': order_id,
        'sku_id': sku_id,
        'team_id': team_id,
        'is_temp': True if is_temp else False
    }
    response = http.post(url, json=request_payload)
    if response:
        print(response)

# 学生自己调个课程走的是sellapi接口
def student_exchange_clazz(uid: int, clazz_id: int ,to_clazz_id: int):
    renewal = renewal_controller.Renewal()
    access_token = renewal.uid2token(uid)
    order_id = renewal.get_order_id_from_payment(uid, clazz_id)
    sku_id = renewal.get_sku_id(to_clazz_id)
    url = sell_api + "/api/1/clazz/exchange_clazz?access_token={}".format(access_token)
    request_payload = {
        'order_id': order_id,
        'sku_id': sku_id,
        'comment': '我自愿的',
    }
    response = http.post(url, json=request_payload)
    if response:
        print(response)

# 注册后台运营账号


if __name__ == "__main__":


    # uid = 11615177
    # create_product("test", 0, 3686)

    # uids = [10981803,11041069,11046868,11079102]
    # uids = db_utils.DBUtils().select("SELECT student_id FROM clazz_student WHERE   team_id in (SELECT t.id FROM team  t LEFT JOIN clazz c on t.clazz_id = c.id WHERE t.master_id = 10755092 AND c.`year`=2020 AND c.`type`= 2 and t.status=1) and status =1;")
    # uids = [uid[0] for uid in uids]
    # print(uids)
    # # clazz_ids = [1793,1987,1424]
    # # # # 报春季班、四年级数学
    # for uid in uids:
    #     apply_clazz_student_nice(uid, clazz_id=3166)
    # apply_clazz_student_nice(uid, clazz_id=3225)
    # apply_clazz_student_nice(uid, clazz_id=2078)
    # apply_clazz_student_nice(uid, clazz_id=3018)

    
    # # 报春季班、四年级数学
    # apply_clazz_student_nice(uid, clazz_id=1424)


    # # # 报春季班、四年级语文
    # apply_clazz_student_nice(uid, clazz_id=1758)

    # # # 报春季班、四年级英语
    # apply_clazz_student_nice(uid, clazz_id=1433)

    # 另外的四年级数学  插班
    # apply_clazz_student_nice(uid, clazz_id=1429)

    # 另外的四年级数学  插班
    # apply_clazz_student_nice(uid, clazz_id=1431)


     # 报秋季班、五年级数学，构成续报
    # apply_clazz_student_nice(uid, clazz_id=1987)

    # 报秋季班、四年级数学，构成续报
    # apply_clazz_student_nice(uid, clazz_id=1973)

    # 报不构成续报的秋季班、五年级英语
    # apply_clazz_student_nice(uid, clazz_id=1997)

    # 报不构成续报的秋季班、四年级英语
    # apply_clazz_student_nice(uid, clazz_id=1983)


    # 报不构成续报的秋季班、五年级语文
    # apply_clazz_student_nice(uid, clazz_id=1995)

    # sleep(1)

    
    # 永久调课
    # data = {"reasonType":3,"toSkuId":11478,"toTeamId":17988,"reasonTag":1,"reason":"1","reasonImgUrls":["https://static.guorou.net/course-static/7974261c6c03410db26037db527b51ab.jpg"],"orderId":8683348807500001,"exchangeClazzTagId":1}
    # uid = 145179
    # exchange_clazz(uid=uid, clazz_id=2079, to_clazz_id=2082, is_temp=False, team_id=94100)
    # exchange_clazz(uid=uid, clazz_id=3011, to_clazz_id=3012, is_temp=False)
    # exchange_clazz(uid=uid, clazz_id=3012, to_clazz_id=3011, is_temp=False)
    # exchange_clazz(uid=uid, clazz_id=2079, to_clazz_id=2511, is_temp=False,team_id=94700)
    # exchange_clazz(uid=uid, clazz_id=3011, to_clazz_id=3019, is_temp=False)

    # exchange_clazz(uid=uid,clazz_id=clazz_ids[0], to_clazz_id=clazz_ids[2], is_temp=False)

    # data1 = {"reasonType":3,"toSkuId":11819,"toTeamId":61314,"reasonTag":1,"reason":"1","reasonImgUrls":["https://static.guorou.net/course-static/87d8cfb863a44cb4ae1244f93bad3b9b.jpg"],"orderId":8683484026200001,"exchangeClazzTagId":1}
    # order_id = 8684781053400001

    # exchange_clazz(uid=uid,clazz_id=1793, to_clazz_id=1424, is_temp=False)


    # # 临时调课
    # order_id = 8640489426000001
    # exchange_clazz(order_id=order_id, sku_id=11478, team_id=47276, is_temp=True)


    # 调小班
    # data = {"reasonType":2,"toTeamId":39227,"reason":"test","reasonImgUrls":["https://static.guorou.net/course-static/f6d11046216f47c8a47b654033054a00.jpg"],"studentId":131,"clazzId":1793}
    # change_team(student_id=149166, clazz_id=2079, team_id=94055)
    # 不同班主任

    # change_team(student_id=149166, clazz_id=2079, team_id=94049)
    # sleep(1)
    # db_utils.DBUtils().pd_from_sql("SELECT * FROM clazz_student_log order BY id DESC limit 10;")
    


    # 调班主任

    # data = {"teamId":55353,"fromMasterId":null,"toMasterId":10706952,"reason":"无","reasonImgUrls":[],"reasonType":2}
    # exchange_team_master(team_id= 61386, from_master_id= 10946874, to_master_id= 10720019)

    # exchange_team_master(team_id= 16725, from_master_id= None, to_master_id= 10574814)
    # exchange_team_master(team_id= 61244, from_master_id= 10919896, to_master_id= 10946845)

    # exchange_team_master(team_id= 61386, from_master_id= 10919894, to_master_id= 10720019)
    

    # 调账号

    # data =  {"toUser":"183","reason":"1","reasonImgUrls":[32266029780001"https://static.guorou.net/course-static/082c6059db96453184a5433e91c10aef.jpg"],"toStudentId":183,"orderId":8631611319900001}
    # exchange_order_user(order_id=59812365960001, to_user_id=11529569)
    # create_product(product_title='test', price=0.00, clazz_id=3575)

    # 学生自主调课
    # 还要获取token用户的token
    # order_id = 32231414620001
    to_clazz_id = 3932
    clazz_id = 3900
    uid = 11529569
    student_exchange_clazz(uid, clazz_id, to_clazz_id)



