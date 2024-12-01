import pandas as pd
import streamlit as st
from Plots import Plots
from EntsoeApi import EntsoeApi


entsoe = EntsoeApi()
plots = Plots()

try:
    df = pd.read_csv('installed_capacity.csv')
except Exception:
    df = entsoe.installed_capacity()
    df = df.drop(index=[0])
    df.to_csv('installed_capacity.csv',index=False)

df = df.melt(id_vars=['Nazione'],var_name='Tech',value_name='Qty')
chart = plots.cap_plot(df)
st.altair_chart(chart)
