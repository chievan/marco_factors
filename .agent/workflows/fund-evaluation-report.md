---
description: how to run the fund evaluation report workflow
---

# 私募评价报告工作流

## 概述
私募评价报告是一个多步骤的工作流页面，位于 `策略研究 > 评价报告` 菜单下（路径：`/strategy/evaluation-report`）。
该页面按策略类别逐步展示产品评级列表，用户在每个策略步骤中选择需要纳入最终报告的产品，选择完成后进入下一个策略模块，最终生成综合评价报告。

## 前置条件：上传 DolphinDB 模块

**⚠️ 必须先将 `.dos` 文件上传到 DolphinDB 服务器才能使用！**

// turbo
1. 将以下 `.dos` 文件上传到 DolphinDB 服务器的模块目录：
   - `pfdp/database/dolphindb_modules/fund_evaluation_report.dos`
   - 上传路径：DolphinDB 服务器的 `privateFund/FundEvaluationReport.dos` 模块目录下

2. 在 DolphinDB 中加载模块：
   ```
   use privateFund::FundEvaluationReport
   ```

3. 验证模块加载成功：
   ```
   getStrategyProducts("股票策略", "沪深300指数增强", "股票多头", "300指增", "000300", 5)
   ```

## 页面路径
- URL: `/strategy/evaluation-report`
- 菜单位置: 策略研究 → 评价报告

## 文件结构
- **DolphinDB 模块**: `pfdp/database/dolphindb_modules/fund_evaluation_report.dos`
  - 模块名: `privateFund::FundEvaluationReport`
  - 函数: `getStrategyProducts(...)`
  - 核心逻辑:
    - **活跃度过滤**: 动态获取数据库中所有产品的最新业务日期（避免停牌数据问题），由此前推10个交易日判断是否为活跃存续产品。
    - **收益率计算**: 调用 `Empyrical` 包按日频计算逐年收益，再通过提取对齐得到年化指标。
    - **评分体系**: 按指数增强策略得分模型计算百分制评分，去重后选取各策略表现最佳的 TopN 产品。
- **数据查询 (Python)**: `pfdp/database/scipts/fund_evaluation_report_db.py`
  - 策略配置 `STRATEGY_CONFIG`（目前包含沪深300、中证500、中证1000指增）
  - `get_strategy_products(strategy_key)` 通过 `get_ddb_data_by_func` 调用 DolphinDB 模块
  - `get_all_strategy_configs()` 获取策略列表
- **视图 (View)**: `pfdp/views/core_pages/fund_evaluation_report.py`
  - 包含页面布局渲染逻辑和 Dash 回调
  - 使用 AntdSteps 组件实现步骤条
  - 每个步骤展示 AntdTable 产品列表（内含 checkbox 选择、产品名称可点击链接到详情页）
  - 生成并导出 Excel 报告功能 (`export_report` 回调)
- **回调 (Callback)**: `pfdp/callbacks/core_pages_c/fund_evaluation_report_c.py`
  - 导出报告功能及步骤间切换处理
- **路由配置**: `pfdp/configs/router_config.py`
  - 菜单、路由、侧边栏均已注册

## 策略模块（当前配置）
1. **沪深300指数增强** - 追踪沪深300，追求稳健超额
2. **中证500指数增强** - 追踪中证500，中盘股超额
3. **中证1000指数增强** - 追踪中证1000，小盘股高弹性
*(注：市场中性、CTA等策略可通过修改 `STRATEGY_CONFIG` 随时恢复/加入)*

## 工作流步骤
1. 打开页面，自动加载第一个策略（沪深300指增）的产品列表
2. 勾选需要纳入报告的产品（可点击产品名称进入详情页查看）
3. 点击"下一步"进入下一个策略
4. 重复步骤 2-3 直到所有策略扫描完成
5. 最终步骤显示汇总页面，展示分组后的全部已选产品
6. 点击"导出报告"按钮，自动生成并下载含各策略分表及汇总页的 Excel 评价报告

## 添加新策略
在 `fund_evaluation_report_db.py` 的 `STRATEGY_CONFIG` 列表中添加新的策略配置字典即可，页面会自动扩展步骤。

## 启动应用
// turbo
```bash
cd /Users/chievan/Desktop/private-fund/pfdp && python app.py
```
