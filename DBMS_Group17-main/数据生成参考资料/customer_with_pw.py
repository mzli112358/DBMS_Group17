import pandas as pd

customer = pd.read_csv('customer_data.csv')
password = pd.read_csv('passwords.csv')

merged_data = pd.concat([customer, password], axis = 1)

merged_data.to_csv('merge_data.csv', index = False)
