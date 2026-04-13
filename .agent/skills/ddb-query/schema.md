# DolphinDB 数据库结构文档

生成时间: 2026-02-28 20:53:11

---

## 数据库: /HAZQ.private_index

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| datetime | DATE |  |
| product_name | SYMBOL |  |
| product_code | SYMBOL |  |
| nav | DOUBLE |  |

---

## 数据库: /HAZQ.fund

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| datetime | DATE |  |
| product_name | SYMBOL |  |
| product_code | SYMBOL |  |
| nav | DOUBLE |  |
| acc_nav | DOUBLE |  |
| virtual_nav | DOUBLE |  |
| holding_share | DOUBLE |  |
| total_share | DOUBLE |  |
| tag | SYMBOL |  |

---

## 数据库: /HFNF.common_person

### 表: data
**表注释**: 人员表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| category | LONG | 人员类别，1-公募基金经理、2-私募基金经理、9-其他 |
| org_id | LONG | 机构ID，关联common_org.org_id |
| person_id | LONG | 人员ID |
| name | STRING | 中文全称 |
| gender | SHORT | 性别：1-男、2-女、0-未知 |
| birthday | DATE | 出生日期 |
| education | SHORT | 最高学历，1-高中、2-大专、3-本科、4-硕士、5-博士、9-其他 |
| nationality | SHORT | 国籍，1-中国、2-中国香港、3-中国台湾、9-其他 |
| professional_title | STRING | 职称名称 |
| email | STRING | 电子邮箱 |
| tel | STRING | 联系电话 |
| background | STRING | 背景介绍 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_manager_info

### 表: data
**表注释**: 私募 - 基金经理基础信息表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| org_id | LONG | 机构ID，关联common_org.org_id |
| person_id | LONG | 人员ID，关联common_person.person_id |
| fof99_id | LONG | FOF99 ID |
| name | STRING | 基金经理姓名 |
| brief | STRING | 简介 |
| st | DATE | 从业开始日期 |
| post_year | DECIMAL64(1) | 任职年限(年) |
| funds | INT | 管理的基金数量 |
| best_return | DECIMAL64(6) | 任职期间最佳基金回报(%) |
| represent_fund | STRING | 代表产品fid |
| active | CHAR | 0删除、1正常 |
| sort | INT | 排序字段 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.fof_subfund

### 表: data
**表注释**: FOF运维子基金表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| parent_id | INT | 母基金表id |
| ta_id | INT | TA账号id（company_ta_account主键） |
| ftype | CHAR | 类型：1-私募平台，2-私募内部 |
| fid | INT | funds对应基金id |
| fund_name | STRING | 基金简称 |
| invest_date | DATE | 投资日期 |
| clear_time | DATE | 清仓日期 |
| initial_share | DECIMAL64(4) | 期初份额（废弃） |
| initial_price | DECIMAL32(4) | 期初净值（废弃） |
| initial_asset | DECIMAL64(4) | 期初资产（废弃）（=期初金额） |
| invest_cost | DECIMAL64(4) | (期末)投资成本 |
| agent | STRING | 经济端 |
| remark | STRING | 备注 |
| active | CHAR | 状态：1-正常 0-下架 |
| status | CHAR | 计算状态：1-正常，2-无净值，3-无交易，4-下架（占用，由funds表active计算得出） |
| last_shares | DECIMAL64(4) | 期末份额 来自估值&清仓台账 |
| last_price | DECIMAL64(8) | 期末净值（来自底层净值维护最新净值） |
| price_date | DATE | 期末日期 |
| update_type | CHAR | 期末数据更新来源0-手动添加已投产品 来自指令也是0 （尚无期末数据来源）1-估值 2-估值表 3-添加已投 |
| uid | INT | 创建人uid |
| cycle_type | CHAR | 净值频率 1：日频 2：周频（废弃） |
| company_id | INT | 底层基金所属母基金的公司id |
| last_asset | DECIMAL64(4) | 期末资产（与底层净值最新期末持仓资产同步，若台账清仓也同步清零 |
| last_cost | DECIMAL64(4) | 期末持仓成本 |
| last_cost_accumulated | DECIMAL64(4) | 期末累计持仓成本 |
| type | CHAR | 类型：1-已投 2-跟踪 |
| remark_uid | INT | 备注人uid |
| remark_time | DATETIME | 备注时间 |
| tag_id | STRING | 标签ID |
| from_type | CHAR | 基金类型：1-私募基金 2-公募基金 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.fof_subfund_price

### 表: data
**表注释**: FOF运维-子基金净值

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| sf_id | INT | 子基金表id |
| pid | INT | 母基金表id |
| price_date | DATE | 净值日期 |
| nav | DECIMAL64(8) | 单位净值 |
| shares | DECIMAL64(4) | 净值日持仓份额 |
| position_assets | DECIMAL64(4) | 净值日持仓资产（市值） |
| remark | STRING | 备注 |
| active | CHAR | 状态：1-正常 0-同一天有来自估值表底层虚拟净值时，其他来源的active为0 |
| uid | INT | 用户id |
| state | CHAR | 0-未审核 1-已审核 2-来自估值表无需审核 |
| from_type | CHAR | 1-邮件解析 2-估值表同步 3-团队上传 |
| cost | DECIMAL64(4) | 成本 |
| value_change | DECIMAL64(4) | 估值增值：市值-成本 |
| suspend_info | STRING | 停牌信息 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.funds_bonus

### 表: data
**表注释**: 基金分红记录

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| fid | INT | funds表基金id |
| price_date | DATE |  |
| from_type | CHAR | 来源类型：1-平台计算，2-ms后台，3-私募牛，4-插件 |
| amount | DECIMAL64(6) | 分红金额 |
| company_id | INT | 公司id |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.valuation_asset_types

### 表: data
**表注释**: 估值表明细分类

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | ID |
| parents_id | SHORT | 父类ID |
| type_name | SYMBOL | 分类名称 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.index_info

