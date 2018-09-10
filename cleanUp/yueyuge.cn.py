# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-09
"""

import os
import pandas as pd

from my_tools.my_files import MyFiles


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
    current_father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    source_path = os.path.join(current_father_path, 'download_data', 'source.xlsx')
    source = pd.read_excel(source_path)

    # 合并duihua
    new_path = os.path.join(current_father_path, 'download_data', 'yueyuge.cn', 'duihua')
    new_path_list = MyFiles(new_path)
    for idx, new_file in enumerate(new_path_list):
        new = pd.read_excel(new_file)
        source = merge(source, new)
        print('merge {} file.. cur_size:{}'.format(idx, len(source)))

    # 合并qingjing
    # new_path = os.path.join(current_father_path, 'download_data', 'yueyuge.cn', 'qingjing')
    # new_path_list = MyFiles(new_path)
    # for idx, new_file in enumerate(new_path_list):
    #     new = pd.read_excel(new_file)
    #     source = merge(source, new)
    #     print('merge {} file.. cur_size:{}'.format(idx, len(source)))

    output_path = os.path.join(current_father_path, 'output', 'ret.xlsx')
    source.to_excel(output_path, index=False)



if __name__ == '__main__' :
    # 考虑加入去重：粤语和普通话的字符串一模一样的数据，删掉
    main()