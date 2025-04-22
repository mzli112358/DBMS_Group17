DROP DATABASE IF EXISTS gym_0418;
CREATE DATABASE gym_0418
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_bin;
USE gym_0418;

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
    stock INT DEFAULT 0,
    branch_id INT,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

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


-- Test Data
INSERT INTO Branch(name, city, district, address) VALUES
('Headquarters Flagship Store', 'Beijing', 'Haidian', 'No.100 Zhichun Road'),
('Wangjing Branch', 'Beijing', 'Chaoyang', 'No.2 Fuan West Road'),
('Xian Greenland Branch', 'Xian', 'Gaoxin', 'No.75 Keji 2nd Road'),
('Shanghai Lujiazui Branch', 'Shanghai', 'Pudong', 'No.88 Century Avenue'),
('Guangzhou Tianhe Branch', 'Guangzhou', 'Tianhe', 'No.100 Tiyu West Road');

INSERT INTO Person(username, password, role, first_name, last_name, gender, birthday, phone, id_number, branch_id, qualification_no, qualification_expiry, specialty)
VALUES 
('admin', 'admin123', 'admin', 'Admin', 'User', 'M', '1990-01-01', '13800001111', '110101199001011234', 1, NULL, NULL, NULL),
('staff1','staff123','staff','frontdesk','frontdesk','F','2000-02-02','13100002121','110101200002021234',1, NULL, NULL, NULL),
('warehouse1','wh123','staff','warehouse','keeper','M','1997-12-06','13288889999','110101199712063456',1, NULL, NULL, NULL),
('coachA', 'coach123', 'coach', 'John', 'Doe', 'M', '1985-07-01', '13811112222', '110101198507013815', 1, 'COACH2024001', '2027-07-01', 'Yoga'),
('coachB', 'coach123', 'coach', 'Jane', 'Smith', 'F', '1992-03-06', '13988887777', '110101199203063318', 2, 'COACH2024002', '2028-12-31', 'Aerobics'),
('coachC', 'coach123', 'coach', 'Mike', 'Brown', 'M', '1988-05-15', '13766665555', '110101198805154321', 3, 'COACH2024003', '2029-05-15', 'Weightlifting'),
('coachD', 'coach123', 'coach', 'Emily', 'Davis', 'F', '1990-11-22', '13699998888', '110101199011225678', 4, 'COACH2024004', '2030-11-22', 'Pilates'),
('coachE', 'coach123', 'coach', 'Chris', 'Wilson', 'M', '1987-09-30', '13577776666', '110101198709309876', 5, 'COACH2024005', '2028-09-30', 'HIIT');

INSERT INTO Person(username, password, role, first_name, last_name, gender, birthday, phone, id_number, branch_id)
VALUES 
('mem01', 'mem123', 'member', 'Alice', 'Green', 'F', '2000-04-02', '18011112222', '110101200004021234', 1),
('mem02', 'mem123', 'member', 'Bob', 'White', 'M', '1995-10-10', '18099998888', '110101199510101234', 2),
('mem03', 'mem123', 'member', 'Charlie', 'Black', 'M', '1998-06-15', '18122223333', '110101199806154321', 3),
('mem04', 'mem123', 'member', 'David', 'Brown', 'M', '1992-02-20', '18244445555', '110101199202205678', 4),
('mem05', 'mem123', 'member', 'Eve', 'Gray', 'F', '1997-08-25', '18366667777', '110101199708259876', 5);

