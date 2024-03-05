if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from pyspark.sql import types
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

@data_exporter
def export_data(*args, **kwargs):
    """
    Read data using pyspark and save it into gcs bucket
    """

    bucket_name = 'malaysian_coffee_chain'
    object_key = '/raw/customer'
    filepath = f'gs://{bucket_name}{object_key}/*csv'
    print(filepath)

    # infer schema
    schema = types.StructType([
        types.StructField('count', types.IntegerType(), True), 
        types.StructField('customer_id', types.StringType(), True), 
        types.StructField('first_name', types.StringType(), True), 
        types.StructField('last_name', types.StringType(), True), 
        types.StructField('gender', types.StringType(), True), 
        types.StructField('birthday', types.TimestampType(), True), 
        types.StructField('email', types.StringType(), True), 
        types.StructField('phone_no', types.StringType(), True)
    ])

    df = kwargs['spark'].read \
        .option('header','True') \
        .option("delimiter", ",") \
        .schema(schema) \
        .csv(filepath)
    
    df = df.drop(col("count"))
    df = df.repartition(20)
    df.write.parquet('gs://malaysian_coffee_chain/processed/customer/',mode='overwrite')
