# -*- coding: utf-8 -*-

from apis import course_apis
from utils import db_utils, str_utils


class Base:

    def __int__(self):
        self.db = db_utils.DBUtils()
        self.api = course_apis
        self.str_utils = str_utils
