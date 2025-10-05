"""
从CNA新加坡新闻网抓取新闻标题。
使用 requests 获取网页，再用 BeautifulSoup 解析。
"""
"""
1、清理抓取后的新闻文本(去掉空格，打印编号)
2、支持关键词搜索,统计关键词在新闻中出现的次数。
"""

import requests
from bs4 import BeautifulSoup 

url = "https://www.channelnewsasia.com/"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")   

# 抓取所有 h3 标签
data = soup.find_all("h3")
print(data)
count=1
mention=input("Enter a keyword of interest:")
mention_count=0
total_words=0
for each_title in data:
    each_title =each_title.text.strip()
    if mention in each_title:
        mention_count+=1
    total_words+=len(each_title.split())
    print(f"{count},{each_title}")
    print(f'mention_count={mention_count}, total_words={total_words}')
    count+=1
print(f"{mention} was mentioned {mention_count} times in")