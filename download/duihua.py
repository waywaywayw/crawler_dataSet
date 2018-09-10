# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-10
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

from my_tools.my_files import MyFiles


def get_page_resource(url):
    """
    从给定资源页面爬取信息
    """
    ret = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf8'), 'html.parser').find('div', {'id':"player"})
    for talk in soup.findAll('p'):
        res = {}
        # 抽取对话
        talk = talk.get_text()
        talk_1 = talk.split('[粤]')[-1]
        yue, pu = talk_1.split('[普]')
        res['粤语'] = yue.strip()
        res['普通话'] = pu.strip()
        # print(res)
        ret.append(res)
    return ret


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_path, '..', 'download_data', 'yueyuge.cn', 'duihua')
    # 列表页
    page_duihua_url = 'http://www.yueyuge.cn/html/duihua/'

    response = requests.get(page_duihua_url)
    soup = BeautifulSoup(response.content.decode('utf8'), 'html.parser')
    duihua_list = soup.findAll('div', {'class':"desc pull-left"})
    print('常用对话用语 数量:', len(duihua_list))

    exist_duihua = list(MyFiles(output_path).file_name_no_suffix())
    for idx, duihua in enumerate(duihua_list):
        duihua = duihua.find('a')
        title = duihua['title']
        # 过滤掉已下载duihua
        if title in exist_duihua :
            print('{}. {}：已存在'.format(idx, title))
            continue
        url = duihua['href']

        data_df = pd.DataFrame(columns=['粤语', '普通话'])
        resource = get_page_resource(url)
        for _idx, res in enumerate(resource):
            data_df.loc[_idx] = [res['粤语'], res['普通话']]
            # data_df.loc[idx] = res.values()
            # 保存
        data_df.to_excel(os.path.join(output_path, title+'.xlsx'), index=False)
        print('{}. {}：下载完毕'.format(idx, title))
        # debug
        # break


if __name__ == '__main__' :
    main()