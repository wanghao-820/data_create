
from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":
    # 测试用例， 报名构成续报的课程  分子加一。


    test = Renewal()
    # 先查询info表确定服务人数
    service_num = test.get_clazz_master_info_field()

    uid = 303
    # # # 报春季班、四年级数学
    portal_apis.apply_clazz_student_nice(uid, clazz_id=2448)
    # 验证数据是否正确
    # info表分母加一，分子不变
    new_service_num = test.get_clazz_master_info_field()
    # assert new_service_num-service_num == 1, "报班后分母没有加一" 
    sleep(1)
    
    # TODO: 可以使用装饰器封装查询数据
    conversion_num = test.get_conversion_num()
    portal_apis.apply_clazz_student_nice(uid, clazz_id=1793)
    new_conversion_num = test.get_conversion_num()
    # 验证数据是否正确
    # info表分子加一
    # assert new_conversion_num-conversion_num == 1, "续报后分子没有加一" 
    # print("续报功能测试通过!")

