
from data_creater.utils import db_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal
import requests




if __name__ == "__main__":
    # 测试用例，内部报班功能


    # 设置非插班生的课程
    # clazz_id = 2440
    # test = Renewal()
    # test.adject_clazz_plan_time(clazz_id, 1)

    # 先查询info表确定服务人数
    # service_num = test.get_clazz_master_info_field()
    # conversion_num = test.get_conversion_num()
    # print(test.get_conversion_num(clazz_id=2440, master_id=10918391),test.get_clazz_master_info_field(clazz_id=2440, master_id=10918391))
    # print(test.get_conversion_num(master_id = 10946874 ,clazz_id = 2448),test.get_clazz_master_info_field(master_id = 10946874 ,clazz_id = 2448))

    # uid = 
    uid = 10941363
    # # # 报春季班、四年级数学
    portal_apis.apply_clazz_student_nice(uid, clazz_id=1987)

    response = requests.get("http://portal.test.guorou.net/portalapi/usercenterapi/api/1/master/rank/task/id?rankId=38&access_token=cyt")
    print(response.json())


    # print(test.get_conversion_num(clazz_id=2440, master_id=10918391),test.get_clazz_master_info_field(clazz_id=2440, master_id=10918391))
    # print(test.get_conversion_num(master_id = 10946874 ,clazz_id = 2448),test.get_clazz_master_info_field(master_id = 10946874 ,clazz_id = 2448))

    # sleep(1)
    # # 验证数据是否正确
    # # info表分母加一，分子不变
    # new_service_num = test.get_clazz_master_info_field()
    # new_conversion_num = test.get_conversion_num()

    # 第一次判断还是有问题如果没有数据,概率不知道是否库慢了
    # assert new_service_num-service_num == 1, "报班后分母没有加一" 
    # assert new_conversion_num-conversion_num == 0, "报班后分子加了一，应该是不变"
    # print("报班功能测试通过!")


# 报春季班



# 春买两科，后拓科，退春课看拓科科数

# 续报后调出后调入续报是否正确

# A买春，B买秋，调A构成续报后看续报数  么有问题的  很大可能是查库的问题


# A买春数和春语，并拓秋英，退春语
# A买春数和春语，并拓秋英，调春语到春语文

# 调账号
# 调春课构成续报
# 调秋课构成续报
# 调春课打破续报
# 调秋课打破续报


# 插班生，没有续报，T+N 里调小班，不同班主任，调到新小班应该还是插班生
