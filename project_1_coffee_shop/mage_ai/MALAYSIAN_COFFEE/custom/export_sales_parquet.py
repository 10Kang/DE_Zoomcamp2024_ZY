from pyspark.sql import types
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from pyspark.sql.functions import year, month, concat
from google.oauth2 import service_account

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def export_data(*args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    
    credentials_location = '/home/src/gcp_terraform.json'
    bucket_name = 'malaysian_coffee_chain'
    object_key = '/raw/sales'
    filepath = f'gs://{bucket_name}{object_key}/*csv'
    print(filepath)

    # infer schema
    schema = types.StructType([
        types.StructField('count', types.IntegerType(), True), 
        types.StructField('invoice_no', types.StringType(), True), 
        types.StructField('date_time', types.TimestampType(), True), 
        types.StructField('customer_id', types.StringType(), True), 
        types.StructField('outlet', types.StringType(), True), 
        types.StructField('product', types.StringType(), True), 
        types.StructField('quantity', types.StringType(), True), 
    ])

    df = kwargs['spark'].read \
        .option('header','True') \
        .option("delimiter", ",") \
        .schema(schema) \
        .csv(filepath)
    
    df = df.drop(col("count"))
    df_with_year_month = df.select("*", year("date_time").alias("year"), month("date_time").alias("month"))
    # df_with_year_month = df.withColumn("year_month", concat(year("date_time"), month("date_time")))

    # save with year/month
    df_with_year_month.write \
        .partitionBy('year') \
        .parquet('gs://malaysian_coffee_chain/processed/sales/',mode='overwrite')

    # save with year_month 
    # df_with_year_month.write.partitionBy("year_month") \
    #     .parquet("gs://malaysian_coffee_chain/processed/sales/sales_{year_month}.parquet")
    # credentials = service_account.Credentials.from_service_account_file(credentials_location)

    # return credentials