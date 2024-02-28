import random
from faker import Faker
from faker.providers import phone_number

fake = Faker()
fake.add_provider(phone_number)

def generate_customer():
    first_name = fake.first_name()
    last_name = fake.last_name()
    gender = random.choice(['Male', 'Female'])
    birthday = fake.date_of_birth(minimum_age=15, maximum_age=80)
    email = fake.email()
    phone_number = fake.phone_number()
    customer_id = fake.random_number( )

    return {
        'ID':customer_id,
        'First Name': first_name,
        'Last Name': last_name,
        'Gender': gender,
        'Birthday': birthday,
        'Email': email,
        'Phone Number': phone_number
    }

def generate_customer_database(num_customers):
    customers = []
    for _ in range(num_customers):
        customers.append(generate_customer())
    return customers

def main():
    num_customers = 10
    customer_database = generate_customer_database(num_customers)
    for idx, customer in enumerate(customer_database, start=1):
        print(f"Customer {idx}:")
        for field, value in customer.items():
            print(f"{field}: {value}")
        print()

if __name__ == "__main__":
    main()
