import pandas as pd
from faker import Faker
import random

# 初始化Faker
fake = Faker()

# 加载branch数据
branch_df = pd.read_csv('branch.csv')
branch_ids = branch_df['branch_id'].tolist()

# 设备配置
EQUIPMENT_TYPES = {
    'Cardio': {
        'items': [
            ('Treadmill', ['TechnoGym', 'Precor', 'Life Fitness']),
            ('Elliptical', ['Matrix', 'NordicTrack', 'ProForm']),
            ('Rowing Machine', 'Concept2'),
            ('Stationary Bike', ['Schwinn', 'Peloton', 'Keiser'])
        ],
        'quantity_range': (5, 15)
    },
    'Strength': {
        'items': [
            ('Weight Bench', ['Rogue', 'CAP', 'Body-Solid']),
            ('Barbell', ['Ivanko', 'Eleiko', 'Rogue']),
            ('Dumbbell Set', ['Bowflex', 'PowerBlock', 'Yes4All']),
            ('Cable Machine', ['Life Fitness', 'Hammer Strength', 'Cybex'])
        ],
        'quantity_range': (3, 10)
    },
    'Functional': {
        'items': [
            ('Kettlebell', ['Rogue', 'Kettlebell Kings', 'CAP']),
            ('Resistance Bands', ['TheraBand', 'WODFitters', 'Fit Simplify']),
            ('Medicine Ball', ['Valeo', 'Dynamax', 'SKLZ']),
            ('Yoga Mat', ['Manduka', 'Lululemon', 'Gaiam'])
        ],
        'quantity_range': (10, 30)
    }
}

STATUS_WEIGHTS = {
    'normal': 0.85,
    'maintenance': 0.12,
    'broken': 0.03
}

def generate_equipment_data(num_records):
    """生成设备数据"""
    data = []

    for i in range(num_records):
        # 选择设备类型
        eq_type = random.choice(list(EQUIPMENT_TYPES.keys()))
        type_config = EQUIPMENT_TYPES[eq_type]

        # 生成设备名称
        item = random.choice(type_config['items'])
        if isinstance(item[1], list):
            brand = random.choice(item[1])
        else:
            brand = item[1]
        model_number = f"{random.randint(100, 999)}"
        name = f"{brand} {item[0]} {model_number}"

        # 生成数量
        min_qty, max_qty = type_config['quantity_range']
        quantity = random.randint(min_qty, max_qty)

        # 生成状态
        status = random.choices(
            list(STATUS_WEIGHTS.keys()),
            weights=STATUS_WEIGHTS.values(),
            k=1
        )[0]

        record = {
            'equipment_id': 600000 + i,
            'name': name,
            'quantity': quantity,
            'status': status,
            'branch_id': random.choice(branch_ids)
        }
        data.append(record)

    return pd.DataFrame(data)


# 生成1000条设备数据
equipment_df = generate_equipment_data(1000)

# 数据清洗
equipment_df['quantity'] = equipment_df.apply(
    lambda x: 0 if x['status'] == 'broken' else x['quantity'],
    axis=1
)

# 保存到CSV
equipment_df.to_csv('equipment.csv', index=False)

# 预览数据
print("生成设备数据样例:")
print(equipment_df.head(5).to_string(index=False))