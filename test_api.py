
from capture import Capture
import requests
from pathlib import Path
# 根据参数，创建一个Capture对象
title = "vase set 2"
# type = "reconstruction"
date = "2023-03-26T15:54:08.000Z"
username = "karan"
slug = "pleasure-bless-j-243665"
latestRun = {
    "status": "dispatched",
    "progress": 50,
    "currentStage": "Preprocessing",
    "artifacts": []
    }
# test case
# {
#   "signedUrls": {
#     "source": "https://storage.googleapis.com/..."
#   },
#   "capture": {
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
# }

import json
d = {
    "title":"eraLi",
    "username":"future",
}
d2 = 'title=eraLi&username=future'
headers = {'Content-Type': 'application/json'}
headers2 = {'Content-Type': 'application/x-www-form-urlencoded'}
headers3 = {'Content-Type': 'multipart/form-data'}
d = json.dumps(d)
response = requests.post(url="http://127.0.0.1:5000/capture",headers=headers,data=d)
print(response.request.headers)
output = response.json()

# output = json.dumps(output)

# 1. request中，当传输json,data输入不可以是dict等数据结构，而是字符串等序列化数据，json数据就是字符串,是序列化数据
# 2. request中，当传输form-data, 字典不可以嵌套，因为表单只能是一层。 传输的data是二进制 混合多种资料格式并一次传送，必须要编码为二进制字符串。
# output = json.dumps(output)
print(type(output))
files = {"file": open("C:/Users/future/Desktop/petal_20230425_170715.mp4", "rb")}
in_data = {
    'source':output['singleUrls']['source'],
}
print(in_data["source"])
# print(output)
response = requests.put(url="http://127.0.0.1:5000/capture",files=files,data=in_data)
print(response.request.headers)
#,files={"file": open(r"C:\Users\future\Desktop\petal_20230425_170715.mp4", "rb")}

print(response.text)