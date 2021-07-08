from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":


    # 测试用例， 报名构成续报的课程 分子加一；并且进行永久调当前课

    uid = 393
    # clazz_ids = [2448,2449]
    clazz_ids = [2448,1987,2449]
    # clazz_ids = [2448,1987,1424]

    test = Renewal()
    # conversion_num = test.get_conversion_num()

    print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2448), test.get_conversion_num(master_id = 10720019, clazz_id = 2448))
    print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2449), test.get_conversion_num(master_id = 10720019, clazz_id = 2449))

    
    for i in range(len(clazz_ids)-1):
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_ids[i])
        print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
        print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2448), test.get_conversion_num(master_id = 10720019, clazz_id = 2448))
        print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2449), test.get_conversion_num(master_id = 10720019, clazz_id = 2449))
        sleep(1)

    portal_apis.exchange_clazz(uid=uid,clazz_id=clazz_ids[0], to_clazz_id=clazz_ids[2], is_temp=False)
    sleep(1)

    print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2448), test.get_conversion_num(master_id = 10720019, clazz_id = 2448))
    print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2449), test.get_conversion_num(master_id = 10720019, clazz_id = 2449))




