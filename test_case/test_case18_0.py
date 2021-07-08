from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":

    # 测试用例， 学生已续报；调班主任  不同班主任  A 的数据进行封存；A 中没有进行续报的学生初始化为 B 的分母


    uid = 464
    clazz_ids = [1793,1987]

    test = Renewal()
    service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(service_num,conversion_num)
    service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706958, field='service_num,conversion_num')
    print(service_num,conversion_num)
    
    for i in range(len(clazz_ids)):
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_ids[i])
        sleep(1)
        # 先查询info表确定服务人数
        service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
        print(service_num, conversion_num)
        service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706958, field='service_num,conversion_num')
        print(service_num, conversion_num)
        print("报班成功!")

    sleep(1)
    portal_apis.exchange_team_master(team_id= 68976, from_master_id= 10706952, to_master_id= 10706958)
    # sleep(1)
    # portal_apis.exchange_team_master(team_id= 66098, from_master_id=10706958 , to_master_id= 10706952)
    sleep(1)
    # info表分母不变算惩罚，分子不变
    new_service_num,new_conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(new_service_num, new_conversion_num)
    new_service_num,new_conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706958, field='service_num,conversion_num')
    print(new_service_num, new_conversion_num)
    assert new_conversion_num-conversion_num == 0, "调小班后分子变化了" 
    assert new_service_num-service_num == 0, "调小班后分母变化了" 
    print("购课后调小班功能测试通过!")
