"""
This file contains the functions that will be used to interact with the database.
"""

# from SQLAlchemy import create_engine
from capture import Capture
import json
from sqlalchemy import create_engine
from sqlalchemy import text
from config import *
engine = create_engine(url, 
                       echo=False)

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
#     result_url VARCHAR(255),
#     job_id VARCHAR(255)
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
            INSERT INTO captures_urls (slug,title,type,date,username,status,latest_run_status,latest_run_progress,latest_run_current_stage,source_url,result_url,job_id)
            VALUES (:slug, :title, :type, :date, :username, :status, :latest_run_status, :latest_run_progress, :latest_run_current_stage, :source_url, :result_url, :job_id)
        """)
        params = {
            "slug":capture.slug,
            "title":capture.title,
            "type":capture.type,
            "date":capture.date,
            "username":capture.username,
            "status":capture.status,
            "latest_run_status":capture.latest_run_status,
            "latest_run_progress":capture.latest_run_progress,
            "latest_run_current_stage":capture.latest_run_stage,
            "source_url":capture.source_url,
            "result_url":capture.result_url,
            "job_id":capture.job_id
        }

        conn.execute(statement=statement,parameters=params)
        conn.commit()
    return capture

def upload_capture():
    pass

def trigger_capture(slug):
    # 修改status 和 latest_run_status和latest_run_current_stage和latest_run_progress和latest_run_artifacts
    pass

def update_capture(slug,**kwargs)->int:
    """
    **kwargs: key-value pairs in table columns
    """
    # 修改capture列
    with engine.connect() as conn:
        for key,val in kwargs.items():
            statement = text(f"""
                UPDATE captures_urls SET {key} = :value WHERE slug = :slug
                """)
            params = {
                "slug":slug,
                "value":val
            }
            conn.execute(statement=statement,parameters=params)
        conn.commit()
    return 0
    

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
        if len(rows) == 0:
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
    print(title,username,"in search_captures")
    if title and not username: 
        statement = text("""
            SELECT * FROM captures_urls WHERE title = :title
            """)
        params = {
            "title":title,
        }
    elif username and not title:
        statement = text("""
            SELECT * FROM captures_urls WHERE username = :username
            """)
        params = {
            "username":username,
        }
    elif username and title:
        statement = text("""
            SELECT * FROM captures_urls WHERE title = :title AND username = :username
            """)
        params = {
            "title":title,
            "username":username,
        }
    else :
        return None
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
                "result_url":i[10],
                "job_id":i[11]
            }
            ret_dict[t['slug']] = t
        return ret_dict 

def delete_capture(slug):
    statement = text("""
        DELETE FROM captures_urls WHERE slug = :slug
        """)
    params = {
        "slug":slug
    }
    with engine.connect() as conn:
        conn.execute(statement=statement,parameters=params)
        conn.commit()
    return 0

def delete_all_captures():
    statement = text("""
        DELETE FROM captures_urls
        """)
    with engine.connect() as conn:
        conn.execute(statement=statement)
        conn.commit()
    return 0

if __name__ == "__main__":
    kwargs = {
        'status':'Started',
        'latest_run_status':'Started',
        'latest_run_progress':100,
        'title':'eraLi',
        'result_url':'1234m'
    }
    a =  update_capture('test',**kwargs)
    # r = search_captures(title='eraLi')
    # print(r)
    # r = get_all_captures()
    # print(r)