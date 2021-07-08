from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":

    # 测试用例， 学生未续报；调班主任  不同班主任   bug分母没有加到新班主任身上
    # A 班主任，学生甲，续报，后拓科，后退拓科
    #然后 学生甲 交接给 B 班主任，B 班主任分子分母不变



    uid = 472
    clazz_ids = [1793,1987,1997]
    master_ids = [10706954, 10652874]

    test = Renewal()
    service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706954, field='service_num,conversion_num')
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706954, field='service_num,conversion_num,expand_clazz_num'))
    service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10652874, field='service_num,conversion_num')
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10652874, field='service_num,conversion_num,expand_clazz_num'))
    
    for i in range(len(clazz_ids)):
        portal_apis.apply_clazz_student_nice(uid, clazz_id=clazz_ids[i])
        sleep(1)
        # 先查询info表确定服务人数
        service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706954, field='service_num,conversion_num')
        print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706954, field='service_num,conversion_num,expand_clazz_num'))
        service_num,conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10652874, field='service_num,conversion_num')
        print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10652874, field='service_num,conversion_num,expand_clazz_num'))
        print("报班成功!")

    sleep(1)
    # 获取orderID
    order_id = str_utils.int2list(test.get_order_id_from_payment(uid,clazz_ids[-1]))
    
    # 退课
    test.quit_clazz(order_id)
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706954, field='service_num,conversion_num,expand_clazz_num'))
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10652874, field='service_num,conversion_num,expand_clazz_num'))

    sleep(1)
    # portal_apis.exchange_team_master(team_id= 68984, from_master_id= 10706954, to_master_id= 10652874)
    # sleep(1)
    portal_apis.exchange_team_master(team_id= 68976, from_master_id=10652874 , to_master_id= 10706954)
    sleep(1)
    # info表分母不变算惩罚，分子不变
    new_service_num,new_conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10706954, field='service_num,conversion_num')
    new_service_num,new_conversion_num=test.get_clazz_master_info_field(clazz_id=1793, master_id=10652874, field='service_num,conversion_num')
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10706954, field='service_num,conversion_num,expand_clazz_num'))
    print(test.get_clazz_master_info_field(clazz_id=1793, master_id=10652874, field='service_num,conversion_num,expand_clazz_num'))
    assert new_conversion_num-conversion_num == 0, "调小班后分子变化了" 
    assert new_service_num-service_num == 1, "调小班后分母变化了" 
    print("购课后调小班功能测试通过!")
