from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":


    # 测试用例， 报名构成续报的课程 分子加一；并且进行永久调当前课  
    # 预期结果当前班主任分子分母都不变调入的班主任分子分母都不变


    uid = 404
    clazz_ids = [2440,1987,1997]

    test = Renewal()
    # conversion_num = test.get_conversion_num()

    print(test.get_conversion_num(clazz_id=2440, master_id=10918391),test.get_clazz_master_info_field(clazz_id=2440, master_id=10918391))
    
    for i in range(len(clazz_ids)-1):
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_ids[i])
        sleep(1)
        print(test.get_conversion_num(clazz_id=2440, master_id=10918391),test.get_clazz_master_info_field(clazz_id=2440, master_id=10918391))
        

    sleep(1)
    portal_apis.exchange_clazz(uid=uid,clazz_id=clazz_ids[1], to_clazz_id=clazz_ids[2], is_temp=False)
    sleep(1)
    # 验证数据是否正确
    # info表分母不变算惩罚，分子不变
    print(test.get_conversion_num(clazz_id=2440, master_id=10918391),test.get_clazz_master_info_field(clazz_id=2440, master_id=10918391))
    

