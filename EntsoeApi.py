import numpy as np
import pandas as pd
from datetime import date
from make_hourly import make_hourly
from entsoe import EntsoePandasClient
from anagraphic import psr_type, country_code, type_translation



class EntsoeApi():

    client = EntsoePandasClient(api_key='d0259571-e1bb-49f7-be2c-c370c180e77e')

    def daily_generation(self, date:date, cc:str) -> pd.DataFrame:
        day = pd.Timestamp(date, tz='Europe/Brussels')
        start = day 
        end = day + pd.Timedelta(days=1)
        df = make_hourly(EntsoeApi.client.query_load(cc, start=start, end=end))
        df
        k = psr_type.keys()
        for psr in k:
            try: 
                gen = make_hourly(EntsoeApi.client.query_generation(cc, start=start, end=end, psr_type=psr))
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

    def installed_capacity(self) -> pd.DataFrame:
        today = pd.Timestamp(date.today(),tz='Europe/Brussels')
        cols = ['Nazione'] + list(psr_type.values())
        df = pd.DataFrame({c:[0] for c in cols})
        fails = []
        for cc in country_code.keys():
            try:
                single = EntsoeApi.client.query_installed_generation_capacity(country_code[cc], start= today, end=today+pd.Timedelta(days=1), psr_type=None)
                single = single.rename(columns=type_translation)
                single['Nazione'] = cc
                df = pd.concat([df,single])[cols]
            except Exception:
                fails.append(cc)
        return df