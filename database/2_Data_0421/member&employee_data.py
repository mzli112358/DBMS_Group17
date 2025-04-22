import pandas as pd
import random

# 加载之前生成的Person数据
person_df = pd.read_csv('persons.csv')


def split_person_data(df, employee_ratio=0.15):
    """分割人员数据为会员和员工"""
    # 生成随机标记列
    df['is_employee'] = [random.random() < employee_ratio for _ in range(len(df))]

    employees = df[df['is_employee']].copy()
    members = df[~df['is_employee']].copy()

    # 生成新ID格式
    employees['employee_id'] = [f"EMP{str(i).zfill(6)}" for i in range(1, len(employees) + 1)]
    members['member_id'] = [f"MEM{str(i).zfill(7)}" for i in range(1, len(members) + 1)]

    return employees, members


# 分割数据（默认5%为员工）
employee_df, member_df = split_person_data(person_df)

# 构建最终表结构
employee_table = employee_df[['employee_id', 'gender', 'username',
                              'first_name', 'last_name', 'birthday', 'branch_id']]

member_table = member_df[['member_id', 'gender', 'username',
                          'first_name', 'last_name', 'birthday', 'branch_id']]

# 验证数据完整性
print(f"总人数: {len(person_df)}")
print(f"员工数: {len(employee_table)} ({len(employee_table) / len(person_df):.1%})")
print(f"会员数: {len(member_table)}")

# 保存数据
employee_table.to_csv('employees.csv', index=False)
member_table.to_csv('members.csv', index=False)