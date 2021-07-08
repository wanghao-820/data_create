#!/usr/bin/env python
# -*- coding:UTF-8 -*-


# DESCRIPTION: 


from utils import db_utils, str_utils
import pprint


class MySqldiff:

    def __init__(self):
        self.db_source = db_utils.DBUtils()
        # self.db_target = db_utils.DBUtils()


        
    def test(self):
        data = self.db_source.select("DESC users;")
        Fields = {Field for Field,Type, Null,Key,Default,Extra in data}
        print(Fields)
        print(len(Fields))
        print("\n")
        
        data1 = self.db_source.select("DESC users_portal;")
        Fields1 = {Field for Field,Type, Null,Key,Default,Extra in data1}
        print(len(Fields1))
        print(Fields1)
        print("\n")

        if Fields ^ Fields1 :
            print(Fields ^ Fields1)
        
        print("nothing")            


        

        


        


if __name__ == "__main__":
    db = MySqldiff()
    db.test()
        





    