INSERT INTO Product(product_id, name, description, image, stock, branch_id) VALUES
('FOOD1001', 'Energy Bar', 'High-protein energy bar', 'bar.jpg', 100, 1),
('DRINK1001', 'Sports Drink', 'Electrolyte-rich sports drink', 'drink.jpg', 200, 1),
('SUPP1001', 'Protein Powder', 'Premium whey protein powder', 'protein.jpg', 50, 2),
('FOOD1002', 'Granola', 'Healthy granola snack', 'granola.jpg', 150, 2),
('DRINK1002', 'Hydration Drink', 'Fast hydration drink', 'hydration.jpg', 250, 3),
('SUPP1002', 'Creatine', 'Pure creatine supplement', 'creatine.jpg', 30, 3),
('FOOD1003', 'Trail Mix', 'Nut and dried fruit mix', 'trailmix.jpg', 120, 4),
('DRINK1003', 'Recovery Shake', 'Post-workout recovery shake', 'shake.jpg', 180, 4),
('SUPP1003', 'BCAA', 'Branched-chain amino acids', 'bcaa.jpg', 40, 5),
('FOOD1004', 'Oatmeal', 'Quick-cook oatmeal', 'oatmeal.jpg', 130, 5),
('DRINK1004', 'Energy Drink', 'Caffeinated energy drink', 'energydrink.jpg', 220, 1),
('SUPP1004', 'Multivitamin', 'Daily multivitamin supplement', 'multivitamin.jpg', 60, 2),
('FOOD1005', 'Rice Cake', 'Low-calorie rice cake', 'ricecake.jpg', 140, 3),
('DRINK1005', 'Coconut Water', 'Natural coconut water', 'coconut.jpg', 190, 4),
('SUPP1005', 'Fish Oil', 'Omega-3 fish oil capsules', 'fishoil.jpg', 50, 5);

INSERT INTO Course(course_id, name, start_date, end_date, hours, coach_id, branch_id, location, fee, requirement, max_seats, img)
VALUES
('YOGA1001', 'Basic Yoga', '2024-07-01', '2024-08-01', 16, 2, 1, 'Room A', 299.00, 'None', 20, 'yoga.jpg'),
('FIT1001', 'HIIT Training', '2024-07-10', '2024-09-01', 20, 3, 1, 'Room B', 399.00, 'Sportswear required', 21, 'hiit.jpg'),
('AEROBIC1001', 'Aerobic Fitness', '2024-07-15', '2024-08-25', 10, 3, 2, 'Room 401', 199.00, 'Bring your own mat', 18, 'aerobic.jpg'),
('PILATES1001', 'Pilates Class', '2024-08-01', '2024-09-15', 12, 5, 3, 'Room C', 250.00, 'Comfortable clothing', 15, 'pilates.jpg'),
('WEIGHT1001', 'Weightlifting', '2024-08-10', '2024-09-30', 15, 4, 4, 'Room D', 350.00, 'Gloves recommended', 12, 'weight.jpg'),
('ZUMBA1001', 'Zumba Dance', '2024-08-15', '2024-09-20', 8, 3, 5, 'Room E', 150.00, 'Dance shoes preferred', 25, 'zumba.jpg'),
('SPIN1001', 'Spin Cycling', '2024-09-01', '2024-10-01', 10, 2, 1, 'Room F', 200.00, 'Cycling shoes optional', 20, 'spin.jpg'),
('BOXING1001', 'Boxing Basics', '2024-09-10', '2024-10-15', 12, 4, 2, 'Room G', 300.00, 'Hand wraps required', 18, 'boxing.jpg'),
('STRETCH1001', 'Stretching Class', '2024-09-15', '2024-10-20', 6, 5, 3, 'Room H', 100.00, 'Loose clothing', 30, 'stretch.jpg'),
('CROSSFIT1001', 'CrossFit Training', '2024-10-01', '2024-11-01', 20, 3, 4, 'Room I', 400.00, 'Athletic wear', 15, 'crossfit.jpg'),
('BOOTCAMP1001', 'Bootcamp', '2024-10-10', '2024-11-15', 14, 4, 5, 'Room J', 250.00, 'Water bottle required', 22, 'bootcamp.jpg'),
('CYCLING1001', 'Indoor Cycling', '2024-10-15', '2024-11-20', 10, 2, 1, 'Room K', 180.00, 'Cycling shoes optional', 25, 'cycling.jpg'),
('BARRE1001', 'Barre Class', '2024-11-01', '2024-12-01', 12, 5, 2, 'Room L', 220.00, 'Comfortable clothing', 20, 'barre.jpg'),
('MEDITATION1001', 'Meditation', '2024-11-10', '2024-12-15', 8, 3, 3, 'Room M', 150.00, 'Quiet space', 30, 'meditation.jpg'),
('KICKBOXING1001', 'Kickboxing', '2024-11-15', '2024-12-20', 10, 4, 4, 'Room N', 280.00, 'Hand wraps required', 18, 'kickboxing.jpg');

