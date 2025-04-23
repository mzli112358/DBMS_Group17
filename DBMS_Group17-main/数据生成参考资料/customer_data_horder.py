import pandas as pd
import random
from faker import Faker
from datetime import timedelta

header = ['h_order_id', 'customer_id', 'hotel_id', 'room_num', 'arrive_date', 'leave_date', 'price']

records = []
fake = Faker()
num_order = 60000
num_customer = 55000

customer_ids = [f'C{str(i+1).zfill(7)}' for i in range(num_customer)]
room_prices = [i for i in range(1000, 4001, 200)]
service_prices = [100, 200, 300, 500]
hotel_ids = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10']
room_nums = [f'{str(i+1).zfill(3)}' for i in range(1, 201)]

for i in range(num_order):
    customer_id = random.choice(customer_ids)
    hotel_id = random.choice(hotel_ids)
    room_num = random.choice(room_nums)
    if i < 50000:
        order_id = f'R{str(i+1).zfill(7)}'
        arrive_date = fake.date_between(start_date='-10y', end_date='today')
        leave_date = arrive_date + timedelta(days = random.randint(1, 7))
        price = random.choice(room_prices)
    else:
        order_id = f'S{str(i-49999).zfill(7)}'
        arrive_date = fake.date_between(start_date='-10y', end_date='today')
        leave_date = arrive_date
        price = random.choice(service_prices)
    records.append([order_id, customer_id, hotel_id, room_num, arrive_date, leave_date, price])

data = pd.DataFrame(records, columns = header)
data.to_csv('customer_data_horder.csv', index = False)