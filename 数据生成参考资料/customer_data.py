import pandas as pd
import random
from faker import Faker

header = ['customer_id', 'first_name', 'last_name', 'gender', 'phone', 'birth']

records = []
fake = Faker()
num = 55000 # the number of customers

# define possible gender
genders = ['Male', 'Female']

for i in range(num):
    # generate the customer order ID in the format 'Cxxxxxxx'
    customer_id = f'C{str(i+1).zfill(7)}'
    # randomly select a gender
    gender = random.choice(genders)
    # generate the first name based on the selected gender
    if gender == 'Male':
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name_female()

    # generate the last name
    last_name = fake.last_name()
    # generate the phone number in 11 numbers
    phone = fake.random_number(digits=11, fix_len=True)
    # generate the birth date for each customer ensuring that the age is between 18 and 100
    birth = fake.date_of_birth(minimum_age = 18, maximum_age = 100)
    records.append([customer_id, first_name, last_name, gender, phone, birth])

data = pd.DataFrame(records, columns = header)
data.to_csv('customer_data.csv', index = False)

