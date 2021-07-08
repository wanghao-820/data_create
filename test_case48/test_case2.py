
from utils import db_utils, str_utils
from apis import portal_apis
from time import sleep
from controllers.renewal_controller import Renewal



if __name__ == "__main__":
    # 测试用例，退课逻辑,退当前课，分母不减

    test = Renewal()
    uid = 442
    clazz_id = 1793

    # 先查询info表确定服务人数
    service_num, conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706952, field='service_num,conversion_num'))

    # 获取orderID
    order_id = str_utils.int2list(test.get_order_id_from_payment(uid,clazz_id))
    
    # 退课
    test.quit_clazz(order_id)
    # 验证数据是否正确
    # info表分母不变算惩罚，分子不变
    new_service_num, new_conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952, field='service_num,conversion_num')
    print(test.get_clazz_master_info_field(clazz_id=1424, master_id=10706952, field='service_num,conversion_num'))
    assert new_service_num-service_num == 0, "退课后分母变化了" 
    print("退课功能测试通过!")

