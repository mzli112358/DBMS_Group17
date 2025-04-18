import pandas as pd

header = ['city_id', 'city_name']

records = []

city_names = ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Nanjing', 'Xian', 
             'Shantou', 'Changsha', 'Chengdu', 'Chongqing']

num = len(city_names)

for i in range(num):
    city_name = city_names[i]
    city_id = f'city_{str(i+1)}'
    records.append([city_id, city_name])

data = pd.DataFrame(records, columns = header)
data.to_csv('city_data.csv', index = False)