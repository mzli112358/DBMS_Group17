import pandas as pd
from faker import Faker
import random

# 初始化Faker实例
fake = Faker()

# 加载分支数据
branch_df = pd.read_csv('gym_branches_en.csv')
branch_ids = branch_df['branch_id'].tolist()

# 修正后的商品配置（所有类别统一字段）
PRODUCT_CATEGORIES = {
    'Protein Powder': {
        'subtypes': ['Whey', 'Casein', 'Plant-Based'],
        'spec_values': ['5lbs', '2kg', '10 servings'],
        'flavors': ['Chocolate', 'Vanilla', 'Strawberry', 'Unflavored'],
        'stock_range': (10, 50)
    },
    'Sports Drink': {
        'subtypes': ['Isotonic', 'Energy', 'Recovery'],
        'spec_values': ['500ml', '1L', '6-pack'],
        'flavors': ['Lemon', 'Berry', 'Tropical'],
        'stock_range': (50, 200)
    },
    'Apparel': {
        'subtypes': ['T-Shirt', 'Shorts', 'Hoodie'],
        'spec_values': ['S', 'M', 'L', 'XL'],
        'colors': ['Black', 'Gray', 'Red', 'Navy'],
        'stock_range': (20, 100)
    },
    'Equipment': {
        'subtypes': ['Dumbbell', 'Resistance Band', 'Yoga Mat'],
        'spec_values': ['5kg', '10kg', '15kg'],
        'materials': ['Rubber', 'Neoprene', 'EVA Foam'],
        'stock_range': (5, 30)
    },
    'Membership': {
        'subtypes': ['Monthly', 'Annual', 'VIP'],  # 统一使用subtypes字段
        'benefits': ['Pool Access', 'PT Sessions', 'All Classes'],
        'stock_range': (999, 1000)
    }
}

BRANDS = {
    'Protein Powder': ['MuscleTech', 'ON', 'Dymatize'],
    'Sports Drink': ['Gatorade', 'Powerade', 'Lucozade'],
    'Apparel': ['Nike', 'Under Armour', 'Gymshark'],
    'Equipment': ['Rogue', 'CAP', 'Yes4All'],
    'Membership': ['Gold', 'Platinum', 'Elite']
}


def generate_product_description(category, details):
    """生成商品描述"""
    descriptors = {
        'Protein Powder': [
            f"High-quality {details['subtype']} protein with {random.choice(['24g', '30g'])} protein per serving",
            "Contains essential amino acids",
            f"Available in {details.get('flavor', 'natural')} flavor"
        ],
        'Sports Drink': [
            f"{details['subtype']} drink with electrolytes",
            "Enhances hydration and performance",
            f"Refreshing {details.get('flavor', 'mixed')} taste"
        ],
        'Apparel': [
            f"Breathable {details.get('material', 'cotton')} fabric",
            "Moisture-wicking technology",
            f"Available in {details.get('color', 'black')} color"
        ],
        'Equipment': [
            f"Durable {details.get('material', 'rubber')} construction",
            "Ergonomic design for comfort",
            f"{details.get('weight', '10kg')} weight option"
        ],
        'Membership': [
            f"Access to {random.randint(3, 5)} classes per week",
            f"Includes {random.choice(['sauna', 'pool', 'parking'])} access",
            "Personal locker included"
        ]
    }
    return ". ".join(random.sample(descriptors[category], 2)) + "."


def generate_product_data(num_records):
    """生成商品数据（最终修复版）"""
    data = []

    for i in range(num_records):
        # 确保选择有效类别
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        config = PRODUCT_CATEGORIES[category]
        brand = random.choice(BRANDS[category])

        # 安全获取subtype
        subtype = random.choice(config['subtypes'])

        # 生成商品名称
        name_parts = [brand, subtype]

        # 添加特征属性
        if category in ['Protein Powder', 'Sports Drink']:
            feature = random.choice(config['flavors'])
            name_parts.append(feature)
        elif category == 'Apparel':
            feature = random.choice(config['colors'])
            name_parts.append(feature)
        elif category == 'Equipment':
            feature = random.choice(config['materials'])
            name_parts.append(feature)

        # 添加规格（所有非会员商品）
        if category != 'Membership':
            spec = random.choice(config['spec_values'])
            name_parts.append(spec)
        else:
            name_parts.append("Membership")

        # 生成图片路径
        img_path = f"/images/{category.lower()}-{subtype.lower().replace(' ', '-')}"
        if category != 'Membership':
            img_path += f"-{feature.lower().replace(' ', '-')}"
        img_path += ".jpg"

        # 构建记录
        record = {
            'product_id': 400000 + i,
            'name': " ".join(name_parts),
            'description': generate_product_description(category, {'subtype': subtype, **locals().get('details', {})}),
            'image': img_path,
            'stock': random.randint(*config['stock_range']),
            'fee': round(random.uniform(50, 300), -1),
            'branch_id': random.choice(branch_ids)
        }

        # 会员特殊处理
        if category == 'Membership':
            record['stock'] = 999

        data.append(record)

    return pd.DataFrame(data)


# 生成并保存数据
product_df = generate_product_data(300)
product_df.to_csv('products.csv', index=False)

# 打印样例
print("成功生成商品数据（样例）：")
print(product_df.head(3).to_string(index=False))