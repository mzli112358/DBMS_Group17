import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# 初始化Faker
fake = Faker()

# 加载基础数据
person_df = pd.read_csv('persons.csv')
branch_df = pd.read_csv('gym_branches_en.csv')

# 有效数据源
valid_usernames = person_df['username'].tolist()
valid_branches = branch_df[['branch_id', 'address']].to_dict('records')

# 物品配置
LOST_ITEMS = {
    'Electronics': {
        'names': ['Smartphone', 'Smart Watch', 'Wireless Earbuds', 'Tablet'],
        'descriptors': ['Color', 'Brand', 'Model', 'Case Feature']
    },
    'Apparel': {
        'names': ['Sports Jacket', 'Gym Gloves', 'Sneakers', 'Towel'],
        'descriptors': ['Color', 'Size', 'Brand', 'Special Markings']
    },
    'Accessories': {
        'names': ['Ring', 'Necklace', 'Fitness Tracker', 'Eyeglasses'],
        'descriptors': ['Material', 'Color', 'Brand', 'Engraving']
    },
    'Daily Essentials': {
        'names': ['Water Bottle', 'Keys', 'Wallet', 'Membership Card'],
        'descriptors': ['Color', 'Brand', 'Contained Items', 'Special Markings']
    }
}


def generate_item_description(category, item_name):
    """Generate item description in English"""
    descriptors = LOST_ITEMS[category]['descriptors']
    details = []

    # 通用特征
    details.append(f"Category: {category}")
    details.append(f"Item Name: {item_name}")

    # 随机特征
    for desc in random.sample(descriptors, 2):
        if desc == 'Color':
            details.append(f"Color: {fake.safe_color_name()}")
        elif desc == 'Brand':
            details.append(f"Brand: {fake.company()}")
        elif desc == 'Model':
            details.append(f"Model: {fake.bothify(text='??-####')}")
        elif desc == 'Contained Items':
            details.append(f"Contains: {fake.random_element(['Cash', 'Credit Cards', 'ID', 'Photos'])}")

    # 添加随机备注
    remarks = [
        "Found in locker room",
        "Stored at reception",
        "Visible wear marks",
        "Good condition"
    ]
    details.append(f"Note: {random.choice(remarks)}")

    return "; ".join(details)


def generate_lost_data(num_records):
    """Generate lost and found data"""
    data = []

    # 时间范围：过去一年内
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    for i in range(num_records):
        # 随机选择分支信息
        branch = random.choice(valid_branches)

        # 生成物品信息
        category = random.choice(list(LOST_ITEMS.keys()))
        item_name = random.choice(LOST_ITEMS[category]['names'])

        record = {
            'pick_id': 700000 + i,
            'pick_name': f"{category}-{item_name}",
            'pick_photo': f"/images/lost/{category.lower()}_{fake.uuid4()[:8]}.jpg",
            'pick_time': fake.date_time_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d %H:%M'),
            'pick_place': f"{branch['address']}-{fake.random_element(['Locker Room', 'Reception', 'Equipment Area', 'Poolside'])}",
            'description': generate_item_description(category, item_name),
            'registrant_username': random.choice(valid_usernames),
            'is_claimed': random.choices([0, 1], weights=[0.8, 0.2], k=1)[0]
        }
        data.append(record)

    return pd.DataFrame(data)


# 生成500条数据
lost_df = generate_lost_data(5000)

# 数据清洗
lost_df['pick_place'] = lost_df['pick_place'].str.replace(' ', '_')

# 保存到CSV
lost_df.to_csv('lost_and_found.csv', index=False)

# 预览数据
print("失物招领数据样例:")
print(lost_df.head(3).to_string(index=False))