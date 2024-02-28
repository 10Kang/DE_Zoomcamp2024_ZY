from faker.providers import BaseProvider
from faker import Faker
from datetime import datetime
import pandas as pd
import random
import argparse

outlet_id_list = pd.read_csv('/Users/kang/Documents/DE_zoomcamp/project_1_coffee_shop/data/outlet_address.csv')['outlet_id'].tolist()
product_id_list = pd.read_csv('/Users/kang/Documents/DE_zoomcamp/project_1_coffee_shop/data/product.csv')['product_id'].tolist()
customer_id_list = pd.read_csv('/Users/kang/Documents/DE_zoomcamp/project_1_coffee_shop/data/customer_data_2024-02-24.csv')['customer_id'].tolist()

class CustomProvider(BaseProvider):
    def invoice_number(self):
        # Customize this method to generate your invoice numbers
        return 'INV-' + str(self.random_number(digits=6))


start_date = datetime(2018, 1, 1)
end_date = datetime(2022, 12, 31)

def generate_sales(number,seed):

    number = int(number)
    seed = int(seed)
    fake = Faker()
    # Add the custom provider to Faker
    fake.add_provider(CustomProvider)

    # add seed
    fake.seed_instance(seed)
    random.seed(seed)

    sales_data = []
    for i in range(number):

        invoice_no = fake.invoice_number()
        date_time = fake.date_time_between_dates(datetime_start = start_date,datetime_end = end_date)
        customer_id = random.choice(customer_id_list)
        outlet = random.choice(outlet_id_list)
        product = random.choice(product_id_list)
        quantity = random.choice([x for x in range(1,5)])
        

        sale = {
            'invoice_no': invoice_no,
            'date_time': date_time,
            'customer_id': customer_id,
            'outlet': outlet,
            'product': product,
            'quantity': quantity,
        }
        sales_data.append(sale)

    df = pd.DataFrame(sales_data)

    return df


def main(params):
    
    seed = params.seed
    number = params.number
    output = params.output
    date_string = params.date_string
    # get date as record to update new 
    if date_string == None:
        today_date = datetime.today()
        date_string = today_date.strftime('%Y-%m-%d')
    else:
        date_string = params.date_string
        
    # filepath to save file 
    filepath = f'{output}_sales_data_{date_string}.csv'

    df = generate_sales(number,seed)

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