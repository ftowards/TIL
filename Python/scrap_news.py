#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
import datetime


# In[2]:


import FinanceDataReader as fdr


# In[3]:


url = "https://finance.naver.com/item/news_news.nhn"
headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}    


# In[4]:


df_krx = fdr.StockListing("KRX")


# In[5]:


def item_name_search(item_code) :
    name = df_krx.loc[df_krx["Symbol"] == item_code, 'Name'].tolist()
    if len(name) == 1 :
        return name[0]
    else :
        return False


# In[6]:


def article_page_scrap(item_code, page, date) :
    """
    한페이지 아티클 불러오기
    - 연관 기사로 불필요하게 행 잡아먹는 아티클은 삭제
    """
    url_code = url + "?code="+item_code+"&page="+str(page)
    response = requests.get(url_code, headers)
    temp = bs(response.text, "lxml")
    article_raw = pd.read_html(str(temp.select("table")))[0]
    
    deadline = datetime.datetime.strptime(date, '%Y%m%d')
    
    for i in range(len(article_raw)) :
        if article_raw.loc[i, "날짜"][:3] != '202' :
            article_raw = article_raw.drop(i)
        elif datetime.datetime.strptime(article_raw.loc[i,"날짜"], '%Y.%m.%d %H:%M') < deadline :
            article_raw = article_raw.drop(i)
    
    return article_raw


# In[7]:


def article_scrap(item_code, date) : 
    """
    item_code 기준으로 뉴스 검색
    date 'YYYYMMDD' 기준의 날짜까지만 검색
    """
    item_name = item_name_search(item_code)
    
    if item_name == False :
        return '아이템 코드 오류'
    
    page = 1
    article_list = []


    while 1 == 1 :
        scrap = article_page_scrap(item_code, page, date)
        article_list.append(scrap)

        if scrap.shape[0] == 0:
            break

        page += 1
        time.sleep(1)

    articles = pd.concat(article_list, ignore_index=True)
    
    file_name = f'{item_code}_{item_name}_{datetime.datetime.today().strftime("%y%m%d")}.csv' 
    articles.to_csv(file_name, index=False)    


# In[10]:


item_code = '066570'

article_scrap(item_code, '20210618')


# In[9]:


pd.read_csv("066570_LG전자_210624.csv")


# In[ ]:




