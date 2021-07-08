
import config
from utils import db_utils
from apis import sell_apis
from apis import quitclazz
from apis import portal_apis
from controllers.user_controller_v2 import User
from time import sleep
from controllers.renewal_controller import Renewal
from faker import Faker
import requests
import calendar
import time

base_url = config.apps[config.env]['sell_api']

if __name__ == "__main__":
    # 测试用例

    source_xxqd = "qd_78841_activity_111"
    source_zh = "zh_xgs_43_wxsl_xgs"  # 转化，source以zh开头，计算绩效
    source_fd = "xk_fd_1575_wxsl"  # 辅导中心，source以xk_fd开头，计算绩效
    source_cpcs = "cpcs_kyy_qt_dbkpappoppo"   #自有流量，source以cpcs开头的，计算绩效
    source_app = "app"  # APP，source为app，无其它字母数字，计算绩效
    source_appzbj = "xk_qt_5444_APPzbjad"  # APP学科老师直播间，source为xk开头APPzbjad结尾，计算绩效
    source_bjjx = "xk_qt_5444_APPzbj"  # 不计算绩效


    # 春秋体验课一期，课程id，商品id
    ts = str(calendar.timegm(time.gmtime()))
    # print(ts)
    clazz_id_2021chunqiu1_shu = portal_apis.create_clazz("线下绩效测试体验课1期数学"+str(calendar.timegm(time.gmtime())), 2021, [1], 11207704, 10, "2021-04-01T10:56:02+08:00", "2022-04-01T10:56:09+08:00", 0, "1", 0, 0, [], 1, 0, 200,[])
    sleep(2)
    # # clazz_id_2021chunqiu1_shu = 3916
    clazz_plan_id_2021chunqiu1_shu = portal_apis.create_clazz_plan("测试课时"+str(calendar.timegm(time.gmtime())), 1, "2021-04-30T13:59:12+08:00", "2021-05-01T13:59:33+08:00", 1, clazz_id_2021chunqiu1_shu)
    sleep(2)
    sku_id_2021chunqiu1_shu = str(portal_apis.create_product("线下绩效测试体验课1期数学"+str(calendar.timegm(time.gmtime())), 19, clazz_id_2021chunqiu1_shu))
    sleep(2)
    portal_apis.clear_stock(sku_id_2021chunqiu1_shu)
    # portal_apis.clear_stock("15468")
    # sku_id_2021chunqiu1_shu = "15468"    #15468,15471,17782
    # # 春季正价课语文，课程id，商品id
    # clazz_id_2021chun0_yu = 3212
    # sku_id_2021chun0_yu = "15064"
    # # 春季正价课数学，课程id，商品id
    # clazz_id_2021chun0_shu = 3739
    # sku_id_2021chun0_shu = "14478"

    # 注册用户
    user = User()
    fake = Faker(locale='zh-CN')
    uid = user.reg([], fake.name())
    print(uid)
    access_token = db_utils.DBUtils().select(f"SELECT access_token FROM users WHERE id = {uid};")[0][0]
    # for _ in range(1):
    #     user.reg([], fake.name())
    # print(user.access_tokens)
    # db = db_utils.DBUtils()
    # uid = db.select(f"SELECT id FROM users WHERE access_token = '{user.access_tokens[0]}';")[0][0]
    # print(uid)
    # access_token = db_utils.DBUtils().select(f"SELECT access_token FROM users WHERE id = {uid};")[0][0]
    # phone = db_utils.DBUtils().select(f"SELECT phone FROM users WHERE id = {uid};")[0][0]
    #
    # # 填写收货地址，获取收货地址的id
    order_address_id = sell_apis.get_order_address_id(uid)
    # #
    # uid1 = 11529579
    # access_token1 = db_utils.DBUtils().select(f"SELECT access_token FROM users WHERE id = {uid1};")[0][0]
    # print(access_token1)
    # order_address_id1 = sell_apis.get_order_address_id(uid1)
    # # #创建春秋体验课1期订单并支付
    order_id_2021chunqiu1_shu = sell_apis.create_order(sku_id_2021chunqiu1_shu,access_token,source_xxqd,order_address_id)
    sleep(2)
    sell_apis.pay_with_remain(order_id=order_id_2021chunqiu1_shu, uid=uid)
    sleep(2)
    #判断用户转正状态


    # order_id_2021chun0_yu =sell_apis.create_order(sku_id_2021chun0_yu,access_token1,source_zh,order_address_id)
    # sleep(2)
    # sell_apis.pay_with_remain(order_id=order_id_2021chun0_yu, uid=uid1)
    # sleep(3)
    # 判断用户转正状态
    #
    # uid1 = 11529579
    # 余额充足
    # db_utils.DBUtils(name='payment').insert(
    #     f"INSERT INTO `sszpay_remain` (`user_id`, `remain_fee`, `recharge_fee`, `ios_recharge_fee`, `freeze_fee`, `can_not_withdraw_fee`, `app_src`, `client_ip`, `device_info`, `status`)VALUES('{uid1}', 100000, 100000, 0, 0.00, 0.00, 4, NULL, NULL, 1);",
    #     commit=True)

    # access_token1 = db_utils.DBUtils().select(f"SELECT access_token FROM users WHERE id = {uid1};")[0][0]
    # print(access_token1)
    # order_address_id1 = sell_apis.get_order_address_id(uid1)
    # order_id_2021chun0_yu =sell_apis.create_order(sku_id_2021chun0_yu,access_token1,source_xxqd,order_address_id1)
    # sleep(2)
    # sell_apis.pay_with_remain(order_id=order_id_2021chun0_yu, uid=uid1)
    # sleep(3)

    # order_id_2021chun0_shu = sell_apis.create_order(sku_id_2021chun0_shu, access_token, source_xxqd, order_address_id)
    # sleep(2)
    # sell_apis.pay_with_remain(order_id=order_id_2021chun0_shu, uid=uid)
    # sleep(2)
    # # 判断用户转正状态
    # #
    # #
    # quitclazz.quit_clazz_by_userids1(uid1, clazz_id_2021chunqiu1_shu)
    # sleep(2)
    # # 判断用户转正状态

    # quitclazz.quit_clazz_by_userids1(uid1,clazz_id_2021chun0_yu)
    # sleep(2)
    # # 判断用户转正状态
    # #
    #  quitclazz.quit_clazz_by_userids1(uid, clazz_id_2021chun0_shu)
    # sleep(2)
    # # 判断用户转正状态
    # to_clazz_id = 3781
    # clazz_id = 3201
    # uid = 11557149
    # student_exchange_clazz(uid, clazz_id, to_clazz_id)
    # sleep(2)
    #
    # quitclazz.quit_clazz_by_userids1(uid, to_clazz_id)
    # sleep(2)


# A在线下购买2021春秋体验课1期英语，目标2021-春
# A在线下窗口期购买2021春季系统课语文
# A在线下窗口期购买2021春季系统课数学
# 退春季系统课语文
# 退春季系统课数学



