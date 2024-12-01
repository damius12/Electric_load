import numpy as np
import pandas as pd
import streamlit as st
from Plots import Plots
from EntsoeApi import EntsoeApi

entsoe = EntsoeApi()
plots = Plots()

cols = ['Nazione','Idroelettrico','Solare','Eolico','Geotermico','Biomassa','Rifiuti','Nucleare','Gas','Carbone']
if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv('installed_capacity.csv')
    except Exception:
        df = entsoe.installed_capacity()
        df['Idroelettrico'] = np.array(df['Idroelettrico bacino'])+np.array(df['Idroelettrico fluente'])+np.array(df['Idroelettrico pompaggio'])
        df['Carbone'] = np.array(df['Carbone'])+np.array(df['Lignite'])
        df['Gas'] = np.array(df['Gas derivato'])+np.array(df['Gas naturale'])
        df['Eolico'] = np.array(df['Eolico offshore'])+np.array(df['Eolico onshore'])
        df['Totale'] = df.iloc[:,1:].sum(axis=1)
        df = df[cols + ['Totale']]
        df.to_csv('installed_capacity.csv',index=False)
        st.session_state.df = df
df = st.session_state.df


df = df.sort_values(by='Totale')
df = df.melt(id_vars=['Nazione'],var_name='Src',value_name='Qty')
chart = plots.cap_plot(df,cols)
st.altair_chart(chart)
