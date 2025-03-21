import numpy as np
import pandas as pd

def group_tech_cap(df:pd.DataFrame) -> pd.DataFrame:
    df['Idroelettrico'] = np.array(df['Idroelettrico bacino'])+np.array(df['Idroelettrico fluente'])+np.array(df['Idroelettrico pompaggio'])
    df['Carbone'] = np.array(df['Carbone'])+np.array(df['Lignite'])
    df['Gas'] = np.array(df['Gas derivato'])+np.array(df['Gas naturale'])
    df['Eolico'] = np.array(df['Eolico offshore'])+np.array(df['Eolico onshore'])
    return df

def group_tech_aep(df:pd.DataFrame) -> pd.DataFrame:
    df['Idroelettrico'] = np.array(df['Hydro'])+np.array(df['Pumped hydro power'])
    df['Carbone'] = np.array(df['Solid fossil fuels'])+np.array(df['Other bituminous coal'])+np.array(df['Lignite'])
    df['Gas'] = np.array(df['Natural gas'])
    df['Biomassa'] = np.array(df['Biogases'])+np.array(df['Primary solid biofuels'])
    df['Rifiuti'] = np.array(df['Non-renewable waste'])+np.array(df['Renewable municipal waste'])+np.array(df['Non-renewable municipal waste'])
    return df