# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 10:40:35 2018

@author: Sixuan Zhu
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_post_linksDates():
    start_time = time.time()
    urls = []
    dates = []
    origin_search_link= input('\n请在这里粘贴搜索关键词后，并点击下面页码后出现的链接（结尾需是page=第几页）\n')
    page = int(input('\n请输入搜索结果页码数\n'))
    search_link = origin_search_link[:-1]
    for i in range (1, page+1):
        search_url = search_link + str(i)
        try:
            r = requests.get(search_url)
        except requests.exceptions.RequestException as e:
            print('\n获取网页请求失败: {}\n'.format(e))
            break
            return None

        r.encoding = r.apparent_encoding
        r = r.text
        soup = BeautifulSoup(r,'lxml')

        #获取每个帖子的链接：
        #原网页解析界面：<h3 class ='xs3'>, 查找所有的这个标签
        links = soup.find_all('h3', {'class': 'xs3'})
        if not links:
            print('\n无法查询帖子链接，可能是搜索link有误\n')
            break
            return None
        for link in links:
            href = link.find('a').get('href')
            url = 'https://forum.chasedream.com/'+ str(href)
            urls.append(url)

        #获取每个帖子的发布日期：
        posts = soup.find_all('li', {'class': 'pbw'})
        if not posts:
            print('\n无法查询帖子链接，可能是搜索link有误\n')
            break
            return None
        for post in posts:
            #经过观察发现，日期在span标签下，并且是第一个
            date = str(post.find_all('span')[0].string)
            dates.append(date)
        print('正在解析第{}页的标题链接\n'.format(i))
    print("本函数运行用时 %s 秒.\n" % (time.time() - start_time))
    return urls, dates

def getContents(urls):
    print ('\n正在获取每贴标题及内容...\n')
    start_time = time.time()

    titles =[]
    contents = []
    p = 0

    for url in urls:
        try:
            r = requests.get(url)
        except requests.exceptions.RequestException as e:
            print('\n获取网页请求失败: {}\n'.format(e))
            break
            return None

        r = r.text
        soup = BeautifulSoup(r,'lxml')

        title = soup.title.get_text()
        content = soup.find('td',{'class':'t_f'}).get_text()

        titles.append(title)
        contents.append(content)

        p += 1
        print('正在下载第{}个内容\n'.format(str(p)))
    print("用时 %s 秒." % (time.time() - start_time))
    return titles, contents


def df_refine(df):
    FalseResult = []
    for i in range(0, len(df['Titles'])):
        #下面这行语句可以用来排除搜索错误的结果，请自行替换关键词
        if ('IC' not in df['Titles'][i]) and ('帝国理工' not in df['Titles'][i]):
            FalseResult.append(i)
    return FalseResult



def main():
    urls, dates = get_post_linksDates()
    if not urls:
        print('\n获取贴子链接失败, 请重启程序\n')
        return None
    if not urls:
        print('\n获取发帖日期失败, 请重启程序\n')
        return None

    titles, contents = getContents(urls)
    if not titles:
        print('\n获取贴子链接失败, 请重启程序\n')
        return None
    if not contents:
        print('\n获取帖子内容失败, 请重启程序\n')
        return None

    data_tuples = list(zip(dates, titles, contents, urls))
    df = pd.DataFrame(data_tuples, columns = ['Dates' ,'Titles', 'Contents', 'link'])

    FalseResult = df_refine(df)
    df.drop(df.index[FalseResult], inplace = True)

    df.to_excel('ChaseDream.xlsx')

if __name__ == "__main__":
	main()
