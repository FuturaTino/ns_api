import redis
import rq
from my_module import create_nerf
import subprocess
from config import *
# pool = redis.ConnectionPool(host=redis_host,port=redis_port,db=0)
redis = redis.Redis(host=redis_host,port=redis_port,db=0,username=redis_username,password=redis_password)


def get_queue(queue_name):
    q = rq.Queue(name=queue_name,connection=redis)
    return q 



if __name__ == '__main__':
    # pass
    # 启用 worker pool
    subprocess.run(f"rq worker --url redis://default:Gwl001201!@r-bp1xdy045xbzxw1dvzpd.redis.rds.aliyuncs.com:6379/0",shell=True)
    
    