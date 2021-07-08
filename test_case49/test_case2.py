from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal



if __name__ == "__main__":
    # 测试用例，退课逻辑,退当前课，分母不减

    test = Renewal()
    uid = 10941501
    clazz_id = 1987

    # 获取orderID
    order_id = str_utils.int2list(test.get_order_id(uid,clazz_id))
    
    # 退课
    test.quit_clazz(order_id)
    # 验证数据是否正确
    # info表分母不变算惩罚，分子不变
    # new_service_num = test.get_clazz_master_info_field()
    # assert new_service_num-service_num == 0, "退课后分母没有减一" 
    # print("退课功能测试通过!")

    # print(test.get_clazz_master_info_field(master_id = 10720073, clazz_id = 2448), test.get_conversion_num(master_id = 10720073, clazz_id = 2448))
    # print(test.get_clazz_master_info_field(master_id = 10720019, clazz_id = 2448), test.get_conversion_num(master_id = 10720019, clazz_id = 2448))

