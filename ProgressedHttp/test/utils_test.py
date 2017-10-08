# coding=utf8
from __future__ import absolute_import, division, print_function

import sys
import random
import string
import unittest

from ProgressedHttp.utils import *


class UtilTest(unittest.TestCase):
    def test_mono_font_width(self):
        self.assertEqual(0, str_len(u''))
        self.assertEqual(1, str_len(u' '))
        self.assertEqual(2, str_len(u'✔'))
        self.assertEqual(3, str_len(u'✔ '))

    def test_random_mono_font_width(self):
        self.assertEqual(100, str_len(u''.join([random.choice(string.ascii_letters) for _ in range(100)])))
        if sys.version_info.major == 2:
            self.assertEqual(str_len(u''.join([unichr(random.randrange(3105, 65535)) for _ in range(100)])), 200)
        else:
            self.assertEqual(str_len(u''.join([chr(random.randrange(3105, 65535)) for _ in range(100)])), 200)

    def test_unit_change(self):
        self.assertEqual('0.00 B', unit_change(0))
        self.assertEqual("-10", unit_change(-10))
        self.assertEqual("1.00 KB", unit_change(1025))
        self.assertEqual("1024.00 B", unit_change(1024))
        self.assertEqual("1.00 MB", unit_change(1024 * 1024 + 1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
