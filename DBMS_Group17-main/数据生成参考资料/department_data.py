import pandas as pd

header = ['department_id', 'department', 'hotel_id']

departments = ['Front Office', 'Housekeeping', 'Food and Beverage', 'Sales and Marketing', 
               'Engineering and Maintenance', 'Security', 'Human Resources', 'Finance', 'Recreation and Leisure',
               'Information Technology']

num = len(departments)
records = []

hotel_ids = [f'H{str(i+1)}' for i in range(10)]

print(hotel_ids)

for hotel_id in hotel_ids:
    for i, department in enumerate(departments):
        department_id = f'{hotel_id}D{str(i+1)}'
        records.append([department_id, department, hotel_id])

# for i in range(num):
#     hotel_id = hotel_ids[i]
#     department = departments[i]
#     department_id = f'D{str(i+1)}'
#     records.append([hotel_id, department, department_id])

data = pd.DataFrame(records, columns = header)
data.to_csv('department_data.csv', index = False)