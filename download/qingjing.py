# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-10
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

from NLP_myTools.files import MyFiles


current_path = os.path.dirname(os.path.abspath(__file__))
headers = {'Connection': 'Keep-Alive'
           # ,'Host': 'zhannei.baidu.com'
           ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}


def get_page_resource_list(start_url):
    """
    从start_url页面获取所有资源页面列表。
    :return 资源页面列表。dict格式，形如： page_resource_list = [ {'url':'http:www.emmm.com', 'title':'emm'}, {'url':'http:www.233.com', 'title':'233'}]
    """
    # 发送请求
    response = requests.get(start_url, headers=headers)
    # 找到资源页列表
    soup = BeautifulSoup(response.content.decode('utf8'), 'html.parser')
    page_resource_list_elem = soup.findAll('div', {'class': "desc pull-left"})
    # 获取page_resource_list
    page_resource_list = []
    for idx, page_resource_elem in enumerate(page_resource_list_elem):
        page_resource = {}
        resource_elem = page_resource_elem.find('a')
        # 获取resource的各种属性   to do
        # dict格式. url项必须有, 其他可选(比如title)
        page_resource['title'] = resource_elem['title']
        page_resource['url'] = resource_elem['href']
        page_resource_list.append(page_resource)
    return page_resource_list


def get_resource_from_page_resource(page_resource):
    """
    从资源页面爬取所需的资源。
    :return 所需的资源列表。dict格式，形如：resource_list = [ {'need_name1':'v1', 'need_name2':'v2'}, {'need_name3':'v3'}]
    """
    resource_list = []
    response = requests.get(page_resource['url'], headers=headers)
    soup = BeautifulSoup(response.content.decode('utf8'), 'html.parser')
    # 解析response, 并保存资源
    p_elem = soup.find('div', {'id':"player"})
    p = p_elem.get_text().strip()
    talk = p.split('[粤]')
    for talk_1 in talk:
        if not len(talk_1): continue
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
        resource_list.append(res)
    return resource_list


def main():
    output_path = os.path.join(current_path, '..', 'download_data', 'yueyuge.cn', 'qingjing')

    start_url = 'http://www.yueyuge.cn/html/qingjing/'
    # 获取page_resource_list
    page_resource_list = get_page_resource_list(start_url)
    # 判重（可选）
    exist_page_resource = list(MyFiles(output_path).file_name_no_suffix())
    page_resource_list = list(filter(lambda x: x['title'] not in exist_page_resource and x['title'].startswith('情景对话用语')>=0, page_resource_list))

    print('需要下载的页面 数量：', len(page_resource_list))
    # 遍历所有page_resource_list
    for idx, page_resource in enumerate(page_resource_list):
        # 获取需要的资源
        resources = get_resource_from_page_resource(page_resource)
        # 保存资源  to do
        data_df = pd.DataFrame(columns=['粤语', '普通话'])
        for _idx, res in enumerate(resources):
            data_df.loc[_idx] = [res['粤语'], res['普通话']]
            # data_df.loc[idx] = res.values()
        data_df.to_excel(os.path.join(output_path, page_resource['title'] + '.xlsx'), index=False)
        print('{}. {}：下载完毕'.format(idx, page_resource['title']))
        # debug
        # break


if __name__ == '__main__':
    main()
