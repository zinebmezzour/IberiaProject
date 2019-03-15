#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 11:02:11 2019

@author: zinebmezzour
"""

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import psycopg2 as pg
from dash.dependencies import Input, Output
import pandas.io.sql as psql
import dash_table_experiments as dt


conn = pg.connect("postgres://bfkubnkgitlzqd:a0f9bca6a8136865f54a307c8cb18b6a36b541640e63f524d7a0938d59d4ff16@ec2-184-73-216-48.compute-1.amazonaws.com:5432/dcsrq4nf3tt2vq")

df = pd.read_sql_query('select * from "App";', conn)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


colors = {
    'background': '#c7f6fc',
    'text': '#111111'
}



app.layout = html.Div(children=[
        
    html.H1(children='IBERIA DASHBOARD',
    style={'color':colors['text']}),
    
    html.Div(children = 'Application !',
    style={'color':colors['text']}),
    
    generate_table(df)])
    
   



if __name__ == '__main__':
    app.run_server(debug=True)

    
    
    