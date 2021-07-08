from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":

    # 测试用例， 学生未续报；调账号   
    """
    A：春 → 调入秋

    B：秋

    A班主任：分子+1   pass 

    B班主任：不变    pass 

    """

    to_uid = 473
    # 春季班
    clazz_ids = [1793]

    test = Renewal()
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num'))
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706958,field='service_num,conversion_num'))
    
    for i in range(len(clazz_ids)):
        portal_apis.apply_clazz_student_nice(to_uid, clazz_id=clazz_ids[i])
        sleep(1)
        # 先查询info表确定服务人数
        service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
        print(service_num, conversion_num)
        print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706958,field='service_num,conversion_num'))
        print("报班成功!")

    sleep(1)
    
    
    uid = 475
    clazz_id = 1987
    portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_id)

    sleep(1)

    # # # 报秋季班、五年级数学
    order_id = test.get_order_id(uid,clazz_id)
    portal_apis.exchange_order_user(order_id=order_id, to_user_id=to_uid)
    sleep(1)
    # info表分母不变算惩罚，分子不变
    new_service_num,new_conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(new_service_num, new_conversion_num)
    new_service_num,new_conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706958, field='service_num,conversion_num')
    print(new_service_num, new_conversion_num)
    # assert new_conversion_num-conversion_num == 0, "调小班后分子变化了" 
    # assert new_service_num-service_num == 0, "调小班后分母变化了" 
    # print("购课后调小班功能测试通过!")
