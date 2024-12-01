import numpy as np
import pandas as pd
import streamlit as st
from Plots import Plots
from datetime import date
from EntsoeApi import EntsoeApi

entsoe = EntsoeApi()
plots = Plots()

st.header('Capacità installata in Europa')

cols = ['Totale','Idroelettrico','Solare','Eolico','Geotermico','Biomassa','Rifiuti','Nucleare','Gas','Carbone']
csv_name = f'installed_capacity_{date.today().year}.csv'
if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv(csv_name)
    except Exception:
        df = entsoe.installed_capacity()
        df['Idroelettrico'] = np.array(df['Idroelettrico bacino'])+np.array(df['Idroelettrico fluente'])+np.array(df['Idroelettrico pompaggio'])
        df['Carbone'] = np.array(df['Carbone'])+np.array(df['Lignite'])
        df['Gas'] = np.array(df['Gas derivato'])+np.array(df['Gas naturale'])
        df['Eolico'] = np.array(df['Eolico offshore'])+np.array(df['Eolico onshore'])
        df['Totale'] = df.iloc[:,1:].sum(axis=1)
        df = df[['Nazione']+cols]
        df.to_csv(csv_name,index=False)
        st.session_state.df = df
df = st.session_state.df

with st.sidebar:
    st.subheader('Ordina per')
    order = st.radio('ordina per',cols,label_visibility='collapsed')
df = df.sort_values(by=order,ascending=False)
order_list = list(df['Nazione'])

df = df.drop(columns=['Totale'])
df = df.melt(id_vars=['Nazione'],var_name='Src',value_name='Qty')
chart = plots.cap_plot(df,cols,order_list,order)
st.altair_chart(chart)
