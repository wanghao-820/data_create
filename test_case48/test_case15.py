from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":

    # 测试用例， 学生已续报；调小班  当前班主任分子分母都不变  并调回原来的小班 分子分母不变
    



    uid = 460
    clazz_ids = [1793,1987]

    test = Renewal()
    service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(service_num,conversion_num)
    
    for i in range(len(clazz_ids)):
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_ids[i])
        sleep(1)
        # 先查询info表确定服务人数
        service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
        print(service_num, conversion_num)
        print("报班成功!")

    sleep(1)
    portal_apis.change_team(student_id=uid, clazz_id=clazz_ids[0], team_id=68977)
    sleep(1)
    new_service_num,new_conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(new_service_num, new_conversion_num)
    portal_apis.change_team(student_id=uid, clazz_id=clazz_ids[0], team_id=68976)
    sleep(1)
    # info表分母不变算惩罚，分子不变
    new_service_num,new_conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(new_service_num, new_conversion_num)
    assert new_conversion_num-conversion_num == 0, "调小班后分子变化了" 
    assert new_service_num-service_num == 0, "调小班后分母变化了" 
    print("购课后调小班功能测试通过!")
