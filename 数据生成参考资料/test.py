# header = ['room_num', 'hotel_id']
# records = []

# # hotel_ids = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10']
# hotel_ids = ['H1', 'H2']

# for hotel_id in hotel_ids:
#     for i in range(1, 201):
#         room_num = f'{str(i).zfill(3)}'
#         if room_num == range(1, 101):
#             room_type = 'Standard Room'
#         records.append([room_num, hotel_id, room_type])
#         print(records)

import pandas as pd

# header = ['room_num', 'hotel_id', 'room_type']
# records = []

# hotel_ids = ['H1', 'H2']

# for hotel_id in hotel_ids:
#     for i in range(1, 201):
#         room_num = f'{i:03}'  # 格式化为三位数
#         if 1 <= i <= 100:
#             room_type = 'Standard Room'
#         else:
#             room_type = 'Other Room Type'  # 根据需求替换为其他房型
#         records.append([room_num, hotel_id, room_type])
#         print(records)

import pandas as pd
import random

header = ['room_num', 'hotel_id', 'floor', 'is_smoking', 'room_type', 'price']
records = []

hotel_ids = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10']
room_types = ['Standard Room', 'Superior Room', 'Deluxe Room', 'Suite', 'Presidential Suite']

for hotel_id in hotel_ids:
    for room_type, start, end in [('Standard Room', 1, 100), 
                                  ('Superior Room', 101, 140), 
                                  ('Deluxe Room', 141, 170), 
                                  ('Suite', 171, 190), 
                                  ('Presidential Suite', 191, 200)]:
        
        room_numbers = list(range(start, end + 1))
        # random.shuffle(room_numbers)  # 打乱房间编号顺序
        smoking_rooms = room_numbers[:len(room_numbers)//2]
        non_smoking_rooms = room_numbers[len(room_numbers)//2:]

        for i in range(start, end + 1):
            room_num = f'{i:03}'
            if i in smoking_rooms:
                is_smoking = 'yes'
            else:
                is_smoking = 'no'

            floor = random.randint(1, 10)
            if hotel_id == 'H1':
                price = 3000 + i - 1
            elif hotel_id == 'H2':
                price = 4000 + i - 1
            else:
                price = random.randint(5000, 10000)

            records.append([room_num, hotel_id, floor, is_smoking, room_type, price])

data = pd.DataFrame(records, columns=header)
data.to_csv('test.csv', index=False)
