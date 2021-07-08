from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":


    # 测试用例， 学生已续报；并且进行永久调未来课  同科目  分子分母都不变



    uid = 456
    # 调到不同科目
    # clazz_ids = [1793,1987,1997]
    # 调到同科目
    clazz_ids = [1793,1987,1973]

    test = Renewal()
    # conversion_num = test.get_conversion_num()

    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num,expand_clazz_num'))
    service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    
    for i in range(len(clazz_ids)-1):
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_ids[i])
        sleep(1)
        # 先查询info表确定服务人数
        print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num,expand_clazz_num'))
        print("报班成功!")

    sleep(1)
    portal_apis.exchange_clazz(uid=uid,clazz_id=clazz_ids[1], to_clazz_id=clazz_ids[2], is_temp=False)
    # sleep(1)
    # portal_apis.exchange_clazz(uid=uid,clazz_id=clazz_ids[1], to_clazz_id=clazz_ids[0], is_temp=False)
    sleep(1)
    # 验证数据是否正确
    # info表分母不变算惩罚，分子不变
    new_service_num,new_conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num,expand_clazz_num'))
    assert new_conversion_num-conversion_num == 1, "调课后分子变化了" 
    assert new_service_num-service_num == 1, "调课后分母变化了" 
    print("购课后调课功能测试通过!")
