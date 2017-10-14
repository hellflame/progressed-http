# coding=utf8
from __future__ import absolute_import, division, print_function

import os
import unittest
import hashlib
import tempfile

from ProgressedHttp.http import *
from ProgressedHttp.http import quote


class HTTPTest(unittest.TestCase):
    """
    static.hellflame.net
        域名下的文件大多数情况下大文件都是chunked编码，小文件可能会被缓存为正常编码
        文件内容为大小与hash已知的随机二进制文件
    raw.githubusercontent.com
        域名下文件未分块
        文件来自 https://raw.githubusercontent.com/hellflame/qiniu_manager/v1.4.6/qiniuManager/manager.py
    """
    @staticmethod
    def chunked_info(resp):
        return "分块编码" if resp.chunked else "常规编码"

    def test_url_parser(self):
        parser = HTTPCons.url_parser
        self.assertDictEqual(parser("http://www.hellflame.net:233/root/hellflame"), {
            'scheme': 'http',
            'host': 'www.hellflame.net',
            'port': 233,
            'href': '/root/hellflame'
        })

        self.assertDictEqual(parser("https://ok/"), {
            'scheme': 'https',
            'host': 'ok',
            'port': 443,
            'href': '/'
        })

        self.assertDictEqual(parser("hellflame.net/"), {
            'scheme': 'http',
            'host': 'hellflame.net',
            'port': 80,
            'href': '/'
        })

        self.assertDictEqual(parser("hellflame.net"), {
            'scheme': 'http',
            'host': 'hellflame.net',
            'port': 80,
            'href': '/'
        })

        self.assertDictEqual(parser("http://hell.net:443"), {
            'scheme': 'http',
            'host': 'hell.net',
            'port': 443,
            'href': '/'
        })

        self.assertDictEqual(parser("https://hell.net:80"), {
            'scheme': 'https',
            'host': 'hell.net',
            'port': 80,
            'href': '/'
        })

        self.assertDictEqual(parser("hell.net:443"), {
            'scheme': 'http',
            'host': 'hell.net',
            'port': 443,
            'href': '/'
        })

    def test_http_parser_quote(self):
        parser = HTTPCons.http_parser

        host = 'www.hellflame.net'
        href = '/what'
        method = 'get'

        result = parser(host, href, method, None, {'name': '中文'})
        href += '?name={}'.format(quote('中文'))

        self.assertEqual(result['request'], "{method} {href} HTTP/1.1".format(method=method.upper(), href=href))

    def test_http_parser_simple_get(self):
        parser = HTTPCons.http_parser

        host = 'www.hellflame.net'
        href = '/'
        method = 'get'

        basic_header = {
            'Host': host,
            'User-Agent': HTTPCons.user_agent,
            'Connection': 'close'
        }

        result = parser(host, href, method, None, None)
        self.assertEqual("{method} {href} HTTP/1.1".format(method=method.upper(), href=href), result['request'])
        self.assertEqual(result['entity'], '')
        for k, v in basic_header.items():
            self.assertTrue("{}: {}".format(k, v) in result['headers'])

    def test_http_parser_simple_post(self):
        parser = HTTPCons.http_parser

        host = 'www.hellflame.net'
        href = '/post'
        method = 'post'

        basic_header = {
            'Host': host,
            'User-Agent': HTTPCons.user_agent,
            'Connection': 'close'
        }

        result = parser(host, href, method, None, None)
        self.assertEqual("{method} {href} HTTP/1.1".format(method=method.upper(), href=href), result['request'])
        self.assertEqual(result['entity'], '')
        for k, v in basic_header.items():
            self.assertTrue("{}: {}".format(k, v) in result['headers'])

        data = "this is post data part"

        result = parser(host, href, method, None, data)
        self.assertEqual("{method} {href} HTTP/1.1".format(method=method.upper(), href=href), result['request'])
        self.assertEqual(result['entity'], data)
        for k, v in basic_header.items():
            self.assertTrue("{}: {}".format(k, v) in result['headers'])

    def test_http_parser_with_header(self):
        parser = HTTPCons.http_parser

        host = 'www.hellflame.net'
        href = '/post'
        method = 'post'

        basic_header = {
            'Host': host,
            'User-Agent': HTTPCons.user_agent,
            'Connection': 'close',
            'Access-Allow-Origin': '*',
            'Name': 'Done'
        }

        result = parser(host, href, method, {'Access-Allow-Origin': '*', 'Name': 'Done'}, None)
        self.assertEqual("{method} {href} HTTP/1.1".format(method=method.upper(), href=href), result['request'])
        self.assertEqual(result['entity'], '')
        for k, v in basic_header.items():
            self.assertTrue("{}: {}".format(k, v) in result['headers'])

        data = "this is post data part"

        result = parser(host, href, method, {'Access-Allow-Origin': '*', 'Name': 'Done'}, data)
        self.assertEqual("{method} {href} HTTP/1.1".format(method=method.upper(), href=href), result['request'])
        self.assertEqual(result['entity'], data)
        for k, v in basic_header.items():
            self.assertTrue("{}: {}".format(k, v) in result['headers'])

    def test_response_in_memory(self):
        req = HTTPCons()
        req.request("https://static.hellflame.net/resource/c8c12b1c34af9808c34fa60d862016b7")
        resp = SockFeed(req)
        resp.disable_progress = True
        resp.http_response()
        self.assertEqual(hashlib.md5(resp.data).hexdigest(),
                         '9a50ddbef4c82eb9003bd496a00e0989',
                         "请保持数据获取正确完整, " + self.chunked_info(resp))

    def test_response_downloading(self):
        file_path = os.path.join(tempfile.gettempdir(), '1m.data')
        req = HTTPCons()
        req.request("https://static.hellflame.net/resource/c8c12b1c34af9808c34fa60d862016b7")
        resp = SockFeed(req)
        resp.disable_progress = True
        resp.http_response(file_path, overwrite=True)

        with open(file_path, 'rb') as handle:
            # 如果上面请求结束未关闭文件，这里将无法读取全部文件
            content = handle.read()

        os.remove(resp.file_handle.name)
        self.assertEqual(hashlib.md5(content).hexdigest(),
                         '9a50ddbef4c82eb9003bd496a00e0989',
                         "这里出错，多半是因为没有关闭文件, " + self.chunked_info(resp))

    def test_small_response_in_memory(self):
        req = HTTPCons()
        req.request("https://static.hellflame.net/resource/5573012afe7227ab4457331df42af57d")
        resp = SockFeed(req)
        resp.disable_progress = True
        resp.http_response()
        self.assertEqual(hashlib.md5(resp.data).hexdigest(),
                         '8688229badcaa3cb2730dab99a618be6',
                         "请保持数据获取正确完整, " + self.chunked_info(resp))

    def test_small_response_downloading(self):
        file_path = os.path.join(tempfile.gettempdir(), '3k.data')
        req = HTTPCons()
        req.request("https://static.hellflame.net/resource/5573012afe7227ab4457331df42af57d")
        resp = SockFeed(req)
        resp.disable_progress = True
        resp.http_response(file_path, overwrite=True)
        with open(file_path, 'rb') as handle:
            # 如果上面请求结束未关闭文件，这里将无法读取全部文件
            content = handle.read()
        os.remove(resp.file_handle.name)
        self.assertEqual(hashlib.md5(content).hexdigest(),
                         '8688229badcaa3cb2730dab99a618be6',
                         "这里出错，多半是因为没有关闭文件, " + self.chunked_info(resp))

    def test_request_get(self):
        resp = get("https://static.hellflame.net/resource/5573012afe7227ab4457331df42af57d", disable_progress=True)
        self.assertEqual(hashlib.md5(resp.data).hexdigest(), '8688229badcaa3cb2730dab99a618be6')

    @unittest.skip("GFW's Fault")
    def test_non_chunked_in_memory(self):
        req = HTTPCons()
        req.request("https://raw.githubusercontent.com/hellflame/qiniu_manager/v1.4.6/qiniuManager/manager.py")
        resp = SockFeed(req)
        resp.disable_progress = True
        resp.http_response()
        self.assertEqual(hashlib.md5(resp.data).hexdigest(),
                         '276efce035d49f7f3ea168b720075523',
                         "请保持数据获取正确完整，" + self.chunked_info(resp))

    @unittest.skip("GFW's Fault")
    def test_test_non_chunked_downloading(self):
        file_path = os.path.join(tempfile.gettempdir(), 'manager.py')
        req = HTTPCons()
        req.request("https://raw.githubusercontent.com/hellflame/qiniu_manager/v1.4.6/qiniuManager/manager.py")
        resp = SockFeed(req)
        resp.disable_progress = True
        resp.http_response(file_path, overwrite=True)
        with open(file_path, 'rb') as handle:
            content = handle.read()
        os.remove(resp.file_handle.name)
        self.assertEqual(hashlib.md5(content).hexdigest(),
                         '276efce035d49f7f3ea168b720075523',
                         "请保持数据获取正确完整，" + self.chunked_info(resp))


if __name__ == '__main__':
    unittest.main(verbosity=2)

