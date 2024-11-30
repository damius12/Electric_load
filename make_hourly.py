import pandas as pd

def make_hourly(df:pd.DataFrame) -> pd.DataFrame:
    df = df.reset_index()
    if len(df)>24:
        df['Hour'] = df['index'].apply(lambda x: x.hour)
        df = df.groupby(['Hour']).mean()
    return df