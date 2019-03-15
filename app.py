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



app = dash.Dash(__name__)
server = app.server

conn = pg.connect("postgres://bfkubnkgitlzqd:a0f9bca6a8136865f54a307c8cb18b6a36b541640e63f524d7a0938d59d4ff16@ec2-184-73-216-48.compute-1.amazonaws.com:5432/dcsrq4nf3tt2vq")

df = pd.read_sql_query('select * from "App";', conn)


df = df.drop(['Description','Resolution'], axis=1)



app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
    id='datatable-interactivity',
    columns=[
            {"name": i, "id": i, "deletable":True } for i in df.columns],
    
    data=df.to_dict("rows"),
    editable=True,
    filtering =True,
    sorting=True,
    sorting_type="multi",
    row_selectable="multi",
    row_deletable=True,
    selected_rows=[],
    pagination_mode="fe",
        pagination_settings={
                "displayed_pages": 1,
                "current_page": 0,
                "page_size": 35,
            },
        navigation="page",
 

    ),
    html.Div(id='datatable-interactivity-container')


])
    
    
@app.callback(
        Output('datatable-interactivity-container',"children"),
        [Input('datatable-interactivity',"derived_virtual_data"),
         Input('datatable-interactivity',"derived_virtual_selected_rows")]
        )

def update_graph(rows,derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
   
    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)
    
    colors = []
    for i in range(len(dff)):
        if i in derived_virtual_selected_rows:
            colors.append("#7FDBFF")
        else:
            colors.append("#0074D9")
    
    
    return html.Div(
            [
                dcc.Graph(
                        id=column,
                        figure={
                                "data": [
                                        {
                            "x": dff["Priority"],
                            # check if column exists - user may have deleted it
                            # If `column.deletable=False`, then you don't
                            # need to do this check.
                            "y": dff[column] if column in dff else [],
                            "type": "bar",
                            "marker": {"color": colors},
                                                }
                                        ],
        
                "layout": {
                            "xaxis": {"automargin": True},
                            "yaxis": {"automargin": True},
                            "height": 250,
                            "margin": {"t": 10, "l": 10, "r": 10},
                            },
                            },
                            )
                    for column in ["Priority","Status","AssignedGroup"]
                                        ])
    
    
        
        
if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    