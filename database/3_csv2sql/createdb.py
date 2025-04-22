import os
from datetime import datetime

def generate_sql_file():
    # 获取当前系统时间并格式化为 mmdd_hhmmss 格式
    current_time = datetime.now()
    formatted_time = current_time.strftime("%m%d_%H%M%S")
    
    # 定义数据库名称和文件名
    db_name = f"gym_{formatted_time}"
    file_name = f"{db_name}.sql"
    
    # SQL 文件的初始内容（删除、创建数据库）
    sql_content = f"""-- 删除已存在的数据库（如果存在）
DROP DATABASE IF EXISTS {db_name};

-- 创建新的数据库
CREATE DATABASE {db_name}
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_bin;

-- 切换到新创建的数据库
USE {db_name};

"""
    
    # 表定义部分，每段SQL前加注释说明，并在每段之间添加空白行
    tables_sql = """
-- 创建 Branch 表：存储健身房分店信息
CREATE TABLE Branch (
    branch_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    city VARCHAR(32),
    district VARCHAR(32),
    address VARCHAR(128)
);


-- 创建 Person 表：存储人员信息（会员、教练、员工、管理员等）
CREATE TABLE Person (
    person_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(32) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,
    role ENUM('member', 'coach', 'staff', 'admin') NOT NULL,
    first_name VARCHAR(32),
    last_name VARCHAR(32),
    gender ENUM('M','F','Other') DEFAULT 'Other',
    birthday DATE,
    phone VARCHAR(15),
    id_number VARCHAR(32),
    join_date DATE DEFAULT CURDATE(),
    branch_id INT,
    qualification_no VARCHAR(32),
    qualification_expiry DATE,
    specialty VARCHAR(128),
    position VARCHAR(32),
    FOREIGN KEY(branch_id) REFERENCES Branch(branch_id)
);


-- 创建 Equipment 表：存储健身器材信息
CREATE TABLE Equipment (
    equipment_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    quantity INT DEFAULT 1,
    status ENUM('normal', 'broken', 'maintenance') DEFAULT 'normal',
    branch_id INT NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);


-- 创建 Product 表：存储商品信息
CREATE TABLE Product (
    product_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(64),
    description TEXT,
    image VARCHAR(128),
    stock INT DEFAULT 0,
    branch_id INT,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);


-- 创建 Course 表：存储课程信息
CREATE TABLE Course (
    course_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(64),
    start_date DATE,
    end_date DATE,
    hours INT,
    coach_id INT,
    branch_id INT,
    location VARCHAR(64),
    fee DECIMAL(8,2),
    requirement VARCHAR(256),
    max_seats INT,
    img VARCHAR(128),
    FOREIGN KEY (coach_id) REFERENCES Person(person_id),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);


-- 创建 CourseEnrollment 表：存储课程报名信息
CREATE TABLE CourseEnrollment (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id VARCHAR(32),
    member_id INT,
    enroll_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(course_id) REFERENCES Course(course_id),
    FOREIGN KEY(member_id) REFERENCES Person(person_id),
    UNIQUE(course_id, member_id)
);


-- 创建 Purchase 表：存储购买记录（课程或商品）
CREATE TABLE Purchase (
    purchase_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    type ENUM('course', 'product'),
    ref_id VARCHAR(32),
    number INT DEFAULT 1,
    total_fee DECIMAL(8,2),
    purchase_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(member_id) REFERENCES Person(person_id)
);


-- 创建 LostAndFound 表：存储失物招领信息
CREATE TABLE LostAndFound (
    pick_id INT PRIMARY KEY AUTO_INCREMENT,
    pick_name VARCHAR(64) NOT NULL,
    pick_photo VARCHAR(128),
    pick_time DATETIME NOT NULL,
    pick_place VARCHAR(128) NOT NULL,
    description TEXT,
    registrant_username VARCHAR(32),
    is_claimed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (registrant_username) REFERENCES Person(username)
);
"""
    
    # 将表定义追加到初始内容中
    sql_content += tables_sql
    
    # 将内容写入到 .sql 文件中
    with open(file_name, "w", encoding="utf-8") as sql_file:
        sql_file.write(sql_content)
    
    print(f"SQL 文件已生成: {os.path.abspath(file_name)}")

if __name__ == "__main__":
    generate_sql_file()