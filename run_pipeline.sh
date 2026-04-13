#!/bin/bash
# ==============================================================================
# 宏观择时与战术配置系统 - 全链路自动刷新脚本 (End-to-End Pipeline)
# ==============================================================================

# 设置发生错误时立即退出
set -e

# 设置执行用的 Python 解释器路径 (根据本地环境)
PYTHON_BIN="/Users/chievan/.pyenv/versions/3.10.2/bin/python"

echo "====================================================="
echo "🚀 启动量化系统全链路刷新流程 (Macro Factor Pipeline)"
echo "当前时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "====================================================="

echo ""
echo ">>> [STAGE 1/3] 数据接入与对齐 (Data Fetching & Overview) <<<"
$PYTHON_BIN data/fetch_data.py
$PYTHON_BIN data/gen_overview.py
echo "✅ Stage 1 完成: 基础数据已更新。"

echo ""
echo ">>> [STAGE 2/3] 宏观高频因子生成 (Factor Engineering) <<<"
$PYTHON_BIN factors/build_macro_system.py
echo "✅ Stage 2 完成: Z-Score与宏观因子池已更新。"

echo ""
echo ">>> [STAGE 3/3] 策略回测与绩效报告 (Strategy Backtesting) <<<"
# 1. 暴露系数与四象限划分
$PYTHON_BIN strategy/scripts/macro_timing_analysis.py

# 2. 资产相关性分析
$PYTHON_BIN strategy/scripts/generate_asset_analysis.py

# 3. 极简白马组合回测 (30%套利 + 30%中性 + 40%择时)
$PYTHON_BIN strategy/scripts/minimalist_backtest.py

# 4. 全量资产池战术轮动回测
$PYTHON_BIN strategy/scripts/tactical_backtest.py
echo "✅ Stage 3 完成: 策略全维分析与双频统计已落盘。"

echo ""
echo ">>> [STAGE 4/4] 整合项目最终研究报告 (Master Report Compilation) <<<"
$PYTHON_BIN strategy/scripts/build_report.py
echo "✅ Stage 4 完成: 综合投研报告已就绪。"

echo ""
echo "====================================================="
echo "🎉 全系统运行完毕！"
echo "完整研究报告在此查看: PROJECT_MASTER_REPORT.md"
echo "所有最新结果图表已保存至: strategy/outputs/plots/"
echo "所有中间数据已保存至: strategy/outputs/data/"
echo "核心结构文档请参考: README.md"
echo "====================================================="
