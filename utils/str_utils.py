# -*- coding: utf-8 -*-


import random
import string

def custom_replace(src: str, **kwargs):
    for k in kwargs:
        src = src.replace('${%s}' % str(k), str(kwargs[k]))
    return src


def replace_append(src: str, **kwargs):
    """
    :param src:
    :param kwargs:  $replace_key=$replace_value, $append_key=$append_value
    :return:
    """
    params_keys = list(kwargs)
    replace_key = params_keys[0]
    result = src.replace('${%s}' % str(replace_key), str(kwargs[replace_key]))
    if len(params_keys) > 1:
        result = result + ' ' + str(kwargs[params_keys[1]])
    return result

def int2list(num: int):
    if isinstance(num,int):
        result = list(map(int, str(num).split(" ")))
    return result

def gen_random_string(str_len):
    """generate random string with specified length
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(str_len))

if __name__ == "__main__":
    print(gen_random_string(9))
    print(string.digits[:5])

#TODO 把返回的SQL结果格式化