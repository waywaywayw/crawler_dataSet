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
    2. 替换数据： 替换掉字符串里面包含的（普通话文字）（粤语文字）
    3. 去掉数据： 粤语栏只包含词语，并且肯定不是粤语词语的。记录no_yue_token
    """
    no_yue_token = [
         '壹'
        ,'贰'
        ,'叁'
        ,'肆'
        ,'伍'
        ,'陆'
        ,'柒'
        ,'捌'
        ,'玖'
        ,'拾'
        ,'佰'
        ,'仟'
        ,'万'
        ,'圆'
        ,'零'
        ,'分'
        ,'角'
        ,'整'
    ]
    # for idx
    # source = source[source[0] not in no_yue_token]
    return source


def main():
    source_path = os.path.join(current_father_path, 'output', 'ret.xlsx')
    source = pd.read_excel(source_path)

    source = clean(source)

    output_path = os.path.join(current_father_path, 'output', 'ret_cleaned.xlsx')
    source.to_excel(output_path, index=False)


if __name__ == '__main__':
    # 考虑加入去重：粤语和普通话的字符串一模一样的数据，删掉
    main()
