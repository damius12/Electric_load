import pandas as pd
import streamlit as st
from plot import plot
from datetime import date
from anagraphic import country_code
from entsoe_query import entsoe_query


st.set_page_config(layout='wide')

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
        cols = cols + ['Nucleare','Carbone','Lignite','Gas fossile','Biomassa','Geotermico','Idroelettrico fluente','Rifiuti']
    if st.checkbox('Rinnovabili aleatorie'):
        cols = cols + ['Eolico offshore','Eolico onshore','Solare']
    if st.checkbox('Picchi e regolazione'):
        cols = cols + ['Gas naturale','Idroelettrico bacino','Idroelettrico pompaggio']
    if st.checkbox('Altro'):
        cols = cols + ['Altro']
    '---'
    if st.toggle("escludi combustibili fossili"):
        for fuel in ['Carbone','Lignite','Gas fossile','Gas naturale']:
            if fuel in cols:
                cols.remove(fuel)

if user_country != None:
    st.header(f'Generazione di elettricità in {user_country}')
    st.markdown('*fonte: entso-e*')
    error = False
    if st.session_state.date != user_date or st.session_state.country != user_country:
        try:
            st.session_state.df = entsoe_query(user_date,country_code[user_country])
            st.session_state.date = user_date
            st.session_state.country = user_country
        except Exception:
            error = True

    if cols == []:
        st.info("Seleziona un'opzione dal menù a sinistra",icon=':material/arrow_back:')
    elif error:
        st.error("Dati non disponibili",icon=':material/error:') 
    else:
        df = st.session_state.df[cols].reset_index()
        if len(df)>24:
            df['Hour'] = df['index'].apply(lambda x: x.hour)
            df = df.groupby(['Hour']).mean()
        df = df.melt(value_name='VAL',var_name='VAR',id_vars='index')
        df['Timestamp'] = df['index']
        for i in df.index:
            df.at[i,'Timestamp'] = df.at[i,'index'] + pd.Timedelta(hours=0.5)
        load = st.session_state.df[['Load']].reset_index()
        if len(load)>24:
            load['Hour'] = load['index'].apply(lambda x: x.hour)
            load = load.groupby(['Hour']).mean()
        load['Label'] = ['Carico']*len(load)
        load['Timestamp'] = load['index']
        for i in load.index:
            load.at[i,'Timestamp'] = load.at[i,'index'] + pd.Timedelta(hours=0.5)

        chart = plot(df,load)
        st.altair_chart(chart)

else:
    st.header('Generazione di elettricità in Europa')
    st.markdown('*fonte: entso-e*')
    st.info("Seleziona una nazione da visualizzare",icon=':material/arrow_back:')