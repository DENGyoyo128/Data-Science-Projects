# AI就业市场趋势分析和薪资预测 Global AI Job Market & AI Salary 

基于公开的 AI Job 数据集，从 **EDA + 关联规则 + 薪资预测模型** 三个角度，分析全球 AI 岗位的薪资与增长趋势。

- 数据文件：`ai_job_dataset.csv`
- EDA：`Ai_Salary_EDA.ipynb`
- 模型代码：`Association_Rules.py`, `CART.py`, `Random_Forest.py`, `Xgboost.py`

---

## 1. 文件结构

```text
.
├── ai_job_dataset.csv
├── Ai_Salary_EDA.ipynb          # 探索性分析 & 可视化
├── Association_Rules.py         # 关联规则（高薪 & 岗位增长模式）
├── CART.py                      # 决策树回归（基线模型）
├── Random_Forest.py             # 随机森林（非线性基准）
├── Xgboost.py                   # XGBoost（效果最好）
└── README.md                    # 说明文档
```
## 2. EDA 要点（来自 `Ai_Salary_EDA.ipynb`）

- **薪资整体右偏**  
  大部分岗位集中在中等收入区间，少数高薪长尾集中在 **ML Engineer / AI Researcher** 等职位。

- **明显的地区差异**  
  北美、西欧整体薪资水平更高。

- **岗位增长集中在**：
  - 行业：**Finance、Education、Healthcare**
  - 角色：**Operations Manager、AI Researcher、Software Engineer** 等

---

## 3. 模型与方法

### 3.1 关联规则（`Association_Rules.py`）
- 对 **薪资、经验、JD 长度、福利** 等做分箱（`Low / Medium / High`）。
- 把 **技能 + 分箱后的特征** 当作 item，使用 **Apriori + `association_rules`**。
- 重点关注关联到 `salary_bin = High` 的规则，寻找「高薪组合」，例如：
  - 某些技能 + 某些地区 / 教育 / 公司规模 → 高薪概率提升。

### 3.2 回归模型（`CART.py`, `Random_Forest.py`, `Xgboost.py`）

**统一预处理思路：**
- 删除与预测无关字段：ID、货币代码、发布时间等。
- 将 **经验等级、学历** 映射为有序变量。
- 将 `required_skills` 展开为多技能哑变量。
- 其余类别特征做 **one-hot 编码**。

**模型：**

- `CART.py`：单棵回归树 → 提供可视化，便于解释「分段加薪逻辑」。
- `Random_Forest.py`：提升精度，输出特征重要性。
- `Xgboost.py`：进一步提升拟合效果，是本项目表现最佳的模型。

---

## 4. 关键结论
### 4.1 经验溢价是非线性的
- 大约在 **4–5 年**、**9–10 年** 附近存在明显的薪资“台阶”，不是简单线性增长。
### 4.2 地点非常关键
- **公司所在地** 对薪资的影响明显大于员工居住地，反映当地市场与付薪能力的差异。
### 4.3 双通道发展路径
- **技术深度路径**：ML Engineer / AI Researcher 等高技能岗位。
- **业务整合路径**：Operations Manager / PM 等兼具技术理解与管理能力的角色。

### 4.4 模型拟合情况
- XGBoost 的 **R² ≈ 0.88**：
  - 对中位数薪资段拟合较好；
  - 对极端高薪略有低估（长尾效应）。