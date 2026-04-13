import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import os

# =================================================================
# 1. 核心映射配置 (Verbatim from Research)
# =================================================================

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Heiti TC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# STEP 1: 原始宏观指标 (Ground Truth Codes)
RAW_MAP = {
    "Growth": ["M002043802", "M001620538", "M001625520", "M002808931"], # PMI, 投资, 社消, 进出口
    "Inflation": ["M002826730", "M002826865"],                       # CPI, PPI
    "Liquidity": ["M001625222", "M004891021"],                       # M2, 社融
    "Rates": ["L001619604"],                                         # 10Y国债
    "Credit": ["L002959791", "L001618296"],                          # AA+, 国开
    "FX": ["DINI.FX"]                                                # 美元指数
}

# 成员名称映射 (用于图表)
MEMBER_NAMES = {
    "M002043802": "制造业PMI", "M001620538": "固投同比", "M001625520": "社消同比", "M002808931": "进出口同比",
    "M002826730": "CPI同比", "M002826865": "PPI同比"
}

# STEP 2: 高频代理映射 (V6.0 Hybrid)
HF_CONFIG = {
    "Direct": {"Rates": ["48488928"], "Credit": ["48919110", "47989178"], "FX": ["DINI.FX"]},
    "Spread": {"Liquidity": ["PE_801813", "PE_801811"]},
    "IVW": {"Growth": ["S000055209", "44029654", "46111941", "47887552"], "Inflation": ["S002808935", "S005402539", "44779723"]}
}

# =================================================================
# 2. 工具单元
# =================================================================

def hp_filter(series, lamb=129600):
    if series.isnull().all(): return series
    clean = series.ffill().bfill()
    if clean.std() == 0: return clean
    cycle, trend = sm.tsa.filters.hpfilter(clean, lamb=lamb)
    return trend

def standardize(s):
    return (s - s.mean()) / s.std() if s.std() > 0 else s

def handle_macro_gap(df):
    """中国宏观插值预处理"""
    return df.interpolate(method='linear', limit=3).ffill().bfill()

# =================================================================
# 3. 生产逻辑 (Production)
# =================================================================

