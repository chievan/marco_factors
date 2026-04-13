import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置绘图风格
plt.rcParams['font.sans-serif'] = ['Heiti TC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 路径配置
FACTOR_CSV = "factors/macro_factor_database.csv"
ASSET_CSV = "data/private_fund_indices.csv"
EXPOSURE_CSV = "strategy/outputs/data/exposure_betas.csv"
SAVE_DIR = "strategy/outputs/plots"

def run_minimalist_backtest():
    print("🚀 Initializing Core-Satellite Minimalist Backtest (Ref: Tactical Logic)...")
    
    # 1. 加载因子与资产数据 (对齐 tactical_backtest 逻辑)
    df_sig = pd.read_csv(FACTOR_CSV, index_col=0, parse_dates=True)
    df_sig_z = df_sig[["HF_Rates", "HF_Credit", "HF_FX", "HF_Liquidity", "HF_Growth", "HF_Inflation"]]
    
    df_prices = pd.read_csv(ASSET_CSV)
    df_prices['date'] = pd.to_datetime(df_prices['date'])
    df_prices = df_prices.pivot(index='date', columns='security_id', values='close')

    # 4类核心投资资产 (GTHT)
    INDEX_NAMES = {
        48333548: "GTHT01 (300指增)", 
        43310702: "GTHT04 (1000指增)", 
        49069575: "GTHT06 (市场中性)",
        42883138: "GTHT10 (CTA量化)"
    }
    INVESTABLE_IDS = list(INDEX_NAMES.keys())
    
    # 统一时间轴
    common_idx = df_sig_z.index.intersection(df_prices.index)
    common_idx = common_idx[common_idx >= '2020-01-01'] # 保持与 tactical 一致的时间起点
    
    df_sig_z = df_sig_z.loc[common_idx]
    df_rets_all = df_prices.loc[common_idx].pct_change().fillna(0)
    
    df_rets = df_rets_all[INVESTABLE_IDS]
    df_rets.columns = [INDEX_NAMES[c] for c in df_rets.columns]
    
    # 3. 加载暴露系数
    df_beta = pd.read_csv(EXPOSURE_CSV, index_col=0)
    df_beta = df_beta.loc[df_beta.index.isin(df_rets.columns)]
    
    # 4. 择时逻辑 (核心-卫星架构)
    scores = df_sig_z.dot(df_beta.T)
    df_valid = df_prices.loc[common_idx, INVESTABLE_IDS].notna()
    df_valid.columns = [INDEX_NAMES[c] for c in df_valid.columns]
    scores = scores.where(df_valid, -999)
    
    # (A) 核心层：市场中性底仓 30%
    weights = pd.DataFrame(0.0, index=scores.index, columns=scores.columns)
    anchor_col = "GTHT06 (市场中性)"
    if anchor_col in weights.columns:
        weights.loc[df_valid[anchor_col], anchor_col] = 0.3
        
    # (B) 卫星层：40% 仓位 (Top 2 轮动)
    rank = scores.rank(axis=1, ascending=False)
    top_mask = (rank <= 2) & (scores > -900)
    tactical_alloc = top_mask.astype(float).div(top_mask.sum(axis=1).replace(0, 1), axis=0) * 0.4
    
    final_weights = weights + tactical_alloc
    
    # (C) 底层套利部分 (30%)
    arb_daily_ret = (1 + 0.04)**(1/252) - 1
    
    # 5. 计算收益
    asset_rets = (df_rets * final_weights.shift(1)).sum(axis=1)
    port_rets = asset_rets + (0.3 * arb_daily_ret) # 底仓套利贡献
    
    cum_strat = (1 + port_rets).cumprod()
    
    # --- 自定义复合基准：334模型 + 80BP (对齐 tactical_backtest) ---
    # ID: 46800542 (全指), 49069575 (中性), 47299187 (中债)
    r_bench_comp = df_rets_all[[46800542, 49069575, 47299187]]
    
    bench_rets = (r_bench_comp[46800542] * 0.3 * 0.8) + \
                 (r_bench_comp[49069575] * 0.3 * 0.8) + \
                 (r_bench_comp[47299187] * 0.4) + (0.008 / 252)
    
    cum_bench = (1 + bench_rets.loc[common_idx]).cumprod()
    
    # 6. 可视化 (对齐风格与统计)
    fig = plt.figure(figsize=(16, 14))
    gs = fig.add_gridspec(3, 2)
    
    # (1) 累计净值 (对比复合基准)
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(cum_strat, label='核心-卫星择时策略 (底仓套利+中性底仓+卫星轮动)', color='#d62728', lw=2.5)
    ax1.plot(cum_bench, label='自定义复合基准 (334+80BP)', color='#7f7f7f', lw=1.2, ls='--')
    ax1.set_title("极简版白马组合：精选轮动绩效 (vs 334复合基准, 2020-2026)", fontsize=16, fontweight='bold')
    ax1.legend()
    ax1.grid(alpha=0.2)
    
    # (2) 权重分配
    ax2 = fig.add_subplot(gs[1, :])
    pw = final_weights.copy()
    pw["4%底层套利核心"] = 0.3
    pw.plot.area(ax=ax2, alpha=0.7, cmap='Set2', linewidth=0)
    ax2.set_title("策略权重动态分布 (Allocation Breakdown)", fontsize=14, fontweight='bold')
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    # (3) 分年度收益
    ax3 = fig.add_subplot(gs[2, 0])
    y_strat = port_rets.groupby(port_rets.index.year).apply(lambda x: (1+x).prod()-1)
    y_bench = bench_rets.groupby(bench_rets.index.year).apply(lambda x: (1+x).prod()-1)
    pd.DataFrame({'Strategy': y_strat, 'Benchmark': y_bench}).plot.bar(ax=ax3, color=['#d62728', '#aec7e8'])
    ax3.set_title("年度收益对比", fontsize=14, fontweight='bold')
    for p in ax3.patches:
        ax3.annotate(f'{p.get_height():.1%}', (p.get_x() * 1.005, p.get_height() * 1.005), fontsize=8)

    # (4) 统计指标
    # (4) 统计指标 (集成日频与周频双维度分析)
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.axis('off')
    
    def get_stats_full(cum_p):
        # 1. 日频统计 (Daily)
        r_d = cum_p.pct_change().dropna()
        ann_d = (cum_p.iloc[-1]**(252/len(cum_p))-1)
        vol_d = r_d.std() * np.sqrt(252)
        sharpe_d = ann_d/vol_d if vol_d>0 else 0
        mdd_d = (cum_p/cum_p.cummax()-1).min()
        
        # 2. 周频统计 (Weekly - 过滤噪音)
        cum_w = cum_p.resample('W-FRI').last().dropna()
        r_w = cum_w.pct_change().dropna()
        ann_w = (cum_w.iloc[-1]**(52/len(cum_w))-1) # 52周
        vol_w = r_w.std() * np.sqrt(52)
        sharpe_w = ann_w/vol_w if vol_w>0 else 0
        mdd_w = (cum_w/cum_w.cummax()-1).min()
        
        return [f"{ann_d:.1%}", f"{sharpe_d:.2f}", f"{mdd_d:.1%}", 
                f"{ann_w:.1%}", f"{sharpe_w:.2f}", f"{mdd_w:.1%}"]

    res_strat = get_stats_full(cum_strat)
    res_bench = get_stats_full(cum_bench)
    
    stats_df = pd.DataFrame({
        "策略 (日)": res_strat[:3], "基准 (日)": res_bench[:3],
        "策略 (周)": res_strat[3:], "基准 (周)": res_bench[3:]
    }, index=["年化收益", "夏普比", "最大回撤"])
    
    table = ax4.table(cellText=stats_df.values, colLabels=stats_df.columns, rowLabels=stats_df.index,
                      loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 2.0)
    ax4.set_title("策略绩效多频统计 (Daily & Weekly Analytics)", fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, "minimalist_backtest_full.png"), dpi=300)
    print("✅ Minimalist Policy analysis (Aligned with Tactical) saved.")

if __name__ == "__main__":
    run_minimalist_backtest()
