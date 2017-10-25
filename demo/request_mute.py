# coding=utf8
from ProgressedHttp import http

import hashlib


def run():
    # 初始化连接对象
    req = http.HTTPCons()

    # 发起http请求
    req.request("https://static.hellflame.net/resource/c8c12b1c34af9808c34fa60d862016b7")

    # 传递连接对象
    resp = http.SockFeed(req)

    # 必须要在 http_response 之前调用，设置 disable_progress = True
    resp.disable_progress = True
    
    # 获取http响应结果，响应结果保存在 resp.data 中
    resp.http_response()

    # 验证下载文件完整性
    assert hashlib.md5(resp.data).hexdigest() == '9a50ddbef4c82eb9003bd496a00e0989'


if __name__ == '__main__':
    run()
