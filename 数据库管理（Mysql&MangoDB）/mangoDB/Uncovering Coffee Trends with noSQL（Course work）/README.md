# Uncovering Coffee Trends with NoSQL  
# 用 NoSQL 挖掘咖啡趋势  

---

## Background (背景)

Uncovering Coffee Trends with NoSQL is a data analytics project based on NoSQL (MongoDB) that aims to uncover trends related to coffee sales, caffeine consumption, and sleep performance.  

By leveraging MongoDB’s aggregation pipeline (using operators such as `$group`, `$bucket`, `$addFields`, and `$switch`), the project analyzes data on beverage types, caffeine intensity, consumption time, sleep quality, and payment behavior to explore the relationship between our daily coffee habits and lifestyle patterns.  

该项目是一个基于 NoSQL (MongoDB) 的数据分析项目，旨在挖掘与咖啡销售、咖啡因摄入和睡眠表现相关的趋势。  

通过使用 MongoDB 的聚合管道（$group, $bucket, $addFields, $switch 等操作符），本项目分析了饮品类型、咖啡因强度、消费时间段、睡眠质量及支付行为等数据，以探索我们的日常咖啡习惯与生活方式之间的联系。

---

## Data Sources (数据来源)

| Collection 名称 | 数据来源 |
|------------------|------------|
| baristacoffeesalesTBL | https://www.kaggle.com/datasets/yashparab/barista-coffee-sales-data-for-eda-csv |
| caffeine_intake_tracker | https://www.kaggle.com/datasets/prekshad2166/caffeine-intake-tracker-csv |
| coffeesales | https://www.kaggle.com/datasets/visabelsarahsargunar/coffee-sales-dataset |

---

## Task List (任务列表)

1、**Collection: `baristacoffeesalesTBL`**  
**Task:** How many product categories are there? For each product category, show the number of records.  
统计产品类别数量及各类别记录数。

---

2、**Collection: `caffeine_intake_tracker`**  
**Task:** What is the average caffeine per beverage type (coffee/tea/energy drink)?  
计算不同饮品类型（咖啡、茶、能量饮料）的平均咖啡因含量。  
**Hint:** `$switch`

---

3、**Collection: `caffeine_intake_tracker`**  
**Task:** How does sleep impact rate vary by time of day (morning/afternoon/evening)?  
分析一天中不同时间段（早上、下午、晚上）的睡眠影响程度差异。  
**Hint:** `$switch`

---

4、**Collection: `caffeine_intake_tracker`**  
**Task:** Bucket caffeine into Low/Med/High and compare average sleep quality.  
将咖啡因含量分为低、中、高三档，并比较各档的平均睡眠质量。  
**Hint:** `$bucket`, `$addFields`, `$switch`

---

5、**Collection: `coffeesales`**  
**Task:** What is the total revenue and order count?  
计算销售总收入和订单总数量。  
**Hint:** `$addFields`

---

6、**Collection: `coffeesales`**  
**Task:** Which drink is most cash-heavy? (cash share by drink)  
找出现金交易占比最高的饮品（即每种饮品中现金支付比例最高者）。
