
import config
from utils import db_utils
from apis import sell_apis
from apis import quitclazz
from controllers.user_controller_v2 import User
from time import sleep
from controllers.renewal_controller import Renewal
from faker import Faker
import requests
from flask import Flask, request, jsonify


base_url = config.apps[config.env]['sell_api']

app = Flask(__name__)
@app.route('/createorder', methods=['get', 'post'])

def get_data():
    source_xxqd = "qd_4410_activity_62"
    source_zh = "zh_xgs_43_wxsl_xgs"  # 辅导中心，source以xk_fd开头，计算绩效
    source_fd = "xk_fd_1575_wxsl"  # 辅导中心，source以xk_fd开头，计算绩效
    source_cpcs = "cpcs_kyy_qt_dbkpappoppo"   #自有流量，source以cpcs开头的，计算绩效
    source_app = "app"  # APP，source为app，无其它字母数字，计算绩效
    source_appzbj = "xk_qt_5444_APPzbjad"  # APP学科老师直播间，source为xk开头APPzbjad结尾，计算绩效

    # 春秋体验课一期，课程id，商品id
    clazz_id_2021chunqiu1_shu = 3916
    sku_id_2021chunqiu1_shu = "15468"    #,15471
    # 春季正价课语文，课程id，商品id
    clazz_id_2021chun0_yu = 3775
    sku_id_2021chun0_yu = "16058"
    # 春季正价课数学，课程id，商品id
    clazz_id_2021chun0_shu = 3739
    sku_id_2021chun0_shu = "14478"

    # 注册用户
    user = User()
    fake = Faker(locale='zh-CN')
    for _ in range(1):
        user.reg([], fake.name())
    print(user.access_tokens)
    db = db_utils.DBUtils()
    uid = db.select(f"SELECT id FROM users WHERE access_token = '{user.access_tokens[0]}';")[0][0]
    print(uid)
    access_token = db_utils.DBUtils().select(f"SELECT access_token FROM users WHERE id = {uid};")[0][0]
    phone = db_utils.DBUtils().select(f"SELECT phone FROM users WHERE id = {uid};")[0][0]

    # 填写收货地址，获取收货地址的id
    order_address_id = sell_apis.get_order_address_id(uid)

    #创建寒假体验课订单并支付
    order_id_2021chunqiu1_shu = sell_apis.create_order(sku_id_2021chunqiu1_shu,access_token,source_xxqd,order_address_id)
    sleep(2)
    sell_apis.pay_with_remain(order_id=order_id_2021chunqiu1_shu, uid=uid)
    sleep(2)
    # #判断用户转正状态


    order_id_2021chun0_yu =sell_apis.create_order(sku_id_2021chun0_yu,access_token,source_appzbj,order_address_id)
    sleep(2)
    sell_apis.pay_with_remain(order_id=order_id_2021chun0_yu, uid=uid)
    sleep(3)
    return(str(uid))
    # # 判断用户转正状态
    #
    # order_id_2021chun0_shu = sell_apis.create_order(sku_id_2021chun0_shu, access_token, source_xxqd, order_address_id)
    # sleep(2)
    # sell_apis.pay_with_remain(order_id=order_id_2021chun0_shu, uid=uid)
    # sleep(2)
    # # 判断用户转正状态
    # #
    # #
    # quitclazz.quit_clazz_by_userids1(uid, clazz_id_2021chunqiu1_shu)
    # sleep(2)
    # # 判断用户转正状态
    # quitclazz.quit_clazz_by_userids1(uid,clazz_id_2021chun0_yu)
    # sleep(2)
    # # 判断用户转正状态
    # #
    # quitclazz.quit_clazz_by_userids1(uid, clazz_id_2021chun0_shu)
    # sleep(2)
    # # 判断用户转正状态



# A在线下购买2021春秋体验课1期英语，目标2021-春
# A在线下窗口期购买2021春季系统课语文
# A在线下窗口期购买2021春季系统课数学
# 退春季系统课语文
# 退春季系统课数学

if __name__ == "__main__":
    app.run(debug=False, port=5001, host='0.0.0.0')

