import streamlit as st

pg = st.navigation([st.Page('Produzione_oraria.py'),st.Page('Produzione_annuale_e_capacità.py')])
st.set_page_config(layout='wide')

pg.run()