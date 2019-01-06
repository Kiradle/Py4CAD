import os
import sys
import ezdxf

import math


class Read(object):
    """docstring for XInsert"""

    def __init__(self, dwg):
        # self.arg = arg
        self.dwg = dwg
        self.modelspace = dwg.modelspace()
        self.Entities = []

    # 获取insert基点
    def get_insert_info(self):
        i = 0
        for insert in self.modelspace.query('INSERT'):
            block = self.dwg.blocks[insert.dxf.name]
            for e in block:
                # 对应Block包含"LINE"的Insert才能被记录下来
                if e.dxftype() == 'LINE':
                    i += 1
                    block_name = insert.dxf.name
                    # 角度
                    rotation = insert.dxf.rotation
                    # Insert中line的起点、终点坐标
                    start = insert.dxf.insert[:2]
                    end = cal_end(e.dxf.end[:2], rotation, start)
                    self.set_entity_line(i, block_name, rotation, start, end)

    def set_entity_line(self, i, block_name, rotation, start, end):
        entity = {}
        entity['id'] = block_name[0].upper() + str(i)
        entity['block_name'] = block_name
        # 分组，暂时用首字符
        entity['group'] = block_name[0].lower()
        # 角度
        entity['rotation'] = rotation
        # Insert中line的起点、终点坐标
        entity['start'] = start
        entity['end'] = end
        self.Entities.append(entity)


    # 分组block
    def set_group(self, group_list):
        pass


# 计算insert中LINE在modelspace的终点
def cal_end(bend, rotation, start):
    x, y = bend
    ro = math.radians(rotation)
    sin = math.sin(ro)
    cos = math.cos(ro)
    x_e = x * cos - y * sin + start[0]
    y_e = x * sin + y * cos + start[1]

    return (x_e, y_e)

# 利用观察者模式中的通知来操作所有类的实例？



class XInsert_bak():
    """docstring for XInsert"""

    def __init__(self, insert):
        # super(XInsert, self).__init__(name, b_start, b_end)
        self.name = insert.dxf.name
        # insert的基点坐标
        self.insert = insert.dxf.insert[:2]
        # insert的角度
        self.rotation = insert.dxf.rotation

    def set_group(self):
        pass


class XGroup():

    def __init__(self):
        self.group_name = group_name




if __name__ == '__main__':
    filepath = 'test2.dxf'
    reader = Read(ezdxf.readfile(filepath))
    reader.get_insert_info()
    for i in reader.Entities:
        print(i)