INSERT INTO Purchase(member_id, type, ref_id, number, total_fee, purchase_time) VALUES
(1, 'product', 'DRINK1001', 5, 150.00, '2024-07-01 10:00:00'),
(1, 'product', 'FOOD1001', 3, 90.00, '2024-07-02 11:00:00'),
(2, 'product', 'SUPP1001', 2, 200.00, '2024-07-03 12:00:00'),
(3, 'product', 'DRINK1002', 4, 120.00, '2024-07-04 13:00:00'),
(4, 'product', 'FOOD1002', 6, 180.00, '2024-07-05 14:00:00'),
(5, 'product', 'SUPP1002', 1, 50.00, '2024-07-06 15:00:00'),
(2, 'product', 'DRINK1003', 2, 60.00, '2024-07-08 17:00:00'),
(3, 'product', 'FOOD1003', 4, 120.00, '2024-07-09 18:00:00'),
(4, 'product', 'SUPP1003', 3, 150.00, '2024-07-10 19:00:00'),
(5, 'product', 'DRINK1004', 5, 150.00, '2024-07-11 20:00:00'),
(1, 'product', 'FOOD1004', 2, 60.00, '2024-07-12 21:00:00'),
(2, 'product', 'SUPP1004', 1, 50.00, '2024-07-13 22:00:00'),
(3, 'product', 'DRINK1005', 3, 90.00, '2024-07-14 23:00:00'),
(4, 'product', 'FOOD1005', 4, 120.00, '2024-07-15 00:00:00'),
(5, 'product', 'SUPP1005', 2, 100.00, '2024-07-16 01:00:00'),
(1, 'product', 'DRINK1001', 6, 180.00, '2024-07-17 02:00:00'),
(2, 'product', 'FOOD1001', 5, 150.00, '2024-07-18 03:00:00'),
(3, 'product', 'SUPP1001', 3, 300.00, '2024-07-19 04:00:00'),
(4, 'product', 'DRINK1002', 7, 210.00, '2024-07-20 05:00:00'),
(5, 'product', 'FOOD1002', 8, 240.00, '2024-07-21 06:00:00'),
(1, 'product', 'SUPP1002', 2, 100.00, '2024-07-22 07:00:00'),
(3, 'product', 'DRINK1003', 4, 120.00, '2024-07-24 09:00:00'),
(4, 'product', 'FOOD1003', 5, 150.00, '2024-07-25 10:00:00'),
(5, 'product', 'SUPP1003', 6, 300.00, '2024-07-26 11:00:00'),
(1, 'product', 'DRINK1004', 3, 90.00, '2024-07-27 12:00:00'),
(2, 'product', 'FOOD1004', 2, 60.00, '2024-07-28 13:00:00'),
(3, 'product', 'SUPP1004', 1, 50.00, '2024-07-29 14:00:00'),
(4, 'product', 'DRINK1005', 5, 150.00, '2024-07-30 15:00:00'),
(5, 'product', 'FOOD1005', 4, 120.00, '2024-07-31 16:00:00'),
(1, 'product', 'SUPP1005', 3, 150.00, '2024-08-01 17:00:00'),
(2, 'product', 'DRINK1001', 4, 120.00, '2024-08-02 18:00:00'),
(3, 'product', 'FOOD1001', 6, 180.00, '2024-08-03 19:00:00'),
(4, 'product', 'SUPP1001', 2, 200.00, '2024-08-04 20:00:00'),
(5, 'product', 'DRINK1002', 5, 150.00, '2024-08-05 21:00:00'),
(1, 'product', 'FOOD1002', 7, 210.00, '2024-08-06 22:00:00'),
(2, 'product', 'SUPP1002', 3, 150.00, '2024-08-07 23:00:00'),
(4, 'product', 'DRINK1003', 6, 180.00, '2024-08-09 01:00:00'),
(5, 'product', 'FOOD1003', 8, 240.00, '2024-08-10 02:00:00'),
(1, 'product', 'SUPP1003', 4, 200.00, '2024-08-11 03:00:00'),
(2, 'product', 'DRINK1004', 7, 210.00, '2024-08-12 04:00:00'),
(3, 'product', 'FOOD1004', 9, 270.00, '2024-08-13 05:00:00'),
(4, 'product', 'SUPP1004', 5, 250.00, '2024-08-14 06:00:00'),
(5, 'product', 'DRINK1005', 8, 240.00, '2024-08-15 07:00:00'),
(1, 'product', 'FOOD1005', 10, 300.00, '2024-08-16 08:00:00'),
(2, 'product', 'SUPP1005', 6, 300.00, '2024-08-17 09:00:00'),
(3, 'product', 'DRINK1001', 9, 270.00, '2024-08-18 10:00:00'),
(4, 'product', 'FOOD1001', 11, 330.00, '2024-08-19 11:00:00'),
(5, 'product', 'SUPP1001', 7, 350.00, '2024-08-20 12:00:00'),
(1, 'product', 'DRINK1002', 10, 300.00, '2024-08-21 13:00:00'),
(2, 'product', 'FOOD1002', 12, 360.00, '2024-08-22 14:00:00'),
(3, 'product', 'SUPP1002', 8, 400.00, '2024-08-23 15:00:00'),
(5, 'product', 'DRINK1003', 11, 330.00, '2024-08-25 17:00:00'),
(1, 'product', 'FOOD1003', 13, 390.00, '2024-08-26 18:00:00'),
(2, 'product', 'SUPP1003', 9, 450.00, '2024-08-27 19:00:00'),
(3, 'product', 'DRINK1004', 12, 360.00, '2024-08-28 20:00:00'),
(4, 'product', 'FOOD1004', 14, 420.00, '2024-08-29 21:00:00'),
(5, 'product', 'SUPP1004', 10, 500.00, '2024-08-30 22:00:00'),
(1, 'product', 'DRINK1005', 13, 390.00, '2024-08-31 23:00:00'),
(2, 'product', 'FOOD1005', 15, 450.00, '2024-09-01 00:00:00'),
(3, 'product', 'SUPP1005', 11, 550.00, '2024-09-02 01:00:00'),
(4, 'product', 'DRINK1001', 14, 420.00, '2024-09-03 02:00:00'),
(5, 'product', 'FOOD1001', 16, 480.00, '2024-09-04 03:00:00'),
(1, 'product', 'SUPP1001', 12, 600.00, '2024-09-05 04:00:00'),
(2, 'product', 'DRINK1002', 15, 450.00, '2024-09-06 05:00:00'),
(3, 'product', 'FOOD1002', 17, 510.00, '2024-09-07 06:00:00'),
(4, 'product', 'SUPP1002', 13, 650.00, '2024-09-08 07:00:00'),
(1, 'product', 'DRINK1003', 16, 480.00, '2024-09-10 09:00:00'),
(2, 'product', 'FOOD1003', 18, 540.00, '2024-09-11 10:00:00'),
(3, 'product', 'SUPP1003', 14, 700.00, '2024-09-12 11:00:00'),
(4, 'product', 'DRINK1004', 17, 510.00, '2024-09-13 12:00:00'),
(5, 'product', 'FOOD1004', 19, 570.00, '2024-09-14 13:00:00'),
(1, 'product', 'SUPP1004', 15, 750.00, '2024-09-15 14:00:00'),
(2, 'product', 'DRINK1005', 18, 540.00, '2024-09-16 15:00:00'),
(3, 'product', 'FOOD1005', 20, 600.00, '2024-09-17 16:00:00'),
(4, 'product', 'SUPP1005', 16, 800.00, '2024-09-18 17:00:00'),
(5, 'product', 'DRINK1001', 19, 570.00, '2024-09-19 18:00:00'),
(1, 'product', 'FOOD1001', 21, 630.00, '2024-09-20 19:00:00'),
(2, 'product', 'SUPP1001', 17, 850.00, '2024-09-21 20:00:00'),
(3, 'product', 'DRINK1002', 20, 600.00, '2024-09-22 21:00:00'),
(4, 'product', 'FOOD1002', 22, 660.00, '2024-09-23 22:00:00'),
(5, 'product', 'SUPP1002', 18, 900.00, '2024-09-24 23:00:00'),
(2, 'product', 'DRINK1003', 21, 630.00, '2024-09-26 01:00:00'),
(3, 'product', 'FOOD1003', 23, 690.00, '2024-09-27 02:00:00'),
(4, 'product', 'SUPP1003', 19, 950.00, '2024-09-28 03:00:00'),
(5, 'product', 'DRINK1004', 22, 660.00, '2024-09-29 04:00:00'),
(1, 'product', 'FOOD1004', 24, 720.00, '2024-09-30 05:00:00'),
(2, 'product', 'SUPP1004', 20, 1000.00, '2024-10-01 06:00:00'),
(3, 'product', 'DRINK1005', 23, 690.00, '2024-10-02 07:00:00'),
(4, 'product', 'FOOD1005', 25, 750.00, '2024-10-03 08:00:00'),
(5, 'product', 'SUPP1005', 21, 1050.00, '2024-10-04 09:00:00'),
-- Alice (member_id = 1) 购买了多个课程
(1, 'course', 'FIT1001', 1, 399.00, '2024-07-08 10:30:00'),
(1, 'course', 'PILATES1001', 1, 250.00, '2024-07-20 14:45:00'),
-- Bob (member_id = 2) 购买了多个课程
(2, 'course', 'ZUMBA1001', 1, 150.00, '2024-08-02 09:15:00'),
(2, 'course', 'SPIN1001', 1, 200.00, '2024-08-28 16:20:00'),
-- Charlie (member_id = 3) 购买了多个课程
(3, 'course', 'WEIGHT1001', 1, 350.00, '2024-08-05 11:00:00'),
(3, 'course', 'CROSSFIT1001', 1, 400.00, '2024-09-25 13:50:00'),
-- David (member_id = 4) 购买了多个课程
(4, 'course', 'BOOTCAMP1001', 1, 250.00, '2024-10-02 08:45:00'),
(4, 'course', 'CYCLING1001', 1, 180.00, '2024-10-10 17:10:00'),
-- Eve (member_id = 5) 购买了多个课程
(5, 'course', 'BARRE1001', 1, 220.00, '2024-11-05 12:30:00'),
(5, 'course', 'MEDITATION1001', 1, 150.00, '2024-11-12 09:50:00');


