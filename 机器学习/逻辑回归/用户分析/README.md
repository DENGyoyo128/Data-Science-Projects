# 基于用户行为的购买意愿预测

## 1. 项目简介

本项目通过模拟电商网站的用户行为数据，构建一个**购买意愿预测模型**，演示完整流程：

- 构造用户行为数据集
- EDA（分布 & 相关性分析）
- 特征工程与特征提取
- 使用逻辑回归模型预测“是否购买”
- 给新用户打分（购买概率），支持业务应用场景

Notebook 文件：`基于用户行为的购买意愿预测.ipynb`  
---

## 2. 数据与特征说明

在 Notebook 中使用 `numpy` 构造了 1000 条合成用户行为数据，每一行代表一个用户会话（或一个用户在某段时间内的行为摘要），包含以下字段：

- `age`：年龄（正态分布）
- `time_spent_on_site`：网站停留时间（分钟）
- `pages_visited`：访问页面数
- `previous_purchases`：历史购买次数
- `cart_value`：当前购物车金额
- `is_returning_customer`：是否回头客（0/1）
- `days_since_last_visit`：距上次访问的天数
- `purchased`：是否完成购买（0/1，作为目标变量）

目标变量 `purchased` 是基于上述特征按一定权重构造出的**“真实购买概率 + 随机波动”**，用来模拟真实业务中的购买行为。

---

## 3. 分析与建模流程

### 3.1 EDA：分布与相关性分析

在 Notebook 中对数据做了基础探索性分析，包括：

- `describe()`：查看各数值特征的均值、标准差、四分位数等统计量；
- 缺失值检查：`isnull().sum()`；
- 目标变量 `purchased` 的分布及正负样本比例；
- 对以下特征按“是否购买”分组绘制直方图 / KDE 曲线：
  - `age`, `time_spent_on_site`, `pages_visited`,  
    `previous_purchases`, `cart_value`, `days_since_last_visit`；
- 绘制**相关性热力图**（`corr()` + `sns.heatmap`），观察哪些特征与 `purchased` 相关更强。

> 直观理解“哪些行为模式更像会购买的用户”。

---

### 3.2 特征工程

在原始特征基础上构造了两个更有业务含义的特征：
- `recency_score = 1 / (1 + days_since_last_visit)`  
  - 越近期访问，分数越高（接近 1）；  
  - 越久未访问，分数越低（接近 0）。
- `engagement_score = (time_spent_on_site * pages_visited) / 10`  
  - 用停留时间 × 页面数衡量“参与度”，再做简单缩放。

最终用于建模的特征矩阵 `X` 包含：  
原始特征 + `recency_score` + `engagement_score`，目标变量为 `purchased`。

---

### 3.3 模型训练与评估：逻辑回归

建模部分主要步骤：

1. **划分训练 / 测试集**

   ```python
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42, stratify=y
   )

2. **训练模型并查看特征系数**：
- 使用 `pipeline.fit(X_train, y_train)` 训练模型；
- 从 `pipeline.named_steps['classifier']` 中提取 `coef_`；
- 按绝对值排序，得到“哪些特征对购买预测影响最大”。

3. **模型评估**：
- 在测试集上预测类别与概率；
- 输出 `classification_report`（精确率、召回率、F1、支持度）；
- 绘制混淆矩阵；
- 绘制 ROC 曲线并计算 AUC（示例数据上约在 0.77 左右）。

总体上，模型能较好地区分“倾向购买 vs 不太可能购买”的用户

ChatGPT 说：### 3.4 新用户购买概率预测接口

Notebook 末尾封装了一个函数，用于对新用户进行打分：

```python
def predict_purchase_probability(new_customer_data, pipeline):
    """
    输入: 新客户特征 DataFrame + 已训练好的 pipeline
    输出: 加上 'purchase_probability' 和 'likely_to_purchase' 的 DataFrame
    """
    ...
``` 
逻辑包括：

- 自动补充 `recency_score` 和 `engagement_score`（如果没提供）；
- 使用训练好的 `pipeline.predict_proba` 计算购买概率；
- 新增两列：
  - `purchase_probability`：购买概率（0–1）；
  - `likely_to_purchase`：布尔标记（默认概率 ≥ 0.5 判定为“较可能购买”）。

Notebook 中给出了 3 个不同画像用户的示例（**年轻新客 / 高参与老客 / 久未访问用户**）来演示预测效果。