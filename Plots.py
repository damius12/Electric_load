import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from AltairCharts import AltairCharts


class Plots():

    items = ['Idroelettrico pompaggio','Idroelettrico bacino','Gas naturale','Altro','Solare','Eolico onshore','Eolico offshore','Idroelettrico fluente','Rifiuti','Biomassa','Geotermico','Gas derivato','Lignite','Carbone','Nucleare']
    colors = [
        '#868686',  # Carico
        '#00008B',  # Idroelettrico pompaggio
        '#0B3AC7',  # Idroelettrico bacino
        '#737373',  # Gas
        '#FFFFFF',  # Altro
        '#ECCC28',  # Solare
        '#9AF7E7',  # Eolico onshore
        '#54B8A7',  # Eolico offshore
        '#478AFF',  # Idroelettrico fluente
        '#153B0B',  # Rifiuti
        '#25A920',  # Biomassa
        '#DE570A',  # Geotermico
        '#808080',  # Gas derivato
        '#45313D',  # Lignite
        '#313131',  # Carbone
        '#B891FC',  # Nucleare
    ]
    colors2 = [
        '#0B3AC7',  # Idroelettrico
        '#ECCC28',  # Solare
        '#9AF7E7',  # Eolico
        '#DE570A',  # Geotermico
        '#25A920',  # Biomassa
        '#153B0B',  # Rifiuti
        '#B891FC',  # Nucleare
        '#737373',  # Gas
        '#313131',  # Carbone
        '#FFFFFF',  # Altro
    ]

    def gen_plot(self, df:pd.DataFrame, load:pd.DataFrame) -> alt.Chart:

        category_order_map = {category: index for index, category in enumerate(Plots.items)}
        df['Order'] = df['VAR'].map(category_order_map)

        altair = AltairCharts(plot_h = 480,plot_w = 1100,x_label_format = '%H:%M',x_title=None)
        load_chart = alt.Chart(load).mark_bar(opacity=0.1).encode(
            x='hours(Timestamp):T',
            y='Load',
            color=alt.Color('Label',title=None, legend = alt.Legend(orient='right',symbolOpacity=1)),
            tooltip = [alt.Tooltip('hours(Timestamp)',title='orario',format='%H:%M'),alt.Tooltip('Load',title='carico [MW]',format='.0f')]
            )
        gen_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('hours(Timestamp):T',title=None),
            y=alt.Y('VAL',title='Potenza [MW]'),
            color=alt.Color(
                'VAR:N',
                scale = alt.Scale(domain=['Carico']+Plots.items,range=Plots.colors),
            ),
            order = alt.Order('Order:Q',sort='descending'),
            tooltip = [alt.Tooltip('VAR',title='fonte'),alt.Tooltip('VAL',title='potenza [MW]',format='.0f')]
            )
        chart =  altair.main_plot(load_chart,gen_chart)
        return chart
    
    def gen_pie(self, df:pd.DataFrame) -> alt.Chart:
        category_order_map = {category: index for index, category in enumerate(df['Tech'])}
        df['Order'] = df['Tech'].map(category_order_map)
        df['Qty'] = np.array(df['Qty'])/1000
        tot = sum(df['Qty'])
        df['Share'] = np.array(df['Qty'])/tot*100
        pie = alt.Chart(df).mark_arc().encode(angle='Qty:Q',color=alt.Color('Tech',title=None,scale = alt.Scale(domain=df['Tech'],range=Plots.colors2+['#D49A79'])),
            tooltip = [alt.Tooltip('Tech',title='fonte'),alt.Tooltip('Qty',title='energia prodotta [GWh]',format='.1f'),alt.Tooltip('Share',title='percentuale [%]',format='.1f')],
            order = 'Order:Q'
            )
        side = 400
        chart = pie.properties(height=side,width=side*4/3)
        return chart