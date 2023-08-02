"""
对Caputure类进行封装，包含meta数据和对应的方法
"""


currentStage = ['Preprocessing','Training','Postprocessing','Complete']
status = ['waiting_for_upload','uploading','dispatched','finish','compelete'] # redis中的状态

from dataclasses import dataclass
import time
# dataclass
@dataclass
# 和数据库保持一致
class Capture:
    def __init__(self,
                 title,
                 username,
                 slug,
                 source_url,
                 type='reconstruction',
): 
        self.title = title
        self.username = username
        self.type = type
        # 生成当前时间、slug、latestRun
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # # 获取date里的时分秒，没有 ":"
        # random_num_str = self.date.split(' ')[1].replace(':','')
        # self.slug = self.username + "-" + self.title + "-" + random_num_str # username-title-103119
        self.slug = slug
        self.status="wait_for_upload"
        self.latest_run_status = "wait_for_upload"
        self.latest_run_progress = 0
        self.latest_run_stage = "wait_for_upload"
        self.source_url = source_url
        self.result_url = ""
        self.job_id =""
    
