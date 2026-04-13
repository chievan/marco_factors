---
name: ddb-query
description: 专门用于DolphinDB时序数据库的查询技能。当用户需要连接DolphinDB数据库、执行查询语句、获取基金、股票、管理人、因子等数据分析和处理时使用。即使用户只是提到"查询数据"、"提取基金因子"、"净值走势"、"DolphinDB"等关键词，也应该使用这个skill。
---

# `ddb-query` 数据库查询技能

本技能帮助您或AI助理通过DolphinDB高效准确的查询并分析系统外部/内部的各项基金和标的数据。

## 📍 核心知识与准备

执行任何查询前，请务必阅读工作区中的完整数据库结构定义。
**【全量 Schema 数据库映射大全位置】：**
请读取或阅读工作目录中的 `.agent/skills/ddb-query/schema.md` 文件了解真实可用的所有表结构和字段信息。

*   **表名必须大小写精确：** 注意区分 `dfs://HAZQ.fund_price` 等表。
*   **上下文过载保护：** 我们在查询工具中已硬编码 `pandas` 表格行列截断保护策略，Agent 无需再担心使用 `select *` 时上下文爆满的问题。
*   **网络环境：** 脚本已经自动包含主备架构：首选本地极速连接 `172.30.44.32:8848`，若失败或在非专线网络下会自动穿透到云端公共IP `106.54.219.69:8848` 提取数据。

## 🚀 工作流与指令

当你被请求从数据库查数据或做分析时：

0.  **【强制】HAZQ 与 HFNF 双库强制联合查询（互联互通）：** `HAZQ` 与 `HFNF`、`HFNS` 由于历史和业务形态可能存在重叠和互补（例如，某些内部代销产品只在 `HAZQ` 中，而全市场私募数据在 `HFNF` 中）。当你去获取产品列表、行情走势、管理人等核心数据时：
    *   **无论如何，必须强制同时在 `HAZQ`（如 `HAZQ.fund`, `HAZQ.fund_price`）和 `HFNF`（如 `HFNF.pf_fund_info`, `HFNF.pf_fund_price`）这两个库中进行搜索和比对**，**绝对不要只查一个库就结束**。
    *   **如何操作**：在同一个 `.dos` 脚本中，先写查询 `HAZQ` 的语句并 `print`，再写查询 `HFNF` 的语句并 `print`。最后向用户汇报时，必须综合两个库中查到的所有相关产品和行情进行合并展示，确保数据不遗漏。

1.  **解析意图与选取表：** 根据用户意图，去查阅 `.agent/skills/ddb-query/schema.md` 寻找对应的数据库和表。
2.  **编写 `.dos` 脚本：** 将你需要执行的 DolphinDB 专属查询语句写入 `.test/your_query_name.dos` 临时文件中。DolphinDB 支持标准 SQL 和特有的时序函数如 `context by`, `ej`, `wj` 等。
3.  **调用 Python 执行：** 运行以下命令获取查询结果：
    ```bash
    python .agent/skills/ddb-query/scripts/query_dolphindb.py --file .test/your_query_name.dos
    ```
4.  **修正错漏：** 若脚本执行报错（比如函数拼写错误 `S02005`，或者分组函数需要 having 等等），请仔细阅读报错内容，修复 `.dos` 脚本后重复步骤 3，通常 2-3 次修正就可以得到干净的结果。
5.  **回答归因：** 拿着获取的 DataFrame 输出给用户做专业的金融资产、净值表现分析等自然语言总结。

## 💡 示例应用 (查询指数增强策略净值)

**场景：** 查询基金数据库过去一年中，具有“300指增”关键词策略的产品表现。

**生成的 `query_example.dos`：**
```dolphindb
// 从HFNF中筛选符合条件的基金代码
enf_300 = select security_id, name, advisor from loadTable("dfs://HFNF.pf_fund_info", "data") where name like "%300%" and (name like "%增强%" or name like "%指增%");

// 获取这些基金的最新因子表现
latest_date = select max(end_date) as md from loadTable("dfs://HFNF.pf_fund_factor", "data");
factors = select security_id, lastOneYearReturn, lastOneYearMaxDrawdown from loadTable("dfs://HFNF.pf_fund_factor", "data") where security_id in enf_300.security_id and end_date = (exec md from latest_date)[0];

res = select name, advisor, lastOneYearReturn * 100 as ret_1y from ej(enf_300, factors, `security_id) order by lastOneYearReturn desc;

// 打印，注意 Python 执行器会自动帮我们截断超过 50 行的信息防止上下文溢出
print(res);
```

**执行并导出 csv (需要时)：**
```bash
python .agent/skills/ddb-query/scripts/query_dolphindb.py --file .test/query_example.dos --output .test/result.csv --format csv
```
