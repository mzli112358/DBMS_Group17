# 数据库 Schema 和关系说明

## 数据库结构

### 表清单
1. Branch - 分店信息
2. Person - 人员信息（会员、教练、员工、管理员）
3. Equipment - 器械设备
4. Product - 产品
5. Course - 课程
6. CourseEnrollment - 课程报名
7. Purchase - 购买记录

## 表关系图

```
Branch
├── 1:M ── Person (branch_id)
├── 1:M ── Equipment (branch_id)
└── 1:M ── Product (branch_id)

Person
├── 1:M ── Course (coach_id)
├── 1:M ── CourseEnrollment (member_id)
└── 1:M ── Purchase (member_id)

Course
├── 1:M ── CourseEnrollment (course_id)
└── 1:1 ── Purchase (通过 ref_id 关联)

Product
└── 1:1 ── Purchase (通过 ref_id 关联)
```

## 详细表结构

### 1. Branch (分店)
- branch_id: 主键，自增
- name: 分店名称
- city: 城市
- district: 区县
- address: 详细地址

### 2. Person (人员)
- person_id: 主键，自增
- username: 用户名，唯一
- password: 密码
- role: 角色（member/coach/staff/admin）
- 个人信息字段（first_name, last_name, gender, birthday等）
- branch_id: 外键，关联Branch
- 教练特有字段（qualification_no, qualification_expiry, specialty）
- 员工特有字段（position）

### 3. Equipment (器械设备)
- equipment_id: 主键，自增
- name: 设备名称
- quantity: 数量
- status: 状态（normal/broken/maintenance）
- branch_id: 外键，关联Branch

### 4. Product (产品)
- product_id: 主键
- name: 产品名称
- description: 描述
- image: 图片路径
- stock: 库存
- branch_id: 外键，关联Branch

### 5. Course (课程)
- course_id: 主键
- name: 课程名称
- 时间信息（start_date, end_date, hours）
- coach_id: 外键，关联Person（教练）
- branch_id: 外键，关联Branch
- location: 上课地点
- fee: 费用
- requirement: 要求
- max_seats: 最大人数
- img: 课程图片

### 6. CourseEnrollment (课程报名)
- enrollment_id: 主键，自增
- course_id: 外键，关联Course
- member_id: 外键，关联Person（会员）
- enroll_time: 报名时间
- 唯一约束：course_id + member_id

### 7. Purchase (购买记录)
- purchase_id: 主键，自增
- member_id: 外键，关联Person（会员）
- type: 类型（course/product）
- ref_id: 关联ID（课程ID或产品ID）
- number: 数量
- total_fee: 总费用
- purchase_time: 购买时间

## 数据关系说明

1. **分店与人员**：一个分店可以有多个人员（会员、教练、员工），通过branch_id关联
2. **分店与设备**：一个分店拥有多台设备，通过branch_id关联
3. **分店与产品**：一个分店存储多种产品，通过branch_id关联
4. **教练与课程**：一个教练可以教授多门课程，通过coach_id关联
5. **课程与报名**：一门课程可以有多个会员报名，通过course_id和member_id关联
6. **会员与购买**：一个会员可以有多个购买记录，通过member_id关联
7. **购买与课程/产品**：购买记录通过ref_id和type字段关联到课程或产品