# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-11
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os, re

from NLP_myTools.files import MyFiles


def get_page_resource(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('gb18030'), 'html.parser')
    try:
        title = soup.find('td', {'class': "biaoti"}).get_text()
    except :
        title = soup.find('td', {'class': "biaoti1"}).get_text()
    contents_elem = soup.find('td', {'class': "zwjd"}).find('p').get_text()

    resouce_list = []
    for idx,line in enumerate(contents_elem.split('\n')):
        if idx%2==1 : continue
        res = {}
        words = line.strip().split(' ')
        res['粤语'] = ''.join(words[1:])
        res['普通话'] = ""
        resouce_list.append(res)
    return resouce_list, title

def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_path, '..', 'download_data', 'fyan8.com', '2')
    # 列表页
    need_topic = [""] + list(range(2, 14))
    need_topic_url = 'http://www.fyan8.com/wenpin{}.htm'
    print('需要下载的topic 数量:', len(need_topic))

    for idx, topic in enumerate(need_topic):
        resource, title = get_page_resource(need_topic_url.format(topic))

        data_df = pd.DataFrame(columns=['粤语', '普通话'])
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