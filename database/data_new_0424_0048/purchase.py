import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# 初始化Faker实例
fake = Faker()

# 加载基础数据
persons_df = pd.read_csv('person.csv')
products_df = pd.read_csv('product.csv')
courses_df = pd.read_csv('course.csv')

# 准备有效数据源
valid_members = persons_df[persons_df['role'] == 'member']['person_id'].tolist()
valid_products = products_df['product_id'].tolist()
valid_courses = courses_df['course_id'].tolist()

# 获取价格字典
product_prices = dict(zip(products_df['product_id'], products_df['fee']))
course_fees = dict(zip(courses_df['course_id'], courses_df['fee']))


def generate_purchase_data(num_records):
    """生成购买记录数据（最终正确版）"""
    data = []

    # 设置时间范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 两年时间范围

    for i in range(num_records):
        purchase_id = 500000 + i
        member_id = random.choice(valid_members)
        purchase_type = random.choices(['product', 'course'], weights=[0.6, 0.4], k=1)[0]

        # 生成引用信息
        if purchase_type == 'product':
            ref_id = random.choice(valid_products)
            number = random.randint(1, 3)
            unit_price = product_prices[ref_id]
        else:
            ref_id = random.choice(valid_courses)
            number = 1
            unit_price = course_fees[ref_id]

        total_fee = unit_price * number

        # 修正时间生成方法
        if purchase_type == 'course':
            # 获取课程开始日期
            course_start = datetime.strptime(
                courses_df[courses_df['course_id'] == ref_id]['start_date'].values[0],
                '%Y-%m-%d'
            )
            # 使用正确的时间生成方法
            purchase_time = fake.date_time_between(
                start_date=start_date,
                end_date=course_start - timedelta(days=1)
            )
        else:
            purchase_time = fake.date_time_between(
                start_date=start_date,
                end_date=end_date
            )

        data.append({
            'purchase_id': purchase_id,
            'member_id': member_id,
            'type': purchase_type,
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