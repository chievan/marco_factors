---
name: page-development
description: 用于本项目（Dash + feffery）的新页面开发与现有页面改造。遇到“新增网页/页面”“新增菜单路由”“补全页面回调”“接入DolphinDB数据并在页面展示”“页面联调与排错”等需求时使用。尤其适用于需要同时修改 views、callbacks、configs/router_config、database/scipts、database/dolphindb_modules 的场景。
---

# 页面开发技能（private-fund）

按下面流程实施，确保页面能被菜单访问、能正确渲染、能拿到数据、权限可控。

## 1. 先确认页面类型

先判断是以下哪一类，再决定改动范围：

- `纯展示页`：只改 `pfdp/views/core_pages/*.py`，一般不新增 db 脚本。
- `交互页`：改 `views + callbacks`，按组件 `id` 对齐回调输入输出。
- `数据页`：改 `views + callbacks + database/scipts + dolphindb_modules`。
- `详情页`：通常通过 query 参数取主键（如 `?id=`），在 `render(current_url)` 里解析。

## 2. 按工程约定创建页面文件

新增页面时，优先遵循现有命名风格：

- 视图：`pfdp/views/core_pages/<page_name>.py`
- 回调：`pfdp/callbacks/core_pages_c/<page_name>_c.py`
- 数据脚本（如需）：`pfdp/database/scipts/<page_name>_db.py`
- DolphinDB 模块（如需）：`pfdp/database/dolphindb_modules/<page_name>.dos`

页面结构优先复用：

- `PageContainer(...)` 作为页面外层容器
- `ContentCard(...)` 作为主要内容块
- 组件命名统一加页面前缀，避免跨页 id 冲突（例如 `market-news-*`）

## 3. 接入路由与菜单（必须）

新增页面至少同步以下配置：

1. `pfdp/configs/router_config.py`
2. `pfdp/callbacks/core_pages_c/__init__.py`

具体操作：

1. 在 `core_side_menu` 增加菜单项（若需要在侧边栏显示）。
2. 在 `valid_pathnames` 新增 `pathname -> 页面标题` 映射。
3. 在 `side_menu_open_keys` 增加该 pathname 对应父菜单展开项。
4. 在 `core_pages_c/__init__.py` 顶部 `from views.core_pages import ...` 引入新页面模块。
5. 在 `core_router` 中新增 `elif pathname == "...": page_content = <page>.render(...)` 分支。

若遗漏任一步，常见表现是：菜单可见但点击 404、路径存在但页面不渲染、侧边栏高亮/展开异常。

## 4. 接入权限（按需）

若页面需要角色限制，更新：

- `pfdp/configs/auth_config.py` 的 `pathname_access_rules`

遵循现有 `include/exclude/all` 规则，不要新增自定义权限模型。

## 5. 数据链路实现（数据页必须）

按项目现有层次实现：

1. 在 `database/dolphindb_modules/*.dos` 定义模块函数。
2. 在 `database/scipts/*_db.py` 封装 Python 调用函数（DataFrame 转换、空结果兜底、异常处理）。
3. 在 `callbacks/core_pages_c/*_c.py` 调用 db 封装函数并做前端展示字段转换。
4. 在 `views/core_pages/*.py` 只放布局和初始状态，避免重逻辑塞进 view。

统一调用入口：

- 使用 `database.dolphin_db.get_ddb_data_by_func(module, func, **kwargs)`。
- 参数尽量保持简单类型（str/int/list/dict/date），复杂转换放在 db 脚本层。

## 6. 回调开发约束

- 回调只写在 `callbacks/core_pages_c/*_c.py`，通过模块导入触发注册。
- `prevent_initial_call` 按需设置，避免页面初始化重复触发重查询。
- 多个互斥筛选项优先参考现有 `CheckableTag` 互斥处理写法。
- 出错时优先返回可展示兜底（空表、提示文案），并打印可定位日志。

## 7. 新增页面最小检查清单

完成后逐项自检：

1. 路由可访问：手输 URL 能打开，不出现 404。
2. 菜单正确：可见性、展开层级、高亮状态正确。
3. 回调生效：交互触发后组件刷新，且无明显循环触发。
4. 数据可用：数据库返回为空时页面仍可渲染，不报错。
5. 权限正确：`admin/normal` 下访问行为符合预期。

## 8. 实施顺序（推荐）
先做路由壳子，再做静态页面，再接回调，最后接数据库。

推荐顺序：

1. 补齐 `router_config.py` 和 `core_pages_c/__init__.py` 的路由分支
2. 建 `views/core_pages/<page>.py` 返回最小可渲染页面
3. 建 `callbacks/core_pages_c/<page>_c.py` 连通基础交互
4. 建 `database/scipts/<page>_db.py` + `.dos` 并替换 mock 数据
5. 联调与异常兜底

