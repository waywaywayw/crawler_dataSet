# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-09
"""

import os
import pandas as pd



def merge(source, new):
    """
    # 合并两个数据集
    :param source:
    :param new:
    :return:
    """
    col = ['粤语', '普通话']
    # 合并
    ret = source.append(new, ignore_index=True)
    # 判断new中与source中重复的数据，删掉
    ret.drop_duplicates(['粤语'], keep='first', inplace=True)
    return ret

def main():
    source_path = os.path.join('test_data', 'source.xlsx')
    new_path = os.path.join('test_data', 'new1.xlsx')
    source = pd.read_excel(source_path, header=True)
    new = pd.read_excel(new_path, header=True)

    ret = merge(source, new)

    output_path = os.path.join('output', 'ret.xlsx')
    ret.to_excel(output_path, index=False)



if __name__ == '__main__' :
    # 考虑加入去重：粤语和普通话的字符串一模一样的数据，删掉
    main()