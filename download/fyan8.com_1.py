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
        title = soup.find('td', {'class': "biaoti1"}).get_text()
    except Exception as e:
        title = soup.find('td', {'class': "biaoti"}).get_text()
    contents_elem = soup.find('td', {'class': "zwjd"})

    resouce_list = []
    for content_elem in contents_elem.findAll('p'):
        res = {}
        content_list = content_elem.get_text().split('\n')
        res['粤语'] = content_list[0].strip()
        if len(content_list)==3 :
            res['普通话'] = content_list[2].strip()
        else :
            res['普通话'] = ""
        resouce_list.append(res)
    return resouce_list, title

def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_path, '..', 'download_data', 'fyan8.com', '1')
    # 列表页
    need_topic = ['rwenhou', 'rhanxuan', 'rjieshao', 'rxunwen', 'rqingqiu', 'rganxie', 'rdaoqian', 'ryaoqing', 'rlvyou', ]
    need_topic_url = 'http://www.fyan8.com/{}.htm'
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