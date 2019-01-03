#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Author: Kiradle
# Created: 2019.01.01

__author__ = "Kiradle <kiradle@outlook.com>"

"""
    程序目的：
        自动添加【正/侧孔】标记，或导出每条钢料【正/侧孔】位置信息。

    过程分析：
        1.读取*.dxf文件，将每条【实例】线段块【分组】，将【实例】线段块【名称】与其【实例基点坐标】记入【实例字典】(eg:{name1:(x1, y1), })，将存在线段块的【分组】记入【分组表】
        2.遍历所有【类】线段块，将每个块包含的线段（有且仅有一条）的【起止点坐标】记入【类线段块字典】(eg:{name1:[(起点x, 起点y), (终点x, 终点y)], })
        3.遍历【实例字典】，找到每一条【实例】所对应的【类起止点坐标】，组合成【实例起止点坐标】，将其记入【实例起止点坐标字典】，
        4.多重遍历循环，计算不同分组可能且可以（”可以“是指相同分组的不打孔，u和c分组不打孔等等，详查【打孔规则表】）产生交点的【实例交点坐标】，
          然后分别与两条线段的【实例基点坐标】组合成【类交点坐标】
        5.创建以【类块】为名的列表（或元组），将【类交点】记入创建的列,(正侧孔信息判断可以在循环内,也可以记录与之相交线段的类别,循环结束后在判断)
        6.将各个【类交点】画至该【类块】上。

    问题点：
        a.以用class 与 实例方式 实现 各个实例线段的记录，但问题是实例是否占用过大，基点和起始点只是过程使用数据，可以回收，实例的回收不知效果如何。
        b.让分组表独立是想防止表过于臃肿，但是计算速度上是否有提升尚未可知。

    功能点：
        · 迭代实例线段记录&分组
        · 迭代生成类线段记录
        · 迭代生成实例起止点


"""

import os
import sys
import ezdxf

# 加载当前路径
sys.path.insert(0, os.path.abspath('..'))

# 创建实例分组列表
EntiriesGroupList = []


# def get_entity(filename):



        # if eInsert.name[0].upper() not in EntiriesGroupList :
        #     EntiriesGroupList.append(eInsert.name[0].upper())

        # u_list = []
        # b_list = []
        # c_list = []
        # d_list = []



        # try:
        #     for e in eInsert:
        #         print(e.dxftype)
        # except Exception as e:
        #     print(eInsert.name+" has no e")



if __name__ == '__main__':

    # get_entity("test1_shilituxing_weibiaoji.dxf")
    # get_entity("test1_shilituxing.dxf")
    dwg = ezdxf.readfile("test1_shilituxing.dxf")
    print(dwg.encoding)

    msp = dwg.modelspace()
    for e in msp:
        print(e.get_dxf_attrib('name'))

        # if e.dxftype() == 'INSERT':
            # print(e.dxfattribs())