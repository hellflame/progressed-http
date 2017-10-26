# coding=utf8
from __future__ import absolute_import, division, print_function

import sys

__all__ = ['str_len', 'unit_change', 'is_python3', 'is_python2']

def is_python3():
    return sys.version_info.major == 3

def is_python2():
    return not is_python3()

def str_len(s):
    """
    获取占用等宽字体终端实际宽度，适用`Monaco`等其他等宽字体字体
    :param s:
    :return:
    """
    length = 0
    for i in s:
        # Chinese,Japanese,Korean character utf8 range
        # Test Font `Monaco`
        if 3105 <= ord(i) <= 65535:
            length += 2
        else:
            length += 1
    return length


def unit_change(target):
    """
    单位换算
    :param target: unsigned int
    :return: str
    """
    if target < 0:
        return str(target)
    unit_list = ('B', 'KB', 'MB', 'GB', 'TB')
    index = 0
    target = float(target)
    while target > 1024:
        index += 1
        target /= 1024
    # 输出浮点数宽度固定
    return "{:.2f} {}".format(round(target, 2), unit_list[index])



