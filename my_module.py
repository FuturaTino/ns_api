import subprocess
import zipfile
from sqlalchemy import text
from pathlib import Path
import utils_db
from config import *
import utils_bucket
import shutil
# config
cwd = Path('/nerfstudio')
data_parent_dir = cwd / f'data/nerfstudio'
output_dir = cwd / f'outputs'

# test_meta
test_slug = 'future-eraLi-123456'
slug = test_slug
title= slug.split('-')[1]
data_dir = data_parent_dir / f'{slug}'
video_path = data_dir / f'{slug}.mp4'


# 连接数据库
engine = utils_db.engine

def download_video_to_dir_from_bucket(slug):
    filename = data_parent_dir / f'{slug}.mp4'
    utils_bucket.download_to_local(slug,filename)

def create_nerf(slug):
 
    # 1. 修改状态），started，processing
    info = {
        'latest_run_status':'Started',
        'latest_run_current_stage': 'Preprocessing',
    }
    utils_db.update_capture(slug,**info)
    # 处理数据
    subprocess.run(f"ns-process-data video --data {video_path} --output-dir {data_dir}",shell=True)

    info = {
        'latest_run_current_stage': 'Training',
    }
    # 2. 修改状态，training
    utils_db.update_capture(slug,**info)
    # 训练nerf
    subprocess.run(f"ns-train nerfacto --data {data_dir}  --output-dir {output_dir} --pipeline.model.predict-normals True \
        --max-num-iterations {200} --save-only-latest-checkpoint True --vis tensorboard  ",shell=True,cwd='/nerfstudio')

    # 3. 修改状态, Exporting
    specific_output_dir = cwd / 'outputs' / slug
    config_path = specific_output_dir.glob('**/config.yml').__next__()
    if not config_path.exists():
        return 1
    info = {
        'latest_run_current_stage': 'Exporting',
    }
    utils_db.update_capture(slug,**info)

    # 4. 导出mesh,将生成的文件夹,命名为job_id ,上传到bucket
    job_id = utils_db.get_a_capture(slug)['job_id']
    specific_mesh_dir = data_dir / job_id
    subprocess.run(f"ns-export poisson --load-config {config_path} --output-dir {specific_mesh_dir}",shell=True)
    shutil.make_archive(specific_mesh_dir, 'zip',base_dir=specific_mesh_dir)
    filename = specific_mesh_dir + '.zip'
    key = specific_mesh_dir.split('/')[-1]
    utils_bucket.upload_to_bucket(key,filename)
    # code


    info = {
        'status':'Finished',
        'latest_run_current_stage': 'Finished',
        'latest_run_progress': 100,
        'result_url':'test',
    }
    utils_db.update_capture(slug,**info)

    # 任务完成后，清理显存
    print('job finished')
    
if __name__ == "__main__":
    create_nerf(test_slug)