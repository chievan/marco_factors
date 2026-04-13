import os
import re

def compile_master_report():
    print("📋 [STAGE 4/4] Generating Integrated Master Report...")
    parts = []
    
    # Title
    parts.append("# 宏观择时与大类资产配置系统 - 全景研究报告\n")
    parts.append("> 自动生成汇总文档，包含数据池引擎、高频因子构建以及复合收益策略的回测详解。\n\n---\n")

    # 1. Data Layer
    data_path = "data/data_overview.md"
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            parts.append(f.read())
            parts.append("\n\n<br>\n\n---\n\n")
            
    # 2. Factors Layer
    fac_path = "factors/macro_factor_system.md"
    if os.path.exists(fac_path):
        with open(fac_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Fix relative image paths to align with the Root directory
            content = re.sub(r'\]\(([^/)\]]+\.png)\)', r'](factors/\1)', content)
            parts.append(content)
            parts.append("\n\n<br>\n\n---\n\n")
            
    # 3. Strategy Layer
    strat_path = "strategy/macro_strategy_framework.md"
    if os.path.exists(strat_path):
        with open(strat_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Fix relative image paths to align with the Root directory
            content = re.sub(r'\]\(outputs/plots/([^)]+\.png)\)', r'](strategy/outputs/plots/\1)', content)
            parts.append(content)
            
    # Output to Root
    master_path = "PROJECT_MASTER_REPORT.md"
    with open(master_path, "w", encoding="utf-8") as f:
        f.write("".join(parts))
        
    print(f"✅ Integrated Master Report successfully compiled at: {master_path}")

if __name__ == "__main__":
    compile_master_report()
