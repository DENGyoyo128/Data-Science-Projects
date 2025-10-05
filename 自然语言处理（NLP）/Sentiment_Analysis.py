"""
用 VADER(NLTK) 对新闻文本进行情感分析，并统计正、负、中性新闻的比例
"""

import pandas as pd
df=pd.read_csv('news.csv')
# print(df.head())

# Find out the sentiments for the news
import nltk
# download the vader lexicon
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# what does the following line prints? 
print(analyzer.polarity_scores(df.iloc[0,-1]))


# Consolidate the sentiment scores for each ecord of news.
# A news is considered negative if the polarity score is less than or equal to -0.05, 
# positive if the score is more than or equal to 0.05. In 
# between these 2 values are considered neutral news.
# This dataset consists of more positive, negative or neutral news?

# 用于统计三类新闻的数量
pos_count = 0
neg_count = 0
neu_count = 0

# 遍历所有新闻并计算情感分数
for index, row in df.iterrows():
    text = str(row["clean_text"])  # 防止空值出错
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    # 分类规则
    if compound >= 0.05:
        sentiment = "Positive"
        pos_count += 1
    elif compound <= -0.05:
        sentiment = "Negative"
        neg_count += 1
    else:
        sentiment = "Neutral"
        neu_count += 1

    print(f"\nNews {index+1}: {text[:100]}...")  # 打印前100字符
    print(f"Scores: {scores} → Sentiment: {sentiment}")

# 汇总统计
print("\n--- Sentiment Summary ---")
print(f"Positive: {pos_count}")
print(f"Negative: {neg_count}")
print(f"Neutral : {neu_count}")