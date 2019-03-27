#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 11:02:11 2019

@author: zinebmezzour
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_auth
import dash_html_components as html
import dash_table
from datetime import datetime as dt
from datetime import date, timedelta
import pandas as pd
import psycopg2 as pg
import pandas.io.sql as psql
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

conn = pg.connect("postgres://woneckmtfjjwnc:31b3c946995783dc7096969c88bc2f841fab2d73e0b2c159267ebc8f53d54255@ec2-75-101-133-29.compute-1.amazonaws.com:5432/d55rsv1snnhe39")

dff=pd.read_sql_query('select * from "JanFeb";', conn)
df = pd.read_sql_query('select "IncidentStatus","IncidentCode","DomainGroup", "Priority" from "JanFeb";', conn)
df1 = pd.read_sql_query('select "CriticalStatus", "SupportDpt","SLA","ApplicationCode" from "App";', conn)

#Add Features
dff['year'] = pd.DatetimeIndex(dff['CreationDate']).year
dff['month'] = pd.DatetimeIndex(dff['CreationDate']).month

c_df=pd.read_sql_query('select * from "critic";', conn)
c_df['year'] = pd.DatetimeIndex(c_df['CreationDate']).year
c_df['month'] = pd.DatetimeIndex(c_df['CreationDate']).month




domain_options=dff["Domain"].unique()
months_options=dff["month"].unique()


c_domain_options=c_df["Domain"].unique()
c_months_options=c_df["month"].unique()


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/dashboard/')
server = app.server
app.config.suppress_callback_exceptions = True


VALID_USERNAME_PASSWORD_PAIRS = [
    ['Araceli', 'AccessAraceli']
]


auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


app.layout = html.Div([
html.Div([

html.Div([ 
    html.Span("Iberia Dashboard", className='app-title'),
    
#    html.Div(
#        html.Img(src=' ',height="100%"),
#        style={"float":"right","height":"100%"})
        ],
   

    className="row header" 
    ), 
 

html.Div([
    dcc.Tabs(
        id="tabs",
        style={"height":"20","verticalAlign":"middle"},
        children=[
            dcc.Tab(label="General Overview", value="general_tab"),
            dcc.Tab(label="Performance", value="performance_tab"),
        ],
        value ="general_tab"
    )
    ],
    className ="row tabs_div"
    ),

 #   html.Div(get_overview().to_json(orient="split"),
 #   id="general_df",
 #   style={"display":"none"},
 #   ),
    
 #   html.Div(get_performance().to_json(orient="split"),
 #   id="performance_df",
 #   style={"display":"none"},
 #   ),


    html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),

    html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
    html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
    html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
    html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
    html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
    html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    
    ],
    className="row",
    style={"margin": "0%"},
    ),


dash_table.DataTable(
id='table',
columns=[{"name": i, "id": i} for i in df.columns],
data=df.to_dict("rows"),
)
]
)

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])

def render_content(tab):
    if tab == "general_tab":
        return general_layout
    elif tab == "performance_tab":
       return performance_layout
    else:
        return general_layout



#GENERAL LAYOUT


general_layout = html.Div([
    html.H2("Overview Incidences"),

    html.Div([
        dcc.Dropdown(
        id='dropdown-1',
        options=[{'label': i, 'value': i} for i in dff['year'].unique()],
        value=2018
        )
    ]),


    dcc.Graph(id='graph1'),


    html.Div([
        dcc.Dropdown(
        id='dropdown-2',
        options=[{'label': i, 'value': i} for i in dff['year'].unique()],
        value=2018
        )
    ]),

    dcc.Graph(id='graph2'),


    html.Div([
        dcc.Dropdown(
        id='dropdown-3',
        options=[{'label': i, 'value': i} for i in c_domain_options],
        value='AIRPORTS'
        )
    ]),

    html.Div([
        dcc.Dropdown(
        id='dropdown-4',
        options=[{'label': i, 'value': i} for i in c_months_options],
        value=1
        )
    ]),


    dcc.Graph(id='graph3'),

],
className= 'six columns'
)


@app.callback(
    Output('graph3', 'figure'),
    [Input('dropdown-3', 'value'),
     Input('dropdown-4','value')
    ])

def graph_3(input,other):
    print(input)
    print(other)
    fil= c_df[(c_df['Domain'] == input) & (c_df['month'] == other)]
    
 #   prio=filtered_df['Priority'].unique()
    domain = fil['Domain'].unique()


    
    traces = []

    for i in domain:
        
        app = fil[fil['Domain']==i].groupby('Application').size()
        nb_app = fil[fil['Domain']==i]['Application'].unique()

        traces.append(go.Bar(
            x=nb_app,
            y=app,
            name=i,

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type':'category', 'title': input},
            yaxis={'title': 'Number of Incidents'},
            barmode="group",
            legend={'x': 0, 'y': 1},
            hovermode='closest',
        )}




@app.callback(
    Output('graph2', 'figure'),
    [Input('dropdown-2', 'value') 
    ])

