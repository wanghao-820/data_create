# -*- coding: utf-8 -*-

import redis
import config


class RedisUtils:

    def __init__(self):
        redis_config = config.redis['course']
        pool = redis.ConnectionPool(
            host=redis_config['host'],
            port=redis_config['port']
        )
        self.redis = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.redis.close()
