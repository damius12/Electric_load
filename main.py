import streamlit as st

pg = st.navigation([st.Page('Generazione_oraria.py'),st.Page('Capacità_installata.py')])
st.set_page_config(layout='wide')

pg.run()