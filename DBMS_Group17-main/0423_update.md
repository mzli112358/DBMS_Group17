#  新增功能：周期课程排课模块

为实现“每周固定时间上课”的排课需求，本次更新实现 **周期课程管理功能**，  
包括模板定义 → 自动生成课程实例 → 实例展示 → 用户报名 的流程。
如下：
---

##  1. 数据库结构扩展

新增两张表用于支持周期排课：

---

###  `CourseTemplate`（课程模板表）

用于定义周期排课规则，例如：每周三 18:00 ~ 19:30 上瑜伽课。

| 字段名         | 含义 |
|----------------|------|
| `template_id`  | 主键，自增 |
| `name`         | 模板名（例如：每周三瑜伽） |
| `coach_id`     | 外键，关联 Person.person_id |
| `branch_id`    | 外键，关联 Branch.branch_id |
| `course_id`    | 外键，关联 Course.course_id（统一课程编号）|
| `course_name`  | 对应课程名称（同步显示） |
| `weekly`       | 上课星期（0=周一，6=周日） |
| `start_time` / `end_time` | 上课时间段 |
| `valid_from` / `valid_to` | 模板适用的时间范围 |
| `location`, `fee`, `max_seats`, `requirement` | 课程信息 |

---

### `CourseInstance`（课程实例表）

由模板生成的每一节课程。每节课都有唯一编号，格式为 `课程ID_日期`，例如：`C101_20250417`。这个和course不同的点在于，这是对于**每一门课**的表，不是一个“大课”的

| 字段名              | 含义 |
|---------------------|------|
| `course_instance_id`| 主键，每节课唯一（如：C101_20250417） |
| `template_id`       | 外键，关联模板 |
| `course_id`         | 外键，关联 Course 表（课程基本信息） |
| `course_name`       | 冗余字段，课程名称 |
| `start_datetime` / `end_datetime` | 实际课程时间 |
| `status`            | 课程状态（present/absent） |

---

## 2. 后端 app.py Flask 路由新增

### `/course_template_manage`
- 管理员可查看并新增课程模板（周期排课规则）

### `/add_course_template`
- 表单提交后，自动调用 `generate_course_instances()` 生成周期课程实例

### `/course_instances`
- 所有用户可查看周期课程安排（已生成实例）

### `/enroll_instance/<course_instance_id>`
- 学员报名具体一节课，写入 `CourseEnrollment` 与 `Purchase` 表

---

## 3. 自动生成课程实例函数

定义函数 `generate_course_instances(...)`：

- 每周匹配 `weekly`
- 每节课生成一条 `CourseInstance` 记录
- 主键为 `course_instance_id = course_id + '_' + 日期`

EG：  
如果模板是 `C101` 每周四上课，范围是 4/1~4/30，这个函数将生成：

- C101_20240404
- C101_20240411
- ...
放在工具函数
---

## 4. 前端页面新增

### `course_template_manage.html`
- 管理员添加课程模板的界面（模态框，支持选择课程 ID 和名称）

### `course_instances.html`
- 用户查看每节课程详情页面，卡片布局
- 支持报名按钮跳转到 `/enroll_instance/<course_instance_id>`

---

## 设计说明

- `Course.course_id` 是“课程种类”的标识（如：C101），和course关联
- `CourseInstance.course_instance_id` 是“每一节课”的唯一 ID
- 所有报名、退课、计数、签到等操作都应基于 `course_instance_id`

---


更新时间：2025-04-23
