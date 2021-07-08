# -*- coding: utf-8 -*-



from apis import course_apis
from utils import db_utils, str_utils
from faker import Faker
from time import sleep


uids = []
class User:

    def __init__(self):
        self.db = db_utils.DBUtils()
        self.api = course_apis
        self.access_tokens = []

    def reg(self, phones: list = [], username: str = None, role=3, size=1):
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
             `phone`, `role`, `is_staff`, `verify_code`, `verify_time`, `is_verified`, `access_token`, `status`, `source`, `phone_city`, `grade`, `register_source`)
        VALUES (
            '${phone}', '${role}', 1, '${verify_code}', CURRENT_TIME(), 0, '${phone_role}', 1, 5, '广州', '6', 'oppo');
        """

        sqls = []
        for phone in phones:
            phone_role = str(phone) + '_' + str(role)
            self.access_tokens.append(phone_role)
            sql = str_utils.custom_replace(src_sql, phone=phone, role=role, verify_code=verify_code, phone_role=phone_role)
            sqls.append(sql)
        self.db.execute_bat(sqls)

        # 执行注册操作
        for phone in phones:
            if not username:
                username = phone
            else:
                username = username
            # 6个 1
            password = '111111'
            uid = self.api.reg(phone, username, password, verify_code, role)
            print(uid)

            # 余额充足
            db_utils.DBUtils(name='payment').insert(f"INSERT INTO `sszpay_remain` (`user_id`, `remain_fee`, `recharge_fee`, `ios_recharge_fee`, `freeze_fee`, `can_not_withdraw_fee`, `app_src`, `client_ip`, `device_info`, `status`)VALUES('{uid}', 100000, 100000, 0, 0.00, 0.00, 4, NULL, NULL, 1);",commit=True)

            # db_utils.DBUtils(name='payment').update(f"UPDATE sszpay_remain set user_id={uid} WHERE id  = 338 ;", commit=True)
            # 余额不足
            # db_utils.DBUtils(name='payment').insert(f"INSERT INTO `sszpay_remain` (`user_id`, `remain_fee`, `recharge_fee`, `ios_recharge_fee`, `freeze_fee`, `can_not_withdraw_fee`, `app_src`, `client_ip`, `device_info`, `status`)VALUES('{uid}', 0, 0, 0, 0.00, 0.00, 4, NULL, NULL, 1);", commit=True)

            # db_utils.DBUtils(name='payment').update(f"UPDATE sszpay_remain set user_id={uid} WHERE id  = 60 ;", commit=True)
            # 插入预设的收货地址
            db_utils.DBUtils(name='portal').insert(f"INSERT INTO `order_address` (`user_id`, `contact_name`, `contact_phone`, `country`, `province`, `city`, `district`, `street`, `detail`, `is_default`, `status`)VALUES('{uid}', '内部测试', '19000000099', '中国', '广东省', '广州市', '越秀区', '', '123456', 1, 1);",commit=True)
            return (uid)
        



if __name__ == '__main__':
    user = User()
    fake = Faker(locale='zh-CN')
    for _ in range(1):
        user.reg([], fake.name())
    # user.reg([18761105189], fake.name())
    print(user.access_tokens)
    db = db_utils.DBUtils()
    uid = db.select(f"SELECT id FROM users WHERE access_token = '{user.access_tokens[0]}';")[0][0]
    print(uid)


    # db_utils.DBUtils().pd_from_sql(f"select * from users where access_token= '{user.access_tokens[0]}';")
    # data = db_utils.DBUtils().select("SHOW CREATE TABLE users;")
    # print(data)
    # for _ in range(2):
    #     print(fake.phone_number())


   
