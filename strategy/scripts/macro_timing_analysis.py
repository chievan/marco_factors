import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os

# 设置绘图字体
plt.rcParams['font.sans-serif'] = ['Heiti TC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# =================================================================
# 1. 配置与路径
# =================================================================
FACTOR_PATH = "factors/macro_factor_database.csv"
ASSET_PATH = "data/private_fund_indices.csv"
SAVE_DIR_PLOTS = "strategy/outputs/plots"
SAVE_DIR_DATA = "strategy/outputs/data"

INDEX_NAMES = {
    48333548: "GTHT01 (300指增)",
    48408839: "GTHT02 (可转债)",
    43494799: "GTHT03 (500指增)",
    43310702: "GTHT04 (1000指增)",
    48585505: "GTHT05 (CTA标准)",
    49069575: "GTHT06 (市场中性)",
    40998561: "GTHT07 (纯债)",
    49361940: "GTHT08 (主观股票)",
    40553563: "GTHT09 (CTA主观)",
    42883138: "GTHT10 (CTA量化)",
    44238744: "GTHT11 (宏观策略)"
}

# =================================================================
# 2. 信号提取引擎
# =================================================================

def extract_signals(df_factors, window=60):
    hf_cols = [c for c in df_factors.columns if c.startswith("HF_")]
    df_hf = df_factors[hf_cols]
    sig_mom = df_hf.diff(window)
    sig_std = sig_mom.rolling(252).std().replace(0, 1)
    sig_z = sig_mom / sig_std
    return sig_z.fillna(0)

# =================================================================
# 3. 暴露分析 (Regression Analysis)
# =================================================================

def run_exposure_analysis():
    print("📈 Starting Full-Scale Macro Exposure Analysis...")
    
    df_factors = pd.read_csv(FACTOR_PATH, index_col=0)
    df_factors.index = pd.to_datetime(df_factors.index)
    df_signals = extract_signals(df_factors)
    
    df_asset_raw = pd.read_csv(ASSET_PATH)
    df_asset_raw['date'] = pd.to_datetime(df_asset_raw['date'])
    df_assets = df_asset_raw.pivot(index='date', columns='security_id', values='close').ffill()
    
    # 对齐
    common_idx = df_signals.index.intersection(df_assets.index)
    df_signals = df_signals.loc[common_idx]
    df_assets = df_assets.loc[common_idx]
    
    # 月频分析以捕捉中长期宏观信号 (对齐报告量级)
    df_asset_ret = df_assets.resample('M').last().pct_change().dropna(how='all')
    df_sig_w = df_signals.resample('M').last().reindex(df_asset_ret.index).ffill()
    
    exposure_results = {}
    
    for sid in df_asset_ret.columns:
        if sid not in INDEX_NAMES: continue
        name = INDEX_NAMES[sid]
        
        y_raw = df_asset_ret[sid].dropna()
        if len(y_raw) < 20: continue
        
        # 1. 去趋势处理 (Detrending)
        cycle, _ = sm.tsa.filters.hpfilter(y_raw, lamb=129600)
        y_scaled = cycle * 100
        
        # 2. 对应自变量
        X = df_sig_w.loc[y_raw.index]
        X = sm.add_constant(X)
        
        # 3. 采用 OLS 回归 (获取真实暴露，用于回测引擎)
        model = sm.OLS(y_scaled, X).fit()
        beta_true = model.params.drop('const')
        exposure_results[name] = beta_true
        
    df_exposure_true = pd.DataFrame(exposure_results).T
    df_exposure_true = df_exposure_true.sort_index()
    
    # 保存真实 Beta (用于后续回测，保留负相关性逻辑)
    df_exposure_true.to_csv(os.path.join(SAVE_DIR_DATA, "exposure_betas.csv"))
    
    # --- 4. 可视化对齐 (符合用户逻辑：展示 Sensitivity/Duration) ---
    df_plot = df_exposure_true.copy()
    for row in df_plot.index:
        if "纯债" in row:
            # 取相反数展现久期敏感度
            df_plot.loc[row] = -1 * df_plot.loc[row]
            
    plt.figure(figsize=(14, 10))
    sns.heatmap(df_plot, annot=True, cmap='RdBu_r', center=0, fmt='.2f', 
                linewidths=0.5, annot_kws={"size": 12})
    plt.title("国泰海通私募策略全集：宏观暴露看板 (Display: Sensitivity)", fontweight='bold', fontsize=16)
    plt.xlabel("宏观因子信号 (Z-Score)", fontsize=12)
    plt.ylabel("私募策略指数", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR_PLOTS, "macro_exposure_heatmap.png"))
    
    print(f"✅ Standardized Exposure Analysis Complete. Results saved.")
    
    # --- 新增：宏观象限划分与历史展示 ---
    plot_macro_regimes(df_signals, SAVE_DIR_PLOTS, SAVE_DIR_DATA)
    
    return df_exposure_true

def plot_macro_regimes(df_signals, save_dir_plots, save_dir_data):
    """
    基于 Growth 和 Inflation 信号划分四象限并绘图
    """
    print("🕰️ Plotting Macro Regime Timeline...")
    regimes = pd.DataFrame(index=df_signals.index)
    regimes['G_up'] = df_signals['HF_Growth'] > 0
    regimes['I_up'] = df_signals['HF_Inflation'] > 0
    
    def classify(row):
        if row['G_up'] and not row['I_up']: return "Recovery (复苏)"
        if row['G_up'] and row['I_up']:     return "Overheat (过热)"
        if not row['G_up'] and row['I_up']: return "Stagflation (滞胀)"
        return "Recession (衰退)"
    
    regimes['Quadrant'] = regimes.apply(classify, axis=1)
    
    # 绘图
    plt.figure(figsize=(16, 6))
    cmap = {
        "Recovery (复苏)": "#2ca02c", "Overheat (过热)": "#d62728",
        "Stagflation (滞胀)": "#ff7f0e", "Recession (衰退)": "#1f77b4"
    }
    
    for q_name, color in cmap.items():
        # 获取该象限的时间段
        mask = regimes['Quadrant'] == q_name
        if mask.any():
            plt.fill_between(regimes.index, -3, 3, where=mask, color=color, alpha=0.2, label=q_name if not plt.gca().get_legend_handles_labels()[1].count(q_name) else "")

    plt.plot(df_signals['HF_Growth'], label='Growth Signal', color='black', lw=1.5)
    plt.plot(df_signals['HF_Inflation'], label='Inflation Signal', color='blue', lw=1, linestyle='--')
    
    plt.axhline(0, color='gray', lw=0.5)
    plt.title("国泰海通宏观高频因子：历史四象限划分 (Macro Regimes)", fontsize=15, fontweight='bold')
    plt.ylim(-3, 3)
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.tight_layout()
    
    regimes.to_csv(os.path.join(save_dir_data, "macro_regimes.csv"))
    plt.savefig(os.path.join(save_dir_plots, "macro_regime_timeline.png"))
    print(f"✅ Regime Analysis saved to {save_dir_plots}")

if __name__ == "__main__":
    if os.path.exists(ASSET_PATH):
        run_exposure_analysis()
    else:
        print(f"❌ Asset data not found. Please ensure DB query output to {ASSET_PATH}")
