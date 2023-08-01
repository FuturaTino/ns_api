#!/usr/bin/env python
import argparse
from redis import Redis
from rq import Worker
from my_module import create_nerf
from utils_redis import redis


parser = argparse.ArgumentParser()
parser.add_argument("-q", type=str, help="queue name",required=True)
args = parser.parse_args()

name = args.q
w = Worker([name],connection=redis)
w.work()

# worker name: 1.download_queue 2.nerf_queue


