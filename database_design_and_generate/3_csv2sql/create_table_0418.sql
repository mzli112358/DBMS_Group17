CREATE TABLE Branch (
    branch_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    city VARCHAR(32),
    district VARCHAR(32),
    address VARCHAR(128)
);

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


CREATE TABLE Equipment (
    equipment_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    quantity INT DEFAULT 1,
    status ENUM('normal', 'broken', 'maintenance') DEFAULT 'normal',
    branch_id INT NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);


CREATE TABLE Product (
    product_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(64),
    description TEXT,
    image VARCHAR(128),
    stock INT DEFAULT 0 CHECK (stock >= 0),
    price INT NOT NULL DEFAULT 0.00 CHECK (price >= 0),
    branch_id INT,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

CREATE TABLE Course (
    course_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(64),
    start_date DATE,
    end_date DATE,
    start_time TIME,
    end_time TIME,
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

CREATE TABLE CourseEnrollment (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id VARCHAR(32),
    member_id INT,
    enroll_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(course_id) REFERENCES Course(course_id),
    FOREIGN KEY(member_id) REFERENCES Person(person_id),
    UNIQUE(course_id, member_id)
);

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

-- 周期课程模板表,新增,即排课规律
CREATE TABLE CourseTemplate (
    template_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64),
    coach_id INT,
    branch_id INT,
    location VARCHAR(64),
    weekly TINYINT,
    start_time TIME,
    end_time TIME,
    valid_from DATE,
    valid_to DATE,
    max_seats INT,
    fee DECIMAL(8,2),
    requirement VARCHAR(256),
    course_id VARCHAR(32),
    course_name VARCHAR(64),
    FOREIGN KEY (coach_id) REFERENCES Person(person_id),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- 周期课程实例表，新增，课程实例，是一天的单个课程的表
CREATE TABLE CourseInstance (
    course_instance_id VARCHAR(32) PRIMARY KEY,   
    course_name VARCHAR(64),                      -- 冗余存名称（非外键）
    template_id INT,                              -- 外键
    course_id VARCHAR(32),                        -- 外键，对应 Course.course_id
    start_datetime DATETIME,
    end_datetime DATETIME,
    status VARCHAR(16) DEFAULT 'present',

    FOREIGN KEY (course_id) REFERENCES Course(course_id),
    FOREIGN KEY (template_id) REFERENCES CourseTemplate(template_id)
);
