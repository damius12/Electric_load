import pandas as pd
import streamlit as st
from Plots import Plots
from datetime import date
from EntsoeApi import EntsoeApi
from group_tech import group_tech
from anagraphic import country_code


entsoe = EntsoeApi()
plots = Plots()

if 'date' not in st.session_state:
    st.session_state.date = None
if 'country' not in st.session_state:
    st.session_state.country = None

with st.sidebar:
    col1,col2 = st.columns([62, 38])
    user_country = col1.selectbox('Nazione',sorted(list(country_code.keys())),index=None,label_visibility='collapsed',placeholder='Nazione')
    user_date = col2.date_input('Data',date.today()-pd.Timedelta(days=1),format='DD/MM/YYYY',max_value=date.today()-pd.Timedelta(days=1),label_visibility='collapsed')
    cols = []
    '---'
    if st.checkbox('Carico di base'):
        cols = cols + ['Nucleare','Carbone','Lignite','Gas derivato','Biomassa','Geotermico','Idroelettrico fluente','Rifiuti']
    if st.checkbox('Rinnovabili aleatorie'):
        cols = cols + ['Eolico offshore','Eolico onshore','Solare']
    if st.checkbox('Picchi e regolazione'):
        cols = cols + ['Gas naturale','Idroelettrico bacino','Idroelettrico pompaggio']
    if st.checkbox('Altro'):
        cols = cols + ['Altro']
    '---'
    if st.toggle("escludi combustibili fossili"):
        for fuel in ['Carbone','Lignite','Gas derivato','Gas naturale']:
            if fuel in cols:
                cols.remove(fuel)

if user_country != None:
    st.header(f'Generazione di elettricità in {user_country}')
    st.markdown('*fonte: entso-e*')
    error = False
    if st.session_state.date != user_date or st.session_state.country != user_country:
        try:
            st.session_state.df = entsoe.daily_generation(user_date,country_code[user_country])
            st.session_state.date = user_date
            st.session_state.country = user_country
        except Exception:
            error = True
    sums = st.session_state.df.drop(columns=['Timestamp','index','Load'])
    sums = group_tech(sums)[['Idroelettrico','Solare','Eolico','Geotermico','Biomassa','Rifiuti','Nucleare','Gas','Carbone','Altro']]
    sums = sums.sum(axis=0).reset_index()
    sums.columns = ['Tech','Qty']

    if cols == []:
        st.success("Seleziona un'opzione dal menù a sinistra",icon=':material/arrow_back:')
    elif error:
        st.error("Dati non disponibili",icon=':material/error:') 
    else:
        df = st.session_state.df[cols+['Timestamp']]
        df = df.melt(value_name='VAL',var_name='VAR',id_vars='Timestamp')
        load = st.session_state.df[['Load','Timestamp']]
        load['Label'] = ['Carico']*len(load)
        chart = plots.gen_plot(df,load)
        st.altair_chart(chart)
    pie_chart = plots.gen_pie(sums)
    st.altair_chart(pie_chart)
    

else:
    st.header('Generazione di elettricità in Europa')
    st.markdown('*fonte: entso-e*')
    st.info("Seleziona una nazione da visualizzare",icon=':material/arrow_back:')