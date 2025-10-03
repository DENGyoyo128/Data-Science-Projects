import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 数据预处理
# -----------------------------

def encode_ordinal(df):
    exp_map = {"EN": 1, "MI": 2, "SE": 3, "EX": 4}   # Entry, Mid, Senior, Expert
    edu_map = {"Associate": 1, "Bachelor": 2, "Master": 3, "PhD": 4}

    if "experience_level" in df.columns:
        df["experience_level"] = df["experience_level"].map(exp_map)
    if "education_required" in df.columns:
        df["education_required"] = df["education_required"].map(edu_map)
    return df

def encode_required_skills(df):
    if "required_skills" in df.columns:
        df_long = df.assign(skill=df['required_skills'].str.split(',')).explode('skill')
        df_long['skill'] = df_long['skill'].str.strip()
        skill_dummies = pd.get_dummies(df_long['skill'], prefix="skill")
        df = pd.concat([df_long.drop(columns=['skill', 'required_skills']), skill_dummies], axis=1)
        df = df.groupby(df.index).max()  # 同一岗位多个技能 → 取并集
    return df

def drop_unused(df):
    drop_cols = ['job_id', 'salary_currency', 'posting_date', 'application_deadline', 'company_name']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return df

def encode_categorical(df, target_col):
    categorical_cols = [col for col in df.columns if df[col].dtype == "object" and col != target_col]
    return pd.get_dummies(df, columns=categorical_cols, drop_first=True)

def preprocess_data(df, target_col="salary_usd"):
    df = drop_unused(df)
    df = encode_ordinal(df)
    df = encode_required_skills(df)
    df = encode_categorical(df, target_col)

    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y

# -----------------------------
# 训练随机森林 + 调参
# -----------------------------

def train_random_forest(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    rf = RandomForestRegressor(random_state=42, n_jobs=-1)

    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 5]
    }

    grid = GridSearchCV(rf, param_grid, cv=5, scoring="r2", n_jobs=-1, verbose=1)
    grid.fit(X_train, y_train)

    print("最优参数:", grid.best_params_)
    print("交叉验证最优 R²:", grid.best_score_)

    best_model = grid.best_estimator_

    # 测试集评估
    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("\n测试集 RMSE:", rmse)
    print("测试集 R²:", r2)

    return best_model, X_train.columns, grid, (y_test, y_pred)

# -----------------------------
# 可视化部分
# -----------------------------

def plot_feature_importance(model, feature_names, top_n=20):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances[indices], y=np.array(feature_names)[indices])
    plt.title("随机森林 - 特征重要性 (Top {})".format(top_n))
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.show()

def plot_predictions(y_test, y_pred):
    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
    plt.xlabel("实际工资")
    plt.ylabel("预测工资")
    plt.title("随机森林 - 实际 vs 预测 工资")
    plt.show()

# -----------------------------
# 主程序
# -----------------------------
if __name__ == "__main__":
    # 假设你的数据是 CSV
    df = pd.read_csv("ai_salary/ai_job_dataset.csv")

    X, y = preprocess_data(df, target_col="salary_usd")
    best_model, features, grid, (y_test, y_pred) = train_random_forest(X, y)

    # 可视化
    plot_feature_importance(best_model, features, top_n=20)
    plot_predictions(y_test, y_pred)
