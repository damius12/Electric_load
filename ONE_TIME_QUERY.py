import numpy as np
import pandas as pd
from EntsoeApi import EntsoeApi
from anagraphic import country_translation
from group_tech import group_tech_cap, group_tech_aep

entsoe = EntsoeApi()
cols = ['Idroelettrico','Solare','Eolico','Geotermico','Biomassa','Rifiuti','Nucleare','Gas','Carbone']

#################
year = 2023
#################

# installed capacity
query = entsoe.installed_capacity(year)
query = group_tech_cap(query)
query = query[['Nazione']+cols]
for col in cols:
    query[col] = np.array(query[col])/1000
query['Totale'] = query.iloc[:,1:].sum(axis=1)
query = query.reset_index()
query = query.drop(columns=['index'])

# annual energy production
df = pd.read_csv('raw_eurostat.csv')
df = df[['geo','siec','OBS_VALUE']]
df = df.pivot(index='geo',columns='siec',values='OBS_VALUE')
df = df[['Nuclear heat','Wind' ,'Natural gas','Hydro','Solid fossil fuels','Solar photovoltaic','Lignite',
         'Other bituminous coal','Primary solid biofuels','Biogases','Pumped hydro power','Geothermal',
         'Non-renewable waste','Renewable municipal waste','Non-renewable municipal waste']]
df = group_tech_aep(df)
df = df.drop('European Union - 27 countries (from 2020)',axis=0)
df = df.reset_index()
df = df.rename(columns={'geo':'Nazione','Nuclear heat':'Nucleare','Solar photovoltaic':'Solare','Wind':'Eolico','Geothermal':'Geotermico'})
df["Nazione"] = df["Nazione"].map(country_translation)
df = df[['Nazione']+cols]
for col in cols:
    df[col] = np.array(df[col])/1000
df["Totale"] = df.iloc[:, 1:].sum(axis=1)

countries_cap = query['Nazione'].unique().tolist()
countries_gen = df['Nazione'].unique().tolist()
countries = list(set(countries_gen) & set(countries_cap))
query = query[query['Nazione'].isin(countries)]
df = df[df['Nazione'].isin(countries)]
query.to_csv('installed_capacity.csv')
df = df.to_csv('AEP.csv')