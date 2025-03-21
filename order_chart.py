import pandas as pd
from Plots import Plots

cols = ['Totale','Idroelettrico','Solare','Eolico','Geotermico','Biomassa','Rifiuti','Nucleare','Gas','Carbone']

def order_chart(df:pd.DataFrame,order,type:str):
    plots = Plots()
    df = df.sort_values(by=order,ascending=False)
    order_list = list(df['Nazione'])
    df = df.drop(columns=['Totale'])
    df = df.melt(id_vars=['Nazione'],var_name='Src',value_name='Qty')
    chart = plots.cap_plot(df,cols,order_list,order) if type == 'cap' else plots.aep_plot(df,cols,order_list,order)
    return chart