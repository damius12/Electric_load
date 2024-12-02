import numpy as np
import pandas as pd

def group_tech(df:pd.DataFrame) -> pd.DataFrame:
    df['Idroelettrico'] = np.array(df['Idroelettrico bacino'])+np.array(df['Idroelettrico fluente'])+np.array(df['Idroelettrico pompaggio'])
    df['Carbone'] = np.array(df['Carbone'])+np.array(df['Lignite'])
    df['Gas'] = np.array(df['Gas derivato'])+np.array(df['Gas naturale'])
    df['Eolico'] = np.array(df['Eolico offshore'])+np.array(df['Eolico onshore'])
    return df