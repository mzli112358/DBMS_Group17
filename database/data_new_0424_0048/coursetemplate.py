import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# 初始化Faker实例
fake = Faker()

# 加载基础数据
branch_df = pd.read_csv('branch.csv')
person_df = pd.read_csv('person.csv')

# 获取有效的教练ID列表
valid_coaches = person_df[person_df['role'] == 'coach']['person_id'].tolist()

# 模板生成配置
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


def generate_course_templates(num_templates):
    """生成周期课程模板数据"""
    templates = []

    for template_id in range(num_templates):
        # 生成课程类型
        category = random.choice(list(COURSE_TYPES.keys()))
        sub_type = random.choice(COURSE_TYPES[category])

        # 生成上课星期（1-3个不同的日期）
        num_days = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        selected_days = random.sample(WEEKDAYS, num_days)
        weekly = ", ".join(sorted(selected_days))

        # 生成时间段
        timeslot = random.choice(TIMESLOTS)
        start_time, end_time = timeslot

        # 生成有效期（4/8/12周）
        duration_weeks = random.choice([4, 8, 12])
        valid_from = fake.date_between(start_date='+30d', end_date='+90d')
        valid_to = valid_from + timedelta(weeks=duration_weeks)

        # 生成课程名称
        name = f"{category} {sub_type} {fake.random_element(['Class', 'Session', 'Workshop'])}"

        # 构建模板记录
        template = {
            'template_id': 100000 + template_id,
            'name': name,
            'coach_id': random.choice(valid_coaches),
            'branch_id': random.choice(branch_df['branch_id'].tolist()),
            'location': f"Studio {random.choice(['A', 'B', 'C'])}{random.randint(1, 5)}",
            'weekly': weekly,
            'start_time': start_time,
            'end_time': end_time,
            'valid_from': valid_from.strftime('%Y-%m-%d'),
            'valid_to': valid_to.strftime('%Y-%m-%d'),
            'max_seats': random.choices([15, 20, 25, 30], weights=[0.1, 0.4, 0.3, 0.2])[0],
            'fee': round(random.uniform(50, 300), -1),
            'requirement': random.choice([
                "Age 16+",
                "Basic fitness required",
                "Medical clearance needed",
                "No experience required"
            ])
        }
        templates.append(template)

    return pd.DataFrame(templates)


# 生成300个课程模板
template_df = generate_course_templates(300)

# 数据清洗
template_df['fee'] = template_df['fee'].astype(int)
template_df = template_df.sort_values('valid_from')

# 保存模板数据
template_df.to_csv('coursetemplate.csv', index=False)

# 预览数据
print("\nGenerated Course Templates Sample:")
print(template_df[['template_id', 'name', 'valid_from', 'valid_to', 'weekly',
                   'start_time', 'end_time', 'coach_id', 'branch_id']].head(3).to_string(index=False))