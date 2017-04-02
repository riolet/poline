from __future__ import print_function

import argparse
import unittest

import sys
from StringIO import StringIO

import poline.core
import poline.utilfuncs

class TestData:
    list_of_lists = [2, 4, 7, 5, 7, 6, 3, 2, 7, 5,
           6, 6, 6, 8, 9, 2, 6, 6, 7, 1,
           9, 4, 5, 2, 6, 3, 4, 2, 7, 7,
           4, 5, 8, 8, 7, 7, 9, 8, 7, 7,
           1, 9, 5, 7, 1, 6, 8, 6, 5, 6,
           9, 6, 9, 8, 3, 8, 5, 9, 9, 5,
           9, 7, 8, 4, 9, 7, 6, 8, 9, 5,
           9, 8, 5, 4, 5, 3, 9, 9, 9, 7,
           0, 4, 6, 4, 8, 4, 9, 8, 8, 9,
           7, 8, 3, 9, 3, 3, 8, 8, 9, 8]
    lsla = """total 28
drwxr-xr-x 11 default root  252 Apr  1 04:01 .
drwxrwxrwt  9 root    root  169 Apr  1 04:01 ..
drwxr-xr-x  8 default root  198 Apr  1 04:01 .git
-rw-r--r--  1 default root  300 Mar 31 14:33 .gitignore
-rw-r--r--  1 default root 1075 Mar 31 14:33 LICENSE
-rw-r--r--  1 default root 5730 Mar 31 14:39 README.md
drwxr-xr-x  2 default root   52 Mar 31 14:33 _compatibility"""

    find = """./poline_venv/lib/python3.4/site-packages/packaging/markers.py
./poline_venv/lib/python3.4/site-packages/packaging/requirements.py
./poline_venv/lib/python3.4/site-packages/packaging/specifiers.py
./poline_venv/lib/python3.4/site-packages/packaging/utils.py
./poline_venv/lib/python3.4/site-packages/packaging/version.py"""

class TestArgs(unittest.TestCase):

    def test_empty_args(self):
        try:
            poline.core.main(argv=[])
            self.assertTrue(False)
        except SystemExit as exc:
            self.assertEquals (exc.code, 2)

    def test_expression_only(self):
        try:
            poline.core.main(argv=['"Hello World"'])
        except SystemExit as exc:
            self.assertEquals(exc.code, 0)

    def test_opt_h(self):
        try:
            poline.core.main(argv=['-h'])
        except SystemExit as exc:
            self.assertEquals(exc.code, 0)

    def test_opt_s_only(self):
        try:
            poline.core.main(argv=['-s'])
        except SystemExit as exc:
            self.assertEquals(exc.code, 2)

    def test_opt_F_only(self):
        try:
            poline.core.main(argv=['-F'])
        except SystemExit as exc:
            self.assertEquals(exc.code, 2)


class TestUtilFuncs(unittest.TestCase):

    list_of_lists = [2, 4, 7, 5, 7, 6, 3, 2, 7, 5,
           6, 6, 6, 8, 9, 2, 6, 6, 7, 1,
           9, 4, 5, 2, 6, 3, 4, 2, 7, 7,
           4, 5, 8, 8, 7, 7, 9, 8, 7, 7,
           1, 9, 5, 7, 1, 6, 8, 6, 5, 6,
           9, 6, 9, 8, 3, 8, 5, 9, 9, 5,
           9, 7, 8, 4, 9, 7, 6, 8, 9, 5,
           9, 8, 5, 4, 5, 3, 9, 9, 9, 7,
           0, 4, 6, 4, 8, 4, 9, 8, 8, 9,
           7, 8, 3, 9, 3, 3, 8, 8, 9, 8]

    def test_counter(self):
        self.assertEquals(poline.utilfuncs.counter (TestData.list_of_lists, n=7),
                          [(9, 19), (8, 17), (7, 15), (6, 13), (5, 11), (4, 9), (3, 7)])

    def test_sh(self):
        test_string = "Hello World"

        result = next(poline.utilfuncs.sh('echo', '{}'.format(test_string)))
        self.assertEquals(test_string, result)

        result = next(poline.utilfuncs.sh('echo', '{}'.format(test_string), s=True))
        self.assertEquals(test_string.split(), result)

class TestChainedExpressions(unittest.TestCase):

    def test_chained_expression_awklike(self):
        self.assertEqual(poline.core.main(["['Hello World','Yellow World']","|_0"]), ['Hello', 'Yellow'])

    def test_chained_expression_awklike_with_FS(self):
        sys.stdin = StringIO(TestData.find)
        self.assertEqual(poline.core.main(["%/%_6"]), ['markers.py', 'requirements.py', 'specifiers.py', 'utils.py',
                                                       'version.py'])

    def test_chained_expression_tupled(self):
        sys.stdin = StringIO(TestData.lsla)
        self.assertEqual(next(poline.core.main(["skip(_)", "|_2", "counter(_)", ":x, c: [x,c]"])),
                         ['default', 6])


if __name__ == '__main__':
    unittest.main()
