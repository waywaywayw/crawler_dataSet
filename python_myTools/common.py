# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-29
"""

import re


def dereplicate(elems):
    """删除重复元素，保证元素顺序不变"""
    ret_elems = []
    for elem in elems:
        if elem not in ret_elems:
            ret_elems.append(elem)
    return ret_elems



if __name__ == '__main__':
    list1 = [1, 7, 8, 2, 4, 1, 5, 4, 8, 1, 7, 9, 4, 3]
    print(dereplicate(list1))