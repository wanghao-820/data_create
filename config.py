# -*- coding: utf-8 -*-

# supports dev or pre

env = 'pre'

apps = {
    'dev': {
        'course_api': 'http://grcourseapi.uae.shensz.local',
        'portal_api': 'http://portalhome.uae.shensz.local/portalapi',
        # 'portal_api': 'http://172.80.10.77:5103/portalapi',
        'sell_api1': 'http://courseapi.uae.shensz.local',
        'sell_api': 'http://sellapi.dev.guorou.net',
        'usercenter_api': 'http://usercenterapi.uae.shensz.local',
        'dataservice_api': 'http://dataservice.uae.shensz.local',
        },
    'test': {
        'course_api': 'http://testgrcourseapi.uae.shensz.local',
        'portal_api': 'http://testportalhome.uae.shensz.local/portalapi',
        # 'portal_api': 'http://172.80.10.77:5103/portalapi',
        'sell_api1': 'http://testcourseapi.uae.shensz.local',
        'sell_api': 'http://testsellapi.dev.guorou.net',
        'usercenter_api': 'http://testusercenterapi.uae.shensz.local',
        'dataservice_api': 'http://testdataservice.uae.shensz.local',
    },
    'pre':{
        #'course_api': 'http://wxapi.test.guorou.net',
        'course_api': 'http://wx.test.guorou.net',
        'portal_api': 'http://portal.test.guorou.net/portalapi',
        'sell_api': 'http://sellapi.test.guorou.net',
        'sales_api': 'http://sale.test.guorou.net',
        'usercenter_api': None,
        'dataservice_api': None,
    }
}


db = {
   'dev':{
        'course': {
            'host': 'rm-bp1u1vnmzhu2ah035xm.mysql.rds.aliyuncs.com',
            'port': 3306,
            'user': 'course_dev_rw',
            'passwd': 'me3eRsm91JDlOCFu',
            'database': 'course_dev'
        },
        'portal': {
            'host': 'rm-bp1u1vnmzhu2ah035xm.mysql.rds.aliyuncs.com',
            'port': 3306,
            'user': 'course_dev_rw',
            'passwd': 'me3eRsm91JDlOCFu',
            'database': 'course_dev'
        },
        'payment': {
            'host': 'rm-bp1u1vnmzhu2ah035xm.mysql.rds.aliyuncs.com',
            'port': 3306,
            'user': 'course_dev_rw',
            'passwd': 'me3eRsm91JDlOCFu',
            'database': 'payment_dev'
        }

   },
    'test': {
        'course': {
            'host': 'rm-bp1u1vnmzhu2ah035.mysql.rds.aliyuncs.com',
            'port': 3306,
            'user': 'highauthority',
            'passwd': 'yXgiGbpsNU-GYU3X',
            'database': 'course'
        },
        'portal': {
            'host': '192.168.30.53',
            'port': 3306,
            'user': 'highauthority',
            'passwd': 'yXgiGbpsNU-GYU3X',
            'database': 'course'
        },
        'payment': {
            'host': '192.168.30.53',
            'port': 3306,
            'user': 'highauthority',
            'passwd': 'yXgiGbpsNU-GYU3X',
            'database': 'payment'
        }

    },
   'pre':{
        'course': {
            'host': 'rm-bp1tjet9282if6519uo.mysql.rds.aliyuncs.com',
            'port': 3306,
            'user': 'highauthority',
            'passwd': 'gArjibFv3TzjnqhH',
            'database': 'shensz_course'
        },
        'portal': {
            'host': 'rm-bp1tjet9282if6519uo.mysql.rds.aliyuncs.com',
            'port': 3306,
            'user': 'highauthority',
            'passwd': 'gArjibFv3TzjnqhH',
            'database': 'shensz_course'
        },
        'payment': {
            'host': 'rm-bp1tjet9282if6519uo.mysql.rds.aliyuncs.com',
            'port': 3306,
            'user': 'highauthority',
            'passwd': 'gArjibFv3TzjnqhH',
            'database': 'payment'
        }   
   }
}

redis = {

    'dev': {
        'course': {
            'host': '192.168.30.53',
            'port': 6380
        }
    },
    'test': {
        'course': {
            'host': '192.168.0.217',
            'port': 6379
        }
    },
    'pre': {
        'course': {
            # 内网 i
            'host': '172.31.227.12',
            'port': 6379
        }
    }

}

mongo = {
    'host': '192.168.30.53:27017'

}


