if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    # turn Camel Case to Snake Case
    data.columns = (data.columns
        .str.replace(r'([a-z0-9])([A-Z])', r'\1_\2',regex=True).str.lower()
    )
    
    # remove rows where trip_distance is 0 or passesnger is 0
    data = data[(data['passenger_count'] != 0) & (data['trip_distance'] != 0)]

    # add the date column
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    # print(data['vendor_id'].unique())
    return data
    
    

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # assert output is not None, 'The output is undefined'
    assert output['vendor_id'].isin([1, 2]).all(), "Assertion 1 failed: VendorID should be one of the existing values."
    assert (output['passenger_count'] > 0).all(), "passenger_count should be greater than 0."
    assert (output['trip_distance'] > 0).all(), "trip_distance should be greater than 0."
