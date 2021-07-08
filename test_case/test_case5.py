from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":
    # 测试用例， 报名春季班课程和报不构成续报的课程；并且退不构成续报的课程，分子不变

    clazz_ids = [1793,1997]

    test = Renewal()
    # 先查询info表确定服务人数
    service_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num')[0]
    # conversion_num = test.get_conversion_num()

    uid = 453
    
    for clazz_id in clazz_ids:
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_id)
        sleep(5)
        new_conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='conversion_num')[0]
        print("报班成功!")


    clazz_id = clazz_ids[1]
    order_id = str_utils.int2list(test.get_order_id_from_payment(uid,clazz_id))
    test.quit_clazz(order_id)
    sleep(1)
    # 验证数据是否正确
    # info表分母不变算惩罚，分子不变
    conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='conversion_num')[0]
    assert new_conversion_num-conversion_num == 0, "退课后分子变化了" 
    print("退非续报课功能测试通过!")

