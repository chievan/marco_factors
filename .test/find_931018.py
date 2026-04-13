import dolphindb as ddb

s = ddb.session()
s.connect("106.54.219.69", 8848, "admin", "123456")

# Querying for 931018 and confirming H11008
script = """
t = select security_id, code, name from loadTable("dfs://HFNF.index_info", "data") where code in ['H11008', '931018'];
res = "";
for(row in t){
    res += string(row.security_id) + " | " + row.code + " | " + row.name + "\\n";
};
res;
"""
try:
    result = s.run(script)
    print("=== ID Lookup Results ===")
    print(result)
except Exception as e:
    print(f"Error: {e}")
