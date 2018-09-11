# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-09
"""

import os
import pandas as pd

current_father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clean(source):
    """
    简单清洗数据集。
    1. 去掉数据： 粤语栏和普通话栏的字符串完全一样的数据
    2. 去掉数据： 粤语栏只包含词语，并且肯定不是粤语词语的。记录no_yue_token
    """

    need_del_rows = []
    for idx, row in source.iterrows():
        if row['粤语']==row['普通话']:
            need_del_rows.append(idx)

    source.drop(need_del_rows, inplace=True)
    return source


def main():
    source_path = os.path.join(current_father_path, 'output', 'ret.xlsx')
    source = pd.read_excel(source_path)
    print('current source data size:{}'.format(len(source)))

    source = clean(source)

    output_path = os.path.join(current_father_path, 'output', 'ret_cleaned.xlsx')
    source.to_excel(output_path, index=False)
    print('清洗并保存完毕.')
    print('current source data size:{}'.format(len(source)))

if __name__ == '__main__':
    main()
