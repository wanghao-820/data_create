from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":


  


    test = Renewal()
    print(test.get_conversion_num(clazz_id=2440, master_id=10918391),test.get_clazz_master_info_field(clazz_id=2440, master_id=10918391))
    print(test.get_conversion_num(master_id = 10946874 ,clazz_id = 2448),test.get_clazz_master_info_field(master_id = 10946874 ,clazz_id = 2448))
    

    uid = 419
    clazz_id = 1987
    # # # 报春季班、四年级数学
    order_id = test.get_order_id(uid,clazz_id)
    portal_apis.exchange_order_user(order_id=order_id, to_user_id=418)


    print(test.get_conversion_num(clazz_id=2440, master_id=10918391),test.get_clazz_master_info_field(clazz_id=2440, master_id=10918391))
    print(test.get_conversion_num(master_id = 10946874 ,clazz_id = 2448),test.get_clazz_master_info_field(master_id = 10946874 ,clazz_id = 2448))