def main():
    print("🏗️ Unified Macro Factor Engine Starting...")
    
    # 1. 数据加载
    df_raw_data = pd.read_csv("data/full_macro_data.csv")
    df_raw_data['date'] = pd.to_datetime(df_raw_data['date'])
    df_price = df_raw_data.pivot(index='date', columns='security_id', values='close').ffill()
    df_adj = handle_macro_gap(df_price)

    # 2. Phase 1: Raw Benchmarks
    print("📋 [Step 1] Building Raw Benchmarks...")
    raw_indicators = pd.DataFrame(index=df_price.index)
    ivw_weights = {}

    for dim in ["Growth", "Inflation"]:
        codes = RAW_MAP[dim]
        data = df_adj[codes].dropna(how='all')
        if data.empty:
            print(f"⚠️ Warning: No data for {dim}")
            continue
        vols = data.std()
        vols[vols == 0] = 0.001 # 避免除0
        weights = (1.0 / vols) / (1.0 / vols).sum()
        ivw_weights[dim] = weights
        raw_indicators[dim] = (data * weights).sum(axis=1)
    
    raw_indicators["Liquidity"] = df_adj["M001625222"] - df_adj["M004891021"]
    raw_indicators["Credit"] = df_adj["L002959791"] - df_adj["L001618296"]
    raw_indicators["Rates"] = df_adj["L001619604"]
    raw_indicators["FX"] = df_adj["DINI.FX"]
    
    # HP平滑长期趋势
    for dim in ["Growth", "Inflation", "Liquidity"]:
        raw_indicators[dim] = hp_filter(raw_indicators[dim], lamb=129600)
    
    raw_bench = raw_indicators.apply(standardize).resample('ME').last().ffill()
    raw_bench.to_csv("factors/raw_macro_benchmarks.csv")

    # 3. Phase 2: HF Factors
    print("🚀 [Step 2] Building HF Proxy Factors...")
    hf_returns = pd.DataFrame(index=df_price.index)
    hf_returns["Rates"] = -1 * df_price[HF_CONFIG["Direct"]["Rates"][0]].pct_change()
    c_codes = HF_CONFIG["Direct"]["Credit"]
    hf_returns["Credit"] = df_price[c_codes[1]].pct_change() - df_price[c_codes[0]].pct_change()
    hf_returns["FX"] = df_price[HF_CONFIG["Direct"]["FX"][0]].pct_change()
    s, b = HF_CONFIG["Spread"]["Liquidity"]
    spread = df_price[s] - df_price[b]
    hf_returns["Liquidity"] = spread.diff().fillna(0) / spread.abs().mean()
    for dim, proxies in HF_CONFIG["IVW"].items():
        avail = [p for p in proxies if p in df_price.columns]
        rets = df_price[avail].pct_change().fillna(0)
        v = rets.rolling(252).std().replace(0, 1e-6)
        w = (1.0 / v).div((1.0 / v).sum(axis=1), axis=0).ffill().bfill()
        hf_returns[dim] = (rets * w).sum(axis=1)
    
    hf_factors = hf_returns.cumsum().ffill()
    combined_db = pd.concat([hf_factors.add_prefix("HF_"), raw_bench.reindex(df_price.index).ffill().add_prefix("Raw_")], axis=1)
    combined_db.to_csv("factors/macro_factor_database.csv")

    # 4. 可视化报告 (Visuals)
    print("📊 [Visuals] Generating PNGs...")
    
    # (1) Raw Overview 3x2
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    dims = ["Growth", "Inflation", "Rates", "Credit", "FX", "Liquidity"]
    for i, dim in enumerate(dims):
        ax = axes[i // 2, i % 2]
        if dim in raw_bench.columns:
            ax.plot(raw_bench.index, raw_bench[dim], color='#1f77b4', lw=2)
            ax.set_title(f"Ground Truth Trend: {dim}", fontweight='bold')
    plt.tight_layout()
    plt.savefig("factors/raw_indicators_overview.png")

    # (2) Raw Indicator Weights
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for i, dim in enumerate(["Growth", "Inflation"]):
        if dim in ivw_weights:
            w = ivw_weights[dim]
            labels = [MEMBER_NAMES.get(k, k) for k in w.index]
            axes[i].pie(w, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("viridis", len(w)))
            axes[i].set_title(f"Raw Benchmark Composition: {dim}", fontweight='bold')
    plt.tight_layout()
    plt.savefig("factors/raw_indicator_weights.png")

    # (3) Final Fidelity Check
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    for i, dim in enumerate(dims):
        ax = axes[i // 2, i % 2]
        if dim in hf_factors.columns: ax.plot(hf_factors.index, standardize(hf_factors[dim]), label="HF Proxy", color='#d62728', alpha=0.9)
        if dim in raw_bench.columns: ax.plot(raw_bench.index, standardize(raw_bench[dim]), label="Raw Bench", color='#1f77b4', alpha=0.4, drawstyle='steps-post')
        ax.set_title(f"Fidelity Sync: {dim}", fontweight='bold')
        ax.legend()
    plt.tight_layout()
    plt.savefig("factors/macro_system_fidelity.png")
    plt.savefig("factors/hf_fidelity_final.png") # 兼容原路径

    # (4) Factor Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(hf_factors.pct_change().corr(), annot=True, cmap='RdYlBu_r', center=0)
    plt.title("HF Factor Correlation Heatmap", fontweight='bold')
    plt.savefig("factors/factor_correlation_heatmap.png")

    print("\n✅ Unified Engine Refreshed. All PNGs and CSVs are up to date.")

if __name__ == "__main__":
    main()
