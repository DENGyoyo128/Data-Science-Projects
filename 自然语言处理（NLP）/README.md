# NLP 工具箱：从新闻抓取到情感分析与文本分类

> 一个小型 **自然语言处理（NLP）练习项目**，串起  
> **网页抓取 → 文本预处理 → 情感分析 → 文本分类** 的完整流程。


---

## 1. 仓库结构

```text
.
├── news.csv                    # 新闻数据（已抓取并清洗后得到）
├── nonsense_dictionary.csv     # “胡说 / 非胡说” 语料字典
├── Web_Scraping.py             # 抓取 CNA 新闻标题 + 关键词统计
├── Text_Preprocessing.py       # 分词 / 词干提取 / 词形还原示例
├── Sentiment_Analysis.py       # 用 VADER 对新闻做情感分析
├── Text_Classification.py      # TF-IDF + 随机森林做“胡说 / 非胡说”分类
└── README.md                    # 说明文档
```
## 2. 功能模块简介

### 2.1 新闻抓取与关键词计数（`Web_Scraping.py`）

- 从 **CNA 新加坡新闻网** 首页抓取所有 `<h3>` 标题；
- 去掉首尾空格后逐条打印，并为每条新闻自动编号；
- 支持用户输入关键词 `mention`，统计该词在所有标题中出现的次数和累计单词数；
- 可作为 `news.csv` 的上游数据来源，也可以单独当作「爬虫 + 简单文本分析」的练习脚本。

---

### 2.2 文本预处理示例（`Text_Preprocessing.py`）

演示经典 NLP 预处理步骤：

- **分句 / 分词**：使用 `PunktSentenceTokenizer` 将文本切成句子，并去掉标点；
- **词干提取（Stemming）**：用 `PorterStemmer` 将单词还原到“词干”形式（如 `studies → studi`）；
- **词形还原（Lemmatization）**：用 `WordNetLemmatizer` 得到真正词根（如 `studies → study`）。

---

### 2.3 新闻情感分析（`Sentiment_Analysis.py`）

- 读取 `news.csv`，假定其中一列为 `clean_text`（清洗后的新闻文本）；
- 使用 **NLTK VADER** 模型对每条新闻计算情感得分：
  - `compound ≥ 0.05` → Positive  
  - `compound ≤ -0.05` → Negative  
  - 介于两者之间 → Neutral
- 遍历所有新闻：
  - 打印每条新闻前若干字符、情感得分和情感标签；
  - 统计正 / 负 / 中性新闻数量，并在最后汇总输出。

> 回答的问题：**这批新闻里，整体情绪是偏正面、负面，还是中性？**

---

### 2.4 “胡说检测”文本分类器（`Text_Classification.py`）

- 使用 `nonsense_dictionary.csv` 作为标注数据：
  - 文本列重命名为 `content`；
  - 标签列重命名为 `label`，并将 `"Nonsense"` 映射为 `1`，`"No Nonsense"` 映射为 `0`。
- 用 `TfidfVectorizer` 将文本转为 TF-IDF 特征；
- 划分训练集 / 测试集（70% / 30%）；
- 训练 **随机森林分类器（RandomForestClassifier）**；
- 在测试集上输出准确率，并用若干新句子测试模型