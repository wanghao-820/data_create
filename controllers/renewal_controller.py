#!/usr/bin/env python
# -*- coding:UTF-8 -*-


# DESCRIPTION:


from apis import course_apis,portal_apis
from utils import db_utils, str_utils, time_utils


spring_clazz = []


class Renewal():
    def __init__(self):
        self.db = db_utils.DBUtils(name='portal')
        self.db.dict = db_utils.DBUtils(name='portal',cursor_dict=True)
        self.db.payment = db_utils.DBUtils(name='payment')
        self.course_api = course_apis
        self.portal_api = portal_apis

    # 调整课时的时间，为了区分插班生和不是插班生,默认是非插班生
    def adject_clazz_plan_time(self, clazz_id: int, days: int=1):
        start_time = time_utils.time_format(time_utils.time_delta(days=days)) 
        stop_time = time_utils.time_format(time_utils.time_delta(days=days,minutes=30)) 
        self.db.update("update clazz_plan set start_time = '{}', stop_time = '{}'  where clazz_id = {} and status = 1 order by seq;".format(start_time,stop_time,clazz_id), commit=True)
        # # 并且废弃掉已有的小班
        self.db.update("update team set `status` = 0 WHERE clazz_id = {};".format(clazz_id), commit=True)
        # 然后新建小班并且分配班主任
        master_ids = [10706952, 10706958, 10706954, 10652874]
        # master_ids = [10706954, 10652874]
        for i in range(2):
            team_id = self.portal_api.create_team(clazz_id=clazz_id)
            # 添加班主任  tom
            self.portal_api.exchange_team_master(team_id= team_id, from_master_id= None, to_master_id= master_ids[i])

    # 退课
    def quit_clazz(self, order_ids: list):
        for order_id in order_ids:
            # order_id = order_id
            self.portal_api.create_clazz_quit(order_id=order_id)
            print("发起退课申请")
            # 获取审批号
            approval_code = self.db.select('SELECT approval_code FROM clazz_quit WHERE order_id = {} and type = 1'.format(order_id))[0][0]
            # 通过审批
            self.portal_api.create_quit_approval_finish(approval_code=approval_code)
            print("通过退课申请")

    # 通过支付库获取skuid
    def get_sku_id(self, clazz_id):
        sku_ids = self.db.payment.select("select sku_id from sszpay_product_attr where attr_key = 'clazz_ids' and attr_value = {} and status = 1 ;".format(clazz_id))
        sku_ids = [sku_id[0] for sku_id in sku_ids]
        if len(sku_ids)>1:
            sku_ids = tuple(sku_ids)
            sku_id = self.db.select(f"SELECT sku_id FROM product_tag_sku WHERE sku_id in {sku_ids} group by product_tag_id, sku_id;")[0][0]
        else:
            sku_id = int(sku_ids[0])
        return sku_id

    # 通过clazz_id和uid获取order_id
    def get_order_id(self, uid, clazz_id):
        team_ids_dict = self.db.dict.select("SELECT id FROM team WHERE clazz_id = {} and `status` = 1 ;".format(clazz_id))
        team_ids = []
        for team_id in team_ids_dict:
            team_ids.append(team_id.get('id'))
        order_id = self.db.dict.select("SELECT order_id FROM clazz_student_log WHERE clazz_id = {} and team_id in {} and student_id = {} GROUP BY student_id ;".format(clazz_id, tuple(team_ids), uid))[0].get('order_id')
        return order_id

    # 直接payment表获取order_id
    def get_order_id_from_payment(self, uid, clazz_id):
        order_id = self.db.payment.select("SELECT so.p_order_id FROM sszpay_product_attr spa LEFT JOIN sszpay_order so on so.sku_id = spa.sku_id WHERE so.user_id in ({}) AND so.status in (1,2) AND spa.attr_key = 'clazz_ids' and spa.attr_value = {} and spa.status = 1;".format(uid,clazz_id))[0][0]
        return order_id
        print("订单号"+order_id)

    # 获取用户的access_token
    def uid2token(self, uid: int):
        access_token = self.db.select("SELECT access_token FROM users WHERE id = {} AND `role` = 3 ;".format(uid))[0][0]
        return access_token

    def get_clazz_master_info_field(self, master_id: int=10706952, clazz_id: int=1793, field='service_num'):
        data = self.db.select("SELECT {} FROM clazz_master_info WHERE master_id in ({}) AND clazz_id = {};".format(field, master_id, clazz_id))
        if data:
            data_num = data[0]
        else:
            data_num = (0,0)
        return data_num


    def get_team_id(self, clazz_id:int):
        data = self.db.select("SELECT id FROM team WHERE clazz_id = {} and status = 1;".format(clazz_id))
        if data:
            team_id = data[0][0]
        else:
            team_id = False
        return team_id


if __name__ == '__main__':
    # 调整课时的时间  为了区分插班和不是插班生
    clazz_id = 1793
    # uid = 10650119
    uid = 196
    test = Renewal()

    # 通过clazz_id 获取skuid
    # sku_id = test.get_sku_id(1793)
    # print(sku_id)
    # order_id = test.get_order_id_from_payment(uid, clazz_id)
    # print(order_id)

    # 通过uid获取access_token
    # token = test.uid2token(uid)
    # print(token)

    # print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706954))

    # test.adject_clazz_plan_time(clazz_id=1424, days=1)
    # sku_id = test.get_sku_id(3015)
    # print(sku_id)
    order_id = [25673213300001]
    test.quit_clazz(order_id)
    db_utils.DBUtils().pd_from_sql("SELECT * FROM clazz_student_log order BY id DESC limit 10;")