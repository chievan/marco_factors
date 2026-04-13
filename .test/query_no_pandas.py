import dolphindb as ddb

s = ddb.session()
s.connect("106.54.219.69", 8848, "admin", "123456")

script = """
target_ids = [49862409, 40525479, 48488928];
select security_id, code, name, short_name from loadTable("dfs://HFNF.index_info", "data") where security_id in target_ids
"""
# s.run(script) returns a pandas dataframe by default, which triggers the numpy error.
# We can use s.run(script, fetchSize=100) or similar, but the return type might still be problematic.
# Let's try to get it as a list of lists if possible, or just print within DDB.
s.run("print(select security_id, code, name, short_name from loadTable('dfs://HFNF.index_info', 'data') where security_id in [49862409, 40525479])")
print("Check console output above or run with redirected output.")
