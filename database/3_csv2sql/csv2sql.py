#------------------------
# 需要修改什么再运行：
# 1. 设置新库的名字（DB_GIVEN_NAME），应为日期，实际新库名字是 gym_{DB_GIVEN_NAME}_{FORMATTED_TIME}。
# 2. 确保建表文件路径（SQL_FILE_PATH）正确。
# 3. 确保 CSV 数据文件夹路径（CSV_FOLDER_PATH）正确。
# 4. 设置 SQL 输出文件夹的父文件夹路径（OUTPUT_FATHER_FOLDER）。
#------------------------

import os
import re
import csv
from datetime import datetime
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=True)

## 用户设置
DB_GIVEN_NAME = "0424"
SQL_FILE_PATH = r"database\3_csv2sql\create_table_0424_2300.sql"
CSV_FOLDER_PATH = r"database\2_data_0424_2300"
OUTPUT_FATHER_FOLDER = r"database"

## 代码自动化设置
CURRENT_TIME = datetime.now()
FORMATTED_TIME = CURRENT_TIME.strftime("%m%d_%H%M")  # 格式化时间
DB_NAME = f"gym_{DB_GIVEN_NAME}_generate_at_{FORMATTED_TIME}"  # 实际数据库名称
OUTPUT_FOLDER_PATH = os.path.join(OUTPUT_FATHER_FOLDER, f"4_{DB_NAME}")  # 统一输出文件夹路径

def generate_create_database_sql():
    """
    生成创建数据库的 SQL 内容。
    :return: 数据库名称和 SQL 内容
    """
    sql_content = f"""-- 删除已存在的数据库（如果存在）
DROP DATABASE IF EXISTS {DB_NAME};

-- 创建新的数据库
CREATE DATABASE {DB_NAME}
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_bin;

-- 切换到新创建的数据库
USE {DB_NAME};
"""
    return DB_NAME, sql_content

def extract_table_names(sql_file_path):
    """
    从 SQL 文件中提取所有表名。
    :param sql_file_path: SQL 文件路径
    :return: 表名列表
    """
    table_names = []
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        matches = re.findall(r'CREATE TABLE\s+(\w+)\s*\(', content, re.IGNORECASE)
        table_names.extend(matches)
    return table_names

def generate_insert_sql(table_name, csv_file_path, output_folder_path, i):
    """
    根据 CSV 文件生成 INSERT INTO SQL 语句。
    :param table_name: 表名
    :param csv_file_path: CSV 文件路径
    :param output_folder_path: 输出文件夹路径
    :param i: 序号，用于命名输出文件
    :return: 是否生成了有效数据
    """
    if not os.path.exists(csv_file_path):
        # 如果 CSV 文件不存在，生成空文件并写入注释
        empty_sql_file_path = os.path.join(output_folder_path, f"action3_{table_name}_EMPTY.sql")
        with open(empty_sql_file_path, 'w', encoding='utf-8') as empty_file:
            empty_file.write(f"-- 注释：此表有建表 SQL 代码，但没有对应的 CSV 数据表，无法生成 INSERT 语句。\n")
        return False

    # 读取 CSV 文件并生成 INSERT SQL
    insert_statements = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 获取列标题
        insert_header = f"INSERT INTO {table_name}({', '.join(headers)})\nVALUES\n"
        values = []
        for row in reader:
            formatted_row = [f"'{value}'" if value else 'NULL' for value in row]
            values.append(f"({', '.join(formatted_row)})")
        insert_values = ",\n".join(values)
        insert_statements.append(insert_header + insert_values + ";")

    # 保存生成的 SQL 文件
    output_sql_file_path = os.path.join(output_folder_path, f"action3_{table_name}.sql")
    with open(output_sql_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("\n".join(insert_statements))
    return True

def main():
    # 动作一：生成创建数据库的 SQL 文件
    print("动作一，建库代码生成.......")
    db_name, create_db_sql = generate_create_database_sql()

    # 构造输出文件名
    create_db_file_name = f"action1_create_database_{DB_NAME}.sql"
    create_db_file_path = os.path.join(OUTPUT_FOLDER_PATH, create_db_file_name)

    # 确保输出文件夹存在
    os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)

    # 将 SQL 内容写入文件
    with open(create_db_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(create_db_sql)
    print(f"成功，存放在 {create_db_file_path}")
    print()  # 空行

    # 动作二：复制建表 SQL 文件到输出文件夹
    print("动作二，建表代码生成.......")
    sql_file_name = os.path.basename(SQL_FILE_PATH)
    new_sql_file_name = f"action2_create_table_{os.path.splitext(sql_file_name)[0]}.sql"
    new_sql_file_path = os.path.join(OUTPUT_FOLDER_PATH, new_sql_file_name)

    # 复制 SQL 文件并重命名
    with open(SQL_FILE_PATH, 'r', encoding='utf-8') as src_file, \
         open(new_sql_file_path, 'w', encoding='utf-8') as dst_file:
        dst_file.write(src_file.read())
    print("识别原文件存在.......")
    print(f"成功，复制且重命名存放在 {new_sql_file_path}")
    print()  # 空行

    # 动作三：生成 INSERT SQL 文件
    print("动作三，insert语句生成")
    table_names = extract_table_names(SQL_FILE_PATH)
    print(f"提取到的表名: {table_names}")

    # 遍历表名并生成 SQL 文件
    for i, table_name in enumerate(table_names, start=1):
        csv_file_name = f"{table_name}.csv"
        csv_file_path = os.path.join(CSV_FOLDER_PATH, csv_file_name)

        if not os.path.exists(csv_file_path):
            # 如果 CSV 文件不存在，生成空文件
            warning_message = f"*** 警告: {csv_file_name} 文件不存在，跳过该表。 ***"
            print(Fore.RED + warning_message)  # 使用红色高亮显示警告信息
            generate_insert_sql(table_name, csv_file_path, OUTPUT_FOLDER_PATH, i)
        else:
            # 生成 INSERT SQL
            print(f"正在处理表: {table_name}")
            generate_insert_sql(table_name, csv_file_path, OUTPUT_FOLDER_PATH, i)

if __name__ == "__main__":
    main()