def graph_2(input):

    filtered_df = dff[dff['year'] == input]
    prio=filtered_df['Priority'].unique()
    
    traces = []

    for i in prio:
        
        incidents =filtered_df[filtered_df['Priority']==i].groupby('month').size()
        months=filtered_df[filtered_df['Priority']==i]['month'].unique()

        traces.append(go.Bar(
            x=months,
            y=incidents,
            name=i,

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type':'category', 'title': 'Month'},
            yaxis={'title': 'Number of Incidents'},
            barmode="group",
            legend={'x': 0, 'y': 1},
            hovermode='closest',

        )}


@app.callback(
    Output('graph1', 'figure'),
    [Input('dropdown-1', 'value') 
    ])

def graph_maker1(input1):
    
    filtered_df = dff[dff['year'] == input1]
    
    prio=filtered_df['Priority'].unique()
    
    traces = []
    
    for i in prio:
        
        incidents =filtered_df[filtered_df['Priority']==i].groupby('CreationDate').size()
        months=filtered_df[filtered_df['Priority']==i]['month'].unique()

#        days=filtered_df[filtered_df['Priority']==i]['CreationDate'].unique()

        print(months)

        traces.append(go.Scatter(
#            x=days
            x=months,
            y=incidents,
            text=prio,
            mode='lines+markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'red'}
            },
            name= i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'category', 'title': 'Months'},
            yaxis={'title': 'Incidents'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }



#df1 = pd.read_sql_query('select "CriticalStatus", "SupportDpt","SLA","ApplicationCode" from "App";', conn)

#PERFORMANCE LAYOUT
performance_layout = html.Div([
        html.H2("Overview App"),

            html.Div([
    
    
                html.Div([ 
                    html.H3('Graph1'),
                    
                    html.Div([
                        dcc.Dropdown(
                        id='dropdown-11',
                        options=[{'label': i, 'value': i} for i in dff['year'].unique()],
                        value=2018
                        )
                    ]),

                    dcc.Graph(id='graph11'),
                        ],
                    className='six columns'),


                html.Div([
    
                        html.H3('Graph2'), 


                        html.Div([
                        dcc.Dropdown(
                        id='dropdown-22',
                        options=[{'label': i, 'value': i} for i in dff['year'].unique()],
                        value=2018
                        )
                            ]),

                        dcc.Graph(id='graph22'),
                            ],
                        className="six columns"
                            ),
                    
            ],
            className="row"),


            html.Div([
                html.H3('Graph3'),

                html.Div([
                    dcc.Dropdown(
                    id='dropdown-33',
                    options=[{'label': i, 'value': i} for i in c_domain_options],
                    value='AIRPORTS'
                    )
                ]),

                html.Div([
                    dcc.Dropdown(
                    id='dropdown-44',
                    options=[{'label': i, 'value': i} for i in c_months_options],
                    value=1
                    )
                ]),


                dcc.Graph(id='graph33'),
            
            ],
            className='row'),

],

)


@app.callback(
    Output('graph33', 'figure'),
    [Input('dropdown-33', 'value'),
     Input('dropdown-44','value')
    ])

def graph_33(input,other):
    print(input)
    print(other)
    fil= c_df[(c_df['Domain'] == input) & (c_df['month'] == other)]
    
 #   prio=filtered_df['Priority'].unique()
    domain = fil['Domain'].unique()


    
    traces = []

    for i in domain:
        
        app = fil[fil['Domain']==i].groupby('Application').size()
        nb_app = fil[fil['Domain']==i]['Application'].unique()

        traces.append(go.Bar(
            x=nb_app,
            y=app,
            name=i,

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type':'category', 'title': input},
            yaxis={'title': 'Number of Incidents'},
            barmode="group",
            legend={'x': 0, 'y': 1},
            hovermode='closest',
        )}




@app.callback(
    Output('graph22', 'figure'),
    [Input('dropdown-22', 'value') 
    ])

def graph_22(input):
    filtered_df = dff[dff['year'] == input]
    prio=filtered_df['Priority'].unique()
    
    traces = []

    for i in prio:
        
        incidents =filtered_df[filtered_df['Priority']==i].groupby('month').size()
        months=filtered_df[filtered_df['Priority']==i]['month'].unique()

        traces.append(go.Bar(
            x=months,
            y=incidents,
            name=i,

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type':'category', 'title': 'Month'},
            yaxis={'title': 'Number of Incidents'},
            barmode="group",
            legend={'x': 0, 'y': 1},
            hovermode='closest',
        )}


@app.callback(
    Output('graph11', 'figure'),
    [Input('dropdown-11', 'value') 
    ])

def graph_maker11(input1):
    
    filtered_df = dff[dff['year'] == input1]
    
    prio=filtered_df['Priority'].unique()
    
    traces = []
    
    for i in prio:
        
        incidents =filtered_df[filtered_df['Priority']==i].groupby('CreationDate').size()
        months=filtered_df[filtered_df['Priority']==i]['month'].unique()

#        days=filtered_df[filtered_df['Priority']==i]['CreationDate'].unique()

        print(months)

        traces.append(go.Scatter(
#            x=days
            x=months,
            y=incidents,
            text=prio,
            mode='lines+markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'red'}
            },
            name= i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'category', 'title': 'Months'},
            yaxis={'title': 'Incidents'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    
    
    
    
    
    
   


if __name__ == '__main__':
    app.run_server(debug=True)