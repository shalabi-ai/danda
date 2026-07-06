import pandas as pd

from .cleaner import clean_dataframe


def read_csv(*args, **kwargs):
    df = pd.read_csv(*args, **kwargs)
    return clean_dataframe(df)

def read_excel(*args, **kwargs):
    df = pd.read_excel(*args, **kwargs)
    return clean_dataframe(df)