#!/usr/bin/env python3
"""
DolphinDB查询执行工具
用于执行 DolphinDB (DOS) 查询语句，保护输出上下文，支持双 IP 回退。
"""

import argparse
import sys
import os

def execute_query(query, output=None, format="csv"):
    import pandas as pd
    
    # Context Blowup Protection: 限制 DataFrame 打印行数，防止大表撑爆 LLM 窗口
    pd.options.display.max_rows = 50
    pd.options.display.max_columns = 20
    pd.options.display.width = 1000

    try:
        import dolphindb as ddb
        
        session = ddb.session()
        connected = False
        
        # 默认本地+云端两分支；可通过环境变量强制云端优先
        local_host = "172.30.44.32"
        cloud_host = "106.54.219.69"
        port = int(os.environ.get("DDB_PORT", "8848"))
        force_cloud = os.environ.get("DDB_FORCE_CLOUD", "0") == "1"
        preferred_host = os.environ.get("DDB_HOST")

        username = os.environ.get("DDB_USER", "admin")
        password = os.environ.get("DDB_PASS", "123456")

        if preferred_host:
            host_order = [preferred_host]
        elif force_cloud:
            host_order = [cloud_host, local_host]
        else:
            host_order = [local_host, cloud_host]

        for idx, host in enumerate(host_order):
            try:
                host_name = "云端" if host == cloud_host else "本地"
                print(f"尝试连接{host_name}数据库 {host}:{port}...")
                session.connect(host, port, username, password)
                session.run("1")
                connected = True
                print(f"✅ 成功连接到{host_name} DolphinDB。")
                break
            except Exception as e:
                if idx < len(host_order) - 1:
                    print(f"⚠️ 连接失败 ({str(e)})，尝试下一个地址...")
                else:
                    print(f"❌ 所有地址连接失败: {str(e)}")
                    return None

        print("正在执行查询...")
        result = session.run(query)

        # 转换为DataFrame
        if isinstance(result, pd.DataFrame):
            df = result
        else:
            try:
                df = pd.DataFrame(result)
            except:
                print(f"查询结果 (非表格): {result}")
                session.close()
                return result

        if output:
            if format == "csv":
                df.to_csv(output, index=False, encoding="utf-8-sig")
                print(f"✅ 结果已保存到: {output}")
            elif format == "json":
                df.to_json(output, orient="records", force_ascii=False, indent=2)
                print(f"✅ 结果已保存到: {output}")
            else:
                df.to_csv(output, index=False, encoding="utf-8-sig")
                print(f"✅ 结果已保存到: {output}")
        else:
            print("\n查询结果 (已开启保护截断, 最多显示50行):")
            print(df)
            print(f"\n✅ 真实总行数: {len(df)}")

        session.close()
        return df

    except ImportError:
        print("❌ 错误: 未安装 dolphindb 或 pandas")
        return None
    except Exception as e:
        print(f"❌ 查询执行失败: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description="执行DolphinDB查询")
    parser.add_argument("query", nargs="?", help="查询语句")
    parser.add_argument("--file", help="dos文件路径")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--format", choices=["table", "csv", "json"], default="csv", help="输出格式")

    args = parser.parse_args()

    # 获取查询语句
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ 错误: 文件不存在: {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            query = f.read()
    elif args.query:
        query = args.query
    else:
        print("❌ 错误: 请提供查询语句或dos文件")
        sys.exit(1)

    result = execute_query(query, args.output, args.format)
    if result is not None:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
