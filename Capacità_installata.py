import pandas as pd
import streamlit as st
from Plots import Plots
from datetime import date
from EntsoeApi import EntsoeApi
from group_tech import group_tech

entsoe = EntsoeApi()
plots = Plots()

st.header('Capacità installata in Europa')

cols = ['Totale','Idroelettrico','Solare','Eolico','Geotermico','Biomassa','Rifiuti','Nucleare','Gas','Carbone']
csv_name = f'installed_capacity_{date.today().year}.csv'
if 'data' not in st.session_state:
    try:
        st.session_state.data = pd.read_csv(csv_name)
    except Exception:
        query = entsoe.installed_capacity()
        query = group_tech(query)
        query['Totale'] = query.iloc[:,1:].sum(axis=1)
        query = query[['Nazione']+cols]
        query.to_csv(csv_name,index=False)
        st.session_state.data = query
df = st.session_state.data

with st.sidebar:
    st.subheader('Ordina per')
    order = st.radio('ordina per',cols,label_visibility='collapsed')
df = df.sort_values(by=order,ascending=False)
order_list = list(df['Nazione'])

df = df.drop(columns=['Totale'])
df = df.melt(id_vars=['Nazione'],var_name='Src',value_name='Qty')
chart = plots.cap_plot(df,cols,order_list,order)
st.altair_chart(chart)
