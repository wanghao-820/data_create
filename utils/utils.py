# -*- coding: utf-8 -*-


import itertools
import collections
import requests
import re
import json
from exceptions import ParamsError
from loguru import logger



absolute_http_url_regexp = re.compile(r"^https?://", re.I)

def get(url):
    response = requests.get(url)
    if response.status_code == 200:
        if response.json()['code'] == 0:
            return response.json()
        else:
            print('[REQUEST FAIL]{}\nresponse:{}'.format(url, response.json()))
    else:
        print('[REQUEST ERROR]{}, \nstatus code:{}'.format(url, response.status_code))


def post(url, json: dict = None, data: str = None):
    if json:
        response = requests.post(url, json=json)
    else:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, headers=headers, data=data.encode('utf-8'))
    if response.status_code == 200:
        if response.json()['code'] == 0:
            return response.json()
        else:
            print('[REQUEST FAIL]{}\nbody:{}\nresponse:{}'.format(url, json if json else data, response.json()))
    else:
        print('[REQUEST ERROR]{}, \nstatus code:{}'.format(url, response.status_code))

def build_url(base_url, path):
    if absolute_http_url_regexp.match(path):
        return path
    elif base_url:
        return "{}/{}".format(base_url.rstrip("/"), path.lstrip("/"))
    else:
        raise ParamsError("base url missed!")


def query_json(json_content, query, delimiter='.'):
    """ Do an xpath-like query with json_content.

    Args:
        json_content (dict/list/string): content to be queried.
        query (str): query string.
        delimiter (str): delimiter symbol.

    Returns:
        str: queried result.

    Examples:
        >>> json_content = {
            "ids": [1, 2, 3, 4],
            "person": {
                "name": {
                    "first_name": "Leo",
                    "last_name": "Lee",
                },
                "age": 29,
                "cities": ["Guangzhou", "Shenzhen"]
            }
        }
        >>>
        >>> query_json(json_content, "person.name.first_name")
        >>> Leo
        >>>
        >>> query_json(json_content, "person.name.first_name.0")
        >>> L
        >>>
        >>> query_json(json_content, "person.cities.0")
        >>> Guangzhou

    """
    raise_flag = False
    response_body = f"response body: {json_content}\n"
    try:
        for key in query.split(delimiter):
            if isinstance(json_content, (list, str, bytes)):
                json_content = json_content[int(key)]
            elif isinstance(json_content, dict):
                json_content = json_content[key]
            else:
                logger.error(
                    f"invalid type value: {json_content}({type(json_content)})")
                raise_flag = True
    except (KeyError, ValueError, IndexError):
        raise_flag = True

    if raise_flag:
        err_msg = f"Failed to extract! => {query}\n"
        err_msg += response_body
        logger.error(err_msg)
        raise exceptions.ExtractFailure(err_msg)

    return json_content


def print_info(info_mapping):
    """ print info in mapping.

    Args:
        info_mapping (dict): input(variables) or output mapping.

    Examples:
        >>> info_mapping = {
                "var_a": "hello",
                "var_b": "world"
            }
        >>> info_mapping = {
                "status_code": 500
            }
        >>> print_info(info_mapping)
        ==================== Output ====================
        Key              :  Value
        ---------------- :  ----------------------------
        var_a            :  hello
        var_b            :  world
        ------------------------------------------------

    """
    if not info_mapping:
        return

    content_format = "{:<16} : {:<}\n"
    content = "\n==================== Output ====================\n"
    content += content_format.format("Variable", "Value")
    content += content_format.format("-" * 16, "-" * 29)

    for key, value in info_mapping.items():
        if isinstance(value, (tuple, collections.deque)):
            continue
        elif isinstance(value, (dict, list)):
            value = json.dumps(value)
            # value = value
        elif value is None:
            value = "None"

        content += content_format.format(key, value)

    content += "-" * 48 + "\n"
    logger.info(content)

def ensure_mapping_format(variables):
    """ ensure variables are in mapping format.

    Args:
        variables (list/dict): original variables

    Returns:
        dict: ensured variables in dict format

    Examples:
        >>> variables = [
                {"a": 1},
                {"b": 2}
            ]
        >>> print(ensure_mapping_format(variables))
            {
                "a": 1,
                "b": 2
            }

    """
    if isinstance(variables, list):
        variables_dict = {}
        for map_dict in variables:
            variables_dict.update(map_dict)

        return variables_dict

    elif isinstance(variables, dict):
        return variables

    else:
        raise exceptions.ParamsError("variables format error!")

def gen_cartesian_product(*args):
    """    

    Args:
        args (list of list): lists to be generated with cartesian product

    Returns:
        list: cartesian product in list

    Examples:

        >>> arg1 = [{"a": 1}, {"a": 2}]
        >>> arg2 = [{"x": 111, "y": 112}, {"x": 121, "y": 122}]
        >>> args = [arg1, arg2]
        >>> gen_cartesian_product(*args)
        >>> # same as below
        >>> gen_cartesian_product(arg1, arg2)
            [
                {'a': 1, 'x': 111, 'y': 112},
                {'a': 1, 'x': 121, 'y': 122},
                {'a': 2, 'x': 111, 'y': 112},
                {'a': 2, 'x': 121, 'y': 122}
            ]

    """
    if not args: 
        return []
    elif len(args) == 1:
        return args[0]

    product_list = []
    for product_item_tuple in itertools.product(*args):
        product_item_dict = {}
        for item in product_item_tuple:
            product_item_dict.update(item)

        product_list.append(product_item_dict)

    return product_list

def lower_dict_keys(origin_dict):
    """ convert keys in dict to lower case

    Args:
        origin_dict (dict): mapping data structure

    Returns:
        dict: mapping with all keys lowered.

    Examples:
        >>> origin_dict = {
            "Name": "",
            "Request": "",
            "URL": "",
            "METHOD": "",
            "Headers": "",
            "Data": ""
        }
        >>> lower_dict_keys(origin_dict)
            {
                "name": "",
                "request": "",
                "url": "",
                "method": "",
                "headers": "",
                "data": ""
            }

    """
    if not origin_dict or not isinstance(origin_dict, dict):
        return origin_dict

    return {
        key.lower(): value
        for key, value in origin_dict.items()
    }

if __name__ == '__main__':
    origin_dict = {
            "Name": "",
            "Request": "",
            "URL": "kk",
            "METHOD": "",
            "Headers": "",
            "Data": ""
        }
    print(lower_dict_keys(origin_dict).get("url"))