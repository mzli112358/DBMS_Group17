import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import numpy as np

# 初始化Faker实例
fake = Faker()

# 加载基础数据
branch_df = pd.read_csv('gym_branches_en.csv')
person_df = pd.read_csv('persons.csv')

# 获取有效的教练ID列表
valid_coaches = person_df[person_df['role'] == 'coach']['person_id'].tolist()

# 课程生成配置
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
COURSE_TYPES = {
    'Yoga': ['Beginner', 'Intermediate', 'Advanced', 'Hot', 'Prenatal'],
    'Pilates': ['Mat', 'Reformer', 'Clinical', 'Group'],
    'Weightlifting': ['Olympic', 'Power', 'Strength', 'Technique'],
    'Cycling': ['Indoor', 'HIIT', 'Endurance'],
    'Dance': ['Zumba', 'Hip-hop', 'Aerobic'],
    'Martial Arts': ['Boxing', 'MMA', 'Kickboxing']
}

TIMESLOTS = [
    ('09:00', '11:00'),
    ('14:00', '16:00'),
    ('18:00', '20:00'),
    ('19:00', '21:00')
]


def generate_start_date(selected_days, start='+30d', end='+120d'):
    """生成符合指定星期几的开始日期"""
    # 转换星期名称到数字（0=Monday）
    day_numbers = [WEEKDAYS.index(day) for day in selected_days]

    # 生成基准日期
    base_date = fake.date_between(start_date=start, end_date=end)
    current_date = base_date

    # 查找最近符合条件的日期（最多检查7天）
    for _ in range(7):
        if current_date.weekday() in day_numbers:
            return current_date
        current_date += timedelta(days=1)
    return base_date  # 理论上不会执行到这里


def generate_course_data(num_records):
    """生成课程数据"""
    data = []

    for i in range(num_records):
        # 生成课程类型
        category = random.choice(list(COURSE_TYPES.keys()))
        sub_type = random.choice(COURSE_TYPES[category])

        # 生成上课星期（1-3个不同的日期）
        num_days = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1], k=1)[0]
        selected_days = random.sample(WEEKDAYS, num_days)

        # 生成日期相关字段
        start_date = generate_start_date(selected_days)
        duration_weeks = random.choice([4, 8, 12])
        end_date = start_date + timedelta(weeks=duration_weeks)

        # 处理时间段
        timeslot = random.choice(TIMESLOTS)
        start_time, end_time = timeslot
        hours = (datetime.strptime(end_time, "%H:%M") -
                 datetime.strptime(start_time, "%H:%M")).seconds / 3600

        # 生成课程信息
        course_id = 300000 + i
        name_parts = [
            fake.random_element(["Morning", "Afternoon", "Evening", "Weekend"]),
            f"{category} {sub_type}",
            fake.random_element(["Class", "Session", "Workshop", "Program"])
        ]

        record = {
            'course_id': course_id,
            'name': " ".join(name_parts),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'start_time': start_time,
            'end_time': end_time,
            'hours': round(hours, 1),
            'weekly': ", ".join(sorted(selected_days)),  # 按字母顺序排列
            'coach_id': random.choice(valid_coaches),
            'branch_id': random.choice(branch_df['branch_id'].tolist()),
            'location': f"Studio {random.choice(['A', 'B', 'C'])}{random.randint(1, 5)}",
            'fee': round(random.uniform(50, 300), -1),
            'requirement': random.choice([
                "Age 16+",
                "Basic fitness required",
                "Medical clearance needed",
                "No experience required"
            ]),
            'max_seats': random.choices([15, 20, 25, 30], weights=[0.1, 0.4, 0.3, 0.2])[0],
            'img': f"/images/{category.lower()}-{random.randint(1, 5)}.jpg"
        }
        data.append(record)

    return pd.DataFrame(data)


# 生成500条课程数据
course_df = generate_course_data(500)

# 数据清洗
course_df['fee'] = course_df['fee'].astype(int)
course_df = course_df.sort_values('start_date')

# 保存到CSV
course_df.to_csv('courses.csv', index=False)

# 预览数据
print("Generated Courses Sample:")
print(course_df[['course_id', 'name', 'start_date', 'end_date', 'start_time', 'end_time', 'weekly', 'hours', 'coach_id', 'branch_id', 'location', 'fee', 'requirement', 'max_seats', 'img']].head(3).to_string(index=False))