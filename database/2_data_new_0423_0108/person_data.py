import pandas as pd
from faker import Faker
import random
from pypinyin import pinyin, Style
from dateutil.relativedelta import relativedelta

# 初始化Faker实例
fake = Faker('en_US')
fake_cn = Faker('zh_CN')

# 加载branch数据
branch_df = pd.read_csv('gym_branches_en.csv')
branch_ids = branch_df['branch_id'].tolist()


def generate_chinese_name():
    """生成中文姓名的拼音版本"""

    def pinyin_convert(name):
        return ' '.join([p[0].capitalize() for p in pinyin(name, style=Style.NORMAL)])

    return {
        'last_name': pinyin_convert(fake_cn.last_name()),
        'first_name': pinyin_convert(fake_cn.first_name())
    }


def generate_id_card(birth_date):
    """生成类身份证号码"""
    address_code = f"{random.randint(110000, 659999):06d}"
    birth_part = birth_date.strftime("%Y%m%d")
    sequence = f"{random.randint(0, 999):03d}"
    checksum = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X'])
    return f"{address_code}{birth_part}{sequence}{checksum}"


def generate_person_data(num_records):
    """生成会员数据"""
    data = []
    specialties = ['Fitness Training', 'Yoga', 'Pilates', 'Nutrition', 'Weightlifting']
    staff_positions = ['Manager', 'Receptionist', 'Sales', 'Accountant']
    roles = ['member', 'staff', 'coach', 'admin']
    role_weights = [0.70, 0.15, 0.10, 0.05]  # 角色分布权重

    for i in range(num_records):
        # 生成基础信息
        birth_date = fake.date_between(start_date='-65y', end_date='-18y')
        cn_name = generate_chinese_name()
        role = random.choices(roles, weights=role_weights, k=1)[0]
        join_date = fake.date_between(start_date='-5y', end_date='today')

        # 处理教练专属字段
        qualification_no = None
        qualification_expiry = None
        specialty = None
        if role == 'coach':
            qualification_no = f"QC{random.randint(10000000, 99999999)}"
            expiry_date = join_date + relativedelta(years=random.randint(1, 5))
            qualification_expiry = expiry_date.strftime('%Y-%m-%d')
            specialty = random.choice(specialties)

        # 处理职位信息
        position = None
        if role == 'staff':
            position = random.choice(staff_positions)
        elif role == 'admin':
            position = 'Administrator'
        elif role == 'coach':
            position = 'Coach'

        # 清理手机格式
        phone = ''.join(filter(str.isdigit, fake_cn.phone_number()))
        if len(phone) != 11 or not phone.startswith('1'):
            phone = f"1{random.randint(1000000000, 9999999999)}"

        record = {
            'person_id': 100000 + i,  # 生成唯一ID
            'id': generate_id_card(birth_date),
            'username': fake.unique.user_name(),
            'password': fake.password(length=12),
            'role': role,
            'phone': phone[:11],  # 确保11位长度
            'join_date': join_date.strftime('%Y-%m-%d'),
            'qualification_no': qualification_no,
            'qualification_expiry': qualification_expiry,
            'specialty': specialty,
            'position': position,
            'first_name': cn_name['first_name'],
            'last_name': cn_name['last_name'],
            'gender': random.choices(['Male', 'Female'], weights=[0.52, 0.48])[0],
            'birthday': birth_date.strftime('%Y-%m-%d'),
            'branch_id': random.choice(branch_ids)
        }
        data.append(record)
    return pd.DataFrame(data)


# 生成70000条数据
person_df = generate_person_data(70000)

# 保存到CSV（注意处理空值）
person_df.to_csv('persons.csv', index=False, na_rep='NULL')

# 查看示例数据
print(person_df.head())