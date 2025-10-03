import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx


# ============ 1. 分箱处理函数 ============
def binning_features(df):
    # 工资分箱
    df['salary_bin'] = pd.qcut(df['salary_usd'], q=3, labels=['Low', 'Medium', 'High'])

    # 年限分箱
    df['years_experience_bin'] = pd.cut(df['years_experience'],
                                        bins=[-1, 3, 7, 50],
                                        labels=['Junior', 'Mid', 'Senior'])

    # 岗位描述长度分箱
    df['job_desc_bin'] = pd.qcut(df['job_description_length'], q=3,
                                 labels=['Short', 'Medium', 'Long'])

    # 福利分箱
    df['benefits_bin'] = pd.qcut(df['benefits_score'], q=3,
                                 labels=['Low', 'Medium', 'High'])

    return df


# ============ 2. 数据清洗 ============
def preprocess_for_association(df):
    df = binning_features(df)

    drop_cols = ['job_id', 'job_title', 'salary_usd', 'salary_currency',
                 'posting_date', 'application_deadline', 'company_name']
    df = df.drop(columns=drop_cols)

    df_long = df.assign(skill=df['required_skills'].str.split(',')).explode('skill')
    df_long['skill'] = df_long['skill'].str.strip()

    # 独立处理分类字段
    cols_for_rules = [
        'salary_bin', 'years_experience_bin', 'job_desc_bin', 'benefits_bin',
        'remote_ratio', 'experience_level', 'employment_type',
        'education_required', 'company_location',
        'employee_residence', 'company_size', 'industry'
    ]

    transactions = df_long.groupby(df_long.index).apply(
        lambda x: [f"{col}={x[col].iloc[0]}" for col in cols_for_rules] + list(x['skill'])
    )

    from mlxtend.preprocessing import TransactionEncoder
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    basket = pd.DataFrame(te_array, columns=te.columns_)

    return transactions, basket


# ============ 3. 关联规则挖掘 ============
def run_salary_rules(basket, salary_level="High", min_support=0.07, min_confidence=0.6):
    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

    target = f"salary_bin={salary_level}"
    rules_salary = rules[rules['antecedents'].astype(str).str.contains(target) |
                         rules['consequents'].astype(str).str.contains(target)]

    return rules_salary.sort_values(by="lift", ascending=False)


# ============ 4. 可视化 ============
def plot_rules(rules_salary, save_prefix="salary_rules"):
    # 1. 散点图
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="support", y="confidence", size="lift",
                    data=rules_salary, alpha=0.6, sizes=(40, 400))
    plt.title("Salary Association Rules: Support vs Confidence (Size ~ Lift)")
    plt.xlabel("Support")
    plt.ylabel("Confidence")
    plt.tight_layout()
    plt.savefig(f"{save_prefix}_scatter.png", dpi=300)
    plt.show()

    # 2. 热力图（Lift）
    if not rules_salary.empty:
        pivot_lift = rules_salary.pivot_table(index='antecedents',
                                              columns='consequents',
                                              values='lift')
        plt.figure(figsize=(10, 8))
        sns.heatmap(pivot_lift, cmap="YlGnBu", annot=False)
        plt.title("Heatmap of Lift between Antecedents and Consequents")
        plt.tight_layout()
        plt.savefig(f"{save_prefix}_heatmap.png", dpi=300)
        plt.show()

    # 3. 网络图（所有规则）
    if not rules_salary.empty:
        G = nx.DiGraph()
        for _, row in rules_salary.iterrows():
            antecedents = list(row['antecedents'])
            consequents = list(row['consequents'])
            for ant in antecedents:
                for con in consequents:
                    G.add_edge(ant, con, weight=row['lift'])

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue",
                font_size=9, font_weight="bold", arrowsize=15, edge_color="gray")
        plt.title("Association Rules Network — All Salary Rules")
        plt.tight_layout()
        plt.savefig(f"{save_prefix}_network_all.png", dpi=300)
        plt.show()

    # 4. 网络图（只看 salary_bin=High 相关规则）
    rules_high = rules_salary[rules_salary['antecedents'].astype(str).str.contains("salary_bin=High") |
                              rules_salary['consequents'].astype(str).str.contains("salary_bin=High")]

    if not rules_high.empty:
        G_high = nx.DiGraph()
        for _, row in rules_high.iterrows():
            antecedents = list(row['antecedents'])
            consequents = list(row['consequents'])
            for ant in antecedents:
                for con in consequents:
                    G_high.add_edge(ant, con, weight=row['lift'])

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G_high, k=0.5, iterations=50, seed=42)
        nx.draw(G_high, pos, with_labels=True, node_size=2000, node_color="lightgreen",
                font_size=9, font_weight="bold", arrowsize=15, edge_color="gray")
        plt.title("Association Rules Network — salary_bin=High")
        plt.tight_layout()
        plt.savefig(f"{save_prefix}_network_high.png", dpi=300)
        plt.show()


# ============ 主程序 ============
if __name__ == "__main__":

    df=pd.read_csv('ai_job_dataset.csv')

    transactions, basket = preprocess_for_association(df)
    print(basket.columns[:50]) 
    
    rules_high = run_salary_rules(basket, "High",min_support=0.1, min_confidence=0.5)
    print("\n关于工资的关联规则 (前10条):")
    print(rules_high[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
    
    plot_rules(rules_high)


###结论：在这个数据里，高工资几乎总是和“资深经验 (Senior)、Expert 职级、硕士/博士学历、大/中型公司”强绑定。