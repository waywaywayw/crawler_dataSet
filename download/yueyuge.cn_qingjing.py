# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-10
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os, re

from my_tools.my_files import MyFiles


def get_page_resource(url):
    """
    从给定资源页面爬取信息
    """
    ret = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf8'), 'html.parser').find('div', {'id':"player"})
    p = soup.get_text().strip()
    talk = p.split('[粤]')
    for talk_1 in talk:
        if not len(talk_1) : continue
        res = {}
        # 抽取对话
        try:
            yue, pu = talk_1.strip().split('\n\n')
        except Exception as e:
            yue, pu = talk_1.strip().split('\n')
            pass
        res['粤语'] = yue.strip()
        res['普通话'] = pu.strip()
        # print(res)
        ret.append(res)
    return ret


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_path, '..', 'download_data', 'yueyuge.cn', 'qingjing')
    # 列表页
    page_duihua_url = 'http://www.yueyuge.cn/html/qingjing/'

    response = requests.get(page_duihua_url)
    soup = BeautifulSoup(response.content.decode('utf8'), 'html.parser')
    duihua_list = soup.findAll('div', {'class':"desc pull-left"})
    print('常用情景用语 数量:', len(duihua_list))

    exist_duihua = list(MyFiles(output_path).file_name_no_suffix())
    for idx, duihua in enumerate(duihua_list):
        duihua = duihua.find('a')
        title = duihua['title']
        # 过滤掉已下载duihua 或者 不是'情景对话用语'开头的文章
        if title in exist_duihua or title.startswith('情景对话用语')<0 :
            print('{}. 已存在或者不符合格式:{}'.format(idx, title))
            continue
        url = duihua['href']

        data_df = pd.DataFrame(columns=['粤语', '普通话'])
        resource = get_page_resource(url)
        for _idx, res in enumerate(resource):
            data_df.loc[_idx] = [res['粤语'], res['普通话']]
            # data_df.loc[idx] = res.values()
            # 保存
        data_df.to_excel(os.path.join(output_path, title+'.xlsx'), index=False)
        print('{}. 下载完毕:{}'.format(idx, title))
        # debug
        # break


if __name__ == '__main__' :
    main()