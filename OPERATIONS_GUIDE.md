# 宏观择时与战术配置系统 —— 运维操作手册 (Operations Guide)

本手册旨在指导如何运维整个宏观配置项目。系统已被划分为严谨的 **Data - Factors - Strategy** 三层架构，确保数据更新、因子合成、策略回测各司其职，互不干扰。

---

## 一、 系统架构说明

本系统根目录下存在三个核心业务模块：

### 1. `data/` (数据底座层)
*   **作用**：连接 DolphinDB，负责从生产环境拉取最新日间行情数据和宏观变量。
*   **执行与产出**：
    *   执行 `fetch_data.py` -> 产出 `full_macro_data.csv` (全市场数据池) 和 `private_fund_indices.csv` (11个量化私募标的 + 基准)。
    *   执行 `gen_overview.py` -> 自动扫描已拉取数据，生成 `data_overview.md` 数据清单，确保底层数据对齐。

### 2. `factors/` (因子工程层)
*   **作用**：通过对低频与高频数据进行处理，包含 HP Filter 降噪与滚动 Z-Score 归一化处理。
*   **执行与产出**：
    *   执行 `build_macro_system.py` -> 将底层数据合成六大宏观维度（Growth, Inflation, Credit, Rates, Liquidity, FX），并产出高频合成因子文件 `macro_factor_database.csv`。同时产出合成逼真度 (Fidelity) 与因子权重的相关图表。

### 3. `strategy/` (策略测试与报告层)
*   **作用**：进行实效分析，根据合成因子的状态执行 FOF 组合的调仓与轮动测试。
*   **内部结构**：
    *   `scripts/`：在此存放所有 Python 分析代码。
    *   `outputs/data/`：存放生成过程中的非展示类数据（例如宏观象限记录、暴露系数）。
    *   `outputs/plots/`：生成并保存面向最终研究报告的图表（回测看板、收益热力图、象限走势等）。
    *   `macro_strategy_framework.md`：本层级的核心逻辑与基准设计解读。

---

## 二、 如何一键更新系统数据与研究报告

项目根目录提供了一个整合脚本 `run_pipeline.sh`，用于**一键刷新整个流水线**。

当市场收盘或您需要将回测时间推移到最新一日时，无需手动执行上文列举的代码，只需在终端中运行：

```bash
# 进入项目根目录
cd /Users/chievan/Desktop/projects/marco_factors

# 确保脚本有执行权限 (仅需一次)
chmod +x run_pipeline.sh

# 执行一键刷新
./run_pipeline.sh
```

**脚本将自动按顺序完成以下任务：**
1. 连通 DDB 获取最新宏微观数据。
2. 重塑基础因子并计算最新高频 Z-Score 信号。
3. 识别当前市场的“宏观大环境所处象限”(Regime)。
4. 运行全量轮动与核心-卫星机制，生成包含“日频/周频”统计指标的投研级大宽幅仪表盘。

操作结束后，所有图表将在 `strategy/outputs/plots/` 目录下被静默更新，您可以直接将其嵌入到您的最终版研报中。

---

## 三、 日常排错与人工介入 (Troubleshooting)

如果运行 `run_pipeline.sh` 中途失败，通常是以下几类问题导致的：

*   **[Stage 1] 失败**：网络异常或 DolphinDB 测试节点无响应。请检查 VPN 或者更换 DDB 连接信息（生产/镜像 IP 切换）。
*   **数据源字段丢失**：如果新增了资产种类导致 `KeyError`，请优先检查 `data/fetch_data.py` 中的 `q_indices` ID 映射是否完备。
*   **基准对比问题**：目前的所有绝对收益和相对基准门槛硬编码为您指定的 **"334+80BP 金标复合模型"**，如您未来需变更这个基准，请到 `strategy/scripts/tactical_backtest.py` 和 `minimalist_backtest.py` 同步调整这段逻辑。

> *Generated automatically as the system operational overview | Updated 2026-04*
