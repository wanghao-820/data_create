from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":

    # 测试用例， 学生已续报；调账号  
    """
    A：秋 → 春

    B：调入秋 → 春  并退秋  

    A班主任：不变   目前是分母会加一 （正常逻辑）

    B班主任：不变后，分母加一    接手前续变成了正常春季未续报的学生

    """

    to_uid = 682
    # 秋季班
    clazz_ids = [1987,1793]

    test = Renewal()
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num'))
    print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706952, field='service_num,conversion_num'))


    sleep(1)
    
    for i in range(len(clazz_ids)):
        portal_apis.apply_clazz_student_nice(to_uid, clazz_id=clazz_ids[i])
        sleep(1)
        # 先查询info表确定服务人数
        print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num'))
        print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706952, field='service_num,conversion_num'))
        print("报班成功!")

    sleep(1)

    uid = 512
    clazz_id = 1424
    # # # 报春季班、四年级数学
    order_id = test.get_order_id(to_uid,clazz_ids[0])
    portal_apis.exchange_order_user(order_id=order_id, to_user_id=uid)
    sleep(1)

    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num'))
    print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706952, field='service_num,conversion_num'))

    portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_id)

    # info表分母不变算惩罚，分子不变
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num'))
    print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706952, field='service_num,conversion_num'))

    order_id = str_utils.int2list(test.get_order_id_from_payment(uid,clazz_ids[0]))
    
    # 退课
    test.quit_clazz(order_id)

    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num'))
    print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706952, field='service_num,conversion_num'))
    # assert new_conversion_num-conversion_num == 0, "调小班后分子变化了" 
    # assert new_service_num-service_num == 0, "调小班后分母变化了"
    # print("购课后调小班功能测试通过!")
