
import config
from utils import db_utils
from apis import sell_apis
from apis import quitclazz
from controllers.user_controller_v2 import User
from time import sleep
from controllers.renewal_controller import Renewal
from faker import Faker
import requests
import re

source = "qd_123_456"
all_index = [substr.start() for substr in re.finditer('_', source)] # 得到所有下标[6, 18, 27, 34, 39]
sources = source.split('_')
print(sources)
print(sources[1])
print(all_index[0])
print(all_index[1])




