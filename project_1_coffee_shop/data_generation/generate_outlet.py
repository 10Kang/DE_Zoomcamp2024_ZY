from bs4 import BeautifulSoup
import requests
import pandas as pd 
import argparse


state = ['perak','johor','melaka','perlis','kedah','penang','kelantan',
         'terengganu', 'pahang','kuala-lumpur-selangor','negeri-sembilan','sabah','sarawak']
url = "https://zuscoffee.com/category/store/"

def scarpe_coffee_shop_location(base_url,location):

    # full url
    url = base_url + location
    # initiate list to store scraped data
    store_name_list = []
    store_address_list =[]
    state_name_list = []
    
    while url:
        # request web response
        response = requests.get(url)
    
        # check status code
        if response.status_code == 200:
            print('----------Scarping the data for at',url,'----------')
    
            # get the content
            soup = BeautifulSoup(response.content, 'html.parser')
    
            # find all <article> 
            store_location_elements = soup.find_all('article')
    
            for i in range (len(store_location_elements)):
    
                # get store name
                store_name = store_location_elements[i].find_all('section')[0].find('p').text
            
                # get store adress
                store_address = store_location_elements[i].find_all('section')[1].find('p').text
            
                if store_name == 'Ingredients':
                    continue
                else:
                    # append to list
                    store_name_list.append(store_name)
                    store_address_list.append(store_address)
                    state_name_list.append(location)

            # check got another page or not
            # Find the <a> tag with class "page-numbers next"
            next_page_link = soup.find_all('a', class_='page-numbers next')
            # Extract the value of the "href" attribute
            if next_page_link:
                url = next_page_link[0]['href']
            else:
                url = None
                    
        else:
            print('Bad response. Status_code:',response.status_code)
            break
            
    return store_name_list, store_address_list, state_name_list

def flatten_comprehension(matrix):
    return [item for row in matrix for item in row]

def main(param):
    output = param.output 
    state = ['perak','johor','melaka','perlis','kedah','penang','kelantan',
         'terengganu', 'pahang','kuala-lumpur-selangor','negeri-sembilan','sabah','sarawak']
    url = "https://zuscoffee.com/category/store/"

    address_all_outlet = []
    name_all_outlet = []
    state_name_all = []

    for i in range (len(state)):
        state_outlet_name, state_outlet_address,state_name = scarpe_coffee_shop_location(url,state[i])

        address_all_outlet.append(state_outlet_address)
        name_all_outlet.append(state_outlet_name)
        state_name_all.append(state_name)
        
    # flatten into address and put into dataframe
    outlets_name = flatten_comprehension(name_all_outlet)
    outlets_address = flatten_comprehension(address_all_outlet)
    outlets_state = flatten_comprehension(state_name_all)
    
    # create unique ID for each store 
    id_column = ['MY' + str(i).zfill(3) for i in range(1, len(outlets_name) + 1)]
    
    # create dataframe
    df = pd.DataFrame({'outlet_id':id_column,'outlet_name':outlets_name,'outlet_address':outlets_address,'outlet_state':outlets_state})

    # add the postcode
    df['postcode'] = df['outlet_address'].str.extract(r'(\b\d{5}\b)')

    # add the name of district
    # due to format of address, we need two ways of extracting the name
    district_part_1 = df['outlet_address'].str.extract(r'\b\d{5}\b\s+(.*),')
    district_part_2 = df['outlet_address'].str.extract(r'\b\d{5}\b\s*,\s*(.*?),')
    district = district_part_1.combine_first(district_part_2)
    # add district column 
    df['district']= district


    # save file
    # filepath = '/Users/kang/Documents/DE_zoomcamp/project_1_coffee_shop/outlet_address'
    print('Save to filepath:',output)
    df.to_csv(output)

    
if __name__ == "__main__":
    
  parser = argparse.ArgumentParser(description='Generating Outlets')

  # Add a positional argument
  parser.add_argument('--output', help='Path to the output file',required=True)

  # Parse the command-line arguments
  args = parser.parse_args()

  main(args)
