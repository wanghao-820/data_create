# -*- coding: utf-8 -*-

import config
from utils import http_utils as http

course_api = config.apps[config.env]['course_api']


def reg(phone, username, password, verify_code, role):
    url = course_api + '/api/1/auth/register'
    form_data = 'phone={}&username={}&password={}&verify_code={}&role={}'.format(
        phone, username, password, verify_code, role
    )
    print(form_data)
    response = http.post(url, data=form_data)
    if response:
        print('[REG SUCCESS]phone={}&username={}&password={}&verify_code={}&role={}'.format(
            phone, username, password, verify_code, role
        ))
        uid = response['data']['user']['id']
        return uid
