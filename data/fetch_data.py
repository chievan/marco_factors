import dolphindb as ddb
import pandas as pd
import os
import json

def fetch_data():
    s = ddb.session()
    # 加载外部配置以保护凭证
    config_path = "db_config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Missing {config_path}. Please create this file with your DDB credentials.")
    
    with open(config_path, "r", encoding="utf-8") as f:
        db_config = json.load(f)
        
    hosts = db_config.get("hosts", [("106.54.219.69", 8848)])
    user = db_config.get("user", "admin")
    pwd = db_config.get("password", "123456")

    connected = False
    for host_info in hosts:
        host, port = host_info[0], host_info[1]
        try:
            s.connect(host, port, user, pwd)
            print(f"✅ Connected to DolphinDB: {host}")
            connected = True
            break
        except: continue
    
    if not connected: raise ConnectionError("Failed to connect to DDB")

    # 1. 综合行情列表 (4类: 宏观代理, 投资资产, 评价基准)
    # 共 24 个 ID
    q_indices = [
        # --- 宏观/高频代理 (11) ---
        46111941, 44029654, 47887552, 49157014, 46632374, 
        44779723, 48488928, 48919110, 47989178, 42630518, 40485417,
        # --- 投资策略标的 (11) ---
        48333548, 48408839, 43494799, 43310702, 48585505, 49069575, 
        40998561, 49361940, 40553563, 42883138, 44238744,
        # --- 基准补充 (2) ---
        46800542, 47299187
    ]
    
    # 2. 宏观核心指标 (15个特征)
    f_codes = [
        "M002043802", "M001620538", "M001625520", "M002808931", "M002826730", "M002826865", 
        "L001619604", "M001625222", "M004891021", "S000055209", "DINI.FX", 
        "L002959791", "L001618296", "S002808935", "S005402539"
    ]
    
    print(f"📥 Fetching Master Data Pool: {len(q_indices)} indices and {len(f_codes)} macro factors...")
    
    script = f"""
    // 1. 行情数据
    q_table = loadTable("dfs://HFNF.index_daily_quote", "data");
    q_data = select date, string(security_id) as security_id, close from q_table 
             where security_id in {q_indices} and date >= 2018.01.01;
             
    // 2. 宏观数值
    f_table = loadTable("dfs://HAZQ.factor_value", "data");
    f_data = select datetime as date, string(factor_code) as security_id, value as close from f_table 
             where factor_code in {f_codes} and datetime >= 2018.01.01;
             
    // 3. 申万大/小盘 PE
    pe_data = select datetime as date, "PE_" + string(underlying_code) as security_id, value as close from f_table 
              where factor_code = "ths_pe_ttm_sr_index" and underlying_code in ["801811", "801813"]
              and datetime >= 2018.01.01;
              
    unionAll(q_data, f_data).unionAll(pe_data)
    """
    
    df = s.run(script)
    if not df.empty:
        df = df.drop_duplicates().sort_values(['security_id', 'date'])
        df.to_csv("data/full_macro_data.csv", index=False)
        
        # 4. 同步私有资产数据库 (仅保留 GTHT + Benchmarks)
        # 基准 ID 用于计算回测收益，必须包含在 private_fund_indices.csv 中
        asset_ids = [str(x) for x in [
            48333548, 48408839, 43494799, 43310702, 48585505, 49069575, 
            40998561, 49361940, 40553563, 42883138, 44238744, 46800542, 47299187
        ]]
        pdf = df[df['security_id'].isin(asset_ids)]
        pdf.to_csv("data/private_fund_indices.csv", index=False)
        
        print(f"📊 Global update successful. Total rows: {len(df)}")
        print(f"✅ Data fully synchronized in CSVs.")
    else:
        print("❌ Critical error: No data returned from DDB.")

if __name__ == "__main__":
    fetch_data()
