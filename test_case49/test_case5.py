from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":
    # 测试用例， 报名春季班课程和报不构成续报的课程；并且退不构成续报的课程，分子不变
    # 买9买秋
    # clazz_ids = [2448, 1987]
    clazz_ids = [1987,2448]
    # 买9买春再买秋
    # clazz_ids = [2448,1793,1987]
    # 买9买秋在买春
    # clazz_ids = [2448,1987,1793]
    # 买9再买两门不同科秋
    # clazz_ids = [2448,1987, 1997]
    # 报9后报秋两门
    # clazz_ids = [2448,1987,1973]
    # 买9买春  然后退春
    # clazz_ids = [2448 , 1793 ]
    # 买9买秋  退秋
    # clazz_ids = [2448,1987 ]


    test = Renewal()
    print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    print(test.get_conversion_num(master_id = 10946874 ,clazz_id = 2448),test.get_clazz_master_info_field(master_id = 10946874 ,clazz_id = 2448))

    uid = 419
    
    for clazz_id in clazz_ids:
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_id)
        print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
        print(test.get_conversion_num(master_id = 10946874 ,clazz_id = 2448),test.get_clazz_master_info_field(master_id = 10946874 ,clazz_id = 2448))
        sleep(1)

     # 获取orderID
    # for clazz_id in range(len(clazz_ids)):
    # order_id = str_utils.int2list(test.get_order_id(uid,clazz_ids[0]))
    # test.quit_clazz(order_id)
    # print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    # print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2448), test.get_conversion_num(master_id = 10720019, clazz_id = 2448))


    print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    print(test.get_conversion_num(master_id = 10946874 ,clazz_id = 2448),test.get_clazz_master_info_field(master_id = 10946874 ,clazz_id = 2448))
