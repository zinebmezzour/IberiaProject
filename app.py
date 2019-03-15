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





app = dash.Dash(__name__)
server = app.server

conn = pg.connect("postgres://bfkubnkgitlzqd:a0f9bca6a8136865f54a307c8cb18b6a36b541640e63f524d7a0938d59d4ff16@ec2-184-73-216-48.compute-1.amazonaws.com:5432/dcsrq4nf3tt2vq")

df = pd.read_sql_query('select * from "App";', conn)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
        
    html.H1(children='Ibe-App'),
    
    html.Div(children = 'Welcome !')])



if __name__ == '__main__':
    app.run_server(debug=True)

    
    
    