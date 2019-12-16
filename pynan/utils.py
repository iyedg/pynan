import numpy as np
import pandas as pd

# Credits for the color palette goes to Setosa.io
# TODO: should add link to docs


def values_to_types(df):
    """Replace all values in a dataframe with their type.

    Arguments:
        df {pd.DataFrame} -- input dataframe

    Returns:
        pd.DataFrame -- DataFrame with the same shape where everycell contains the type of its previous value.
    """
    return df.applymap(
        lambda val: "<class 'np.nan'>" if pd.isnull(val) else str(type(val))
    )


def types_as_percentage_of_columns(df):
    values_to_types_df = df.pipe(values_to_types).reset_index().melt(id_vars=["index"])
    return (
        values_to_types_df.groupby(["variable", "value"])
        .pipe(lambda gb: gb.size().div(values_to_types_df.groupby(["variable"]).size()))
        .to_frame()
        .reset_index()
        .pipe(lambda df: df.rename(columns={"value": "type", 0: "percent_of_col"}))
    )


if __name__ == "__main__":
    # example_df = pd.read_csv(
    #     "https://raw.githubusercontent.com/setosa/csv-fingerprint/master/example2.csv"
    # )
    # TODO: use in tests
    print(df.pipe(types_as_percentage_of_columns))
