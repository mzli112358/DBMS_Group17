import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# 初始化Faker实例
fake = Faker()

# 加载基础数据
persons_df = pd.read_csv('person.csv')
products_df = pd.read_csv('product.csv')

# 准备有效数据源
valid_members = persons_df[persons_df['role'] == 'member']['person_id'].tolist()
valid_products = products_df['product_id'].tolist()

# 获取价格字典
product_prices = dict(zip(products_df['product_id'], products_df['price']))


def generate_purchase_data(num_records):
    """生成购买记录数据（仅商品版）"""
    data = []

    # 设置时间范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 两年时间范围

    for i in range(num_records):
        purchase_id = 500000 + i
        member_id = random.choice(valid_members)

        # 固定为商品类型
        ref_id = random.choice(valid_products)
        number = random.randint(1, 3)
        unit_price = product_prices[ref_id]
        total_fee = unit_price * number

        # 生成购买时间
        purchase_time = fake.date_time_between(
            start_date=start_date,
            end_date=end_date
        )

        data.append({
            'purchase_id': purchase_id,
            'member_id': member_id,
            'type': 'product',  # 固定类型
            'ref_id': ref_id,
            'number': number,
            'total_fee': total_fee,
            'purchase_time': purchase_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    return pd.DataFrame(data)


# 生成并保存数据
purchase_df = generate_purchase_data(10000)
purchase_df.to_csv('purchase.csv', index=False)

print("成功生成购买记录样例:")
print(purchase_df.head(3).to_string(index=False))