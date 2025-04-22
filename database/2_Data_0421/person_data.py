import pandas as pd
from faker import Faker
import random
from pypinyin import pinyin, Style
from datetime import datetime

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
    # 前6位地址码（模拟行政区代码）
    address_code = f"{random.randint(110000, 659999):06d}"  # 覆盖主要城市范围

    # 生日部分
    birth_part = birth_date.strftime("%Y%m%d")

    # 顺序码（3位）+ 校验位（1位）
    sequence = f"{random.randint(0, 999):03d}"
    checksum = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X'])

    return f"{address_code}{birth_part}{sequence}{checksum}"


def generate_person_data(num_records):
    """生成会员数据"""
    data = []
    for _ in range(num_records):
        # 生成生日（保证与身份证日期一致）
        birth_date = fake.date_between(start_date='-65y', end_date='-18y')

        record = {
            'id': generate_id_card(birth_date),
            'gender': random.choices(['Male', 'Female'], weights=[0.52, 0.48])[0],
            'username': fake.unique.user_name(),
            'first_name': generate_chinese_name()['first_name'],
            'last_name': generate_chinese_name()['last_name'],
            'birthday': birth_date.strftime('%Y-%m-%d'),
            'branch_id': random.choice(branch_ids)
        }
        data.append(record)
    return pd.DataFrame(data)


# 生成50000条数据
person_df = generate_person_data(70000)

# 保存到CSV
person_df.to_csv('persons.csv', index=False)

# 查看示例数据
print(person_df.head())