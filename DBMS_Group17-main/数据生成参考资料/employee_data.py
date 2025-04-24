import pandas as pd
import random
from faker import Faker

header = ['employee_id', 'first_name', 'last_name', 'gender', 'contact', 'birth', 'department_id']

records = []
fake = Faker()
num = 2000

genders = ['Male', 'Female']
hotel_ids = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10']
departments = [('D1', 25), ('D2', 60), ('D3', 50), ('D4', 12), ('D5', 15),
               ('D6', 10), ('D7', 8), ('D8', 10), ('D9', 5), ('D10', 5)]
employee_conuter = 1

for hotel_id in hotel_ids:
    for department, count in departments:
        for i in range(count):
            employee_id = f'E{str(employee_conuter).zfill(7)}'
            gender = random.choice(genders)
            if gender == 'Male':
                first_name = fake.first_name_male()
            else:
                first_name = fake.first_name_female()

            last_name = fake.last_name()
            phone = fake.random_number(digits=11, fix_len=True)
            birth = fake.date_of_birth(minimum_age = 18, maximum_age = 70)
            department_id = f'{hotel_id}{department}'
            records.append([employee_id, first_name, last_name, gender, birth, phone, department_id])
            employee_conuter += 1

data = pd.DataFrame(records, columns = header)
data.to_csv('employee_data.csv', index = False)