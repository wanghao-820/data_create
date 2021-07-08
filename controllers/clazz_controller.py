# -*- coding: utf-8 -*-



from apis import course_apis, portal_apis
from utils import db_utils, time_utils

class Clazz:
    def __init__(self):
        self.db = db_utils.DBUtils()
        self.course_api = course_apis
        self.portal_api = portal_apis
        # self.portal_api.test()
    def create_new_clazz(self, mentor_id: int):
        # 先创建课程
        clazz_name = '测试课程' + str(time_utils.get_now())
        year = time_utils.get_year()
        # 默认 7 年级
        grade = ['7']
        # 根据时间，指定课程类型
        month = time_utils.get_month()
        if month in [7, 8]:
            clazz_type = 1
        elif month in [9, 10, 11, 12]:
            clazz_type = 2
        elif month in [1, 2]:
            clazz_type = 8
        else:
            clazz_type = 9

        start_time = time_utils.time_format_utc()
        stop_time = time_utils.time_format_utc(time_utils.time_delta(days=3))
        time_type = 0
        time_text = ''
        level = 0
        star_count = 0
        tags = []
        time_seq = 0
        is_staff = 0
        master_student_limit = 200
        time_type_detail = []
        clazz_id = self.portal_api.create_clazz(name=clazz_name, year=year, grade=grade, mentor_id=mentor_id,
                                                clazz_type=clazz_type, start_time=start_time, stop_time=stop_time,
                                                time_type=time_type, time_text=time_text, level=level,
                                                star_count=star_count,
                                                tags=tags, time_seq=time_seq, is_staff=is_staff,
                                                master_student_limit=master_student_limit,
                                                time_type_detail=time_type_detail
                                                )

        # 再创建课时，只创建一个
        if clazz_id:
            clazz_plan_title = '课时 1'
            clazz_plan_type = 1
            start_time = time_utils.time_format_utc()
            stop_time = time_utils.time_format_utc(time_utils.time_delta(minutes=10))
            seq = 1
            self.portal_api.create_clazz_plan(title=clazz_plan_title, clazz_plan_type=clazz_plan_type,
                                              start_time=start_time, stop_time=stop_time,
                                              seq=seq, clazz_id=clazz_id)
            print('点击修改特定信息: '
                  'http://portalhome.uae.shensz.local/portal/dashboard/clazz-detail/{}'.format(clazz_id))


if __name__ == '__main__':
    clazz = Clazz()
    clazz.create_new_clazz(mentor_id=10608)
