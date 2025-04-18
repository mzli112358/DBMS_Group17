import pandas as pd
import random

customer = pd.read_csv('customer_data.csv')

header = ['vip_id', 'first_name', 'last_name', 'customer_id', 'contact']

records = []

vip_customers = customer.sample(n = 5000, random_state=1)
vip_customers['vip_id'] = [f'VIP{i:06}' for i in range(1, 5001)]
vip_customers['contact'] = vip_customers['phone']

records = vip_customers[['vip_id', 'first_name', 'last_name', 'customer_id', 'contact']]

data = pd.DataFrame(records, columns = header)
data.to_csv('vip_data.csv', index = False)