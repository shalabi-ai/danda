def clean_dataframe(df):
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    return df
