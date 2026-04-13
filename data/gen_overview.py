import pandas as pd
import os

# 全量指标名称映射 (包含全集: 宏观代理, 投资资产, 评价基准, 宏观原语)
NAME_MAP = {
    # 1. 宏观核心/低频
    "M002043802": "制造业PMI",
    "M001620538": "固定资产投资同比",
    "M001625520": "社会消费品零售同比",
    "M002808931": "进出口总额同比",
    "M002826730": "CPI同比 (宏观基准)",
    "M002826865": "PPI同比",
    "L001619604": "10Y国债收益率 (核心信号)",
    "L002959791": "AA+级中债3Y收益率",
    "L001618296": "国开债3Y收益率",
    "M001625222": "M2同比",
    "M004891021": "社会融资规模同比",
    "S000055209": "CRB工业原料指数",
    "DINI.FX": "美元指数 (DXY)",
    "S002808935": "猪肉价格",
    "S005402539": "原油价格",
    "PE_801811": "申万大盘指数 PE",
    "PE_801813": "申万小盘指数 PE",
    
    # 2. 宏观/高频代理 (4系列)
    "46111941": "恒生指数",
    "44029654": "沪铜主连",
    "47887552": "房地产板块指数",
    "49157014": "南华猪肉指数",
    "46632374": "南华原油指数",
    "44779723": "南华螺纹钢指数",
    "48488928": "中证10Y国债净价指数",
    "48919110": "中证企业债指数 (H11008)",
    "47989178": "中证国债指数 (H11006)",
    "42630518": "南华贵金属指数",
    "40485417": "南华农产品指数",
    
    # 3. 投资资产 pool (GTHT系列)
    "48333548": "GTHT01 (300指增)",
    "48408839": "GTHT02 (可转债)",
    "43494799": "GTHT03 (500指增)",
    "43310702": "GTHT04 (1000指增)",
    "48585505": "GTHT05 (CTA标准)",
    "49069575": "GTHT06 (市场中性)",
    "40998561": "GTHT07 (纯债)",
    "49361940": "GTHT08 (主观权益)",
    "40553563": "GTHT09 (CTA主观)",
    "42883138": "GTHT10 (CTA量化)",
    "44238744": "GTHT11 (宏观策略)",
    
    # 4. 评价基准 components
    "46800542": "中证全指 (基准权益)",
    "47299187": "中债综合财富 (基准固收)"
}

def generate_overview():
    print("📋 Generating full data inventory overview...")
    csv_path = "data/full_macro_data.csv"
    if not os.path.exists(csv_path):
        print("❌ CSV file not found! Run fetch_data.py first.")
        return

    df = pd.read_csv(csv_path)
    df['security_id'] = df['security_id'].astype(str)
    
    # 获取统计
    stats = df.groupby('security_id').agg({
        'date': ['min', 'max', 'count']
    })
    stats.columns = ['Start_Date', 'End_Date', 'Total_Count']
    stats = stats.reset_index()
    
    # 丰富名称
    stats['Chinese_Name'] = stats['security_id'].map(NAME_MAP).fillna("Unknown/New Asset")
    
    # 分类逻辑
    macro_mask = stats['security_id'].str.contains(r'^[A-Z]|PE_') | stats['security_id'].isin([
        "46111941", "44029654", "47887552", "49157014", "46632374", "44779723", "48488928", "48919110", "47989178", "42630518", "40485417"
    ])
    
    macro_stats = stats[macro_mask].sort_values('security_id')
    invest_stats = stats[~macro_mask].sort_values('security_id')

    # 生成 Markdown
    now = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    md = f"# 宏观因子系统全量数据概览\n\n更新时间: {now}\n\n"
    
    md += "## 1. 宏观因子与代理标的 (Macro Factors & Proxies)\n\n"
    md += "| 指标名称 | 代码/sec_id | 起始日期 | 截止日期 | 数据点 | \n"
    md += "| :--- | :--- | :--- | :--- | :--- |\n"
    for _, r in macro_stats.iterrows():
        md += f"| {r['Chinese_Name']} | `{r['security_id']}` | {r['Start_Date']} | {r['End_Date']} | {r['Total_Count']} |\n"
        
    md += "\n## 2. 投资资产与评价基准 (Assets & Benchmarks)\n\n"
    md += "| 指标名称 | sec_id | 起始日期 | 截止日期 | 数据点 | \n"
    md += "| :--- | :--- | :--- | :--- | :--- |\n"
    for _, r in invest_stats.iterrows():
        md += f"| {r['Chinese_Name']} | `{r['security_id']}` | {r['Start_Date']} | {r['End_Date']} | {r['Total_Count']} |\n"

    md += "\n---\n*注：数据全量通过 fetch_data.py 从 DolphinDB 生产/云端镜像同步。两表（full_macro_data.csv 与 private_fund_indices.csv）已实现 ID 级对齐。*"

    with open("data/data_overview.md", "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"✅ Full overview metadata updated at data/data_overview.md. (Total IDs: {len(stats)})")

if __name__ == "__main__":
    generate_overview()
