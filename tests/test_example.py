import pytest
import shutil
from pathlib import Path
import os 
import sys
import requests

# 将运行目录更改为tests
# 从上个目录引用
os.chdir('D:/Repo/algorithm/ns_api/tests')
sys.path.append('..')
import utils_bucket


cwd = Path('D:/Repo/algorithm/ns_api/')
base_name = fr'{str(cwd)}\123213412321341242131'
print(base_name)
archive = Path(rf'C:\Users\future\Desktop\eraLi')
root_dir = Path('C:/User/future/Desktop')
video_path = '../eraLi.mp4'


url = 'http://localhost:8080/capture'
url_single = 'http://localhost:8080/capture/future-test-123456'
class Test_capture:
    def test_create_capture(self):
        response = requests.post(url,data={'username':'future','title':'eraLi'})
        # print(response.json())
        capture_data = response.json()
        slug = capture_data['slug']
        source_url = capture_data['source_url']
    def test_upload_to_bucket(self):
        slug = 'future-test-123456'
        utils_bucket.upload_to_bucket(slug,filename=video_path)
    def test_triger_nerf(self):
        response = requests.post
    def test_delete_capture(self):
        # #只在linux上测试
        # url_single = url + '/' + slug
        # requests.post(url=url_single) # 触发nerf

