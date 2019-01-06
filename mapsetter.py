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

    # 获取insert基点
    def get_insert_info(self, insert):
        pass

    # 分组block
    def set_group(self, group_list):
        pass

    # 计算insert中LINE在modelspace的起止点
    def cal_coordinate(self, insert):
        pass
# 利用观察者模式中的通知来操作所有类的实例。


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
