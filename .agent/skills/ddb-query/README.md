# DolphinDB 查询助手 Skill (ddb-query)

这是一个专门用于DolphinDB时序数据库查询、数据分析及挖掘的Kiro skill。

## 升级声明

- 📡 **双线接入** - 脚本优先连接本地 `172.30.44.32`，连接失败自动穿透公网/跳板 `106.54.219.69`。
- 🛡️ **大表截断防护** - 内置 `pandas` 最大50行显示限制。告别 Select * 导致的大模型 Context Blowup 长下文撑爆现象，从根源保障AI安全执行任务并节省极高API Token费。
- 📖 **真实 Schema** - 完全摒弃虚拟模板，所有的查询基于所在技能包目录内的 `.agent/skills/ddb-query/schema.md` (2000行+的真实数据库快照字典)执行。
- 🧹 **去除冗余** - 剔除了导致大模型行为散乱（分散注意）的额外报表/图片/诊断周边功能。现在的核心功能极其专注：即 **思考业务需求 -> 编写`.dos`语句 -> `query_dolphindb.py` 查出结果 -> AI自主总结并返回**。

## 环境要求

### Python依赖包
```bash
pip install dolphindb pandas
```

## 目录结构
```bash
ddb-query/
├── SKILL.md                    # 让AI理解查询边界和查询逻辑的核心文件
├── README.md                   # 本说明文件
└── scripts/                    # 工具脚本
    └── query_dolphindb.py      # 查询执行主脚本
```

## 快速使用说明

你可以通过 AI 助手直接请求其调用本 skill 进行自然语言驱动的情报挖掘和对冲基金分析：

### 命令行测试

**查询一条简单的命令:**
```bash
python .agent/skills/ddb-query/scripts/query_dolphindb.py "select count(*) from loadTable('dfs://HAZQ.private_index', 'data')"
```

**执行现成的 `.dos` 脚本并截断打印:**
```bash
python .agent/skills/ddb-query/scripts/query_dolphindb.py --file my_query.dos
```

**执行现成的 `.dos` 脚本并输出为 csv 文件:**
```bash
python .agent/skills/ddb-query/scripts/query_dolphindb.py --file my_query.dos --output result.csv --format csv
```
