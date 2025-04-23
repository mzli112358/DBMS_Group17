import os
import re
import csv
from datetime import datetime

# 全局变量：指定数据文件夹路径
DATA_FOLDER = "./data_new"

def parse_table_names(sql_content):
    """
    从 SQL 内容中提取表名并返回表名列表和计数。
    """
    # 使用正则表达式匹配 "CREATE TABLE 表名 (" 并提取表名
    table_pattern = r"CREATE TABLE (\w+) \("
    table_names = re.findall(table_pattern, sql_content)
    return table_names, len(table_names)

def check_csv_existence(table_names):
    """
    检查 DATA_FOLDER 中是否存在对应的小写表名 CSV 文件。
    返回一个二维数组，第一列是表名（小写），第二列是布尔值表示文件是否存在。
    """
    table_csv_status = []
    for table in table_names:
        lowercase_table = table.lower()
        csv_file_path = os.path.join(DATA_FOLDER, f"{lowercase_table}.csv")
        exists = os.path.isfile(csv_file_path)
        table_csv_status.append([lowercase_table, int(exists)])
    return table_csv_status

def generate_insert_statements(table_name, csv_file_path):
    """
    根据表名和对应的 CSV 文件生成 INSERT INTO 语句。
    """
    insert_statements = []
    
    # 打开 CSV 文件并读取数据
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # 第一行是表头
        insert_header = ", ".join(headers[1:])  # 跳过主键列（假设第一列是主键）
        
        # 构造 INSERT INTO 语句的开头部分
        insert_prefix = f"INSERT INTO {table_name}({insert_header}) VALUES\n"
        
        # 存储每一行的数据
        rows = []
        for row in reader:
            # 将每一行的数据用单引号包裹并拼接成 SQL 值格式
            values = ", ".join([f"'{value}'" for value in row[1:]])
            rows.append(f"({values})")
        
        # 拼接完整的 INSERT 语句
        insert_body = ",\n".join(rows)
        insert_statement = insert_prefix + insert_body + ";"
        insert_statements.append(insert_statement)
    
    return insert_statements

def aigc(filename, table_name):
    """
    处理单个 CSV 文件并生成对应的 INSERT INTO 语句。
    """
    csv_file_path = os.path.join(DATA_FOLDER, filename)
    if not os.path.isfile(csv_file_path):
        print(f"没有找到 {filename}")
        return []
    
    print(f"正在处理 {filename}...")
    return generate_insert_statements(table_name, csv_file_path)

def main():
    # 获取当前时间并生成数据库名称和 SQL 文件名
    current_time = datetime.now()
    formatted_time = current_time.strftime("%m%d_%H%M%S")
    db_name = f"gym_{formatted_time}"
    sql_file_name = f"{db_name}.sql"
    
    # 读取 tables_sql.sql 文件内容
    with open("tables_sql.sql", "r", encoding="utf-8") as sql_file:
        sql_content = sql_file.read()
    
    # 解析表名并计数
    table_names, table_count = parse_table_names(sql_content)
    print(f"共找到 {table_count} 个表: {table_names}")
    
    # 检查 CSV 文件是否存在
    table_csv_status = check_csv_existence(table_names)
    print(f"CSV 文件检查结果: {table_csv_status}")
    
    # 初始化最终的 SQL 内容
    final_sql_content = f"""-- 删除已存在的数据库（如果存在）
DROP DATABASE IF EXISTS {db_name};

-- 创建新的数据库
CREATE DATABASE {db_name}
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_bin;

-- 切换到新创建的数据库
USE {db_name};

"""
    final_sql_content += sql_content + "\n\n"
    
    # 遍历每个表，生成 INSERT INTO 语句
    for table_info in table_csv_status:
        table_name_lower, exists = table_info
        if not exists:
            print(f"没有找到 {table_name_lower}.csv")
            continue
        
        # 调用 aigc 函数生成 INSERT 语句
        insert_statements = aigc(f"{table_name_lower}.csv", table_name_lower)
        final_sql_content += "\n".join(insert_statements) + "\n\n"
    
    # 将最终内容写入 SQL 文件
    with open(sql_file_name, "w", encoding="utf-8") as output_file:
        output_file.write(final_sql_content)
    
    print(f"SQL 文件已生成: {os.path.abspath(sql_file_name)}")

if __name__ == "__main__":
    main()