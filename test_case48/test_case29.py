from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":

    # 测试用例 
    # 一个班主任数据交接给多个班主任
    # 一个班主任在一个班里带多个小班，把其中一个小班的数据给别人，自己还保留剩下的小班，还可能再接手其他班主任的数据（就是这个班主任即是交接的旧班主任，又是交接的新班主任）
    # 班主任交接的时候用了同一个账号，改了名字（莫开芬，10745203）
    
    test = Renewal()

    uid = 445
    clazz_id = 3579
    order_id = test.get_order_id_from_payment(uid,clazz_id)
    portal_apis.exchange_order_user(order_id=order_id, to_user_id=446)
    