-- Insert test data into Equipment table
-- Extended Test Data for Equipment Table
INSERT INTO Equipment (name, quantity, status, branch_id) VALUES
('Treadmill', 10, 'normal', 1),
('Stationary Bike', 8, 'maintenance', 1),
('Smith Machine', 5, 'broken', 2),
('Dumbbells', 20, 'normal', 2),
('Elliptical Machine', 6, 'normal', 3),
('Rowing Machine', 4, 'maintenance', 3),
('Leg Press Machine', 3, 'broken', 4),
('Barbell Set', 15, 'normal', 4),
('Cable Machine', 7, 'normal', 5),
('Kettlebells', 12, 'maintenance', 5),
('Lat Pulldown Machine', 5, 'normal', 1),
('Pec Deck Machine', 4, 'broken', 2),
('Abdominal Crunch Machine', 6, 'normal', 3),
('Power Rack', 8, 'maintenance', 4),
('Battle Ropes', 10, 'normal', 5),
('Medicine Balls', 25, 'normal', 1),
('Jump Ropes', 30, 'maintenance', 2),
('Foam Rollers', 20, 'normal', 3),
('Resistance Bands', 50, 'normal', 4),
('Pull-Up Bar', 12, 'broken', 5),
('Weight Bench', 15, 'normal', 1),
('Squat Rack', 6, 'maintenance', 2),
('Deadlift Platform', 3, 'normal', 3),
('Leg Extension Machine', 4, 'broken', 4),
('Shoulder Press Machine', 5, 'normal', 5),
('Incline Bench', 8, 'normal', 1),
('Decline Bench', 7, 'maintenance', 2),
('Preacher Curl Bench', 5, 'normal', 3),
('Hack Squat Machine', 3, 'broken', 4),
('Leg Curl Machine', 6, 'normal', 5),
('Chest Press Machine', 7, 'normal', 1),
('Tricep Pushdown Machine', 5, 'maintenance', 2),
('Bicep Curl Machine', 4, 'normal', 3),
('Leg Raise Station', 8, 'normal', 4),
('Hyperextension Bench', 6, 'broken', 5),
('Assault Bike', 4, 'normal', 1),
('Air Bike', 5, 'maintenance', 2),
('Spin Bike', 6, 'normal', 3),
('Stair Climber', 3, 'broken', 4),
('Vertical Leg Press', 4, 'normal', 5),
('Glute Ham Developer', 5, 'normal', 1),
('Landmine Station', 6, 'maintenance', 2),
('Rogue Rack', 3, 'normal', 3),
('GHD Machine', 4, 'broken', 4),
('Reverse Hyper', 5, 'normal', 5),
('Plate-Loaded Machines', 10, 'normal', 1),
('Functional Trainer', 8, 'maintenance', 2),
('Suspension Trainer', 15, 'normal', 3),
('Olympic Weightlifting Platform', 5, 'broken', 4),
('Adjustable Benches', 20, 'normal', 5);

