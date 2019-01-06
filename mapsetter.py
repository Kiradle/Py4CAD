import os
import sys
import ezdxf

import math


class XBlock(object):
    """docstring for XBlock"""

    def __init__(self, insert):
        self.name = insert.dxf.name
        # block中line的起点、终点坐标
        self.b_start = insert
        self.b_end = ""

    def set_insert(self, insert, rotation):
        pass

    def get_info(self, name):


class XInsert(XBlock):
    """docstring for XInsert"""

    def __init__(self, name, b_start, b_end, insert, rotation):
        super(XInsert, self).__init__(name, b_start, b_end)
        # insert的基点坐标
        self.insert = insert[:2]
        # insert的角度
        self.rotation = rotation


if __name__ == '__main__':
    pass
