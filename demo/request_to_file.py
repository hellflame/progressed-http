# coding=utf8
from ProgressedHttp import http

import hashlib


def run():
    file_path = '1m.data'

    # 初始化连接对象
    req = http.HTTPCons()

    # 发起http请求
    req.request("https://static.hellflame.net/resource/c8c12b1c34af9808c34fa60d862016b7")

    # 传递连接对象
    resp = http.SockFeed(req)

    # 获取http响应结果，并保存在 `1m.data` 文件中
    resp.http_response(file_path, overwrite=True)  # 多次下载，文件将被重写

    # 验证下载文件完整性
    with open(file_path, 'rb') as handle:
        # 如果上面请求结束未关闭文件，这里将无法读取全部文件
        content = handle.read()

    assert hashlib.md5(content).hexdigest() == '9a50ddbef4c82eb9003bd496a00e0989'


if __name__ == '__main__':
    run()


