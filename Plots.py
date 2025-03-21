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
        '#0000FF',  # Idroelettrico bacino
        '#FF0000',  # Gas
        '#D49A79',  # Altro
        '#FFFF00',  # Solare
        '#87CEEB',  # Eolico onshore
        '#549399',  # Eolico offshore
        '#3366FF',  # Idroelettrico fluente
        '#75D86A',  # Rifiuti
        '#006400',  # Biomassa
        '#DE570A',  # Geotermico
        '#990000',  # Gas derivato
        '#32161F',  # Lignite
        '#333333',  # Carbone
        '#5A2DA8',  # Nucleare
    ]
    colors2 = [
        '#0000FF',  # Idroelettrico
        '#FFFF00',  # Solare
        '#87CEEB',  # Eolico
        '#DE570A',  # Geotermico
        '#006400',  # Biomassa
        '#75D86A',  # Rifiuti
        '#5A2DA8',  # Nucleare
        '#FF0000',  # Gas
        '#333333',  # Carbone
    ]

    def gen_plot(self, df:pd.DataFrame, load:pd.DataFrame) -> alt.Chart:

        category_order_map = {category: index for index, category in enumerate(Plots.items)}
        df['Order'] = df['VAR'].map(category_order_map)

        altair = AltairCharts(plot_h = 480,plot_w = 1100,x_label_format = '%H:%M',x_title=None)
        load_chart = alt.Chart(load).mark_bar(opacity=0.1).encode(
            x='hours(Timestamp):T',
            y='Load',
            color=alt.Color('Label',title=None, legend = alt.Legend(orient='right',symbolOpacity=1)),
            tooltip = [alt.Tooltip('hours(Timestamp)',title='orario',format='%H:%M'),alt.Tooltip('Load',title='carico [MW]')]
            )
        gen_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('hours(Timestamp):T',title=None),
            y=alt.Y('VAL',title='Potenza [MW]'),
            color=alt.Color(
                'VAR:N',
                scale = alt.Scale(domain=['Carico']+Plots.items,range=Plots.colors),
            ),
            order = alt.Order('Order:Q',sort='descending'),
            tooltip = [alt.Tooltip('VAR',title='fonte'),alt.Tooltip('VAL',title='potenza [MW]')]
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

    def cap_plot(self, df:pd.DataFrame, cols:list, order_list:list, leading:str) -> alt.Chart:
        altair = AltairCharts(plot_h = 1400, plot_w = 1000)
        d = alt.Chart(df).mark_bar().encode(
            y=alt.Y('Nazione:N',title=None,sort=order_list),
            x=alt.X('Qty:Q',title='Potenza installata [MW]'),
            color=alt.Color(
                'Src:N',
                scale = alt.Scale(domain=cols[1:],range=Plots.colors2),
                legend = None,
            ),
            tooltip = [alt.Tooltip('Src',title='fonte'),alt.Tooltip('Qty',title='potenza [MW]')],
            opacity = alt.condition(alt.datum.Src == leading, alt.value(1),alt.value(0.2)) if leading != 'Totale' else alt.value(1),
            order = alt.Order('Order:Q',sort='descending')
            )
        chart = altair.main_plot(d)
        return chart

    def aep_plot(self, df:pd.DataFrame, cols:list, order_list:list, leading:str) -> alt.Chart:
        altair = AltairCharts(plot_h = 1400, plot_w = 1000)
        d = alt.Chart(df).mark_bar().encode(
            y=alt.Y('Nazione:N',title=None,sort=order_list),
            x=alt.X('Qty:Q',title='Generazione annua [GWh]'),
            color=alt.Color(
                'Src:N',
                scale = alt.Scale(domain=cols[1:],range=Plots.colors2),
                legend = None,
            ),
            tooltip = [alt.Tooltip('Src',title='fonte'),alt.Tooltip('Qty',title='Quantità [GWh]')],
            opacity = alt.condition(alt.datum.Src == leading, alt.value(1),alt.value(0.2)) if leading != 'Totale' else alt.value(1),
            order = alt.Order('Order:Q',sort='descending')
            )
        chart = altair.main_plot(d)
        return chart