import numpy as np
import pandas as pd
import altair as alt
from AltairCharts import AltairCharts


class Plots():

    items = ['Idroelettrico pompaggio','Idroelettrico bacino','Gas naturale','Altro','Solare','Eolico onshore','Eolico offshore','Idroelettrico fluente','Rifiuti','Biomassa','Geotermico','Gas derivato','Lignite','Carbone','Nucleare']
    colors = [
        '#868686',  # Battleship gray
        '#00008B',  # Dark Blue
        '#0000FF',  # Blue
        '#FF0000',  # Red
        '#D49A79',  # Buff
        '#FFFF00',  # Yellow
        '#87CEEB',  # Sky Blue
        '#549399',  # Dark cyan
        '#3366FF',  # Light Blue
        '#75D86A',  # Light Green
        '#006400',  # Dark Green
        '#DE570A',  # Orange
        '#990000',  # Dark Crimson
        '#32161F',  # Dark Purple
        '#333333',  # Dark Gray
        '#5A2DA8',  # Indigo
    ]
    colors2 = [
        '#0000FF',  # Blue
        '#FFFF00',  # Yellow
        '#87CEEB',  # Sky Blue
        '#DE570A',  # Orange
        '#006400',  # Dark Green
        '#75D86A',  # Light Green  
        '#5A2DA8',  # Indigo
        '#FF0000',  # Red
        '#333333',  # Dark Gray
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
        tot = sum(df['Qty'])/1000
        df['Share'] = np.array(df['Qty'])/tot*100/1000
        pie = alt.Chart(df).mark_arc().encode(angle='Qty:Q',color=alt.Color('Tech',title=None,scale = alt.Scale(domain=df['Tech'],range=Plots.colors2+['#D49A79'])),
            tooltip = [alt.Tooltip('Tech',title='fonte'),alt.Tooltip('Qty',title='energia prodotta [GWh]'),alt.Tooltip('Share',title='percentuale [%]',format='.1f')],
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