# -*- coding: utf-8 -*-



import pymysql
import traceback
import config
import pandas as pd


class DBUtils():

    def __init__(self, name='portal',cursor_dict=False, autocommit=True):
        self.name = name
        db_config = config.db[config.env][self.name]
        try:
            if cursor_dict:
                cursorclass = pymysql.cursors.DictCursor
            else:
                cursorclass = pymysql.cursors.Cursor
            self.connect = pymysql.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                passwd=db_config['passwd'],
                db=db_config['database'],
                charset='utf8mb4',
                use_unicode=True,
                cursorclass = cursorclass
                
            )
        except:
            print(traceback.format_exc())
            print('connect {} fail, process exit'.format(config.db[config.env]['database']))
            exit(-1)
        self.connect.autocommit(autocommit)
        self.cursor = self.connect.cursor()


    def __del__(self):
        if self.cursor:
            self.cursor.close()
        self.connect.close()
    
    def execute(self, sql, commit=True):
        """
        只适用于单 sql 执行，有批量需求请使用 execute_bat
        :param sql:
        :param commit:
        :return:
        """
        self.cursor.execute(sql)
        if commit:
            self.connect.commit()
        
    def execute_bat(self, sqls: list, commit=True):
        """
        有批量数据插入时使用此方法
        :param sqls:
        :param commit:
        :return:
        """
        self.connect.autocommit(False)
        try:
            for sql in sqls:
                print(sql)
                try:
                    self.cursor.execute(sql)
                except pymysql.err.IntegrityError:
                    print(traceback.format_exc())
            if commit:
                self.connect.commit()
        except pymysql.err.IntegrityError:
            print(traceback.format_exc())
        self.connect.autocommit(True)
        
    def select(self, sql: str):
        self.execute(sql)
        return self.cursor.fetchall()
    
    def insert(self, sql: str, commit=True):
        self.execute(sql, commit)
    
    def insert_bat(self, sqls: list, commit=True):
        self.execute_bat(sqls, commit)
    
    def update(self, sql: str, commit:True):
        self.execute(sql, commit)
        
    def update_bat(self, sqls: list, commit:True):
        self.execute_bat(sqls, commit)

    def pd_from_sql(self, sql: str):
        df = pd.read_sql(sql, con=self.connect)
        print(df)
        print(len(df))



if __name__ == "__main__":
    db = DBUtils()
    # # print(db.select("select * from users limit 1;"))
    # print(db.select("SELECT student_id FROM clazz_student WHERE clazz_id = 3618 and status = 1;"))
    # a = db.select("SELECT student_id FROM clazz_student WHERE clazz_id = 3618 and status = 1;")
    # b = [uid[0] for uid in a]
    # print(b)
    sql = "SELECT * FROM clazz_student_log order BY id DESC limit 10;"
    db.pd_from_sql(sql)
    
    
