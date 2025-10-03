import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 


# ============ 1. 数据处理 ============
# 1. 分类变量：One-hot 编码
def encode_categorical(df, categorical_cols):
    return pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# 2. 等级变量：映射成整数
def encode_ordinal(df):
    exp_map = {"EN": 1, "MI": 2, "SE": 3, "EX": 4}  # Entry / Mid / Senior / Expert
    edu_map = {"Associate": 1, "Bachelor": 2, "Master": 3, "PhD": 4}

    if "experience_level" in df.columns:
        df["experience_level"] = df["experience_level"].map(exp_map)
    if "education_required" in df.columns:
        df["education_required"] = df["education_required"].map(edu_map)

    return df

# 3. 特殊处理：required_skills 转成哑变量
def encode_required_skills(df):
    if "required_skills" in df.columns:
        df_long = df.assign(skill=df['required_skills'].str.split(',')).explode('skill')
        df_long['skill'] = df_long['skill'].str.strip()
        skill_dummies = pd.get_dummies(df_long['skill'], prefix="skill")
        df = pd.concat([df_long.drop(columns=['skill', 'required_skills']), skill_dummies], axis=1)
        df = df.groupby(df.index).max()  # 聚合回去（同一个岗位多个技能取1）
    return df

# 4. 丢掉无用变量
def drop_unused(df):
    drop_cols = ['job_id', 'salary_currency', 'posting_date',
                 'application_deadline', 'company_name']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return df

# 5. 总控函数：构造 X, y
def preprocess_data(df, target_col="salary_usd"):
    df = drop_unused(df)
    df = encode_ordinal(df)

    # required_skills 先展开 & 编码
    df = encode_required_skills(df)

    # 剩下的 object 类型变量 → One-hot
    categorical_cols = [col for col in df.columns if df[col].dtype == "object" and col != target_col]
    df = encode_categorical(df, categorical_cols)

    X = df.drop(columns=[target_col])
    y = df[target_col]

    return X, y



# ============ 2. 训练 + 交叉验证 ============
def train_cart_regressor(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 参数网格
    param_grid = {
        "max_depth": [3, 5, 7, 10, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 5]
    }

    cart = DecisionTreeRegressor(random_state=42)
    grid = GridSearchCV(cart, param_grid, cv=5, scoring="r2", n_jobs=-1)
    grid.fit(X_train, y_train)

    print("最优参数:", grid.best_params_)
    print("交叉验证最优 R²:", grid.best_score_)

    best_model = grid.best_estimator_

    # 测试集表现
    y_pred = best_model.predict(X_test) 
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("\n测试集 RMSE:", rmse)
    print("测试集 R²:", r2)

    return best_model, X_train.columns,grid


# ============ 3. 可视化决策树 ============
def plot_decision_tree(model, feature_names, class_names=None, max_depth=3):
    plt.figure(figsize=(18, 8))
    plot_tree(
        model,
        feature_names=feature_names,
        filled=True,
        max_depth=max_depth,   # 只展示前3层
        fontsize=8
    )
    plt.title(f"CART 决策树 (回归版, 展示前 {max_depth} 层)")
    plt.show()

# ============ 4. 可视化 GridSearchCV 的参数搜索过程 ============
def plot_gridsearch_results(grid, param_x="max_depth", param_y="min_samples_split", score_metric="mean_test_score"):
    """
    可视化 GridSearchCV 的参数搜索过程
    :param grid: 已经 fit 的 GridSearchCV 对象
    :param param_x: 横轴参数
    :param param_y: 纵轴参数
    :param score_metric: 显示的得分指标（默认 mean_test_score）
    """
    results = pd.DataFrame(grid.cv_results_)

    # 取需要的参数和分数
    pivot_table = results.pivot_table(
        values=score_metric,
        index=f"param_{param_y}",
        columns=f"param_{param_x}"
    )

    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".3f", cmap="YlGnBu")
    plt.title(f"GridSearchCV - {param_x} vs {param_y} ({score_metric})")
    plt.xlabel(param_x)
    plt.ylabel(param_y)
    plt.tight_layout()
    plt.show()



# ============ 5. 变量重要性 ============
def plot_feature_importance(model, feature_names):
    importance = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x="importance", y="feature", data=importance.head(20))
    plt.title("特征重要性 (CART 回归)")
    plt.tight_layout()
    plt.show()

    return importance


# ============ 主程序 ============
if __name__ == "__main__":
    # 加载数据
    df = pd.read_csv("/Users/liyanping/Desktop/ai-analytic/ai_salary/ai_job_dataset.csv")

    X, y = preprocess_data(df)
    best_model, features,grid = train_cart_regressor(X, y)

    # 决策树可视化（只展示前几层，避免太复杂）
    plot_decision_tree(best_model, features, max_depth=4)
    
    # 可视化参数搜索过程
    plot_gridsearch_results(grid, param_x="max_depth", param_y="min_samples_split")

    # 特征重要性
    importance = plot_feature_importance(best_model, features)
    print("\n前10个重要特征:\n", importance.head(10))



