import pandas as pd
import random

header = ['service_id', 'hotel_id', 'service_type', 'service', 'cost']
records = []

service_types = {
    'Room Services': ['Housekeeping', 'In-Room Dining'],
    'Food & Beverage Services': ['Restaurant', 'Bar & Lounge', 'Café'],
    'Front Desk Services': ['Reception and Check-in', 'Luggage Assistance', 'Concierge Services'],
    'Business Services': ['Meeting and Banquet Facilities', 'Business Center', 'Courier and Mail Services'],
    'Recreational and Fitness Services': ['Fitness Center', 'Swimming Pool', 'Spa and Sauna'],
    'Transportation Services': ['Airport Shuttle', 'Valet Parking', 'Car Rental'],
    'Other Services': ['Laundry and Dry Cleaning', 'Babysitting', 'Pet Services']
}

prices = {
    'Housekeeping': 0,
    'In-Room Dining': 0,
    'Restaurant': 150,
    'Bar & Lounge': 100,
    'Café': 30,
    'Reception and Check-in': 0,
    'Luggage Assistance': 0,
    'Concierge Services': 0,
    'Meeting and Banquet Facilities': 800,
    'Business Center': 50,
    'Courier and Mail Services': 10,
    'Fitness Center': 80,
    'Swimming Pool': 80,
    'Spa and Sauna': 150,
    'Airport Shuttle': 80,
    'Valet Parking': 10,
    'Car Rental': 150,
    'Laundry and Dry Cleaning': 20,
    'Babysitting': 30,
    'Pet Services': 30
}

hotel_ids = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10']
service_counter = 1

for hotel_id in hotel_ids:
    for service_type, services in service_types.items():
        for service in services:
            service_id = f'{str(service_counter).zfill(3)}'
            if hotel_id == 'H1' or hotel_id == 'H2':
                cost = prices[service] + 100
            elif hotel_id in ['H3', 'H4', 'H5', 'H6']:
                cost = prices[service] + 50
            if service_type in ['Room Services', 'Front Desk Services']:
                 cost = 0
            else:
                cost = prices[service]
            records.append([service_id, hotel_id, service_type, service, cost])
            service_counter += 1

data = pd.DataFrame(records, columns = header)
data.to_csv('sevice_data.csv', index = False)