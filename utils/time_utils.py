# -*- coding: utf-8 -*-

import datetime
import time

now = datetime.datetime.now()


def get_year():
    return now.year


def get_month():
    return now.month


def get_now():
    return now


def time_format_utc(time: datetime.datetime = now):
    return time.strftime('%Y-%m-%dT%H:%M:%S+08:00')


def time_format(time: datetime.datetime = now):
    return time.strftime('%Y-%m-%d %H:%M:%S')


def time_delta(days=0, minutes=0):
    return now + datetime.timedelta(days=days, minutes=minutes)

def get_timestamp(str_len=13):
    """get timestamp string, length can only between 0 and 16
    """
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]

    #TODO  完善异常信息的判断输出

def get_current_date(fmt="%Y-%m-%d"):
    """get current date, default format is %Y-%m-%d
    """ 
    return datetime.datetime.now().strftime(fmt)

def sleep(n_secs):
    """sleep n seconds
    """
    time.sleep(n_secs)

if __name__ == '__main__':
    print(sleep(3))