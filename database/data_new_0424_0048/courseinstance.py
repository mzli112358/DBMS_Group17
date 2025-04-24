import pandas as pd
from datetime import datetime, timedelta
import random

# 加载基础数据
course_df = pd.read_csv('course.csv')
template_df = pd.read_csv('coursetemplate.csv')
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def assign_template(course_row, templates):
    """为课程分配最匹配的模板"""
    # 先匹配相同教练、分店和课程类型的模板
    matched = templates[
        (templates['coach_id'] == course_row['coach_id']) &
        (templates['branch_id'] == course_row['branch_id']) &
        (templates['name'].str.contains(course_row['name'].split()[0]))
        ]

    if not matched.empty:
        return random.choice(matched['template_id'].tolist())

    # 次选相同教练和分店的模板
    matched = templates[
        (templates['coach_id'] == course_row['coach_id']) &
        (templates['branch_id'] == course_row['branch_id'])
        ]

    return random.choice(matched['template_id'].tolist()) if not matched.empty else random.choice(
        templates['template_id'].tolist())


def generate_instances():
    """生成课程实例数据"""
    # 为每个课程分配模板ID
    course_df['template_id'] = course_df.apply(
        lambda x: assign_template(x, template_df), axis=1)

    instances = []

    # 合并课程和模板数据
    merged = pd.merge(course_df, template_df, on='template_id', suffixes=('_course', '_template'))

    for _, row in merged.iterrows():
        # 解析时间参数
        weekly_days = row['weekly'].split(', ')
        course_start = datetime.strptime(row['start_date'], '%Y-%m-%d').date()
        course_end = datetime.strptime(row['end_date'], '%Y-%m-%d').date()
        template_start = datetime.strptime(row['valid_from'], '%Y-%m-%d').date()
        template_end = datetime.strptime(row['valid_to'], '%Y-%m-%d').date()

        # 计算实际有效日期范围
        start_date = max(course_start, template_start)
        end_date = min(course_end, template_end)

        if start_date > end_date:
            continue

        # 生成所有符合条件的日期
        day_numbers = [WEEKDAYS.index(day) for day in weekly_days]
        current_date = start_date
        dates = []

        while current_date <= end_date:
            if current_date.weekday() in day_numbers:
                dates.append(current_date)
            current_date += timedelta(days=1)

        # 为每个日期创建实例
        for date in dates:
            start_dt = datetime.combine(date, datetime.strptime(row['start_time'], '%H:%M').time())
            end_dt = datetime.combine(date, datetime.strptime(row['end_time'], '%H:%M').time())

            instance_id = f"C{row['course_id']}_{date.strftime('%Y%m%d')}"

            instances.append({
                'course_instance_id': instance_id,
                'course_name': row['name_course'],
                'template_id': row['template_id'],
                'course_id': row['course_id'],
                'start_datetime': start_dt.strftime('%Y-%m-%d %H:%M:%S'),
                'end_datetime': end_dt.strftime('%Y-%m-%d %H:%M:%S'),
                'status': random.choice(['present', 'absent'])
            })

    return pd.DataFrame(instances)


# 生成实例数据
instance_df = generate_instances()

# 数据清洗与验证
instance_df = instance_df.drop_duplicates('course_instance_id')
instance_df = instance_df.sort_values('start_datetime')

# 保存结果
instance_df.to_csv('courseinstance.csv', index=False)

# 预览数据
print("\nGenerated Course Instances Sample:")
print(instance_df[['course_instance_id', 'course_name', 'template_id',
                   'start_datetime', 'end_datetime', 'status']].head(3).to_string(index=False))