#!/usr/bin/env python
from redis import Redis
from rq import Worker


from my_module import create_nerf
from utils_redis import redis

w = Worker(['default'],connection=redis)
w.work()



