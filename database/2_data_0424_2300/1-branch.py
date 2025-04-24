from faker import Faker
import random
import pandas as pd
import pypinyin  # 需要安装pypinyin包：pip install pypinyin

# 初始化英文Faker实例
fake = Faker('en_US')


def chinese_to_pinyin(chinese_str):
    """将中文字符串转换为拼音"""
    return ' '.join([item[0] for item in pypinyin.pinyin(chinese_str)])


# 预定义城市区划转换（中文->拼音）
def create_district_mapping():
    district_map = {
        # 直辖市
        'Beijing': ['Dongcheng', 'Xicheng', 'Chaoyang', 'Haidian', 'Fengtai', 'Shijingshan', 'Tongzhou'],
        'Shanghai': ['Huangpu', 'Xuhui', 'Changning', 'Jing''an', 'Putuo', 'Hongkou', 'Yangpu'],
        'Tianjin': ['Heping', 'Hedong', 'Hexi', 'Nankai', 'Hebei', 'Hongqiao'],
        'Chongqing': ['Yuzhong', 'Jiangbei', 'Shapingba', 'Jiulongpo', 'Nan''an', 'Beibei'],

        # 省会城市
        'Guangzhou': ['Tianhe', 'Yuexiu', 'Haizhu', 'Liwan', 'Baiyun', 'Huangpu'],
        'Shenzhen': ['Futian', 'Luohu', 'Nanshan', 'Yantian', 'Bao''an', 'Longgang'],
        'Chengdu': ['Jinjiang', 'Qingyang', 'Jinniu', 'Wuhou', 'Chenghua', 'Longquanyi'],
        'Hangzhou': ['Shangcheng', 'Xiacheng', 'Jianggan', 'Gongshu', 'Xihu', 'Binjiang'],
        'Nanjing': ['Xuanwu', 'Qinhuai', 'Jianye', 'Gulou', 'Qixia', 'Yuhuatai'],
        'Wuhan': ['Jiang''an', 'Jianghan', 'Qiaokou', 'Hanyang', 'Wuchang', 'Hongshan'],
        'Xi''an': ['Xincheng', 'Beilin', 'Lianhu', 'Yanta', 'Weiyang', 'Baqiao'],
        'Changsha': ['Furong', 'Tianxin', 'Yuelu', 'Kaifu', 'Yuhua', 'Wangcheng'],
        'Zhengzhou': ['Zhongyuan', 'Erqi', 'Jinshui', 'Huiji', 'Guancheng', 'Shangjie'],
        'Jinan': ['Lixia', 'Shizhong', 'Huaiyin', 'Tianqiao', 'Licheng', 'Changqing'],

        # 计划单列市
        'Dalian': ['Zhongshan', 'Xigang', 'Shahekou', 'Ganjingzi', 'Lvshunkou'],
        'Qingdao': ['Shinan', 'Shibei', 'Huangdao', 'Laoshan', 'Licang', 'Chengyang'],
        'Ningbo': ['Haishu', 'Jiangbei', 'Zhenhai', 'Beilun', 'Yinzhou', 'Fenghua'],
        'Xiamen': ['Siming', 'Haicang', 'Huli', 'Jimei', 'Tong''an', 'Xiang''an'],

        # 其他重点城市
        'Suzhou': ['Gusu', 'Huqiu', 'Wuzhong', 'Xiangcheng', 'Industrial Park', 'Wujiang'],
        'Dongguan': ['Guancheng', 'Nancheng', 'Dongcheng', 'Wanjiang', 'Songshanhu'],
        'Foshan': ['Chancheng', 'Nanhai', 'Shunde', 'Sanshui', 'Gaoming'],
        'Wuxi': ['Liangxi', 'Binhu', 'Xinwu', 'Xishan', 'Huishan']
    }
    return {city: [f"{d} District" for d in districts] for city, districts in district_map.items()}


city_districts = create_district_mapping()

# 健身房品牌转换
gym_brands_pinyin = [chinese_to_pinyin(brand) for brand in
                     ['金仕堡', '威康', '力美', '奥美', '健乐', '美格菲', '一兆韦德', '威尔士']]


# 结果示例：['jin shi bao', 'wei kang', 'li mei', ...]

def generate_gym_data(num_records):
    """Generate gym branch data"""
    city_weights = {
        'Beijing': 12, 'Shanghai': 12, 'Guangzhou': 10, 'Shenzhen': 10,
        'Chengdu': 8, 'Hangzhou': 8, 'Wuhan': 7, 'Chongqing': 7,
        'Other': 5
    }

    cities = []
    weights = []
    for city, weight in city_weights.items():
        if city != 'Other':
            cities.append(city)
            weights.append(weight)

    other_cities = list(set(city_districts.keys()) - set(cities))
    cities += other_cities
    weights += [city_weights['Other']] * len(other_cities)

    data = []
    branch_id_order = 1
    for _ in range(num_records):
        city = random.choices(cities, weights=weights, k=1)[0]
        district = random.choice(city_districts[city])

        # 生成英文地址组件
        street_address = fake.street_address()
        landmark = random.choice(['Metro Station', 'Shopping Mall', 'University'])

        data.append({
            'branch_id': f"{branch_id_order:04d}",
            'name': f"{random.choice(gym_brands_pinyin).title()} {district.split()[0]} Flagship",
            'city': city,
            'district': district,
            'address': f"{street_address} (Near {landmark})"
        })
        branch_id_order += 1
    return pd.DataFrame(data)


# 生成并保存数据
gym_df = generate_gym_data(500)
gym_df.to_csv('branch.csv', index=False)

# 示例输出
print(gym_df.head())