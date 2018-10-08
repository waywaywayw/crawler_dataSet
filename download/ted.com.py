# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-10
"""

import os
import re
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint

from crawler_myTools.selenium_tools.webdriver import MyWebDriver
from python_myTools.files import MyFiles, legal_file_name


# 请求头(改改host)   NEED DO
headers = {'Connection': 'Keep-Alive'
           # ,'Host': 'zhannei.baidu.com'
           ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
# 获取当前路径
current_path = os.path.dirname(os.path.abspath(__file__))
# 统计资源总数
global resource_cnt
# 爬取数据保存路径  NEED DO
output_path = os.path.join(current_path, '..', 'download_data', 'ted.com')


def get_resourcePage_list(start_url):
    """
    从start_url页面获取所有资源页面列表。
    :return 资源页面列表。dict格式，形如： resourcePage_list = [ {'url':'http:www.emmm.com', 'title':'emm'}, {'url':'http:www.233.com', 'title':'233'}]
    """
    def _parse_html(page_source):
        """分析页面源代码，获取resourcePage_list  NEED DO --->
        """
        resourcePage_list = []
        # 创建soup
        soup = BeautifulSoup(page_source, 'html.parser')
        # 找到资源页列表
        resourcePage_list_elem = soup.findAll('div', {'class': "media__message"})
        # 获取resourcePage
        for idx, resourcePage_elem in enumerate(resourcePage_list_elem):
            resourcePage = {}
            resource_elem = resourcePage_elem.find('a', {'class': 'ga-link'})
            # 获取resource的各种属性
            # dict格式. url项和title项必须有, 其他项可选
            resourcePage['title'] = resource_elem.get_text().strip()    # 获取title
            resourcePage['url'] = 'https://www.ted.com' + resource_elem['href'] # 获取url
            resourcePage_list.append(resourcePage)
        return resourcePage_list

    # 获取页面源代码(requests系)
    response = requests.get(start_url, headers=headers)
    page_source = response.content.decode('utf8')
    # debug. 将页面源代码写到临时html文件
    # with open('temp.html', 'r', encoding='utf8') as fout:
    #     fout.write(page_source)
    # debug. 直接输出页面源代码
    # pprint(page_source)

    resourcePage_list = _parse_html(page_source)
    return resourcePage_list


def get_resource_from_resourcePage(resourcePage):
    """
    从资源页面爬取所需的资源。   NEED DO --->
    :return 资源页面的所有资源。dict格式，形如：resource_list = [ {'need_name1':'v1', 'need_name2':'v2'}, {'need_name3':'v3'}]
    """
    def _parse_html_get_id(page_source):
        obj = re.match(r'.*"current_talk":"(\d*?)".*', page_source, re.DOTALL)
        # print(obj.group(1))
        id = obj.group(1)
        return id

    def _parse_json(page_source, language):
        """分析资源json，获取resourcePage_list  NEED DO --->
        """
        # 加载json, data_json是 dict 类型
        data_json = json.loads(page_source)
        # pprint(data_json)
        resource_list = []
        for cues in data_json['paragraphs']:
            for text in cues['cues']:
                sentence = text['text'].strip()
                res = {}
                # 获取resource的各种属性   to do
                res[language] = sentence
                resource_list.append(res)
        return resource_list

    def _work(id, language_symbol, language):
        # 发送请求
        response = requests.get('https://www.ted.com/talks/{}/transcript.json?language={}'.format(id, language_symbol), headers=headers)
        # resource_list_elem_yue = soup_yue.findAll('div', {'class': "Grid__cell flx-s:1 p-r:4"})
        if response.status_code == 404:
            return []
        else:
            resource_list = _parse_json(response.text, language)
            return resource_list

    # 获取id
    response = requests.get(resourcePage['url'], headers=headers)
    page_source = response.content.decode('utf8')
    id = _parse_html_get_id(page_source)
    # print('id = ', id)
    # debug
    # with open('temp.html', 'w', encoding='utf8') as fout:
    #     fout.write(response.text)
    resource_list = []
    resource_list.extend(_work(id, 'zh', '粤语'))
    resource_list.extend(_work(id, 'zh-tw', '繁体'))
    resource_list.extend(_work(id, 'zh-cn', '普通话'))
    return resource_list


def save_resources(resources, output_path, output_file_name):
    """保存资源到指定路径    NEED DO --->
    """
    data_df = pd.DataFrame(columns=['粤语', '普通话', '繁体'])
    for _idx, res in enumerate(resources):
        data_df.loc[_idx] = [res.get('粤语', ""), res.get('普通话', ""), res.get('繁体', "")]
    data_df.to_excel(os.path.join(output_path, output_file_name + '.xlsx'), index=False)


def work(url):
    """爬虫主流程
    """
    # 获取第page页的resourcePage_list.   每个resourcePage有title项和url项
    resourcePage_list = get_resourcePage_list(url)
    # 根据资源的title项 判重（可选）
    exist_resourcePage = list(MyFiles(output_path).file_name_no_suffix())
    resourcePage_list = list(filter(lambda x: x['title'] not in exist_resourcePage, resourcePage_list))

    print('需要下载的资源数量：', len(resourcePage_list))
    # 遍历resourcePage_list
    for idx, resourcePage in enumerate(resourcePage_list):
        # 获取资源
        resources = get_resource_from_resourcePage(resourcePage)
        # 清理文件名
        output_file_name = legal_file_name(resourcePage['title'])
        # 保存资源
        save_resources(resources, output_path, output_file_name)
        print('第{}个资源下载并保存完毕：{}'.format(idx, resourcePage['title']))
        # 总资源数+1
        global resource_cnt
        resource_cnt += 1
        # debug
        # break


def page_turning_mode(start_page, end_page):
    """翻页模式"""
    # 开启访问的URL  NEED DO
    start_url = 'https://www.ted.com/talks?language=zh&sort=newest&page={}'
    # 当前页数：page
    for page in range(start_page, end_page + 1):
        print('--- 第{}页 ---'.format(page))
        work(start_url.format(page))
        # debug
        # break


def main():
    global resource_cnt
    resource_cnt = 0
    # 翻页模式. 设置开始页和结束页   NEED TO
    start_page, end_page = 1, 5
    page_turning_mode(start_page, end_page)
    print('运行完毕. 下载的资源总数量：{}'.format(resource_cnt))


if __name__ == '__main__':
    main()
