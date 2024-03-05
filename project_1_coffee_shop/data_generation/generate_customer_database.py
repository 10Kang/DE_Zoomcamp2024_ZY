from faker import Faker
import random
from faker.providers.phone_number import Provider
import pandas as pd

from datetime import datetime
import argparse

class MalaysiaPhoneNumberProvider(Provider):
    """
    A Provider for phone number.
    """

    def malaysia_phone_number(self):
        return f'+60 {self.msisdn()[4:]}'

def generate_customer_data(number,seed):
    number = int(number)
    seed = int(seed)
    fake = Faker()
    fake.add_provider(MalaysiaPhoneNumberProvider)
    fake.seed_instance(seed)
    random.seed(seed)

    customer_data = []
    for i in range(number):
        customer_id = fake.uuid4()
        gender = random.choice(['Male','Female'])

        if gender == 'Male':
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
        else:
            first_name = fake.first_name_female()
            last_name = fake.last_name_female()
            
        birthday = fake.date_of_birth(minimum_age = 18, maximum_age=75)
        email = fake.email()
        phone_number = fake.malaysia_phone_number()

        customer = {
            'customer_id': customer_id,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'birthday': birthday,
            'email': email,
            'phone_no': phone_number
        }
        customer_data.append(customer)

    df = pd.DataFrame(customer_data)

    return df

def main(params):
    date_string = params.date_string
    seed = params.seed
    number = params.number
    output = params.output
    # get date as record to update new 
    if date_string == None:
        today_date = datetime.today()
        date_string = today_date.strftime('%Y-%m-%d')
    else:
        date_string = params.date_string
        
    # filepath to save file 
    filepath = f'{output}customer_data_{date_string}.csv'

    df = generate_customer_data(number,seed)

    df.to_csv(filepath)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Generating customer database')
    
    # Add a positional argument
    parser.add_argument('--output', help='Path to the output file',required=True)
    parser.add_argument('--number', help='Number of new customer',required=True)
    parser.add_argument('--seed', help='seed to ensure not replicate',required=True)
    parser.add_argument('--date_string','-o', help='date of generating the new customer')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    main(args)