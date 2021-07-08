from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":


    # 测试用例， 学生未续报；并且进行永久调当前课  
    # 预期结果当前班主任分母跨课目不减，算惩罚；分子不变



    uid = 449
    clazz_ids = [1793,1758]

    test = Renewal()
    # conversion_num = test.get_conversion_num()

    conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='conversion_num')[0]
    service_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num')[0]
    print(service_num)
    t2 = test.get_clazz_master_info_field(clazz_id=1758, master_id=10636257, field='service_num')[0]
    print(t2)
    
    for i in range(len(clazz_ids)-1):
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_ids[i])
        sleep(1)
        # 先查询info表确定服务人数
        print("报班成功!")

    sleep(1)
    portal_apis.exchange_clazz(uid=uid,clazz_id=clazz_ids[0], to_clazz_id=clazz_ids[1], is_temp=False)
    # sleep(1)
    # portal_apis.exchange_clazz(uid=uid,clazz_id=clazz_ids[1], to_clazz_id=clazz_ids[0], is_temp=False)
    sleep(1)
    # 验证数据是否正确
    # info表分母不变算惩罚，分子不变
    new_conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='conversion_num')[0]
    new_service_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num')[0]
    new_t2 = test.get_clazz_master_info_field(clazz_id=1758, master_id=10636257, field='service_num')[0]
    print(new_service_num)
    print(new_t2)
    assert new_conversion_num-conversion_num == 0, "调课后分子变化了" 
    assert new_service_num-service_num == 1, "调课后分母变化了" 
    print("购课后调课功能测试通过!")
