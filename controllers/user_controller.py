# -*- coding: utf-8 -*-



from apis import course_apis
from utils import db_utils, str_utils


class User:

    def __init__(self):
        self.db = db_utils.DBUtils()
        self.api = course_apis

    def reg(self, phones: list = [], role=3, size=1):
        if size >= 50 or len(phones) >= 5000:
            print('请勿一次注册过多账号（上限 50）')
            return
        """
        注册流程：
        * 往数据插入预备数据
        * 调用 reg 接口进行注册
        """
        # 不传要注册的手机号，则默认使用 121% 系列
        if len(phones) == 0:
            max_phone_sql = 'select max(phone) from users where phone like "121%"'
            max_phone = int(self.db.select(max_phone_sql)[0][0])
            for i in range(1, size + 1):
                phones.append(max_phone + 1)

        verify_code = 11111

        # 插入预设数据
        src_sql = """
        INSERT INTO `users` (
             `phone`, `role`, `is_staff`, `verify_code`, `verify_time`, `is_verified`, `access_token`, `status`, `source`)
        VALUES (
            '${phone}', '${role}', 0, '${verify_code}', CURRENT_TIME(), 0, '${phone_role}', 1, 5);
        """

        sqls = []
        for phone in phones:
            phone_role = str(phone) + '_' + str(role)
            sql = str_utils.custom_replace(src_sql, phone=phone, role=role, verify_code=verify_code, phone_role=phone_role)
            sqls.append(sql)
        self.db.execute_bat(sqls)

        # 执行注册操作
        for phone in phones:
            username = phone
            # 6个 1
            password = '111111'
            self.api.reg(phone, username, password, verify_code, role)


if __name__ == '__main__':
    user = User()
    user.reg()
