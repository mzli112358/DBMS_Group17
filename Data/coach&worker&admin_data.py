import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('en_US')

# 加载员工数据
employees = pd.read_csv('employees.csv')


def generate_qualification_number(emp_id):
    """生成资格证编号"""
    date_part = datetime.now().strftime("%Y%m")
    random_part = f"{random.randint(1000, 9999):04d}"
    return f"CERT-{date_part}-{emp_id[3:6]}-{random_part}"


def generate_specialty():
    """生成教练专长领域"""
    specialties = [
        'Yoga Instruction',
        'Strength Training',
        'Nutrition Coaching',
        'CrossFit Training',
        'Pilates Instruction',
        'Sports Rehabilitation',
        'Weight Management'
    ]
    return random.choices(specialties, weights=[30, 25, 15, 10, 10, 5, 5])[0]


def generate_expiry_date():
    """生成资格证有效期"""
    base_date = datetime.now()
    return (base_date + timedelta(days=random.randint(365, 365 * 5))).strftime("%Y-%m-%d")


def split_employees(df):
    """分割员工数据"""
    # 设置岗位比例：教练60%，工作人员30%，管理员10%
    positions = ['coach', 'worker', 'admin']
    df['position'] = random.choices(positions,
                                    weights=[0.6, 0.3, 0.1],
                                    k=len(df))

    # 生成教练专用数据
    coaches = df[df['position'] == 'coach'].copy()
    coaches['specialty'] = [generate_specialty() for _ in range(len(coaches))]
    coaches['qualification_no'] = [generate_qualification_number(eid) for eid in coaches['employee_id']]
    coaches['qualification_expiry'] = [generate_expiry_date() for _ in range(len(coaches))]

    return {
        'coach': coaches[['employee_id', 'gender', 'username', 'first_name',
                          'last_name', 'birthday', 'specialty', 'qualification_no',
                          'qualification_expiry', 'branch_id']],
        'worker': df[df['position'] == 'worker'][['employee_id', 'gender', 'username',
                                                  'first_name', 'last_name', 'birthday',
                                                  'branch_id']],
        'admin': df[df['position'] == 'admin'][['employee_id', 'gender', 'username',
                                                'first_name', 'last_name', 'birthday',
                                                'branch_id']]
    }


# 分割数据
tables = split_employees(employees)

# 验证数据完整性
print(f"总员工数: {len(employees)}")
print(f"教练数量: {len(tables['coach'])} ({len(tables['coach']) / len(employees):.1%})")
print(f"工作人员: {len(tables['worker'])}")
print(f"管理员: {len(tables['admin'])}")

# 保存数据
tables['coach'].to_csv('coaches.csv', index=False)
tables['worker'].to_csv('workers.csv', index=False)
tables['admin'].to_csv('admins.csv', index=False)