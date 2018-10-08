# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-09
"""

import os
import pandas as pd

from python_myTools.files import MyFiles

current_father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def merge_dataSet(source, new):
    """
    # 合并两个数据集
    :param source: DataFrame格式
    :param new: DataFrame格式
    :return: 合并好的数据集。DataFrame格式
    """
    col = ['粤语', '普通话', '繁体']
    # 合并
    ret = source.append(new, ignore_index=True)
    # 判断new中与source中重复的数据，删掉
    ret.drop_duplicates(col, keep='first', inplace=True)
    return ret


def merge_dataSet_floder(source, new_path):
    print('正在合并文件夹：{}'.format(new_path))
    for idx, new_file in enumerate(MyFiles(new_path)):
        new = pd.read_excel(new_file)
        print('\t{} files: {}.. data size:{}'.format(idx, new_file, len(new_file)))
        source = merge_dataSet(source, new)
    print('current source data size:{}'.format(len(source)))
    return source


def main():
    # 打开当前的数据集
    source_path = os.path.join(current_father_path, 'output', 'ret.xlsx')
    try:
        source = pd.read_excel(source_path)
    except:
        source_path = os.path.join(current_father_path, 'download_data', 'source.xlsx')
        source = pd.read_excel(source_path)
    print('current source data size:{}'.format(len(source)))

    need_datas_path = [
        # yueyuge.cn
        os.path.join(current_father_path, 'download_data', 'yueyuge.cn', 'duihua'),
        os.path.join(current_father_path, 'download_data', 'yueyuge.cn', 'qingjing'),
        # fyan8.com
        os.path.join(current_father_path, 'download_data', 'fyan8.com', '1'),
        os.path.join(current_father_path, 'download_data', 'fyan8.com', '2'),
        # ted.com
        os.path.join(current_father_path, 'download_data', 'ted.com')
    ]
    # 合并数据集
    for new_path in need_datas_path:
        source = merge_dataSet_floder(source, new_path)

    # 保存数据集
    source.to_excel(source_path, index=False)


if __name__ == '__main__':
    main()
