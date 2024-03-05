from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Execute Transformer Action: ActionType.REMOVE

    Docs: https://docs.mage.ai/guides/transformer-blocks#remove-columns
    """

    df['postcode'] = df['postcode'].astype(int)

    df['postcode'] = df['postcode'].apply(lambda x: '{:05d}'.format(x))

    return df
@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'