### **1. 实体与属性**

#### **Branch（分店）**
- **主键**：`branch_id`
- **属性**：
  - `name`（分店名称）
  - `city`（所在城市）
  - `district`（所在区）
  - `address`（详细地址）

#### **Person（用户）**
- **主键**：`person_id`
- **属性**：
  - `username`（用户名，唯一）
  - `password`（密码）
  - `role`（角色：`member`、`coach`、`staff`、`admin`）
  - `first_name`（名）
  - `last_name`（姓）
  - `gender`（性别：`M`、`F`、`Other`）
  - `birthday`（生日）
  - `phone`（电话）
  - `id_number`（身份证号）
  - `join_date`（加入日期，默认值为当前时间）
  - `branch_id`（外键，关联到 `Branch` 表）
  - `qualification_no`（资格证编号，仅教练有）
  - `qualification_expiry`（资格证有效期，仅教练有）
  - `specialty`（专长，仅教练有）
  - `position`（职位，仅员工有）

#### **Equipment（器材）**
- **主键**：`equipment_id`
- **属性**：
  - `name`（器材名称）
  - `quantity`（数量，默认值为 1）
  - `status`（状态：`normal`、`broken`、`maintenance`，默认值为 `normal`）
  - `branch_id`（外键，关联到 `Branch` 表）

#### **Product（商品）**
- **主键**：`product_id`
- **属性**：
  - `name`（商品名称）
  - `description`（商品描述）
  - `image`（商品图片路径）
  - `stock`（库存，默认值为 0）
  - `branch_id`（外键，关联到 `Branch` 表）

#### **Course（课程）**
- **主键**：`course_id`
- **属性**：
  - `name`（课程名称）
  - `start_date`（开始日期）
  - `end_date`（结束日期）
  - `hours`（总课时）
  - `coach_id`（外键，关联到 `Person` 表中的教练）
  - `branch_id`（外键，关联到 `Branch` 表）
  - `location`（上课地点）
  - `fee`（费用）
  - `requirement`（课程要求）
  - `max_seats`（最大座位数）
  - `img`（课程图片路径）

#### **CourseEnrollment（课程报名）**
- **主键**：`enrollment_id`
- **属性**：
  - `course_id`（外键，关联到 `Course` 表）
  - `member_id`（外键，关联到 `Person` 表中的会员）
  - `enroll_time`（报名时间，默认值为当前时间）
- **约束**：
  - 联合唯一约束：同一个人不能重复报名同一课程。

#### **Purchase（购买记录）**
- **主键**：`purchase_id`
- **属性**：
  - `member_id`（外键，关联到 `Person` 表中的会员）
  - `type`（购买类型：`course` 或 `product`）
  - `ref_id`（引用 ID，对应课程或商品的 ID）
  - `number`（购买数量，默认值为 1）
  - `total_fee`（总费用）
  - `purchase_time`（购买时间，默认值为当前时间）

#### **LostAndFound（失物招领）**
- **主键**：`pick_id`
- **属性**：
  - `pick_name`（拾取物品名称）
  - `pick_photo`（拾取物品照片路径）
  - `pick_time`（拾取时间）
  - `pick_place`（拾取地点）
  - `description`（物品描述）
  - `registrant_username`（登记人用户名，外键关联到 `Person` 表）
  - `is_claimed`（是否已被认领，默认值为 `FALSE`）

---

### **2. 关系描述**

#### **Branch 和 Person**
- `Branch` 和 `Person` 是一对多关系：
  - 一个分店可以有多名用户（会员、教练、员工、管理员）。
  - 每个用户属于一个分店。
  - 外键：`Person.branch_id` → `Branch.branch_id`

#### **Branch 和 Equipment**
- `Branch` 和 `Equipment` 是一对多关系：
  - 一个分店可以有多件健身器材。
  - 每件器材属于一个分店。
  - 外键：`Equipment.branch_id` → `Branch.branch_id`

#### **Branch 和 Product**
- `Branch` 和 `Product` 是一对多关系：
  - 一个分店可以有多种商品。
  - 每种商品属于一个分店。
  - 外键：`Product.branch_id` → `Branch.branch_id`

#### **Branch 和 Course**
- `Branch` 和 `Course` 是一对多关系：
  - 一个分店可以开设多门课程。
  - 每门课程属于一个分店。
  - 外键：`Course.branch_id` → `Branch.branch_id`

#### **Person 和 Course**
- `Person` 和 `Course` 是多对一关系：
  - 一门课程由一名教练授课。
  - 一名教练可以教授多门课程。
  - 外键：`Course.coach_id` → `Person.person_id`

#### **Course 和 CourseEnrollment**
- `Course` 和 `CourseEnrollment` 是一对多关系：
  - 一门课程可以有多个报名记录。
  - 每个报名记录对应一门课程。
  - 外键：`CourseEnrollment.course_id` → `Course.course_id`

#### **Person 和 CourseEnrollment**
- `Person` 和 `CourseEnrollment` 是一对多关系：
  - 一名会员可以报名多门课程。
  - 每个报名记录对应一名会员。
  - 外键：`CourseEnrollment.member_id` → `Person.person_id`

#### **Person 和 Purchase**
- `Person` 和 `Purchase` 是一对多关系：
  - 一名会员可以有多条购买记录。
  - 每条购买记录对应一名会员。
  - 外键：`Purchase.member_id` → `Person.person_id`

#### **Person 和 LostAndFound**
- `Person` 和 `LostAndFound` 是一对多关系：
  - 一名用户可以登记多条失物招领记录。
  - 每条失物招领记录由一名用户登记。
  - 外键：`LostAndFound.registrant_username` → `Person.username`
