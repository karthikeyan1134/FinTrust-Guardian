import json
import random
from faker import Faker

fake = Faker()

def generate_mock_data(num_records=100):
    mock_data = []
    for _ in range(num_records):
        record = {
            "user_id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "transaction_history": [
                {
                    "transaction_id": fake.uuid4(),
                    "amount": round(random.uniform(10.0, 1000.0), 2),
                    "date": fake.date_time_this_year().isoformat(),
                    "description": fake.sentence()
                } for _ in range(random.randint(1, 5))
            ]
        }
        mock_data.append(record)
    
    return mock_data

def save_mock_data_to_file(data, filename='backend/data/mock_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    mock_data = generate_mock_data()
    save_mock_data_to_file(mock_data)