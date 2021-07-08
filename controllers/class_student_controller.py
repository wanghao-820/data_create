# -*- coding: utf-8 -*-


import redis_keys
from utils import str_utils
from utils.db_utils import DBUtils
from utils.redis_utils import RedisUtils


class StudentTag:

    def __init__(self):
        self.redis = RedisUtils().redis
        self.db = DBUtils()
        self.redis_keys = redis_keys.student_tag
        self.str_utils = str_utils

    def __del__(self):
        print('student tag execute done')

    def replace(self, src, **kwargs):
        return self.str_utils.custom_replace(src, **kwargs)

    def set2renew(self, clazz_id, student_id):
        renew_key = self.redis_keys['renew']
        not_renew_key = self.redis_keys['not_renew']
        # 增对应的student_id,并且删除未续报的key的数据
        self.redis.sadd(self.replace(renew_key, clazz_id=clazz_id), student_id)
        self.redis.delete(self.replace(not_renew_key, clazz_id=clazz_id))

    def set2not_renew(self, clazz_id, student_id):
        renew_key = self.redis_keys['renew']
        not_renew_key = self.redis_keys['not_renew']
        self.redis.srem(self.replace(renew_key, clazz_id=clazz_id), student_id)
        self.redis.delete(self.replace(not_renew_key, clazz_id=clazz_id))

    def change_focus(self, clazz_id, student_id, focus=True):
        focus_key = self.redis_keys['focus']
        target_focus_key = self.replace(focus_key, clazz_id=clazz_id)
        if focus:
            self.redis.sadd(target_focus_key, student_id)
        else:
            self.redis.srem(target_focus_key, student_id)

    def change_praise(self, clazz_plan_id, student_id, praise=True):
        praise_key = redis_keys.student_tag['key_praise']
        if praise:
            sql = """
            INSERT INTO `key_praise` (`clazz_plan_id`, `student_id`, `status`)
            VALUES (${clazz_plan_id}, ${student_id}, 1);
            """
        else:
            sql = """
            DELETE FROM `key_praise` 
            WHERE `clazz_plan_id`=${clazz_plan_id} and `student_id`=${student_id};
            """
        sql = str_utils.custom_replace(sql, clazz_plan_id=clazz_plan_id, student_id=student_id)
        self.db.execute(sql)
        self.redis.delete(self.replace(praise_key, clazz_plan_id=clazz_plan_id))



