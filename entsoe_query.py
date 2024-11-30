import numpy as np
import pandas as pd
import streamlit as st
from datetime import date
from anagraphic import psr_type
from make_hourly import make_hourly
from entsoe import EntsoePandasClient

client = EntsoePandasClient(api_key='d0259571-e1bb-49f7-be2c-c370c180e77e')

def entsoe_query(date:date, cc:str) -> pd.DataFrame:
    day = pd.Timestamp(date, tz='Europe/Brussels')
    start = day 
    end = day + pd.Timedelta(days=1)
    df = make_hourly(client.query_load(cc, start=start, end=end))
    df
    k = psr_type.keys()
    for psr in k:
        try: 
            gen = make_hourly(client.query_generation(cc, start=start, end=end, psr_type=psr))
        except Exception:
            gen = pd.DataFrame(np.zeros(len(df)))
        if psr == 'B16':
            df[psr_type[psr]] = np.array(gen.iloc[:,1])
        elif len(gen.columns) > 2:
            df[psr_type[psr]] = np.array(gen.iloc[:,1]) - np.array(gen.iloc[:,2])
        else :
            df[psr_type[psr]] = np.array(gen.iloc[:,-1])
        df = df.fillna(0).rename(columns={'Actual Load':'Load'})
        df['Timestamp'] = df['index']
        for i in df.index:
            df.at[i,'Timestamp'] = df.at[i,'index'] + pd.Timedelta(hours=0.5)
    return df
