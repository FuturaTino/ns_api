"""
This file contains the functions that will be used to interact with the database.
"""

# from SQLAlchemy import create_engine
from capture import Capture
import json
from sqlalchemy import create_engine
from sqlalchemy import text

dialect = 'mysql'
driver= 'pymysql'
user = '4f51thh64qb39pbg1p1d'
password = 'pscale_pw_9JSU9E4IiWCHqB6aFBEisU1BtbKxGuxeAMzClZp5fI1'
hostname = 'aws.connect.psdb.cloud'
dbname = 'joviancareers'
url = f'{dialect}+{driver}://{user}:{password}@{hostname}/{dbname}'
engine = create_engine(url,
                       pool_recycle=3600, 
                       echo=True,
                       connect_args={
                           'ssl':{
                                "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       })

# CREATE TABLE captures_urls (
#     slug VARCHAR(255) PRIMARY KEY,
#     title VARCHAR(255),
#     `type` VARCHAR(255) DEFAULT 'reconstruction',
#     `date` VARCHAR(255),
#     username VARCHAR(255) NOT NULL,
#     `status` VARCHAR(255) DEFAULT 'waiting_for_upload',
#     latest_run_status VARCHAR(255) DEFAULT 'waiting_for_upload',
#     latest_run_progress INT DEFAULT 0,
#     latest_run_current_stage VARCHAR(255) DEFAULT 'waiting_for_upload',
#     source_url VARCHAR(255) NOT NULL,
#     result_url VARCHAR(255)
# );


# 数据库列顺序 slug,title,type,date,username,status,latest_run_status,latest_run_progress,latest_run_current_stage,source_url,result_url

# 连接数据库

def create_capture(title,username,slug,source_url):
    """

    """
    capture = Capture(title,username,slug,source_url)
    
    # 根据列顺序，将记录输入数据库中
    with engine.connect() as conn:
        statement = text("""
            INSERT INTO captures_urls (slug ,title ,`type` ,`date` ,username ,`status` ,latest_run_status ,latest_run_progress ,latest_run_current_stage,source_url,result_url)
            VALUES (:slug ,:title ,:type ,:date ,:username ,:status ,:latest_run_status ,:latest_run_progress ,:latest_run_current_stage ,:source_url,:result_url)
        """)
        params = {
            "slug":capture.slug,
            "title":capture.title,
            "type":capture.type,
            "date":capture.date,
            "username":capture.username,
            "status":capture.status,
            "latest_run_status":capture.latestRun["status"],
            "latest_run_progress":capture.latestRun["progress"],
            "latest_run_current_stage":capture.latestRun["currentStage"],
            "source_url":capture.source_url,
            "result_url":capture.result_url
        }
        conn.execute(statement=statement,parameters=params)
    return capture

def upload_capture():
    pass

def trigger_capture(slug):
    # 修改status 和 latest_run_status和latest_run_current_stage和latest_run_progress和latest_run_artifacts
    pass

def update_capture(title=None):
    pass
    

def get_a_capture(slug):
    # slug是主键，只选择唯一的一条记录
    statement = text("""
        select * from captures_urls where slug = :slug
        """)
    params= {
        "slug":slug
    }
    with engine.connect() as conn:
        result = conn.execute(statement=statement,parameters=params)
        rows= result.all()
        if not rows:
            return None
        ret = {}
        for i in rows:
            ret= {
                "slug":i[0],
                "title":i[1],
                "type":i[2],
                "date":i[3],
                "username":i[4],
                "status":i[5],
                "latest_run_status":i[6],
                "latest_run_progress":i[7],
                "latest_run_current_stage":i[8],
                "source_url":i[9],
                "result_url":i[10]
            }
        return ret

def get_all_captures():
    statement = text("""
        SELECT * FROM captures_urls
        """)
    with engine.connect() as conn:
        result = conn.execute(statement=statement)
        rows= result.all()
        if not rows:
            return None
        # 转成字典
        ret_dict = {}
        for i in rows:
            t= {
                "slug":i[0],
                "title":i[1],
                "type":i[2],
                "date":i[3],
                "username":i[4],
                "status":i[5],
                "latest_run_status":i[6],
                "latest_run_progress":i[7],
                "latest_run_current_stage":i[8],
                "source_url":i[9],
                "result_url":i[10]
            }
            ret_dict[t['slug']] = t
        return ret_dict

def search_captures(title=None,username=None):
    if not username: 
        statement = text("""
            SELECT * FROM captures_urls WHERE title = :title
            """)
        params = {
            "title":title,
        }
    elif not title:
        statement = text("""
            SELECT * FROM captures_urls WHERE username = :username
            """)
        params = {
            "username":username,
        }
    else:
        statement = text("""
            SELECT * FROM captures_urls WHERE title = :title AND username = :username
            """)
        params = {
            "title":title,
            "username":username,
        }
    with engine.connect() as conn:
        result = conn.execute(statement=statement,parameters=params)
        rows= result.all()
        if not rows:
            return None
        # 转成字典
        ret_dict = {}
        for i in rows:
            t= {
                "slug":i[0],
                "title":i[1],
                "type":i[2],
                "date":i[3],
                "username":i[4],
                "status":i[5],
                "latest_run_status":i[6],
                "latest_run_progress":i[7],
                "latest_run_current_stage":i[8],
                "source_url":i[9],
                "result_url":i[10]
            }
            ret_dict[t['slug']] = t
        return ret_dict 

if __name__ == "__main__":
    r = search_captures(title='future')
    print(type(r))
    print(r)