-- 插入测试数据
INSERT INTO LostAndFound (pick_name, pick_time, pick_place, description, registrant_username) VALUES
('Wallet', '2024-10-01 10:00:00', 'Gym entrance', 'Brown leather wallet with some cards', 'admin'),
('Phone', '2024-10-02 14:30:00', 'Locker room', 'Black smartphone with a cracked screen', 'coachA'),
('Keys', '2024-10-03 09:15:00', 'Fitness area', 'A set of keys with a keychain', 'staff1'),
('Watch', '2024-10-04 16:45:00', 'Cafeteria', 'Silver watch with a leather strap', 'mem01'),
('Glasses', '2024-10-05 11:20:00', 'Yoga studio', 'Black framed glasses', 'admin'),
('Backpack', '2024-10-06 13:50:00', 'Entrance hall', 'Blue backpack with multiple pockets', 'coachA'),
('Jacket', '2024-10-07 15:35:00', 'Lounge area', 'Black leather jacket', 'staff1'),
('Umbrella', '2024-10-08 17:10:00', 'Reception', 'Red umbrella', 'mem01'),
('Book', '2024-10-09 10:45:00', 'Reading corner', 'A novel about adventure', 'admin'),
('Headphones', '2024-10-10 12:25:00', 'Cardio room', 'Wireless headphones', 'coachA'),
('Camera', '2024-10-11 14:00:00', 'Photography area', 'Digital camera with a zoom lens', 'staff1'),
('Tennis racket', '2024-10-12 16:30:00', 'Tennis court', 'Wilson tennis racket', 'mem01');