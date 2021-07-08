
from utils import db_utils
from apis import portal_apis
from time import sleep
from controllers.renewal_controller import Renewal
import requests




if __name__ == "__main__":
    # 测试用例，内部报班功能


    # 设置非插班生的课程
    clazz_id = 3614
    test = Renewal()
    # test.adject_clazz_plan_time(clazz_id, 1)


    # 先查询info表确定服务人数
    # service_num,conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952,field='service_num,conversion_num')
    # print(service_num, conversion_num)

    uid = 10924577
    # # # 报春季班、四年级数学
    portal_apis.apply_clazz_student_nice(uid, clazz_id=3619)
    sleep(1)
    
    # 验证数据是否正确
    # info表分母加一，分子不变
    # new_service_num,new_conversion_num = test.get_clazz_master_info_field(clazz_id=1793, master_id=10706952,field='service_num,conversion_num')
    # print(new_service_num, new_conversion_num)

    # 第一次判断还是有问题如果没有数据,概率不知道是否库慢了
    # assert new_service_num-service_num == 1, "报班后分母没有加一" 
    # assert new_conversion_num-conversion_num == 0, "报班后分子加了一，应该是不变"
    # print("报班功能测试通过!")



# 春买两科，后拓科，退春课看拓科科数

# 续报后调出后调入续报是否正确


# A买春数和春语，并拓秋英，退春语
# A买春数和春语，并拓秋英，调春语到春语文



