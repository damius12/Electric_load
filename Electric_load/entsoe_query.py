import numpy as np
import pandas as pd
from datetime import date
from anagraphic import psr_type
from entsoe import EntsoePandasClient

client = EntsoePandasClient(api_key='d0259571-e1bb-49f7-be2c-c370c180e77e')

def entsoe_query(date:date, country:str) -> pd.DataFrame:
    day = pd.Timestamp(date, tz='Europe/Brussels')
    start = day 
    end = day + pd.Timedelta(days=1)
    cc = country
    df = client.query_load(cc, start=start, end=end)
    k = psr_type.keys()
    for psr in k:
        try: 
            gen = client.query_generation(cc, start=start, end=end, psr_type=psr)
        except Exception:
            gen = pd.DataFrame(np.zeros(len(df)))
        if psr == 'B16':
            df[psr_type[psr]] = np.array(gen.iloc[:,0])
        elif len(gen.columns) > 1:
            df[psr_type[psr]] = np.array(gen.iloc[:,0]) - np.array(gen.iloc[:,1])
        else :
            df[psr_type[psr]] = gen
        df = df.fillna(0).rename(columns={'Actual Load':'Load'})
    return df

    
