from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":


    # 测试用例
    # 买9元后，调小班
    clazz_ids = [2448]
    # 买9 买秋，调小班
    # clazz_ids = [2448, 1987]


    test = Renewal()
    print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    print(test.get_clazz_master_info_field(master_id = 10946845, clazz_id = 2449), test.get_conversion_num(master_id = 10946845, clazz_id = 2449))
    print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2449), test.get_conversion_num(master_id = 10720019, clazz_id = 2449))



    # uid = 347
    
    # for clazz_id in clazz_ids:
    #     portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_id)
    #     print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    #     print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2448), test.get_conversion_num(master_id = 10720019, clazz_id = 2448))
    #     print(test.get_clazz_master_info_field(master_id = 10946845, clazz_id = 2449), test.get_conversion_num(master_id = 10946845, clazz_id = 2449))
    #     sleep(1)

    # 调班主任
    portal_apis.exchange_team_master(team_id= 55169, from_master_id= None, to_master_id= 10946845)
    sleep(1)

    print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    print(test.get_clazz_master_info_field(master_id = 10946845, clazz_id = 2449), test.get_conversion_num(master_id = 10946845, clazz_id = 2449))
    print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2449), test.get_conversion_num(master_id = 10720019, clazz_id = 2449))