### 表: data
**表注释**: 指数 - 基础信息

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| fof99_id | LONG | FOF99 ID |
| code | SYMBOL | 指数官方编码Code |
| name | STRING | 指数全称 |
| short_name | STRING | 指数简称 |
| abbr | STRING | 指数中文首字母缩写 |
| en_name | STRING | 指数英文全称 |
| en_short_name | STRING | 指数英文简称 |
| publisher | STRING | 指数发布者，例：火富牛 |
| category | SYMBOL | 一级分类，stock(股票)、commingled(混合)、bond(债券)、currency(货币基金)、qdii(QDII基金)、other(其他) |
| sub_category | SYMBOL | 二级分类，stock-stock(股票-股票型)、stock-index(股票-指数型)、stock-index-enhance(股票-增强指数型)、commingled-stock(混合偏股)、commingled-bond(混合偏债)、commingled-flexible(混合灵活)、commingled-balance(混合平 |
| intro | STRING | 指数简述 |
| homepage | STRING | 指数官网URL |
| market | SYMBOL | 指数覆盖市场，如：全球、境内、香港、沪深港 |
| currency | SYMBOL | 货币单位，默认CNY(人民币)、USD(美元)、EUR(欧元)、HKD(港币) |
| type | SYMBOL | 指数类别，如风格、规模、主题、行业、策略 |
| asset_type | SYMBOL | 资产类别，如股票、债券、多资产、期货 |
| scheme_intro | STRING | 编制说明文案 |
| issue_date | DATE | 发布日期 |
| baseline_date | DATE | 基日(指数创建日期) |
| baseline_price | DECIMAL64(6) | 基点(指数创建点数) |
| sample_date | DATE | 最新编制样本股日期 |
| sample_number | LONG | 最新编制样本股数量 |
| price_date | DATE | 最新点数日期 |
| pre_price_nav | DECIMAL64(6) | 昨收点数 |
| open_price_nav | DECIMAL64(6) | 开盘点数 |
| high_price_nav | DECIMAL64(6) | 最高点数 |
| low_price_nav | DECIMAL64(6) | 最低点数 |
| price_nav | DECIMAL64(6) | 收盘点数 |
| price_change | DECIMAL64(6) | 涨跌点数 |
| price_change_ratio | DECIMAL64(6) | 涨跌点数比例 |
| hotspots | STRING | 指数热点列表，多个用英文逗号隔开 |
| tags | STRING | 标签列表，多个用英文逗号隔开 |
| order | CHAR | 排序，数字越小越靠前 |
| remark | STRING | 备注信息 |
| active | CHAR | 状态，1(启用)、0(禁用) |
| is_default | CHAR | 是否默认 |
| is_used | CHAR | 是否常用 |
| wa_method | SYMBOL | 加权方式 |
| contrast_index | SYMBOL | 默认对比指数 |
| pub_index_type | SYMBOL | 指数类别(发布机构) |
| total_value | DECIMAL128(4) | 指数市值 |
| roa | DECIMAL128(4) | ROA |
| roe | DECIMAL128(4) | ROE |
| net_profit_yoy | DECIMAL128(4) | 净利润增速 |
| operating_revenue_yoy | DECIMAL128(4) | 营业收入增速 |
| pb | DECIMAL128(4) | 指数PB |
| pe | DECIMAL128(4) | 指数PE |
| dividend_ratio | DECIMAL128(4) | 股息率 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_info

### 表: data
**表注释**: 私募 - 基金基础信息

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| fof99_id | LONG | FOF99 ID |
| father_security_id | INT | 分级基金所属父基金id |
| amac_id | STRING | AMAC协会ID |
| amac_url | STRING | AMAC协会基金URL |
| name | STRING | 基金全称 |
| short_name | STRING | 基金简称 |
| register_number | STRING | 协会备案编码 |
| quantitative_strategy | CHAR | -1 未知 0.不采用量化策略 1.采用量化策略 |
| initial_unit_value | DECIMAL64(2) | 基金初始值 |
| city | SYMBOL | 城市 |
| company_id | INT | 投资顾问ID |
| advisor | STRING | 投资顾问 |
| company_id2 | INT | 基金管理人公司id |
| advisor2 | STRING | 基金管理人名称 |
| manager_ids | STRING | 对应系统的mangaerid |
| managers_name | STRING | 私募网管理人名称 |
| mandator_name | STRING | 托管人名称 |
| inception_date | DATE | 成立日期 |
| inception_year | INT | 成立年份 |
| liquidate_date | DATE | 清算日期 |
| profession_background | INT | -1.其他 1.券商 2.公募 3.金融 4.媒体 5.海外 6.民间 7.期货 8.实业 9.学者 |
| price_date | DATE | 最新净值日期 |
| price_cw_nav | DECIMAL64(8) | 期末复权累计净值收益再投资 |
| price_nav | DECIMAL64(8) | 期末单位净值 |
| price_cnw | DECIMAL64(8) | 期末累计净值（分红不投资） |
| price_change | DECIMAL64(10) |  |
| manager_type | STRING | 管理类型 |
| puton_date | DATE | 备案时间 |
| fund_type | INT | 1.股权基金\r2.私募证券基金\r3.券商资管\r4.银行理财\r5.保险资管\r6.信托计划\r7.创投基金\r8.基金子公司\r9.期货资管\r10.其他基金 12.证券公司集合资管产品 13.信托登记产品 |
| fund_state | INT | 1.正在运作2.正常清算3.提前清算4.延期清算 5.投顾协议已终止 6.非正常清算 |
| cycle_type | CHAR | 净值更新周期类型 0：未知 1：日更新 2；周更新 3：月更新 |
| strategy_one | SYMBOL | 一级策略 |
| strategy_two | SYMBOL | 二级策略 |
| strategy_verify | CHAR | 策略是否确认：0-否 1- 是 |
| fund_index | INT | -1：无需基准对比 0：未知 大于0 对应的指数id |
| fund_idx_default | CHAR | 基金指数是否默认 |
| fund_index_name | STRING | 基准指数名称 |
| price_integrity | FLOAT | 净值完整度 |
| is_famous | CHAR | 是否热门：0-否；1-是 |
| amac_tips | STRING | 基金业协会特别提示（针对基金） |
| amac_update_time | DATE | 基金信息最后更新时间 |
| amac_scale | CHAR | 协会披露产品规模0-未知 1-小于500w 2-大于5000w |
| is_public | CHAR | 是否公开要素 1-公开 0-不公开 |
| active | CHAR | -4：新建在投产品或跟踪产品-3：未备案产品临时备案-2:重复数据临时下架 -1：下架 0：待处理 1：公开 2：公司内部产品（在运维新建的内部公司产品，不对外开放，仅内部可见） |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.company_price_funds

### 表: data
**表注释**: 团队净值-基金关系表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| fid | INT | funds表中基金id |
| fund_short_name | STRING | 基金简称 |
| uid | INT | 添加人用户id |
| company_id | INT | 团队公司id |
| active | CHAR | 0:不可用 1：可用 |
| from_team | CHAR | 是否有团队上传的净值 0-否 1-是 |
| from_email | CHAR | 是否有通过邮箱抓取的净值 0-否 1-是 |
| price_nav | DECIMAL64(8) | 期末单位净值 |
| price_cw_nav | DECIMAL64(8) | 期末复权累计净值收益再投资 |
| price_cnw | DECIMAL64(8) | 期末累计净值（分红不投资） |
| price_change | DECIMAL64(10) | 最新净值变动 |
| price_date | DATE | 最新净值日期 |
| cycle_type | CHAR | 净值更新周期类型 0：未知 1：日更新 2；周更新 3：月更新 |
| price_integrity | FLOAT | 净值完整度 |
| last_cash | DECIMAL64(4) | 期末现金余额(同步自估值&估值表) |
| sum_assets | DECIMAL64(4) | 期末总资产(同步自估值&估值表) |
| value_date | DATE | 期末最新估值或估值表日期 |
| debt | DECIMAL64(4) | 期末最新的负债 |
| product_share | DECIMAL64(2) | 实收资本(母基金份额) |
| lack_nav_sum | INT | 缺失净值数 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.email_valuation_rules

### 表: data
**表注释**: 邮件解析 - 各托管估值表解析规则表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| mandator_id | INT | 托管公司ID(对应mandator表ID)，0：默认规则，-1：信托产品默认规则 |
| code | STRING | 科目代码 |
| first_code | SYMBOL | 一级代码 |
| second_code | SYMBOL | 二级代码 |
| third_code | SYMBOL | 三级代码 |
| fourth_code | SYMBOL | 四级代码 |
| category | SHORT | 一级分类 |
| sub_category | SHORT | 二级分类 |
| remark | STRING | 备注 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.users

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| user_id | STRING |  |
| user_name | STRING |  |
| password_hash | STRING |  |
| user_role | STRING |  |
| session_token | STRING |  |
| other_info | STRING |  |
| created_at | DATETIME |  |
| updated_at | DATETIME |  |

---

## 数据库: /HFNS.valuation

### 表: data
**表注释**: 估值表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| vf_id | INT | 产品id |
| fund_id | INT | 基金id |
| value_date | SYMBOL | 估值日期 |
| nav | DECIMAL64(6) | 单位净值 |
| last_nav | DECIMAL64(6) | 昨日单位净值 |
| cumulative_nav | DECIMAL64(6) | 累计净值 |
| bank_cash | DECIMAL64(2) | 银行存款 |
| bank_ratio | DECIMAL32(6) | 存款占比 |
| product_cash | DECIMAL64(2) | 产品总金额(资产合计) |
| product_ratio | DECIMAL32(6) | 产品占比 |
| total_debt | DECIMAL64(2) | 负债合计 |
| debt_ratio | DECIMAL32(6) | 负债占比 |
| future_cash | DECIMAL64(2) | 期货保证金 （期货存出保证金103113） |
| future_ratio | DECIMAL32(6) | 保证金占比 |
| settlement_balance | DECIMAL64(2) | 期货结算备付金（102113） |
| settlement_ratio | DECIMAL32(6) | 备付金占比 |
| cumulative_income | DECIMAL64(2) | 累计实现收益 |
| stock_value | DECIMAL64(2) | 股票投资市值 |
| bond_balance | DECIMAL64(2) | 证券户资产 = 股票资产 + 券商存出保证金 + 券商清算保证金 |
| nav_rise_ratio | DECIMAL32(6) | 累计净值增长率（成立以来净值增长率） |
| nav_daily_rise_ratio | DECIMAL32(6) | 净值日增长率 |
| nav_weekly_rise_ratio | DECIMAL32(6) | 净值周增长率 |
| nav_monthly_rise_ratio | DECIMAL32(6) | 净值月增长率 |
| nav_quarterly_rise_ratio | DECIMAL32(6) | 净值季度增长率 |
| nav_annual_rise_ratio | DECIMAL32(6) | 净值年增长率 |
| file_path | STRING | 上传的报表地址（相对地址） |
| uid | INT | 上传报表的uid |
| active | CHAR | 0:下架 1: 正常 |
| is_sync | CHAR | 是否同步给估值 -1：有私募底层未匹配成功 0-否 1-是 |
| product_share | DECIMAL64(2) | 实收资本金额（数量） |
| unit_cost | FLOAT | 实收资本金额（单位成本） |
| product_cost | DECIMAL64(2) | 实收资本金额（成本） |
| from_type | CHAR | 来源：1-手动上传 2-托管邮箱 3-其他邮箱 |
| level | CHAR | 估值表级数 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_strategy

### 表: data
**表注释**: 基金策略

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| type | CHAR | 1私募基金策略、2公募基金策略 |
| strategy_name | STRING | 策略名称 |
| level | CHAR | 1 按照1级分类、2按2级分类 |
| pid | INT | 0为1级策略母级id |
| sort | INT | 排序字段 |
| active | CHAR |  |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.fof_product

### 表: data
**表注释**: FOF运维母基金表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| ftype | CHAR | 类型：1-私募平台，2-私募内部 |
| fid | INT | funds表对应基金id |
| fund_name | STRING | 基金简称 |
| agent | STRING | 经济端 |
| initial_date | DATE | 期初日期 |
| initial_debt | DECIMAL64(4) | 期初负债余额 |
| debt_factor | DECIMAL64(4) | 负债计提因子 |
| initial_cash | DECIMAL64(4) | 期初现金余额 |
| active | CHAR | 状态：1-正常 0-下架 |
| uid | INT | 创建人uid |
| init_shares | DECIMAL64(4) | 母基金期初份额 |
| init_bond | DECIMAL64(4) | 期初证券余额 |
| init_future | DECIMAL64(4) | 期初期货余额 |
| cycle_type | CHAR | 净值频率 1：日频 2：周频（废弃） |
| company_id | INT | 公司id |
| last_cash | DECIMAL64(4) | 期末现金余额 |
| last_bond | DECIMAL64(4) | 期末证券户余额 |
| last_future | DECIMAL64(4) | 期末期货户余额 |
| sum_assets | DECIMAL64(4) | 期末总资产 |
| last_price | DECIMAL64(8) | 期末净值（最新估值 |
| price_date | DATE | 最新净值日期 |
| update_type | CHAR | 期末数据更新来源：1-估值 2-估值表 |
| orderNum | CHAR | 排序 |
| local_cash | DECIMAL64(4) | 本地余额（最后一次查询的余额） |
| last_query_time | DATETIME | 上一次查询本地余额时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.manager_info

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| manager_id | SYMBOL | 管理人ID |
| manager_name | SYMBOL | 基金管理人全称 |
| artificial_person_name | SYMBOL | 法定代表人 |
| register_no | SYMBOL | 登记编号 |
| establish_date | DATE | 成立时间 |
| manager_has_product | BOOL | 是否有产品 |
| manager_url | SYMBOL | 管理人链接 |
| register_date | DATE | 登记时间 |
| register_address | SYMBOL | 注册地址 |
| register_province | SYMBOL | 注册省份 |
| register_city | SYMBOL | 注册城市 |
| reg_adr_agg | SYMBOL | 注册地址聚合 |
| office_adr_agg | SYMBOL | 办公地址聚合 |
| fund_count | INT | 在管基金数量 |
| paid_in_capital | DOUBLE | 实缴资本 |
| subscribed_capital | DOUBLE | 认缴资本 |
| has_special_tips | BOOL | 是否有提示信息 |
| has_credit_tips | BOOL | 是否有诚信信息 |
| reg_coordinate | SYMBOL | 注册地址坐标 |
| office_coordinate | SYMBOL | 办公地址坐标 |
| office_address | SYMBOL | 办公地址 |
| office_province | SYMBOL | 办公省份 |
| office_city | SYMBOL | 办公城市 |
| primary_invest_type | SYMBOL | 机构类型 |
| fund_type_scale_map | SYMBOL | 管理人规模区间 |
| member_type | SYMBOL | 会员类型 |
| org_form | SYMBOL | 机构组织形式 |

---

## 数据库: /HFNS.company_funds_data

### 表: data
**表注释**: 团队基金数据

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| type | CHAR | 类型：0-未知，1-人工，2-邮箱 |
| company_id | INT | 公司id |
| fid | INT | 基金id |
| uid | INT | 用户id |
| active | CHAR | 状态：0-下架，1-上架 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.contract

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| datetime | NANOTIMESTAMP |  |
| symbol | SYMBOL |  |
| exchange | SYMBOL |  |
| name | SYMBOL |  |
| shortname | SYMBOL |  |
| contract_type | SYMBOL |  |
| product | SYMBOL |  |
| pricetick | DOUBLE |  |
| size | DOUBLE |  |
| margin_ratio | DOUBLE |  |
| commission_num | DOUBLE |  |
| commission_unit | SYMBOL |  |
| list_date | NANOTIMESTAMP |  |
| last_date | NANOTIMESTAMP |  |

---

## 数据库: /HFNF.pf_company_amac_info

### 表: data
**表注释**: 私募 - AMAC管理人列表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| org_id | LONG | 机构ID，关联common_org.org_id |
| amac_id | STRING | AMAC协会ID |
| code | STRING | AMAC协会登记编号 |
| name | STRING | AMAC协会基金管理人全称 |
| url | STRING | AMAC协会基金管理人URL |
| register_date | DATETIME | 登记时间 |
| register_address | STRING | 注册地址 |
| register_province | STRING | 注册（省份） |
| register_city | STRING | 注册（城市） |
| reg_coordinate | STRING | 注册地坐标 |
| establish_date | DATETIME | 成立时间 |
| reg_adr_agg | STRING | 注册 |
| artificial_person_name | STRING | 法定代表人、执行事务合伙人（委派代表）姓名 |
| fund_count | INT | 在管基金数量 |
| has_credit_tips | CHAR | 是否有诚信信息:1是，0否 |
| has_special_tips | CHAR | 是否有提示信息:1是，0否 |
| manager_has_product | CHAR | 1是，0否 |
| member_type | CHAR | 会员类型：0非会员机构，1普通会员，2联席会员，3观察会员，4特别会员 |
| office_address | STRING | 办公地址 |
| office_adr_pro | STRING | 办公地址（省份） |
| office_adr_city | STRING | 办公地址（城市） |
| office_coordinate | STRING | 办公地坐标 |
| office_adr_agg | STRING | 办公 |
| paid_in_capital | INT |  |
| subscribed_capital | INT |  |
| primary_invest_type | CHAR | 机构类型：0未填报管理人类型，1私募证券投资基金管理人， 2私募股权、创业投资基金管理人，3其他私募投资基金管理人，4私募资产配置类管理人 |
| org_form | CHAR | 组织形式：0未知，1股份有限公司，2有限责任公司，3普通合伙企业，4有限合伙企业，5其他 |
| fund_type_scale_map | STRING |  |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.common_security

### 表: data
**表注释**: 证券代码表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| category | LONG | 证券类别，1-A股股票、2-公募基金、3-私募基金、4-指数 |
| security_id | LONG | 证券代码ID，固定格式：证券标识(2位) + 随机数(6位) |
| org_id | LONG | 机构ID，关联common_org.org_id |
| market | SHORT | 证券市场：1-上交所、2-深交所、3-北交所、9-其他 |
| code | SYMBOL | 证券代码，备注：最近一个转型的代码改为J |
| name | STRING | 中文全称 |
| short_name | STRING | 中文简称 |
| name_en | STRING | 英文全称 |
| short_name_en | STRING | 英文简称 |
| pinyin | STRING | 拼音简称 |
| extended_short_name | STRING | 扩展简称(备注名) |
| extended_pinyin | STRING | 扩展拼音简称 |
| listed_date | DATE | 上市日期 |
| listed_state | SHORT | 上市状态：1-上市，2-退市，3-暂停上市，9-其他 |
| listed_sector | SHORT | 上市板块，1-主板，2-中小企业板，3-三板，4-其他，5-大宗交易系统，6-创业板，7-科创板，8-北交所股票 |
| currency | SYMBOL | 货币，CNY-人民币、USD-美元 |
| isin | STRING | 国际证券识别码 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.fund_info_ext

### 表: data
**表注释**: 公募 - 基金扩展信息表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券代码ID，关联common_security.security_id |
| summary | STRING | 基金简介 |
| invest_orientation | STRING | 投资方向 |
| invest_target | STRING | 投资目标 |
| invest_field | STRING | 投资范围 |
| invest_area | STRING | QDII投资区域 |
| performance_benchmark | STRING | 业绩基准 |
| risk_returncharacter | STRING | 风险收益特征 |
| profit_distribution_rule | STRING | 收益分配原则 |
| lowest_sum_subll | DECIMAL64(6) | 最低认购金额下限(元) |
| lowest_sum_subscribing | STRING | 最低认购申购金额描述 |
| lowest_sum_purll | DECIMAL64(6) | 最低申购金额下限(元) |
| lowest_sum_redemption | DECIMAL64(6) | 最低赎回份额(份) |
| large_redemption_ratio | DECIMAL64(10) | 巨额赎回认定比例 |
| type_first_level | LONG | 最新一级分类ID，引用fund_type.first_level |
| type_first_level_name | STRING | 最新一级分类名称，引用fund_type.first_level_name |
| type_second_level | LONG | 最新二级分类ID，引用fund_type.second_level |
| type_second_level_name | STRING | 最新二级分类名称，引用fund_type.second_level_name |
| type_third_level | LONG | 最新三级分类ID，引用fund_type.third_level |
| type_third_level_name | STRING | 最新三级分类名称，引用fund_type.third_level_name |
| risk_level | SHORT | 最新风险等级，引用fund_risk_level.risk_level |
| redeem_status | LONG | 最新赎回状态，引用fund_status.redeem_status |
| applying_status | LONG | 最新申购状态，引用fund_status.applying_status |
| netvalue_end_date | DATE | 最新净值日期，引用fund_netvalue.end_date |
| netvalue_unit_nv | DECIMAL64(6) | 最新单位净值，引用fund_netvalue.unit_nv |
| netvalue_unit_nv_change | DECIMAL64(10) | 最新基金单位净值日增长率(%)，引用fund_netvalue.unit_nv_change |
| netvalue_acc_nv | DECIMAL64(6) | 最新累计净值，引用fund_netvalue.acc_nv |
| netvalue_acc_nv_change | DECIMAL64(10) | 最新基金累计净值日增长率(%)，引用fund_netvalue.acc_nv_change |
| netvalue_adj_nv | DECIMAL64(6) | 最新调整净值，引用fund_adj_netvalue.adj_nv |
| netvalue_adj_nv_change | DECIMAL64(10) | 最新基金调整净值日增长率(%)，引用fund_adj_netvalue.adj_nv_change |
| currency_daily_profit | DECIMAL64(6) | 每万份基金单位当日收益(元)，引用fund_currency_netvalue.daily_profit |
| currency_latest_weekly_yield | DECIMAL64(10) | 最近7日折算年收益率，引用fund_currency_netvalue.latest_weekly_yield |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.transaction_record

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| confirm_date | DATE | 交易确认日 |
| product_name | SYMBOL | 产品名称 |
| product_code | SYMBOL | 产品代码 |
| confirm_nav | DOUBLE | 确认净值 |
| change_share | DOUBLE | 份额变动 |
| balance | DOUBLE | 成交金额 |
| business_type | SYMBOL | 交易类型 |
| tag | SYMBOL | 标签 |
| comment | SYMBOL | 备注 |

---

## 数据库: /HFNF.pf_company_amac_detail_changes

### 表: data
**表注释**: 私募 - AMAC管理人详情变更记录（月频）

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| org_id | LONG | 机构ID，关联common_org.org_id |
| report_month | SYMBOL | 抓取月份 |
| credit_tips | STRING | 机构诚信信息 |
| special_tips | STRING | 机构提示信息 |
| full_employee_num | INT | 全职员工人数 |
| practitioners_num | INT | 取得基金从业人数 |
| capital_scale_min | INT | 管理规模最小值，单位：亿元 |
| capital_scale_max | INT | 管理规模最大值，单位：亿元 |
| major_issues | STRING | 管理人最近一次重大事项变更 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.fund_price

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| datetime | DATE |  |
| product_name | SYMBOL |  |
| product_code | SYMBOL |  |
| nav | DOUBLE |  |
| acc_nav | DOUBLE |  |
| virtual_nav | DOUBLE |  |
| holding_share | DOUBLE |  |
| total_share | DOUBLE |  |
| tag | SYMBOL |  |

---

## 数据库: /HFNS.funds_split

### 表: data
**表注释**: 基金拆分记录

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| fid | INT | funds表基金id |
| price_date | DATE |  |
| ratio | DECIMAL128(6) | 拆分比例 |
| company_id | INT | 公司id |
| from_type | INT | 1 :ms  2:私募牛 |
| active | INT | 1正常 0删除 |
| uid | INT |  |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.portfolio_configs

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| config_id | SYMBOL | 配置ID |
| config_name | STRING | 配置名称 |
| username | STRING | 用户名 |
| create_time | TIMESTAMP | 创建时间 |
| product_index | INT | 产品序号 |
| product_name | STRING | 产品名称 |
| product_code | SYMBOL | 产品代码 |
| data_source | SYMBOL | 数据来源 |
| weight | DOUBLE | 权重 |
| amount | DOUBLE | 金额 |
| start_buy_date | DATE | 开始买入时间 |

---

## 数据库: /HFNF.style_factor_netvalue

### 表: data
**表注释**: 市场 - 风格因子净值表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| style_factor_id | LONG | 因子ID |
| price_date | DATE | 净值日期 |
| price_nav | DECIMAL64(6) | 净值 |
| price_change | DECIMAL64(10) | 净值变动 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_bonus

### 表: data
**表注释**: 私募 - 基金分红

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| report_date | DATE | 分红日期 |
| bonus | DECIMAL64(6) | 每份分红 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.common_trading_day

### 表: data
**表注释**: 交易日历表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| market | SHORT | 证券市场：1-上交所、2-深交所、3-北交所 |
| trading_date | DATE | 交易日 |
| is_open | SHORT | 是否交易日：0-否、1-是 |
| is_week_end | SHORT | 是否周最后交易日：0-否、1-是 |
| is_month_end | SHORT | 是否月最后交易日：0-否、1-是 |
| is_quarter_end | SHORT | 是否季最后交易日：0-否、1-是 |
| is_year_end | SHORT | 是否年最后交易日：0-否、1-是 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.comparison_groups

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| group_id | SYMBOL | 组合ID |
| group_name | STRING | 组合名称 |
| username | STRING | 用户名 |
| create_time | TIMESTAMP | 创建时间 |
| product_index | INT | 产品序号 |
| product_name | STRING | 产品名称 |
| product_code | SYMBOL | 产品代码 |
| data_source | SYMBOL | 数据来源 |
| benchmark_code | SYMBOL | 基准指数代码 |
| start_date | STRING | 开始日期 |
| end_date | STRING | 结束日期 |

---

## 数据库: /HAZQ.loginlogs

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| id | INT |  |
| user_name | STRING |  |
| user_id | STRING |  |
| ip | STRING |  |
| browser | STRING |  |
| os | STRING |  |
| status | STRING |  |
| login_datetime | DATETIME |  |
| created_at | DATETIME |  |

---

## 数据库: /HFNF.email_future

### 表: data
**表注释**: 邮件解析 - 期货产品表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| future_id | SYMBOL | 期货简称 |
| future_name | SYMBOL | 期货名称 |
| market_id | INT | 期货市场 1：上海期货 2：大连 3：郑州 4:中金所 5：广州交易所 |
| cate_id | INT | 0:未知 1:黑色 2:有色 3:能化 4:农产 5:股指 6：国债  |
| unit_num | INT | 交易单位(每手数量) |
| last_date | SYMBOL |  |
| volume | DECIMAL64(2) | 成交量 |
| open_interest | DECIMAL64(2) | 持仓量 |
| open_interest_change | DECIMAL64(2) | 持仓变化 |
| active | SHORT |  |
| market_date | SYMBOL | 上市日期 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.fund_info

### 表: data
**表注释**: 公募 - 基金概况信息表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| org_id | LONG | 管理人机构ID，关联common_org.org_id |
| security_id | LONG | 证券代码ID，关联common_security.security_id |
| code | SYMBOL | 基金代码 |
| name | STRING | 中文全称 |
| short_name | STRING | 中文简称 |
| name_en | STRING | 英文全称 |
| short_name_en | STRING | 英文简称 |
| pinyin | STRING | 拼音简称 |
| extended_short_name | STRING | 扩展简称(备注名) |
| extended_pinyin | STRING | 扩展拼音简称 |
| front_code | SYMBOL | 前端申购代码 |
| back_code | SYMBOL | 后端申购代码 |
| market | SHORT | 场内申购证券市场：1-上交所、2-深交所、3-北交所、9-其他 |
| market_code | SYMBOL | 场内申购代码 |
| market_short_name | STRING | 场内市场中文简称 |
| market_profit_distri | CHAR | 场内收益分配方式, 1-现金分红，2-红利再投资，3-现金分红或红利再投资，4-不分配 |
| market_sector | SHORT | 上市板块，1-主板，2-中小企业板，3-三板，4-其他，5-大宗交易系统，6-创业板，7-科创板，8-北交所股票 |
| op_type | SHORT | 基金运作方式：1-契约型封闭式，2-开放式，3-LOF，4-ETF，6-创新型封闭式，7-开放式(带固定封闭期)，8-ETF联接基金 |
| nature | SHORT | 基金性质：1-常规基金，2-QDII基金，3-互认基金 |
| invest_style | SHORT | 基金投资风格：1-普通股票型，2-指数型，3-配置型，4-货币市场，5-积极债券型，6-债券型，7-普通债券型，8-短债型，9-保本型，10-积极配置型，11-保守混合型，12-偏股型，13-偏债型，14-中短债型 |
| is_initiating_fund | CHAR | 是否为发起基金，1-是、0-否 |
| is_fof | CHAR | 是否为FOF基金，1-是、0-否 |
| is_pension_target | CHAR | 是否为养老金目标基金，1-是、0-否 |
| profit_distri | CHAR | 场外收益分配方式, 1-现金分红，2-红利再投资，3-现金分红或红利再投资，4-不分配 |
| float_type | CHAR | 发售方式: 1-场内，2-场外，3-场内和场外 |
| found_date | DATE | 成立日期 |
| found_size | DECIMAL64(6) | 成立规模(份) |
| listed_date | DATE | 上市日期 |
| clearing_date | DATE | 清算日期 |
| start_date | DATE | 存续开始日期 |
| end_date | DATE | 存续结束日期 |
| duration | DECIMAL64(2) | 存续期限(年) |
| trustee_org_id | LONG | 托管人机构ID，关联common_org.org_id |
| manager | STRING | 基金经理列表，多个用英文逗号隔开 |
| carry_over_type | INT | 货币基金收益分配方式(份额结转方式), 1-按日结转，30-按月结转，99-按期结转。如果该字段不为空，则表明是披露万份收益的  |
| carry_over_date | LONG | 货币基金结转日, 1-每月1日，2-每月2日，3-每月3日，4-每月4日，5-每月5日，6-每月6日等等 |
| confirmation_date | SHORT | 申赎确认日, 该字段的数值含义指的是T+n，1代表T+1,2代表T+2，以此类推。 |
| delivery_days | SHORT | 赎回款到账天数, 指一般基金的赎回款到账日。 |
| status | SHORT | 基金状态：1-上市，2-退市，3-暂停上市，9-其他 |
| is_valid | CHAR | 是否有效，0-无效，1-有效 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.valuation_rules

### 表: data
**表注释**: 各托管估值表解析规则

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | ID |
| mandator_id | INT | 托管公司ID(对应mandator表ID)，0：默认规则，-1：信托产品默认规则 |
| code | STRING | 科目代码 |
| first_code | SYMBOL | 一级代码 |
| second_code | SYMBOL | 二级代码 |
| third_code | SYMBOL | 三级代码 |
| fourth_code | SYMBOL | 四级代码 |
| category | SHORT | 一级分类 |
| sub_category | SHORT | 二级分类 |
| remark | STRING | 备注 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.company_price_scrap_logs

### 表: data
**表注释**: 邮件抓取记录表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 自增ID |
| cid | LONG | 公司ID |
| message_id | STRING | 消息ID MD5值 |
| from | STRING | 发送邮箱地址 |
| to | STRING | 接收邮箱地址 |
| send_time | DATETIME | 邮件发送时间，CST时区 |
| subject | STRING | 邮件主题 |
| file | STRING | 下载保存的邮件内容和附件文件，多个用逗号隔开 |
| filenames | STRING | 邮件附件文件名 |
| prices | STRING | 解析的Price列表，JSON格式 |
| is_success | CHAR | 是否处理成功，1是、0否 |
| virtual_prices | STRING | 虚拟净值 |
| is_virtual_success | CHAR |  |
| is_valuation_success | CHAR | 是否处理成功估值表 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.stock_data

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| date | DATE | 日期 |
| stock_code | SYMBOL | 股票代码 |
| stock_name | SYMBOL | 股票名称 |
| open_price | DOUBLE | 开盘价 |
| high_price | DOUBLE | 最高价 |
| low_price | DOUBLE | 最低价 |
| close_price | DOUBLE | 收盘价 |
| avg_price | DOUBLE | 均价 |
| change | DOUBLE | 涨跌 |
| change_ratio | DOUBLE | 涨跌幅 |
| limit_up_price | DOUBLE | 涨停价 |
| limit_down_price | DOUBLE | 跌停价 |
| volume | DOUBLE | 成交量 |
| amount | DOUBLE | 成交额 |
| turnover_ratio | DOUBLE | 换手率 |
| transaction_amount | DOUBLE | 成交笔数 |
| total_shares | DOUBLE | 总股本 |
| total_market_cap | DOUBLE | 总市值 |
| float_shares | DOUBLE | A股流通股本 |
| float_market_cap | DOUBLE | A股流通市值 |
| pe_ttm | DOUBLE | 市盈率TTM |
| pe | DOUBLE | 市盈率 |
| pb | DOUBLE | 市净率 |
| ps | DOUBLE | 市销率 |
| pcf | DOUBLE | 市现率 |
| trading_status | SYMBOL | 交易状态 |
| up_down_status | SYMBOL | 涨跌停状态 |
| valid_turnover | DOUBLE | 有效换手率 |
| adj_factor | DOUBLE | 后复权因子 |

---

## 数据库: /HFNF.pf_company_amac_detail

### 表: data
**表注释**: 私募 - AMAC管理人详情

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| org_id | LONG | 机构ID，关联common_org.org_id |
| name_en | STRING | 基金管理人全称（英文） |
| license_code | STRING | 组织机构代码 |
| reg_capital | DECIMAL64(2) | 注册资本，单位：万元 |
| reg_capital_currency | SYMBOL | 注册资本币种，CNY人民币，USD美元 |
| actual_capital | DECIMAL64(2) | 实缴资本，单位：万元 |
| actual_capital_currency | SYMBOL | 注册资本币种，CNY人民币，USD美元 |
| company_type | STRING | 企业性质 |
| business_type | STRING | 业务类型 |
| full_employee_num | INT | 全职员工人数 |
| practitioners_num | INT | 取得基金从业人数 |
| website | STRING | 机构网址 |
| match_flag | CHAR | 是否为符合提供投资建议条件的第三方机构 |
| capital_scale_min | INT | 管理规模最小值，单位：亿元 |
| capital_scale_max | INT | 管理规模最大值，单位：亿元 |
| last_updated_at | DATETIME | 机构最后更新时间 |
| member_detail | STRING | 会员信息 |
| actual_controller | STRING | 实际控制人信息 |
| credit_tips | STRING | 机构诚信信息 |
| special_tips | STRING | 机构提示信息 |
| legal_opinion | STRING | 法律意见书 |
| execs_detail | STRING | 高管信息 |
| relation_detail | STRING | 关联方信息（仅包含关联私募基金管理人） |
| promoters_detail | STRING | 出资人信息 |
| products_detail | STRING | 产品信息 |
| major_issues | STRING | 管理人最近一次重大事项变更 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_factor

### 表: data
**表注释**: 私募 - 基金因子表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| end_date | DATE | 净值日期 |
| cucmulativeReturn | FLOAT | 累计收益 |
| excessReturn | FLOAT | 超额收益 |
| ytdExcessReturn | FLOAT | 今年以来超额收益 |
| pastWeekExcessReturn | FLOAT | 近一周超额收益 |
| lastOneMonthExcessReturn | FLOAT | 近一个月超额收益 |
| lastThreeMonthExcessReturn | FLOAT | 近三个月超额收益 |
| lastSixMonthExcessReturn | FLOAT |  |
| lastOneYearExcessReturn | FLOAT |  |
| lastTwoYearExcessReturn | FLOAT |  |
| excessYearReturn | FLOAT | 超额年化收益 |
| ytdExcessYearReturn | FLOAT | 今年以来超额年化收益 |
| lastSixMonthExcessYearReturn | FLOAT |  |
| lastOneYearExcessYearReturn | FLOAT |  |
| lastTwoYearExcessYearReturn | FLOAT |  |
| lastOneWeekReturn | FLOAT | 上周收益 |
| pastWeekReturn | FLOAT | 近一周收益 |
| lastOneMonthReturn | FLOAT | 近一月收益 |
| yearReturn | FLOAT | 年化收益 |
| ytdYearReturn | FLOAT | 今年以来年化收益 |
| lastThreeMonthYearReturn | FLOAT | 三月以来年化收益 |
| lastSixMonthYearReturn | FLOAT | 六月以来年化收益 |
| lastOneYearYearReturn | FLOAT | 一年以来年化收益 |
| lastTwoYearYearReturn | FLOAT | 两年以来年化收益 |
| ytdReturn | FLOAT | 今年以来收益 |
| lastThreeMonthReturn | FLOAT | 三月以来收益 |
| lastSixMonthReturn | FLOAT | 六月以来收益 |
| lastOneYearReturn | FLOAT | 一年以来收益 |
| lastTwoYearReturn | FLOAT | 两年以来收益 |
| vol | FLOAT | 波动性 |
| ytdVol | FLOAT |  |
| lastSixMonthVol | FLOAT |  |
| lastOneYearVol | FLOAT |  |
| lastTwoYearVol | FLOAT |  |
| trackingError | FLOAT | 跟踪误差 |
| ytdTrackingError | FLOAT |  |
| lastSixMonthTrackingError | FLOAT |  |
| lastOneYearTrackingError | FLOAT |  |
| lastTwoYearTrackingError | FLOAT |  |
| informationRatio | FLOAT |  |
| ytdInformationRatio | FLOAT |  |
| lastSixMonthInformationRatio | FLOAT |  |
| lastOneYearInformationRatio | FLOAT |  |
| lastTwoYearInformationRatio | FLOAT |  |
| sharpeRatio | FLOAT | 夏普比率 |
| ytdSharpeRatio | FLOAT | 今年以来夏普 |
| lastSixMonthSharpeRatio | FLOAT | 六个月以来夏普 |
| lastOneYearSharpeRatio | FLOAT | 一年以来夏普 |
| lastTwoYearSharpeRatio | FLOAT | 两年以来夏普 |
| sortinoRatio | FLOAT | 索提诺比率 |
| ytdSortinoRatio | FLOAT |  |
| lastSixMonthSortinoRatio | FLOAT |  |
| lastOneYearSortinoRatio | FLOAT |  |
| lastTwoYearSortinoRatio | FLOAT |  |
| downsideStd | FLOAT | 下行标准差 |
| ytdDownsideStd | FLOAT |  |
| lastThreeMonthDownsideStd | FLOAT |  |
| lastSixMonthDownsideStd | FLOAT |  |
| lastOneYearDownsideStd | FLOAT |  |
| lastTwoYearDownsideStd | FLOAT |  |
| downsideDev | FLOAT | 下行风险 |
| ytdDownsideDev | FLOAT | 今年以来下行风险 |
| lastThreeMonthDownsideDev | FLOAT | 三个月以来下行风险 |
| lastSixMonthDownsideDev | FLOAT | 六个月以来下行风险 |
| lastOneYearDownsideDev | FLOAT | 一年以来下行风险 |
| lastTwoYearDownsideDev | FLOAT | 两年以来下行风险 |
| maxDrawdown | FLOAT | 最大回撤 |
| ytdMaxDrawdown | FLOAT | 今年以来最大回撤 |
| lastThreeMonthMaxDrawdown | FLOAT | 三个月以来最大回撤 |
| lastSixMonthMaxDrawdown | FLOAT | 六个月以来最大回撤 |
| lastOneYearMaxDrawdown | FLOAT | 一年以来最大回撤 |
| lastTwoYearMaxDrawdown | FLOAT | 两年以来最大回撤 |
| maxDrawdownDays | INT | 最大回撤回补期（天） |
| ytdMaxDrawdownDays | INT |  |
| lastSixMonthMaxDrawdownDays | INT |  |
| lastOneYearMaxDrawdownDays | INT |  |
| lastTwoYearMaxDrawdownDays | INT |  |
| cVaR | FLOAT | VaR 95% |
| ytdCVaR | FLOAT |  |
| lastSixMonthCVaR | FLOAT |  |
| lastOneYearCVaR | FLOAT |  |
| lastTwoYearCVaR | FLOAT |  |
| calmarRatio | FLOAT | 卡玛比率 |
| ytdCalmarRatio | FLOAT |  |
| lastSixMonthCalmarRatio | FLOAT |  |
| lastOneYearCalmarRatio | FLOAT |  |
| lastTwoYearCalmarRatio | FLOAT |  |
| alpha | FLOAT |  |
| ytdAlpha | FLOAT |  |
| lastSixMonthAlpha | FLOAT |  |
| lastOneYearAlpha | FLOAT |  |
| lastTwoYearAlpha | FLOAT |  |
| beta | FLOAT |  |
| ytdBeta | FLOAT |  |
| lastSixMonthBeta | FLOAT |  |
| lastOneYearBeta | FLOAT |  |
| lastTwoYearBeta | FLOAT |  |
| skew | FLOAT | 偏度 |
| ytdSkew | FLOAT |  |
| lastSixMonthSkew | FLOAT |  |
| lastOneYearSkew | FLOAT |  |
| lastTwoYearSkew | FLOAT |  |
| kurt | FLOAT | 峰度 |
| ytdKurt | FLOAT |  |
| lastSixMonthKurt | FLOAT |  |
| lastOneYearKurt | FLOAT |  |
| lastTwoYearKurt | FLOAT |  |
| positiveRatio | FLOAT | 盈利占比 |
| ytdPositiveRatio | FLOAT |  |
| lastSixMonthPositiveRatio | FLOAT |  |
| lastOneYearPositiveRatio | FLOAT |  |
| lastTwoYearPositiveRatio | FLOAT |  |
| excessVol | FLOAT | 超额波动率 |
| ytdExcessVol | FLOAT | 今年以来超额波动率 |
| lastSixMonthExcessVol | FLOAT | 近六个月超额波动率 |
| lastOneYearExcessVol | FLOAT | 近一年超额波动率 |
| lastTwoYearExcessVol | FLOAT | 近两年超额波动率 |
| excessSharpeRatio | FLOAT | 超额夏普 |
| ytdExcessSharpeRatio | FLOAT | 今年以来超额夏普 |
| lastSixMonthExcessSharpeRatio | FLOAT | 近六个月超额夏普 |
| lastOneYearExcessSharpeRatio | FLOAT | 近一年超额夏普 |
| lastTwoYearExcessSharpeRatio | FLOAT | 近两年超额夏普 |
| excessCalmarRatio | FLOAT | 超额卡玛 |
| ytdExcessCalmarRatio | FLOAT | 今年以来超额卡玛 |
| lastSixMonthExcessCalmarRatio | FLOAT | 近六个月超额卡玛 |
| lastOneYearExcessCalmarRatio | FLOAT | 近一年超额卡玛 |
| lastTwoYearExcessCalmarRatio | FLOAT | 近两年超额卡玛 |
| excessMaxDrawdown | FLOAT | 超额最大回撤 |
| ytdExcessMaxDrawdown | FLOAT | 今年以来超额最大回撤 |
| lastSixMonthExcessMaxDrawdown | FLOAT | 近六个月超额最大回撤 |
| lastOneYearExcessMaxDrawdown | FLOAT | 近一年超额最大回撤 |
| lastTwoYearExcessMaxDrawdown | FLOAT | 近两年超额最大回撤 |
| lastThreeYearReturn | FLOAT | 近三年收益 |
| lastThreeYearYearReturn | FLOAT |  |
| lastThreeYearVol | FLOAT |  |
| lastThreeYearTrackingError | FLOAT |  |
| lastThreeYearInformationRatio | FLOAT |  |
| lastThreeYearSharpeRatio | FLOAT |  |
| lastThreeYearSortinoRatio | FLOAT |  |
| lastThreeYearDownsideStd | FLOAT |  |
| lastThreeYearDownsideDev | FLOAT |  |
| lastThreeYearMaxDrawdown | FLOAT |  |
| lastThreeYearMaxDrawdownDays | FLOAT |  |
| lastThreeYearCVaR | FLOAT |  |
| lastThreeYearCalmarRatio | FLOAT |  |
| lastThreeYearExcessReturn | FLOAT |  |
| lastThreeYearExcessYearReturn | FLOAT |  |
| lastThreeYearAlpha | FLOAT |  |
| lastThreeYearBeta | FLOAT |  |
| lastThreeYearSkew | FLOAT |  |
| lastThreeYearKurt | FLOAT |  |
| lastThreeYearPositiveRatio | FLOAT |  |
| lastThreeYearExcessVol | FLOAT |  |
| lastThreeYearExcessSharpeRatio | FLOAT |  |
| lastThreeYearExcessCalmarRatio | FLOAT |  |
| lastThreeYearExcessMaxDrawdown | FLOAT |  |
| lastFiveYearReturn | FLOAT | 近五年收益 |
| lastFiveYearYearReturn | FLOAT |  |
| lastFiveYearVol | FLOAT |  |
| lastFiveYearTrackingError | FLOAT |  |
| lastFiveYearInformationRatio | FLOAT |  |
| lastFiveYearSharpeRatio | FLOAT |  |
| lastFiveYearSortinoRatio | FLOAT |  |
| lastFiveYearDownsideStd | FLOAT |  |
| lastFiveYearDownsideDev | FLOAT |  |
| lastFiveYearMaxDrawdown | FLOAT |  |
| lastFiveYearMaxDrawdownDays | FLOAT |  |
| lastFiveYearCVaR | FLOAT |  |
| lastFiveYearCalmarRatio | FLOAT |  |
| lastFiveYearExcessReturn | FLOAT |  |
| lastFiveYearExcessYearReturn | FLOAT |  |
| lastFiveYearAlpha | FLOAT |  |
| lastFiveYearBeta | FLOAT |  |
| lastFiveYearSkew | FLOAT |  |
| lastFiveYearKurt | FLOAT |  |
| lastFiveYearPositiveRatio | FLOAT |  |
| lastFiveYearExcessVol | FLOAT |  |
| lastFiveYearExcessSharpeRatio | FLOAT |  |
| lastFiveYearExcessCalmarRatio | FLOAT |  |
| lastFiveYearExcessMaxDrawdown | FLOAT |  |
| lastOneMonthYearReturn | FLOAT | 近一个月年化收益 |
| lastOneMonthVol | FLOAT |  |
| lastOneMonthTrackingError | FLOAT |  |
| lastOneMonthInformationRatio | FLOAT |  |
| lastOneMonthSharpeRatio | FLOAT |  |
| lastOneMonthSortinoRatio | FLOAT |  |
| lastOneMonthDownsideStd | FLOAT |  |
| lastOneMonthDownsideDev | FLOAT |  |
| lastOneMonthMaxDrawdown | FLOAT |  |
| lastOneMonthMaxDrawdownDays | FLOAT |  |
| lastOneMonthCVaR | FLOAT |  |
| lastOneMonthCalmarRatio | FLOAT |  |
| lastOneMonthExcessYearReturn | FLOAT |  |
| lastOneMonthAlpha | FLOAT |  |
| lastOneMonthBeta | FLOAT |  |
| lastOneMonthSkew | FLOAT |  |
| lastOneMonthKurt | FLOAT |  |
| lastOneMonthPositiveRatio | FLOAT |  |
| lastOneMonthExcessVol | FLOAT |  |
| lastOneMonthExcessSharpeRatio | FLOAT |  |
| lastOneMonthExcessCalmarRatio | FLOAT |  |
| lastOneMonthExcessMaxDrawdown | FLOAT |  |
| lastThreeMonthVol | FLOAT |  |
| lastThreeMonthTrackingError | FLOAT |  |
| lastThreeMonthInformationRatio | FLOAT |  |
| lastThreeMonthSharpeRatio | FLOAT |  |
| lastThreeMonthSortinoRatio | FLOAT |  |
| lastThreeMonthMaxDrawdownDays | FLOAT |  |
| lastThreeMonthCVaR | FLOAT |  |
| lastThreeMonthCalmarRatio | FLOAT |  |
| lastThreeMonthExcessYearReturn | FLOAT |  |
| lastThreeMonthAlpha | FLOAT |  |
| lastThreeMonthBeta | FLOAT |  |
| lastThreeMonthSkew | FLOAT |  |
| lastThreeMonthKurt | FLOAT |  |
| lastThreeMonthPositiveRatio | FLOAT |  |
| lastThreeMonthExcessVol | FLOAT |  |
| lastThreeMonthExcessSharpeRatio | FLOAT |  |
| lastThreeMonthExcessCalmarRatio | FLOAT |  |
| lastThreeMonthExcessMaxDrawdown | FLOAT |  |
| thisWeekReturn | FLOAT |  |
| thisWeekExcessReturn | FLOAT |  |
| thisMonthReturn | FLOAT |  |
| thisMonthExcessReturn | FLOAT |  |
| monthlyPositiveRatio | FLOAT |  |
| ytdMonthlyPositiveRatio | FLOAT |  |
| lastOneYearMonthlyPositiveRatio | FLOAT |  |
| lastTwoYearMonthlyPositiveRatio | FLOAT |  |
| lastThreeYearMonthlyPositiveRatio | FLOAT |  |
| lastFiveYearMonthlyPositiveRatio | FLOAT |  |
| lastOneYearScore | DECIMAL64(6) |  |
| lastTwoYearScore | DECIMAL64(6) |  |
| lastThreeYearScore | DECIMAL64(6) |  |
| lastFiveYearScore | DECIMAL64(6) |  |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.baroverview

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| symbol | SYMBOL |  |
| exchange | SYMBOL |  |
| interval | SYMBOL |  |
| count | INT |  |
| start | NANOTIMESTAMP |  |
| end | NANOTIMESTAMP |  |
| datetime | NANOTIMESTAMP |  |

---

## 数据库: /HFNS.codematch

### 表: data
**表注释**: 备案号匹配表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| code | SYMBOL | 匹配备案号 |
| fid | INT | 对应的基金产品id |
| fund_name | STRING | 基金名称 |
| register_number | SYMBOL | 匹配备案号 |
| active | SHORT | -1:删除 1:上架 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.feeds

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| id | SYMBOL | 公众号唯一标识ID |
| mp_name | SYMBOL | 公众号名称 |
| mp_cover | STRING | 公众号封面 |
| mp_intro | STRING | 公众号介绍 |
| status | INT | 状态 |
| sync_time | INT | 同步时间 |
| update_time | INT | 更新时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |
| faker_id | SYMBOL | 伪造ID |

---

## 数据库: /HAZQ.index_component

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| date | DATE | 日期 |
| index_code | SYMBOL | 指数代码 |
| index_name | SYMBOL | 指数名称 |
| stock_code | SYMBOL | 股票代码 |
| stock_name | SYMBOL | 股票名称 |

---

## 数据库: /HFNF.common_id_maps

### 表: data
**表注释**: ID映射为FOF99 ID

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| category | LONG | 类型：1 - 私募基金、2-私募管理人、3-私募基金经理、4 公募基金、5 - 公募基金公司、6 - 公募基金经理、7 - 指数 |
| object_id | LONG | 对象ID |
| fof99_id | LONG | FOF99 ID |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.funds

### 表: data
**表注释**: 私募基金表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| fund_name | STRING | 基金名称 |
| fund_short_name | STRING | 基金简称 |
| register_number | SYMBOL | 备案编码 |
| father_id | LONG | 母基金fid |
| fund_type | INT | 1.股权基金\r2.私募证券基金\r3.券商资管\r4.银行理财\r5.保险资管\r6.信托计划\r7.创投基金\r8.基金子公司\r9.期货资管\r10.其他基金 12.证券公司集合资管产品 13.信托登记产品 |
| strategy_one | SYMBOL | 一级策略 |
| strategy_two | SYMBOL | 二级策略 |
| company_id | INT | 0:系统 记录添加基金的公司id |
| advisor | STRING | 投资顾问 |
| mandator_name | STRING | 托管人名称 |
| inception_date | DATE | 成立日期 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_company_amac_cancelled

### 表: data
**表注释**: 私募 - AMAC管理人注销信息

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| org_id | LONG | 机构ID，关联common_org.org_id |
| name | STRING | AMAC协会基金管理人全称 |
| url | STRING | 投顾详情页面 |
| license_code | STRING | 组织机构代码 |
| cancel_date | DATE | 注销时间 |
| cancel_type | INT | 注销类型，100-主动注销、200-依公告注销、300-协会注销 |
| cancel_type_name | SYMBOL | 注销类型描述 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.email_valuation_asset_types

### 表: data
**表注释**: 邮件解析 - 估值表明细分类

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| parents_id | SHORT | 父类ID |
| type_name | SYMBOL | 分类名称 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.index_daily_quote

### 表: data
**表注释**: 指数 - 日线行情

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| date | DATE | 编制日期 |
| pre | DECIMAL64(6) | 昨收点数 |
| open | DECIMAL64(6) | 今开点数 |
| high | DECIMAL64(6) | 今最高点数 |
| low | DECIMAL64(6) | 今最低点数 |
| close | DECIMAL64(6) | 今收盘点数 |
| change | DECIMAL64(6) | 涨跌点数 |
| change_ratio | DECIMAL64(6) | 涨跌点数比例,单位(%) |
| volume | DECIMAL128(2) | 成交量，单位：(股) |
| amount | DECIMAL128(2) | 成交额，单位：(元) |
| is_checked | CHAR | 数据是否已校验，1(是)，0(否) |
| invalid_reason | STRING | 数据不合法的原因 |
| remark | STRING | 备注信息 |
| active | CHAR | 状态，1(启用)、0(禁用) |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.company_email_scrap_num

### 表: data
**表注释**: 团队邮件抓取统计数

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| cid | INT | 公司id |
| to_email | STRING | 团队邮箱 |
| total_num | INT | 解析总数 |
| success_num | INT | 解析成功数 |
| fail_num | INT | 解析失败数 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.bar

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| symbol | SYMBOL |  |
| exchange | SYMBOL |  |
| datetime | NANOTIMESTAMP |  |
| interval | SYMBOL |  |
| volume | DOUBLE |  |
| turnover | DOUBLE |  |
| open_interest | DOUBLE |  |
| open_price | DOUBLE |  |
| high_price | DOUBLE |  |
| low_price | DOUBLE |  |
| close_price | DOUBLE |  |
| settle_price | DOUBLE |  |

---

## 数据库: /HFNF.pf_manager_experience

### 表: data
**表注释**: 私募 - 基金经理基金任职记录表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| person_id | LONG | 人员ID，关联common_person.person_id |
| security_id | LONG | 证券ID，关联common_security.security_id |
| name | STRING | 基金经理姓名 |
| begin_date | SYMBOL | 开始时间 |
| end_date | SYMBOL | 结束时间 |
| is_represent | CHAR | 是否为代表基金，0不是、1是 |
| begin_price | DECIMAL64(6) | 任职起始日净值 |
| best_return | DECIMAL64(6) | 任职区间收益(%) |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.email_fof_name2ids

### 表: data
**表注释**: 邮件抓取虚拟净值母基金名称到ID映射关系表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| type | CHAR | 类型：1-FOF匹配，2-累计=单位，3-分级产品 |
| title | STRING | 要匹配的文本 |
| fof_company_id | INT | 匹配的 FOF 公司 ID |
| fof_fund_name | STRING | 匹配的FOF母基金名 |
| fof_fund_id | LONG | 匹配的FOF母基金ID |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.articles

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| id | SYMBOL | 文章唯一标识ID |
| mp_id | SYMBOL | 公众号ID |
| title | STRING | 文章标题 |
| pic_url | STRING | 文章封面图片URL |
| url | STRING | 文章链接URL |
| description | STRING | 文章描述/摘要 |
| status | INT | 文章状态 |
| publish_time | INT | 发布时间戳 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |
| is_export | INT | 是否已导出 |
| is_read | INT | 是否已读 |
| content | STRING | 文章完整内容 |

---

## 数据库: /HFNS.valueinfo_match_log

### 表: data
**表注释**: 估值底层匹配修改日志

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| vf_id | INT | 产品id(fundanaly的id) |
| origin_fund_id | INT | 原底层基金id |
| title | STRING | 估值表中条目的title |
| new_fund_id | INT | 新匹配基金id |
| fund_short_name | STRING | 新匹配基金简称 |
| uid | INT | 修改匹配的用户id |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_company_info

### 表: data
**表注释**: 私募 - 管理人基础信息表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| org_id | LONG | 机构ID，关联common_org.org_id |
| fof99_id | LONG | FOF99 ID |
| manager_id | SYMBOL | 协会公司id |
| manager_url | STRING | 协会公司url |
| logo | STRING | 公司logo |
| register_code | SYMBOL | 登记编号 |
| code_number | SYMBOL | 组织机构代码 |
| register_date | SYMBOL | 登记时间 |
| found_date | SYMBOL | 成立时间 |
| register_address | STRING | 注册地址 |
| office_address | STRING | 办公地址 |
| register_capital | INT | 注册资本(万元)(人民币) |
| paid_capital | INT | 实缴资本(万元)(人民币) |
| nature | SYMBOL | 企业性质 |
| paid_ratio | FLOAT | 注册资本实缴比例 |
| main_type | STRING | 机构类型 |
| other_type | STRING | 业务类型 |
| numbers | INT | 员工人数 |
| site | STRING | 机构网址 |
| member | CHAR | 是否会员 0 否 1 是 |
| member_type | SYMBOL | 当前会员类型 |
| member_date | SYMBOL | 入会时间 |
| corporate | STRING | 法定代表人 |
| corporate_id | INT | 对应manager表id |
| update_date | SYMBOL | 机构信息最后更新时间 |
| team_info | STRING | 团队介绍 |
| invest_value | STRING | 投资理念 |
| invest_strategy | STRING | 投资策略 |
| brief | STRING | 公司简介 |
| fund_num | INT | 上架的基金数量 |
| strategy | STRING | 核心策略，多个逗号隔开（原公司策略） |
| fund_strategys | STRING | 旗下产品涉及策略 |
| represent_fund | STRING | 代表产品fid |
| is_famous | CHAR | 是否知名：0-否；1-是 |
| scale | STRING | 资产规模 |
| scale_issue | STRING | 自主发行规模(万) |
| scale_manage | STRING | 顾问管理规模(万) |
| scale_allocate | STRING | 资产配置规模(万) |
| response_info | STRING | 机构诚信信息 |
| advise_type | CHAR | 是否为符合提供投资建议条件的第三方机构 0-未知 1-是 2-否 |
| tags | STRING | 平台标签，逗号隔开 |
| key_strategys_rel | STRING | 代表产品策略id |
| fund_strategys_rel | STRING | 旗下产品策略id |
| active | CHAR | 状态 -1:下架 0:待定 1： 正常 2:曾备案，已注销 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_factor_annual

### 表: data
**表注释**: 私募 - 基金因子（年度）表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| year | SHORT | 年份 |
| cucmulativeReturn | FLOAT | 累计收益 |
| yearReturn | FLOAT | 年化收益 |
| excessReturn | FLOAT | 超额收益 |
| excessYearReturn | FLOAT | 超额年化收益 |
| vol | FLOAT | 波动性 |
| excessVol | FLOAT | 超额波动率 |
| sharpeRatio | FLOAT | 夏普比率 |
| excessSharpeRatio | FLOAT | 超额夏普 |
| calmarRatio | FLOAT | 卡玛比率 |
| excessCalmarRatio | FLOAT | 超额卡玛 |
| sortinoRatio | FLOAT | 索提诺比率 |
| downsideStd | FLOAT | 下行标准差 |
| downsideDev | FLOAT | 下行风险 |
| maxDrawdown | FLOAT | 最大回撤 |
| excessMaxDrawdown | FLOAT | 超额最大回撤 |
| maxDrawdownDays | INT | 最大回撤回补期（天） |
| alpha | FLOAT |  |
| beta | FLOAT |  |
| trackingError | FLOAT | 跟踪误差 |
| informationRatio | FLOAT |  |
| skew | FLOAT | 偏度 |
| kurt | FLOAT | 峰度 |
| cVaR | FLOAT | VaR 95% |
| positiveRatio | FLOAT | 盈利占比 |
| monthlyPositiveRatio | FLOAT | 月胜率 |
| score | DECIMAL64(6) |  |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.style_factor

### 表: data
**表注释**: 市场 - 风格因子表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| style_factor_id | LONG | 因子ID |
| category | LONG | 风格因子类型：1-期货(全部)，2-有色，3-能化，4-农产，5-黑色，6-股票CNE5，7-股票CNE6 8-期货商品 9-米筐股票CNE5 10-米筐股票CNE6 |
| name | STRING | 中文全称 |
| name_en | STRING | 英文全称 |
| price_date | DATE | 最新净值日期 |
| price_nav | DECIMAL64(6) | 最新净值 |
| price_change | DECIMAL64(10) | 净值变动 |
| active | CHAR | 状态 0:删除， 1正常 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.ai_analysis_log

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| page_name | SYMBOL | 页面名称 |
| model_provider | SYMBOL | 模型提供商 |
| request_content | STRING | 请求内容 |
| response_content | STRING | 响应内容 |
| token_info | STRING | Token使用信息 |
| analysis_time | TIMESTAMP | 分析时间 |

---

## 数据库: /HFNF.pf_fund_price

### 表: data
**表注释**: 私募 - 基金净值

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| price_date | DATE | 净值日期 |
| nav | DECIMAL64(8) | 单位净值 |
| cumulative_nav_withdrawal | DECIMAL64(8) | 累计净值(分红不投资) |
| cumulative_nav | DECIMAL64(8) | 累计复权净值(分红再投资) |
| price_change | DECIMAL64(10) | 净值变化（%） |
| active | CHAR | -2：平台净值下架，转到团队净值中 -1:团队净值披露给平台，待审核 0:不可用 1：可用（都展示） 2：对平台（mp）展示 3：对客户（u）展示 4：投递任务处理中 5：计算失败 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.company_price_emails

### 表: data
**表注释**: 抓取邮箱配置表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| cid | INT | 公司id |
| email | STRING | 团队净值邮箱 |
| psw | STRING | 邮箱密码加密串 |
| mail_protocol | CHAR | 邮箱协议 1-IMAP 2-POP |
| mail_server | STRING | 邮箱服务器 |
| mail_server_port | SHORT | 邮箱服务器端口 |
| is_ssl | CHAR | 是否使用ssl：1-是 0-否 |
| des | STRING | 备注 |
| active | CHAR | 状态 0-下架 1-正常 2-待处理 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.valueinfo

### 表: data
**表注释**: 估值表明细

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| vid | INT | 估值表id |
| vf_id | INT | 产品id |
| fund_id | INT | 私募基金id（funds）或期货id（future） |
| value_date | SYMBOL | 估值日期 |
| code | SYMBOL | 证券代码 |
| title | STRING | 产品名称 |
| market | CHAR | 证券市场 1：上海期货 2：大连 3：郑州 4:中金所 5:上交所 6：深交所7：创业板 8：港交所 9：新三板 10：北交所 11：科创板 12：广期所 |
| type | SHORT | 0:多头 1:空头 |
| asset_type | CHAR | 资产类型：simu.valuation_asset_types主键 |
| shares | DECIMAL64(2) | 份额数量 |
| nav_cost | DECIMAL64(2) | 单位成本 |
| cost | DECIMAL64(2) | 成本金额 |
| cost_ratio | DECIMAL32(6) | 成本占比 |
| nav | DECIMAL64(6) | 当前净值（市价or行情） |
| values | DECIMAL64(2) | 市值 |
| values_ratio | DECIMAL32(6) | 市值占比 |
| value_change | DECIMAL64(2) | 市值变化（估值增值=市值-成本） |
| suspend_info | STRING | 停牌信息 |
| active | CHAR | 0:下架 1: 正常 |
| sub_code | STRING | 上一级科目代码 |
| sub_title | STRING | 上一级科目名称 |
| strategy_one | SYMBOL | 一级策略 |
| strategy_two | SYMBOL | 二级策略 |
| level | CHAR | 第几级明细 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.fund_mandator

### 表: data
**表注释**: 产品与托管对应关系（特殊匹配）

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | ID |
| fund_id | LONG | 基金ID(对应funds表ID) |
| fund_name | STRING | 基金名称(对应funds表fund_name) |
| register_number | SYMBOL | 备案编码(对应funds表register_number) |
| mandator_id | LONG | 托管公司ID(对应mandator表ID) |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /orca_sys_db

### 表: data

**错误**: <Exception> in run: Server response: 'pt = loadTable("dfs:///orca_sys_db", "data") => getFileBlocksMeta on path '//orca_sys_db/data.tbl' failed, reason: path does not exist' script: 'pt = loadTable("dfs:///orca_sys_db", "data"); [schema(pt).colDefs, schema(pt).tableComment]'

---

## 数据库: /HFNS.fof_product_price

### 表: data
**表注释**: FOF运维-母基金估值

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| pid | INT | 在母基金表里的id |
| price_date | DATE | 估值日期 |
| nav | DECIMAL64(8) | 单位净值 |
| active | CHAR | 状态：1-正常 0-下架 |
| uid | INT | 用户id |
| state | CHAR | 是否确认估值 0-未确认 1-自动确认 2-人工确认3-来自估值表无需确认 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.trade_cal

### 表: data
**表注释**: 上交所交易日历

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| cal_date | SYMBOL | 日历日期 |
| is_open | CHAR | 是否交易 0休市 1交易 |
| is_week_end | CHAR | 是否周最后交易日，1是、0否 |
| is_month_end | CHAR | 是否月末最后交易日，1是、0否 |
| is_quarter_end | CHAR | 是否季度最后个交易日，1是、0否 |
| is_year_end | CHAR | 是否年最后交易日，1是、0否 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.company_price

### 表: data
**表注释**: 团队基金净值表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| fid | INT |  |
| nav | DECIMAL64(8) | 期末单位净值 |
| cumulative_nav_withdrawal | DECIMAL64(8) | 期末累计净值(分红不投资) |
| cumulative_nav | DECIMAL64(8) | 期末累计复权净值(分红再投资) |
| price_change | DECIMAL64(10) | 净值变化 |
| price_date | DATE | 净值日期 |
| active | CHAR | -1：从邮箱抓取无累计净值的记录0:不可用 1：可用 4：投递任务处理中 5：计算失败  |
| uid | INT | 记录上传净值的用户uid |
| company_id | INT |  |
| from_type | CHAR | 来源：1-火富牛绑定邮箱 2-平台上传 3-运维同步 4-来自托管 5-同步团队净值6-估值表上传 7-用户定义规则生成 8-私募大赛披露 9-price邮箱 10-API商城 (新来源不再在此表备注修改，详细看数据字典) |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_codematch

### 表: data
**表注释**: 私募 - 基金备案号匹配表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| fund_name | STRING | 基金名称 |
| code | SYMBOL | 匹配备案号 |
| register_number | SYMBOL | 匹配备案号 |
| active | SHORT | -1:删除 1:上架 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.common_org

### 表: data
**表注释**: 机构表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| category | LONG | 机构类别，1-A股上市公司，2-公募基金公司，3-私募基金管理人，4-指数公司，5-基金托管人、9-其他 |
| org_id | LONG | 机构ID |
| name | STRING | 中文全称 |
| short_name | STRING | 中文简称 |
| name_en | STRING | 英文全称 |
| short_name_en | STRING | 英文简称 |
| nature | STRING | 机构性质 |
| organization_number | STRING | 机构代码 |
| credit_code | STRING | 统一信用代码 |
| found_date | DATE | 成立日期 |
| maturity_end_date | DATE | 存续截止日期 |
| reg_capital | DECIMAL128(6) | 注册资本(元) |
| paid_capital | DECIMAL128(6) | 实收资本(元) |
| reg_address | STRING | 注册地址 |
| office_address | STRING | 办公地址 |
| legal_person | STRING | 法人代表 |
| general_manager | STRING | 总经理 |
| inst_status | SHORT | 工商状态：1-运行，2-注销，3-吊销，9-其他 |
| website | STRING | 官网URL |
| background | STRING | 背景介绍 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_amac_info

### 表: data
**表注释**: 私募 - AMAC产品信息表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| amac_id | STRING | AMAC协会ID |
| code | STRING | AMAC协会基金编号 |
| name | STRING | AMAC协会基金名称 |
| url | STRING | AMAC协会产品信息URL |
| inception_date | DATE | 成立时间 |
| liquidate_date | DATE | 清算时间 |
| puton_date | DATE | 备案时间 |
| puton_stage | CHAR | 备案阶段，0=未知，1=暂行办法实施前成立，2=暂行办法实施后成立 |
| fund_type | STRING | 基金类型 |
| currency | STRING | 币种 |
| classified | CHAR | 是否分级，0=是，1=否 |
| manager_type | STRING | 管理类型 |
| advisor_id | STRING | AMAC基金投顾ID |
| advisor | STRING | 基金投顾 |
| advisor_url | STRING | AMAC投顾URL |
| manager_id | STRING | AMAC基金管理人ID |
| manager | STRING | 基金管理人 |
| manager_url | STRING | AMAC管理人URL |
| mandator_id | STRING | AMAC托管人ID |
| mandator | STRING | 托管人 |
| mandator_url | STRING | AMAC管理人URL |
| invest_type | STRING | 投资类型 |
| amac_update_date | DATE | AMAC最后更新时间 |
| amac_tips | STRING | AMAC特别提示 |
| working_state | STRING | 运作状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.job

### 表: data
**表注释**: 任务表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| type | CHAR | 任务类型 1-计算组合净值 2-重算平台&团队复权净值 3-全量重新计算牛牛私募指数 4-私有净值计算复权 5-自建基金计算复权， 6-内部基金计算复权 7-理财师计算客户组合净值 8-自定义报告计算指 |
| name | STRING | 任务名，便于查看 |
| params | STRING | 任务执行参数 json字符串 |
| status | CHAR | 任务状态：0：已投递，待执行 1：执行中 -1：取消执行 2：执行成功 -2：执行失败 |
| error | STRING | 执行错误信息 |
| relate_id | INT | 关联id，避免重复执行 |
| uid | INT | 操作人uid |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.fof_property

### 表: data
**表注释**: FOF运维-母基金资产表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| pid | INT | 母基金表id |
| trade_date | DATE | 底层净值维护的日期 |
| subfunds_assets | DECIMAL64(4) | 私募底层持仓资产 |
| debt | DECIMAL64(4) | 负债 |
| cash_equivalent | DECIMAL64(4) | 现金等价物 |
| shares | DECIMAL64(4) | 母基金份额(实收资本) |
| bond_balance | DECIMAL64(4) | 证券户余额 |
| future_balance | DECIMAL64(4) | 期货户余额 |
| cash_balance | DECIMAL64(4) | 托管户现金余额 |
| active | CHAR | 状态1-正常 0-删除 |
| state | CHAR | 状态：0-未审核 1-已审核 2-来自估值表无需审核 |
| other_assets | DECIMAL64(4) | 其它类资产 |
| gm_assets | DECIMAL64(4) | 公募底层资产 |
| liquidation_reserves | DECIMAL64(4) | 清算备付金 |
| refundable_deposits | DECIMAL64(4) | 存出保证金 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_info_ext

### 表: data
**表注释**: 私募 - 基金扩展信息

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| fund_type_investment_way | STRING | 是否是母子基金 |
| fee_trust | STRING | 托管外包费 |
| fee_manage | STRING | 管理费（管理费说明） |
| fee_manage_rate | DECIMAL64(4) | 管理费率2%填0.02 |
| fee_redeem | STRING | 赎回费率 |
| fee_pay | STRING | 业绩报酬 |
| fee_subscription | STRING | 认购费率 |
| fee_purchase | STRING | 申购费率 |
| risk_income_character | STRING | 风险收益特征 |
| income_distribution | STRING | 分红条款 |
| orientation | STRING | 投资方向 |
| instruction | STRING | 简介 |
| investment_idea | STRING | 投资理念 |
| investment_restriction | STRING | 投资限制 |
| investment_target | STRING | 投资目标 |
| investment_strategy | STRING | 投资策略 |
| investment_range | STRING | 投资范围 |
| investment_region | CHAR | 投资区域：1-国内市场 2-海外市场 |
| asset_allocation | STRING | 资产比例 |
| comparison_datum | STRING | 业绩基准 |
| financing_cost | STRING | 优先级利息 |
| issuing_scale | STRING | 发行规模 |
| real_financing_scale | STRING | 实际发行规模 |
| total_financing_scale | STRING | 总规模 |
| is_paied | STRING | 是否扣完业绩报酬 |
| mini_amount | FLOAT | 最低认购/申购金额（万） |
| add_amount | STRING | 追加认购/申购金额（追加说明） |
| duration | STRING | 预计存续期限 |
| operate_way | CHAR | 运作方式 0-未知 1-开放式 2-封闭式 |
| closed_period | STRING | 封闭期 |
| open_day | STRING | 开放日 |
| has_precautious_line | CHAR | 是否设置预警线 1-是 0-否 |
| precautious_line | FLOAT | 预警线 |
| has_stop_line | CHAR | 是否设置止损线 1-是 0-否 |
| stop_line | FLOAT | 止损线 |
| fee_admin_service | STRING | 行政外包服务费 |
| last_time | DATETIME | 最新开放日 |
| is_temporary_open | CHAR | 是否可临开： 1-是（全选可临开申购和可临开赎回） 0-否 2-可临开申购 3-可临开赎回 |
| pay_type | CHAR | 业绩报酬计提方式：1-固定比例 2-按年化收益梯度 3-按超额年化收益梯度4-按计提基准计提 |
| pay_ratio | FLOAT | 业绩报酬type为1时，填写计提比例，%前的数字 |
| pay_refer_ratio | FLOAT | pay_type=4时 计提基准传%前的数字 |
| pay_gradient | STRING | 业绩报酬计提梯度 json [{"gte":0, "lt":50,"ratio":1},{"gte":50, "lt":80,"ratio":1.5}] |
| pay_refer_index | INT | pay_type为3时，填写基准指数 |
| lockup_period_des | STRING | 锁定期说明 |
| operation_date | DATE | 运作日期 |
| price_cycle | CHAR | 净值披露频率 -1 不展示 1-日频（全部展示）2-周频3-月频 |
| price_cycle_config | STRING | price_cycle为2或3时，填写净值展示设置，{"fixed_day": 5, "trading_day":"prev","last_day": 0} |
| abstract | STRING | 摘要 |
| expiry_date | DATE | 到期日 |
| risk_rate | CHAR | 产品风险评级 |
| currency | CHAR | 币种 1-人民币 2-港币 3-美元 |
| structured | CHAR | 是否结构化产品 1:是 2:否 |
| structure_description | STRING | 结构说明 |
| close_period_month | CHAR | 封闭期月数 |
| raise_begin_date | DATE | 募集开始日期 |
| raise_end_date | DATE | 募集结束日期 |
| huge_redemption | CHAR | 巨额赎回 1-是 2-否 |
| huge_redemption_num | FLOAT | 巨额赎回数值 |
| warning_remark | STRING | 预警线说明 |
| prevent_losses_remark | STRING | 止损线说明 |
| outsourced_agency_name | STRING | 外包机构 |
| sales_rate | STRING | 销售费 |
| explain_reason | STRING | 投顾费费用说明 |
| other_fee | STRING | 其他费用 |
| dividend_method | CHAR | 分红方式 1 现金分红 2 红利再投资 3 投资者意愿 4 待红利再投资 5 不分红 |
| performance_rate_time_point | STRING | 业绩报酬计提时点 |
| performance_rate_fixed_time | DATE | 业绩报酬固定计提日期 |
| meta_data | STRING | 元数据KV, JSON格式 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.email_mandator

### 表: data
**表注释**: 邮件解析 - 托管公司表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| mandator_name | STRING | 托管公司名称 |
| mandator_short_name | STRING | 托管公司简称 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_amac_detail_changes

### 表: data
**表注释**: 私募 - AMAC信息披露变更表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| report_month | SYMBOL | 更新月份，格式: YYYYMM |
| amac_tips | STRING | AMAC特别提示 |
| year_report | SYMBOL | 年报披露信息，格式：应披露数|按时披露数|未披露数 |
| half_year_report | SYMBOL | 半年报披露信息，格式：应披露数|按时披露数|未披露数 |
| quarter_report | SYMBOL | 季报披露信息，格式：应披露数|按时披露数|未披露数 |
| month_report | SYMBOL | 月报披露信息，格式：应披露数|按时披露数|未披露数 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_split

### 表: data
**表注释**: 私募 - 基金拆分

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| report_date | DATE | 拆分折算日 |
| ratio | DECIMAL64(10) | 拆分折算比例 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.mandator

### 表: data
**表注释**: 托管公司表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| mandator_name | STRING | 托管公司名称 |
| mandator_short_name | STRING | 托管公司简称 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HAZQ.product_label

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| product_code | SYMBOL |  |
| product_name | SYMBOL |  |
| manager | SYMBOL |  |
| primary_strategy | SYMBOL |  |
| secondary_strategy | SYMBOL |  |
| tertiary_strategy | SYMBOL |  |
| comment1 | SYMBOL |  |
| comment2 | SYMBOL |  |
| comment3 | SYMBOL |  |

---

## 数据库: /HAZQ.factor_value

### 表: data

| name | typeString | comment |
| --- | --- | --- |
| datetime | DATE |  |
| factor_code | SYMBOL |  |
| factor_name | SYMBOL |  |
| underlying_code | SYMBOL |  |
| underlying_name | SYMBOL |  |
| value | DOUBLE |  |

---

## 数据库: /HFNS.fundanaly

### 表: data
**表注释**: 产品分析表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| fund_id | LONG | 基金id |
| fund_name | STRING | 产品名称 |
| fund_cid | INT | 基金所属公司id（取在投产品时排除公司产品） |
| uid | INT | 创建人的用户id |
| company_id | INT | 所属公司id |
| active | CHAR | 0:删除 1：正常 2：测试范例 |
| value_start_time | DATETIME | 估值表或结算单 起始时间 |
| value_end_time | DATETIME | 估值表或结算单 结束时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.email_fof_name2ids

### 表: data
**表注释**: 邮件解析 - 基金名称到ID映射关系表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| type | CHAR | 类型：1-FOF匹配，2-累计=单位，3-分级产品 |
| title | STRING | 要匹配的文本 |
| fof_company_id | INT | 匹配的 FOF 公司 ID |
| fof_fund_name | STRING | 匹配的FOF母基金名 |
| fof_fund_id | LONG | 匹配的FOF母基金ID |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.company_ta_account

### 表: data
**表注释**: 团队TA账号-母基金关联表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| account_no | SYMBOL | TA账号 |
| account_name | STRING | TA账号名称 |
| fid | INT | 通过账号名称匹配到的基金id（账号名称为机构，即直投填0） |
| company_id | INT | 拥有邮箱的公司id |
| from_type | CHAR | 来源：1-邮箱 2-手动 |
| active | CHAR | 状态：1-正常 0-下架 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.email_fund_mandator

### 表: data
**表注释**: 邮件解析 - 产品与托管对应关系（特殊匹配）表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| fund_id | LONG | 基金ID(对应funds表ID) |
| fund_name | STRING | 基金名称(对应funds表fund_name) |
| register_number | SYMBOL | 备案编码(对应funds表register_number) |
| mandator_id | LONG | 托管公司ID(对应mandator表ID) |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_manager_resume

### 表: data
**表注释**: 私募 - 基金经理从业信息表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| person_id | LONG | 人员ID，关联common_person.person_id |
| name | STRING | 基金经理姓名 |
| begin_date | SYMBOL | 开始时间 |
| end_date | SYMBOL | 结束时间 |
| title | STRING | 职称 |
| work_unit | STRING | 单位 |
| dept | STRING | 任职部门 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNF.pf_fund_strategy_rel

### 表: data
**表注释**: 私募 - 基金策略关系

| name | typeString | comment |
| --- | --- | --- |
| id | LONG | 主键 |
| security_id | LONG | 证券ID，关联common_security.security_id |
| strategy_id | LONG | 策略ID |
| is_del | CHAR | 是否删除（0-否，1-是） |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.future

### 表: data
**表注释**: 期货产品表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| future_id | SYMBOL | 期货简称 |
| future_name | SYMBOL | 期货名称 |
| market_id | INT | 期货市场 1：上海期货 2：大连 3：郑州 4:中金所 5：广州交易所 |
| cate_id | INT | 0:未知 1:黑色 2:有色 3:能化 4:农产 5:股指 6：国债  |
| unit_num | INT | 交易单位(每手数量) |
| last_date | SYMBOL |  |
| volume | DECIMAL64(2) | 成交量 |
| open_interest | DECIMAL64(2) | 持仓量 |
| open_interest_change | DECIMAL64(2) | 持仓变化 |
| active | SHORT |  |
| market_date | SYMBOL | 上市日期 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.gm_fund

### 表: data
**表注释**: 公募基金表

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| fund_name | STRING | 基金名称 |
| fund_short_name | STRING | 基金简称 |
| register_number | SYMBOL | 基金代码 |
| fund_type | STRING | 基金类型 |
| fund_type2 | STRING | 基金类型 |
| company_id | INT | 基金的公司id |
| advisor | STRING | 基金的公司 |
| mandator_name | STRING | 托管人名称 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 数据库: /HFNS.valuation_parse_log

### 表: data
**表注释**: 估值表上传解析记录

| name | typeString | comment |
| --- | --- | --- |
| id | LONG |  |
| fa_id | INT | fundanaly的id |
| file_name | STRING | 上传文件原文件名 |
| file_path | STRING | 估值表文件路径 |
| company_id | INT | 公司id |
| uid | INT | 上传的用户id |
| is_success | CHAR | 解析是否成功 0：否 1：是 |
| reparse_vid | INT | 重新解析的估值表id |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---
