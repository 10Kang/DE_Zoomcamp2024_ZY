from bs4 import BeautifulSoup
import requests
import pandas as pd
import argparse

url = "https://menuprice.my/zus-coffee-menu/"

def scrap_product_price(url):

    # request web
    response = requests.get(url)

    # instantiate list to store
    product_list = []
    price_list = []
    
    # check response
    if response.status_code == 200:
        print("----------Scarping data at", url,'----------')

        # get the content
        soup = BeautifulSoup(response.content,'html.parser')

        # find where the product and price locate
        product_elements = soup.find_all('figure',class_='wp-block-table')

        # loop through each element
        for element in product_elements:
            # get the products 
            products_name = element.find_all('td',class_='')
            for i in range (len(products_name)):
                product = products_name[i].text
                product_list.append(product)

            # price and calories 
            products_price = element.find_all('td',class_="has-text-align-center")
            for i in range (len(products_price)):
                price = products_price[i].text
                price_list.append(price)

            # get the price only 
            price_list = [item for item in price_list if isinstance(item, str) and item.startswith('RM')]
    else:
        print('Bad reponse',response.status_code)

    return product_list, price_list


def main(param):

    output = param.output
    # scap and get the data
    product_list, price_list = scrap_product_price(url)

    # create unique id for each product
    id_column = ['PD' + str(i).zfill(3) for i in range(1, len(product_list) + 1)]

    df = pd.DataFrame({'product_id':id_column,'product_name':product_list,'product_price':price_list})

    df.to_csv(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generating Product Info')

    # Add a positional argument
    parser.add_argument('--output', help='Path to the output file',required=True)
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    main(args)
