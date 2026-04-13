import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置绘图风格
plt.rcParams['font.sans-serif'] = ['Heiti TC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

DATA_PATH = "data/private_fund_indices.csv"
SAVE_DIR = "strategy/outputs/plots"

INDEX_NAMES = {
    48333548: "GTHT01 (300指增)", 48408839: "GTHT02 (可转债)", 43494799: "GTHT03 (500指增)",
    43310702: "GTHT04 (1000指增)", 48585505: "GTHT05 (CTA标准)", 49069575: "GTHT06 (市场中性)",
    40998561: "GTHT07 (纯债)", 49361940: "GTHT08 (主观股票)", 40553563: "GTHT09 (CTA主观)",
    42883138: "GTHT10 (CTA量化)", 44238744: "GTHT11 (宏观策略)"
}

def generate_asset_correlation():
    print("🧬 Generating Asset Correlation Matrix...")
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    df_pivot = df.pivot(index='date', columns='security_id', values='close').ffill()
    
    # 获取收益率并映射名称
    df_rets = df_pivot.pct_change().dropna(how='all')
    df_rets = df_rets[[c for c in df_rets.columns if c in INDEX_NAMES]]
    df_rets.columns = [INDEX_NAMES[c] for c in df_rets.columns]
    
    # 排序
    df_rets = df_rets.reindex(sorted(df_rets.columns), axis=1)
    
    # 计算相关性
    corr = df_rets.corr()
    
    # 绘图
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f', linewidths=0.5)
    plt.title("国泰海通私募策略全集：全口径标的相关性矩阵", fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, "asset_correlation_heatmap.png"), dpi=300)
    print("✅ Asset Correlation Heatmap saved.")

if __name__ == "__main__":
    generate_asset_correlation()
