from data_creater.utils import db_utils, str_utils
from data_creater.apis import portal_apis
from time import sleep
from data_creater.controllers.renewal_controller import Renewal


if __name__ == "__main__":


  


    test = Renewal()
    print(test.get_conversion_num(clazz_id=2440, master_id=10918391),test.get_clazz_master_info_field(clazz_id=2440, master_id=10918391))

    uid = 411
    # # # 报春季班、四年级数学
    portal_apis.apply_clazz_student_nice(uid, clazz_id=1987)


    print(test.get_conversion_num(clazz_id=2440, master_id=10918391),test.get_clazz_master_info_field(clazz_id=2440, master_id=10918391))