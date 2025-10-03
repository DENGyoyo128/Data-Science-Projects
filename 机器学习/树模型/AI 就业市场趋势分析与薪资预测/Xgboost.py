import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor, plot_importance

# -----------------------------
# 数据预处理（沿用之前的模块）
# -----------------------------

def encode_ordinal(df):
    exp_map = {"EN": 1, "MI": 2, "SE": 3, "EX": 4}
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
        df = df.groupby(df.index).max()
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
# XGBoost 训练 + 调参
# -----------------------------

def train_xgboost(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    xgb = XGBRegressor(objective="reg:squarederror", random_state=42, n_jobs=-1)

    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [3, 5, 7],
        "learning_rate": [0.05, 0.1, 0.2],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0]
    }

    grid = GridSearchCV(xgb, param_grid, cv=5, scoring="r2", n_jobs=-1, verbose=1)
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

    return best_model, X_train.columns, grid, (y_test, y_pred)

# -----------------------------
# 可视化
# -----------------------------

def plot_feature_importance_xgb(model, feature_names, top_n=20):
    plt.figure(figsize=(10, 6))
    plot_importance(model, max_num_features=top_n, importance_type="gain")
    plt.title("XGBoost - 特征重要性 (Top {})".format(top_n))
    plt.show()

def plot_predictions(y_test, y_pred):
    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
    plt.xlabel("实际工资")
    plt.ylabel("预测工资")
    plt.title("XGBoost - 实际 vs 预测 工资")
    plt.show()

# -----------------------------
# 主程序
# -----------------------------
if __name__ == "__main__":
    df = pd.read_csv("ai_salary/ai_job_dataset.csv")

    X, y = preprocess_data(df, target_col="salary_usd")
    best_model, features, grid, (y_test, y_pred) = train_xgboost(X, y)

    plot_feature_importance_xgb(best_model, features, top_n=20)
    plot_predictions(y_test, y_pred)
