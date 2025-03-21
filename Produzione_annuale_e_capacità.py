import numpy as np
import pandas as pd
import streamlit as st
from Plots import Plots
from order_chart import order_chart

plots = Plots()

st.header(f'Produzione annuale e capacità installata (2023)')

cols = ['Totale','Idroelettrico','Solare','Eolico','Geotermico','Biomassa','Rifiuti','Nucleare','Gas','Carbone']
if 'capacity' not in st.session_state:
    st.session_state.capacity = pd.read_csv('installed_capacity.csv')
if 'aep' not in st.session_state:
    st.session_state.aep = pd.read_csv('AEP.csv')
capacity = st.session_state.capacity
aep = st.session_state.aep

with st.sidebar:
    st.subheader('Ordina per')
    order = st.radio('ordina per',cols,label_visibility='collapsed')
tab1,tab2 = st.tabs(['Produzione annuale','Capacità installata'])
with tab1:
    st.markdown('*fonte: Eurostat*')
    chart2 = order_chart(aep,order,'aep')
    st.altair_chart(chart2)
with tab2:
    st.markdown('*fonte: entso-e*')
    chart1 = order_chart(capacity,order,'cap')
    st.altair_chart(chart1)
