import pandas as pd
import random

header = ['room_num', 'hotel_id', 'floor', 'is_smoking', 'room_type', 'price']
records = []

hotel_ids = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10']
# list of room types
room_types = ['Standard Room', 'Superior Room', 'Deluxe Room', 'Suite', 'Presidential Suite']
# smoking status options
is_smokings = ['yes', 'no']
# price additions for each room type
price_add = {'Standard Room': 0, 'Superior Room': 200, 'Deluxe Room': 400, 
             'Suite': 600, 'Presidential Suite': 800}

for hotel_id in hotel_ids:
    for room_type, start, end in [('Standard Room', 1, 100), # 100 standard rooms
                                  ('Superior Room', 101, 140), # 40 superior rooms
                                  ('Deluxe Room', 141, 170), # 30 deluxe rooms
                                  ('Suite', 171, 190), # 20 suite rooms
                                  ('Presidential Suite', 191, 200)]: # 10 presidential suite rooms
        
        # generate room numbers
        room_numbers = list(range(start, end + 1))
        # divide the rooms into smoking and non-smoking
        # 50% can smoke and 50% cannot smoke
        smoking_rooms = room_numbers[:len(room_numbers)//2]
        non_smoking_rooms = room_numbers[len(room_numbers)//2:]

        for i in range(start, end + 1):
            room_num = f'{i:03}'
            if i in smoking_rooms:
                is_smoking = 'yes'
            else:
                is_smoking = 'no'

            # randomly set the floor between 1 and 10 for rooms 
            floor = random.randint(1, 10)
            # set the room price based on the hotel's star level and room type
            if hotel_id == 'H1' or hotel_id == 'H2':
                price = 3000 + price_add.get(room_type)
            elif hotel_id == 'H3' or hotel_id == 'H4' or hotel_id == 'H5':
                price = 2000 + price_add.get(room_type)
            else:
                price = 1000 + price_add.get(room_type)

            records.append([room_num, hotel_id, floor, is_smoking, room_type, price])

data = pd.DataFrame(records, columns = header)
data.to_csv('room_data.csv', index = False)
