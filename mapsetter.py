import os
import sys
import ezdxf
import math
import numpy as np
import time





# 加载当前路径
sys.path.insert(0, os.path.abspath('..'))

class Read(object):
    """docstring for XInsert"""

    def __init__(self, dwg):
        # self.arg = arg
        self.dwg = dwg
        self.modelspace = dwg.modelspace()
        self.entities = []

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


def cal_end(b_end, rotation, start):

    # 计算insert中LINE在modelspace的终点
    ro = math.radians(rotation)
    sin = math.sin(ro)
    cos = math.cos(ro)

    # print('ro : ', rotation)
    x_e = b_end[0] * cos - b_end[1] * sin + start[0]
    y_e = b_end[0] * sin + b_end[1] * cos + start[1]
    # print('bend : ', b_end)
    # print('nend : ', int(x_e), int(y_e))

    return x_e, y_e


def inSegment(p, linea, lineb):
    """
    检查某交点是否在线段line上（不含line的端点），在求交点时已经确认两条直线不平行
    所以，对于竖直的line，lineb不可能竖直，却有可能水平，所以检查p是否在lineb上，只能检查x值即p[0]
    """
    if linea[0][0] == linea[1][0]: # 如果line竖直
        if min(linea[0][1], linea[1][1]) < p[1] < max(linea[0][1], linea[1][1]):
            if min(lineb[0][0], lineb[1][0]) <= p[0] <= max(lineb[0][0], lineb[1][0]):
                return True

    elif linea[0][1] == linea[1][1]  :  # 如果line水平
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
    # 计算实际交点，快？
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

def cal_crossover_point_v2(linea ,lineb):
    # 计算实际交点v2 ,慢？
    xa, ya = linea['start']
    xb, yb = linea['end']
    xc, yc = lineb['start']
    xd, yd = lineb['end']

    # 判断两条直线是否相交，矩阵行列式计算
    a = np.matrix(
        [
            [xb - xa, -(xd - xc)],
            [yb - ya, -(yd - yc)]
        ]
    )
    delta = np.linalg.det(a)
    # 不相交,返回两线段
    if np.fabs(delta) < 1e-6:
        return None
                      # 求两个参数lambda和miu
    c = np.matrix(
        [
            [xc - xa, -(xd - xc)],
            [yc - ya, -(yd - yc)]
        ]
    )
    d = np.matrix(
        [
            [xb - xa, xc - xa],
            [yb - ya, yc - ya]
        ]
    )
    lamb = np.linalg.det(c) / delta
    miu = np.linalg.det(d) / delta
    # 相交
    if 1 >= lamb >= 0 and 0 <= miu <= 1:
        x = xc + miu * (xd - xc)
        y = yc + miu * (yd - yc)
        return x, y
    # 相交在延长线上
    else:
        return None


def crossover(reader):

    while reader.entities:
        insert = reader.entities.pop()
        for line in reader.entities:
            if line['group'] != insert['group']:

                point = cal_crossover_point_v1(insert, line)

                if point :
                    pass

                    print(insert['block_name'], line['block_name'], point)

                    # x = (point[0] - insert['start'][0])
                    # y = (point[1] - insert['start'][1])
                    #
                    # print('xy ：： ', x, y)
                    # # 需要追加rotation的问题
                    # block = reader.dwg.blocks.get(insert['block_name'])
                    # block.add_line((-2, y), (+2, y))
                    #
                    # x = (point[0] - line['start'][0])
                    # y = (point[1] - line['start'][1])
                    #
                    # print('xy ：： ', x, y)
                    # # 需要追加rotation的问题
                    # block = reader.dwg.blocks.get(line['block_name'])
                    # block.add_line(( - 25, y+50), ( + 25, y-50))

if __name__ == '__main__':
    t1 = time.perf_counter()



    filepath = 'test1_2010.dxf'
    reader = Read(ezdxf.readfile(filepath))
    reader.get_insert_info()
    crossover(reader)
    reader.dwg.saveas('daaaa.dxf')


    t2 = time.perf_counter()
    print(t2-t1)


