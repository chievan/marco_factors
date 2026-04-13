import dolphindb as ddb
import pandas as pd

def get_names():
    s = ddb.session()
    hosts = [("172.30.44.32", 8848), ("106.54.219.69", 8848)]
    connected = False
    for host, port in hosts:
        try:
            s.connect(host, port, "admin", "123456")
            connected = True
            break
        except:
            continue
    if not connected:
        print("Could not connect to DDB")
        return
    
    ids = [47989178, 48919110, 48488928, 45645208, 48714340, 41021909, 45128117, 45709958]
    ids_str = "[" + ",".join(map(str, ids)) + "]"
    q = f"select distinct security_id, fund_code, fund_name from loadTable('dfs://wind', 'index_quote') where security_id in {ids_str}"
    res = s.run(q)
    print(res)

if __name__ == "__main__":
    get_names()
