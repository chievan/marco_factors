import dolphindb as ddb

s = ddb.session()
s.connect("106.54.219.69", 8848, "admin", "123456")

# Use run(script) but handle the output as a dictionary or string
# DDB Python API 'run' can return different things.
# If we run a print command, it goes to DDB server console unless we redirect.
# Better: use s.run(script) but select columns as vectors? No, that's still pandas.
# How about: select into a scalar string?

script = """
t = select security_id, code, name from loadTable("dfs://HFNF.index_info", "data") where name like "%中证企业债%" or name like "%中债综合财富%";
res = "";
for(row in t){
    res += string(row.security_id) + " | " + row.code + " | " + row.name + "\\n";
};
res;
"""
result = s.run(script)
print("=== Lookup Results ===")
print(result)
