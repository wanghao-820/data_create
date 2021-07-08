
import config
from utils import db_utils
from apis import sell_apis
from apis import quitclazz
from controllers.user_controller_v2 import User
from time import sleep
from controllers.renewal_controller import Renewal
from faker import Faker
import requests


base_url = config.apps[config.env]['sell_api']

if __name__ == "__main__":
    # 测试用例

    source_xxqd = "qd_4410_activity_62"
    # 寒假体验课英语，课程id，商品id
    clazz_id_2021han8 = 3554
    sku_id_2021han8 = "14881"
    # 春季正价课语文，课程id，商品id
    clazz_id_2021chun9_yu = 3775
    sku_id_2021chun9_yu = "16058"
    # 春季正价课数学，课程id，商品id
    clazz_id_2021chun9_shu = 3739
    sku_id_2021chun9_shu = "14478"

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
    order_id_2021han8 = sell_apis.create_order(sku_id_2021han8,access_token,source_xxqd,order_address_id)
    sleep(2)
    sell_apis.pay_with_remain(order_id=order_id_2021han8, uid=uid)
    sleep(2)
    #判断用户转正状态


    order_id_2021chun9_yu =sell_apis.create_order(sku_id_2021chun9_yu,access_token,source_xxqd,order_address_id)
    sleep(2)
    sell_apis.pay_with_remain(order_id=order_id_2021chun9_yu, uid=uid)
    sleep(2)
    # 判断用户转正状态

    # order_id_2021chun9_shu = sell_apis.create_order(sku_id_2021chun9_shu, access_token, source_xxqd, order_address_id)
    # sleep(2)
    # sell_apis.pay_with_remain(order_id=order_id_2021chun9_shu, uid=uid)
    # sleep(2)
    # # 判断用户转正状态


    quitclazz.quit_clazz_by_userids(uid,clazz_id_2021chun9_yu)
    sleep(2)
    # 判断用户转正状态

    # quitclazz.quit_clazz_by_userids(uid, clazz_id_2021chun9_shu)
    # sleep(2)
    # # 判断用户转正状态



# A在线下购买2021寒假体验课英语，目标2021-春
# A在线下窗口期购买2021春季系统课语文
# A在线下窗口期购买2021春季系统课数学
# 退春季系统课语文
# 退春季系统课数学