## 9. 与 ddb-query 协作

当页面开发涉及 DolphinDB 查询语句编写、定位字段或跨库对照时，调用 `$ddb-query` skill 负责查询语句与数据校验，再把稳定查询收敛到本页面的 `*_db.py` 与 `.dos` 模块中。

## 10. 本项目高频坑位（强制检查）

### 10.1 组件属性兼容性（feffery 版本差异）

- `fac.AntdTable` 在当前项目版本不支持 `scroll`，使用 `maxWidth` / `maxHeight` 控制。
- `fac.AntdStatistic` 的数值更新用 `value`，不要输出到 `children`。
- 若 `feffery_antd_charts` 图表不稳定，优先切换到 `dcc.Graph + plotly`，回调输出 `figure`。

### 10.2 回调输出类型对齐

- Output 属性必须与组件真实属性一致（例如 `AntdStatistic.value`、`dcc.Graph.figure`）。
- 若“表格有数据但图/统计为空”，第一步先单独调用回调函数，检查返回值长度和类型。

### 10.3 DolphinDB 计算口径

- 年化收益不要用净值点数量（`count(*)`）做分母；应使用自然日跨度（`latest_date - start_date + 1`）。
- `.dos` 中统一使用标准算术符号（如 `/`），避免非预期写法导致兼容问题。

### 10.4 `.dos` 生效流程

- 本地仓库改完 `.dos` 不会自动在数据库服务器生效。
- 必须由用户手动上传 `.dos` 到服务器并重新加载模块后，页面查询结果才会反映新逻辑。

## 11. 联调测试流程（必须按顺序）

1. **Python 语法检查**  
   `python -m py_compile` 检查 `views/callbacks/db.py`。
2. **回调直调检查（优先）**  
   在 `venv` 中直接调用回调函数，确认三类输出同时有值：  
   `table data`、`chart(figure or data)`、`stats`。
3. **应用链路检查**  
   启动 `python pfdp/app.py`，用 `admin / admin123` 登录目标页面。
4. **页面实测检查**  
   核对：菜单进入、表格行数、统计卡片、图表曲线是否同时正常。
5. **服务器模块检查（涉及 .dos 必做）**  
   用户上传 `.dos` 后，在 DolphinDB 执行模块函数进行最终确认。

## 12. 本次页面开发复盘要点（千衍三涛页）

- 出现过 `AntdTable.scroll` 不兼容导致页面报错。
- 出现过统计卡片 Output 写成 `children` 导致“表格有数据但卡片空值”。
- 出现过图表组件路径不稳定导致“表格有数据但图不渲染”，最终改为 `dcc.Graph` 解决。
- 出现过年化收益计算口径错误（按净值点数量），已改为按自然日跨度。

## 13. 新增强制规范（用户要求）

### 13.1 DOS 必须先用 ddb-query 测试并自动修正

- 每次新写或修改 `.dos` 后，必须先用 `.agent/skills/ddb-query/scripts/query_dolphindb.py` 做实测。
- 优先直接调用服务器模块函数验证，不依赖 `run("本地路径.dos")`（云端看不到本地文件）。
- 若报错，必须先自动修复 `.dos` 并再次测试，直到函数可执行且结果结构符合页面需要。

### 13.2 图表与表格保持同组件体系

- 图表组件优先采用与表格一致的 Antd/feffery 体系，保证页面视觉和交互语言统一。
- 图表必须放在 `ContentCard` 等同风格容器内，标题、间距、交互提示与表格区域保持一致。
- 若同体系图表存在稳定性问题，再回退 `dcc.Graph`，并在变更说明中明确原因。

### 13.3 测试网络必须使用本地网络

- 数据库连接测试必须基于用户本地网络环境执行（不可仅依赖沙箱网络结果）。
- 网页联调与自动化测试（含 Playwright）必须在本地网络可达条件下执行。
- 若当前环境网络受限，应明确请求在本地网络权限下执行后再给结论。

### 13.4 页面登录测试账号（固定）

- 页面联调默认登录账号：`admin`
- 页面联调默认登录密码：`admin123`
- 在未收到用户新账号前，自动化测试与手工复现均使用该账号密码。

### 13.5 策略指标页必须建立“算法-函数-数据”映射

- 对每个指标至少提供三项可见信息：`算法说明`、`dos函数名`、`页面实际数据`。
- 页面上要有可追踪关系：指标表中展示 `dos函数/实现状态`，详情区展示“当前指标算法 + dos函数 + 查询结果”。
- 新增指标时优先在独立 `.dos` 中逐个实现，Python `*_db.py` 只做参数转换与结果清洗，避免把算法散落在回调层。
- 对“未实现”指标要显式标注 `待实现`，不要返回静默空图。
