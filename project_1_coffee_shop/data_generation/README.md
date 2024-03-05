## Generating the data needed 👨🏻‍💻

## Authenticate the google service account in the virtual machine

Prior running the python script for data generation, we have to authenticate our identity in google cloud as follow

```
export GOOGLE_APPLICATION_CREDENTIALS=~/.google/gcp_terraform.json

```

```
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

## Generating the data

![](../images/data_model.png)

Overall, the data model look like figure above which made up of four major tables, the customers, sales, products and outlet with its own unique keys. All the data can be generated via the python script in `./data_generation/` directory. Specifically, the  [`generate_outlet.py`](./data_generation/generate_outlet.py) and [`generate_outlet.py`](./data_generation/generate_outlet.py) are the script that scrap the data of Malaysian first tech driven coffee chain called [ZUS coffee, Malaysia](https://zuscoffee.com/menu/). 

The scraping of data can be run in terminal with python installed

```{Python}

# to scrap the product name and price
python data_generation/generate_product.py --output /path/to/destination

```

```{Python}

# to scrap the outlet name and address
python data_generation/generate_outlet.py --output /path/to/destination

```

Next, we generate the customer database by specifying number of records and seeds to make sure not replication. All the records here are fake and for project purpose.

```{python}

python data_generation/generate_customer_database.py 
  --seed 10 
  --output /path/to/destination/ 
  --number 500000 
  --date_string "2024-02-24"

```


To prepare the sales data, we first need to get outlet, product and customer data ready prior running the `generate_coffee_order.py` file in `./data_generation/` as they referencing the other 3 tables.  All the records here are fake and for project purpose.

```{python}
  python generate_coffee_order.py 
    --seed 10 
    --number 20 
    --date_string "2024-01-01" 
    --output ~/data/sales/ 
    --outlet_id_path ~/data/outlet.csv 
    --customer_id_path ~/data/customer/customer_data_2024-02-24.csv 
    --product_id_path ~/data/product.csv
```     

## Copy to the GCS

The generated file is then uploaded to GCS as raw_file. You can also tuned it to upload the file directly into GCS using with credentials set in the python script.

```
gsutil cp file.csv gs://bucket/files
```

## Important Notes

The address of the outlet from data scraping might lake of information. It is manually corrected as uploaded into bucket while doing the data modelling using dbt.

You may check the outlet information at [dbt_coffee_chain](../dbt_coffee_chain/seeds/outlet.csv) folder. 