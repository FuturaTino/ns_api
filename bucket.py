# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os
import logging
import requests
from pathlib import Path

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


# 1. 设置用户属性, 包括 secret_id, secret_key, region 等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
secret_id = os.environ['COS_SECRET_ID']     # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
secret_key = os.environ['COS_SECRET_KEY']   # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
region = 'ap-nanjing'      # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS 支持的所有 region 列表参见https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填


config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)
rate_record = 0
def upload_percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前上传的百分比
    :param consumed_bytes: 已经上传的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate))
        sys.stdout.flush()

def get_bucket_source_url(slug):

    
    # 生成上传 URL，未限制请求头部和请求参数
    key = slug + '.mp4'
    url = client.get_presigned_url(
        Method='PUT',
        Bucket='bucket-storage-1312694620',
        Key=key,
        Expired=600  # 120秒后过期，过期时间请根据自身场景定义,
    )

    return url

def download_source_url(slug):
    parent_path = Path(f"./data/{slug}")
    parent_path.mkdir(parents=True,exist_ok=True)
    file_path = parent_path / f"{slug}.mp4"
    file_path = str(file_path)
    key = slug + '.mp4'
    # 使用高级接口下载一次，不重试，此时没有使用断点续传的功能
    client.download_file(
        Bucket='bucket-storage-1312694620',
        Key=key,
        DestFilePath=file_path, # must be a str
        progress_callback=upload_percentage     
    )


if __name__ =="__main__":
    # 'C:/Users/future/Desktop/petal_20230425_170715.mp4'
    url = get_bucket_source_url('gwl-eraLi-123456')
    file_path = 'C:/Users/future/Desktop/petal_20230425_170715.mp4'
    requests.put(url=url,data=open(file=file_path,mode='rb'))
    download_source_url('gwl-eraLi-123456')