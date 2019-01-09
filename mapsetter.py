import os
import sys
import ezdxf
import math
import time

# 加载当前路径
sys.path.insert(0, os.path.abspath('..'))


class Read(object):
    """docstring for XInsert"""

    def __init__(self, dwg):
        # self.arg = arg
        self.dwg = dwg
        self.mspace = dwg.modelspace()
        self.entities = []

    # 获取insert基点
    def get_insert_info(self):
        i = 0
        for insert in self.mspace.query('INSERT'):
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
                    end = cal_insert_end(e.dxf.end[:2], rotation, start)
                    self.set_entity_line(i, block_name, rotation, start, end)

    def set_entity_line(self, i, block_name, rotation, start, end):
        # 分组，暂时用首字符
        # 角度
        # Insert中line的起点、终点坐标
        entity = {
            'id': block_name[0].upper() + str(i),
            'block_name': block_name,
            'group': block_name[0].lower(),
            'rotation': rotation,
            'start': start,
            'end': end
        }

        self.entities.append(entity)


def cal_insert_end(b_end, rotation, start):
    # 计算insert中LINE在mspace的终点
    ro = math.radians(rotation)
    sin = math.sin(ro)
    cos = math.cos(ro)

    # print('ro : ', rotation)
    x = b_end[0] * cos - b_end[1] * sin + start[0]
    y = b_end[0] * sin + b_end[1] * cos + start[1]

    return x, y


def cal_block_point(point, rotation):
    pass
    # 计算crossover point在block中的坐标 可以与cal_insert_end合并
    ro = math.radians(360 - rotation)
    sin = math.sin(ro)
    cos = math.cos(ro)

    # print('ro : ', rotation)
    x = point[0] * cos - point[1] * sin
    y = point[0] * sin + point[1] * cos

    return x, y


def inSegment(p, linea, lineb):
    """
    检查某交点是否在线段line上（不含line的端点），在求交点时已经确认两条直线不平行
    所以，对于竖直的line，lineb不可能竖直，却有可能水平，所以检查p是否在lineb上，只能检查x值即p[0]
    """
    if linea[0][0] == linea[1][0]:  # 如果line竖直
        if min(linea[0][1], linea[1][1]) < p[1] < max(linea[0][1], linea[1][1]):
            if min(lineb[0][0], lineb[1][0]) <= p[0] <= max(lineb[0][0], lineb[1][0]):
                return True

    elif linea[0][1] == linea[1][1]:  # 如果line水平
        if min(linea[0][0], linea[1][0]) < p[0] < max(linea[0][0], linea[1][0]):
            if min(lineb[0][1], lineb[1][1]) <= p[1] <= max(lineb[0][1], lineb[1][1]):
                return True

    else:
        if min(linea[0][0], linea[1][0]) < p[0] < max(linea[0][0], linea[1][0]):
            # line为斜线时，lineb有可能竖直也有可能水平，所以对x和y都需要检查
            if min(lineb[0][1], lineb[1][1]) <= p[1] <= max(lineb[0][1], lineb[1][1]) and \
                    min(lineb[0][0], lineb[1][0]) <= p[0] <= max(lineb[0][0], lineb[1][0]):
                return True

    return False


def cal_crossover_point_v1(linea, lineb):
    # 计算实际交点
    xa, ya = linea['start']
    xb, yb = linea['end']
    xc, yc = lineb['start']
    xd, yd = lineb['end']

    try:
        x = ((xa * yb - ya * xb) * (xc - xd) - (xa - xb) * (xc * yd - yc * xd)) / (
                (xa - xb) * (yc - yd) - (ya - yb) * (xc - xd))
        y = ((xa * yb - ya * xb) * (yc - yd) - (ya - yb) * (xc * yd - yc * xd)) / (
                (xa - xb) * (yc - yd) - (ya - yb) * (xc - xd))

        if inSegment((x, y), ((xa, ya), (xb, yb)), ((xc, yc), (xd, yd))):
            return x, y
        else:
            return None
    except ZeroDivisionError:
        # 平行
        return None


def crossover(dwg_info):
    # 循环取出最后一个线段与剩余的计算交点坐标
    while dwg_info.entities:
        insert = dwg_info.entities.pop()
        for line in dwg_info.entities:
            if line['group'] != insert['group']:

                point = cal_crossover_point_v1(insert, line)

                if point:
                    
                    cp = (point[0] - insert['start'][0], point[1] - insert['start'][1])
                    cpa = cal_block_point(cp, insert['rotation'])
                    cp = (point[0] - line['start'][0], point[1] - line['start'][1])
                    cpb = cal_block_point(cp, line['rotation'])

                    print(insert['block_name'], cpa, line['block_name'], cpb)

                    block = dwg_info.dwg.blocks.get(insert['block_name'])
                    block.add_line((-25, cpa[1] + 50), (+25, cpa[1] - 50))
                    block = dwg_info.dwg.blocks.get(line['block_name'])
                    block.add_line((- 25, cpb[1] + 50), (+ 25, cpb[1] - 50))


if __name__ == '__main__':
    t1 = time.perf_counter()

    filepath = 'test1_2010.dxf'
    reader = Read(ezdxf.readfile(filepath))
    reader.get_insert_info()
    crossover(reader)
    reader.dwg.saveas('daaaa.dxf')

    t2 = time.perf_counter()
    print(t2 - t1)
