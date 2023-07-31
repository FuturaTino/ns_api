from pathlib import Path
# config
cwd = Path('/nerfstudio')
data_parent_dir = cwd / f'data/nerfstudio'
output_dir = cwd / f'outputs' 



# mysql
dialect = 'mysql'
driver= 'pymysql'
user = 'future'
password = 'Gwl001201!'
host = 'rm-bp1dd176yj6mi4l3udo.mysql.rds.aliyuncs.com'
port = '3306'
dbname = 'careers'
url=fr'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'

# redis
redis_host = 'r-bp1xdy045xbzxw1dvzpd.redis.rds.aliyuncs.com'
redis_port = 6379
redis_username = 'default'
redis_password = 'Gwl001201!'

# bucket  临时url上传，无需配置