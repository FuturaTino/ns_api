"""
通过API进行：
1. 上传视频
2. 处理视频
3. 开启nerf训练
4. 输出结果

"""

from flask import Flask, request,jsonify
from flask_restful import reqparse, abort, Api, Resource
from pathlib import Path
from capture import Capture
from utils_db import *
import json
import time
import redis,rq
import utils_redis
import utils_db
from my_module import create_nerf
app = Flask(__name__)
api = Api(app)



# meta
parser = reqparse.RequestParser()

parser.add_argument("title", type=str)
parser.add_argument("type", type=str)
parser.add_argument("date", type=str)
parser.add_argument("username")
parser.add_argument("slug", type=str)
parser.add_argument("latestRun", type=dict)

# cache list
cache_dict = {}


# def abort_if_List_doesnt_exist(Capture_id):
#     if Capture_id not in capture_list:
#         abort(404, message="Capture {} doesnt exist".format(Capture_id))


# Capture
class Caputures_Management(Resource):
    # get all captures
    def get(self):
        # 搜索
        title = None
        username = None
        if request.form:
            if request.form.__contains__("title"):
                title = request.form["title"]
            if request.form.__contains__("username"):
                username = request.form["username"]
            cache_dict = search_captures(title,username)
        elif request.json:
            args = parser.parse_args()
            title = args["title"]
            try:
                username = args["username"]
            finally:
                pass
            cache_dict = search_captures(title,username)
        elif not request.data and not request.form and not request.json: # 无参数
            # 获取所有的Capture的状态，返回一个json，包含所有的信息
            cache_dict = get_all_captures()
        
        if not cache_dict:
            return "No data",400
        return cache_dict, 200
        
        

    # create a capture
    def post(self):
        if request.form:
            print(request.form)
            title = request.form["title"]
            username = request.form["username"]
        elif request.json:
            # 数据为json格式 , REST_FUL API开发的接口，一般用json格式传数据 , 这很重要
            args = parser.parse_args()
            title = args["title"]
            username = args["username"]
        elif request.data:
            # 处理二进制数据， 内容类型为form-data
            pass
        else: 
            return "No data", 400
        print(request.form)
        print(request.data)

        # 补充信息，根据参数,添加slug,source
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        random_num_str = date.split(' ')[1].replace(':','')
        slug = username + "-" + title + "-" + random_num_str # username-title-103119
        source = get_bucket_source_url(slug)
        # source = Path.cwd() / "video_data" / slug 
        # 准备输出，到cache中，数据库中
        source = str(source)
        capture =create_capture(title,username,slug=slug,source=source) # 创建实例，并添加到数据库中
        cache_dict[capture.slug] = capture.__dict__
        return capture.__dict__,200
        
    # upload a video temporarily
    def put(self):
        if not request.files:
            return "No files", 400
        
        # 上传视频到指定的signedUrls中source文件夹中
        if request.method == "PUT":
            f = request.files['file']
            # 接受data参数,一个表单，只能是一层
            if request.form.__contains__('source'): # 指定存储路径
                data = request.form
                source = Path(data["source"])
                print(source)
                # 创建文件夹
                if not source.exists():
                    source.mkdir(parents=True, exist_ok=True)
                print(source)
                p = Path(source) / f.filename
                f.save(p)
            return "uploading successfully",200
        else:
            return "Not saved,please upload again", 400
    
class single_Capture(Resource):
    # get a single capture
    def get(self, slug):
        target = get_a_capture(slug)
        # 获取单个Capture的状态，返回一个json，包含其信息
        if target:
            return target, 200
        else:
            return "No such slug", 400
    
    # trigger a capture
    def post(self, slug):
        if 1:
            # 修改状态，添加到队列中
            info = {
                'status': "enqueued",
                'latest_run_status': "enqueued",
                'latest_run_current_stage': "enqueued",
                'latest_run_progress': 0
                
            }
            utils_db.update_capture(slug, **info)    
            q = utils_redis.q # q.name = 'default'
            # triger the process of the capture and modify the status of the capture
            job = q.enqueue(create_nerf, slug,job_timeout='2h')
            

            return f"{slug} is enquened" , 201
        else:
            return "No such slug", 400

api.add_resource(Caputures_Management, "/capture")
api.add_resource(single_Capture, "/capture/<slug>")
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)