"""
对Caputure类进行封装，包含meta数据和对应的方法
"""
# {
#     "title": "sofa set",
#     "type": "reconstruction",
#     "date": "2023-03-26T15:54:08.268Z",
#     "username": "karan",
#     "status": "uploading",
#     "slug": "pleasure-bless-j-243665"
#     "latestRun": {
#         "status": "new",
#         "progress": 0,
#         "currentStage": "Queued",
#         "artifacts": []
#     }
#     "source_url": "https://storage.googleapis.com/...,
#     "result_url": "https://storage.googleapis.com/...,
# }

currentStage = ['Preprocessing','Training','Postprocessing','Complete']
status = ['waiting_for_upload','uploading','dispatched','finish','compelete'] # redis中的状态

from dataclasses import dataclass
import time
# dataclass
@dataclass
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
        self.status="waiting_for_upload"
        self.latestRun = {
            "status": "dispatched",
            "progress": 0,
            "currentStage": "Preprocessing",
            "artifacts": []
        }
        self.source_url = source_url
        self.result_url = ""
    def test(self):
        print('test')
    
    
