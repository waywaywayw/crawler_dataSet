# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-10
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os, re

from NLP_myTools.files import MyFiles


def get_page_resource(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('gb18030'), 'html.parser')
    title = soup.find('td', {'class': "biaoti1"}).get_text()
    raw_data = soup.find('td', {'class': "zwjd"}).get_text()

    resouce_list = []
    res = {}
    for line in raw_data.split('\n'):
        if not len(line.strip()) :
            resouce_list.append(res)
            res = {}
        else :
            if '粤语' in res:
                res['普通话'] = line.strip()
            else :
                res['粤语'] = line.strip()
    return resouce_list, title

def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_path, '..', 'download_data', 'fyan8')
    # 列表页
    need_topic = ['rwenhou', 'rhanxuan', 'rjieshao', 'rxunwen', 'rqingqiu', 'rganxie', 'rdaoqian', 'ryaoqing', 'rlvyou', ]
    need_topic_url = 'http://www.fyan8.com/{}.htm'
    print('需要下载的topic 数量:', len(need_topic))

    for idx, topic in enumerate(need_topic):
        data_df = pd.DataFrame(columns=['粤语', '普通话'])
        resource, title = get_page_resource(need_topic_url.format(topic))
        for _idx, res in enumerate(resource):
            data_df.loc[_idx] = [res['粤语'], res['普通话']]
            # data_df.loc[idx] = res.values()
            # 保存
        data_df.to_excel(os.path.join(output_path, title+'.xlsx'), index=False)
        print('{}. 下载完毕:{}'.format(idx, title))
        # debug
        break


if __name__ == '__main__' :
    main()