from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":


    # 测试用例
    # 买9元后，调小班
    # clazz_ids = [2448]
    # 买9 买秋，调小班
    clazz_ids = [2448, 1987]


    test = Renewal()
    print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2448), test.get_conversion_num(master_id = 10720019, clazz_id = 2448))

    uid = 334
    
    for clazz_id in clazz_ids:
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_id)
        print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
        print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2448), test.get_conversion_num(master_id = 10720019, clazz_id = 2448))
        sleep(1)

    # 不区分班主任
    portal_apis.change_team(student_id=uid, clazz_id=clazz_ids[1], team_id=66100)
    sleep(1)

    print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2448), test.get_conversion_num(master_id = 10720019, clazz_id = 2448))