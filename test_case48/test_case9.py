from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":


    # 测试用例， 报名构成续报的课程 分子加一；并且进行临时调当前课  
    # 预期结果当前班主任分子分母都不变调入的班主任分子分母都不变
    # 再临时调课调回来


    uid = 446
    clazz_ids = [1793,1987,1424]

    test = Renewal()
    # conversion_num = test.get_conversion_num()

    print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706954,field='service_num,conversion_num'))
    
    for i in range(len(clazz_ids)-1):
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_ids[i])
        sleep(1)
        # 先查询info表确定服务人数
        service_num,conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
        print(service_num, conversion_num)
        print("报班并续报成功!")

    sleep(1)
    portal_apis.exchange_clazz(uid=uid,clazz_id=clazz_ids[0], to_clazz_id=clazz_ids[2], is_temp=True)
    sleep(1)
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num'))
    print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706954,field='service_num,conversion_num'))
    portal_apis.exchange_clazz(uid=uid,clazz_id=clazz_ids[2], to_clazz_id=clazz_ids[0], is_temp=True)
    sleep(1)
    # 验证数据是否正确
    # info表分母不变算惩罚，分子不变
    new_service_num,new_conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(new_service_num, new_conversion_num)
    assert new_conversion_num-conversion_num == 0, "调课后分子变化了" 
    assert new_service_num-service_num == 0, "调课后分母变化了" 
    print("续报后临时调课后调回功能测试通过!")

    print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706954,field='service_num,conversion_num'))

