from __future__ import print_function

import argparse
import unittest

import sys

import poline.core
import poline.utilfuncs

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

    def test_counter(self):
        l = [2, 4, 7, 5, 7, 6, 3, 2, 7, 5,
           6, 6, 6, 8, 9, 2, 6, 6, 7, 1,
           9, 4, 5, 2, 6, 3, 4, 2, 7, 7,
           4, 5, 8, 8, 7, 7, 9, 8, 7, 7,
           1, 9, 5, 7, 1, 6, 8, 6, 5, 6,
           9, 6, 9, 8, 3, 8, 5, 9, 9, 5,
           9, 7, 8, 4, 9, 7, 6, 8, 9, 5,
           9, 8, 5, 4, 5, 3, 9, 9, 9, 7,
           0, 4, 6, 4, 8, 4, 9, 8, 8, 9,
           7, 8, 3, 9, 3, 3, 8, 8, 9, 8]
        self.assertEquals(poline.utilfuncs.counter (l, n=7),
                          [(9, 19), (8, 17), (7, 15), (6, 13), (5, 11), (4, 9), (3, 7)])

    def test_sh(self):
        test_string = "Hello World"

        result = next(poline.utilfuncs.sh('echo', '{}'.format(test_string)))
        self.assertEquals(test_string, result)

        result = next(poline.utilfuncs.sh('echo', '{}'.format(test_string), s=True))
        self.assertEquals(test_string.split(), result)


if __name__ == '__main__':
    unittest.main()