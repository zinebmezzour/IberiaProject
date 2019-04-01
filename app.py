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
from datetime import datetime as dt
from datetime import date, timedelta
import pandas as pd
import psycopg2 as pg
import pandas.io.sql as psql
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

conn = pg.connect("postgres://woneckmtfjjwnc:31b3c946995783dc7096969c88bc2f841fab2d73e0b2c159267ebc8f53d54255@ec2-75-101-133-29.compute-1.amazonaws.com:5432/d55rsv1snnhe39")

dff=pd.read_sql_query('select * from "JanFeb";', conn)
c_df=pd.read_sql_query('select * from "critic";', conn)
jf_df=pd.read_sql_query('select * from "janfebraised";', conn)
servAvail_df=pd.read_sql_query('select * from "ServAvailJF";', conn)
servRelial_df=pd.read_sql_query('select * from "ServReliabilityJF";', conn)
MTTR_df=pd.read_sql_query('select * from "MTTR_per_Service";', conn)



#Add Features
dff['year'] = pd.DatetimeIndex(dff['CreationDate']).year
dff['month'] = pd.DatetimeIndex(dff['CreationDate']).month

c_df['year'] = pd.DatetimeIndex(c_df['CreationDate']).year
c_df['month'] = pd.DatetimeIndex(c_df['CreationDate']).month


jf_df['year'] = pd.DatetimeIndex(jf_df['CreationDate']).year
jf_df['month'] = pd.DatetimeIndex(jf_df['CreationDate']).month




critical_services_options= servAvail_df['Service'].unique()

domain_options=dff["Domain"].unique()
months_options=dff["month"].unique()
service_options=dff["Service"].unique()



c_domain_options=c_df["Domain"].unique()
c_months_options=c_df["month"].unique()



jann = jf_df[jf_df['month']==1]
jann['Month'] = jann['month'].apply(lambda x:'January')
jann= jann.reset_index()


fevrier = jf_df[jf_df['month']==2]
fevrier['Month'] = fevrier['month'].apply(lambda x:'February')
fevrier= fevrier.reset_index()


raised_by_month = jann.append(fevrier, ignore_index=True)



def generate_table(dataframe, max_rows=10):
    '''Given dataframe, return template generated using Dash components
    '''
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def indicator(color, text, id_value):
    return html.Div(
        [
            
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value",
                style={'color': 'red','fontSize': 23, 'opacity':0.6}

            ),

        ],
        className="four columns indicator",
        style={'height': 100}
        
    )


APP_NAME = 'Iberia Dashboard App'
APP_URL = 'https://iberia-dashboard.herokuapp.com'



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True


VALID_USERNAME_PASSWORD_PAIRS = [
    ['Araceli', 'AccessAraceli'],
    ['User1', 'Access1'],
    ['User2', 'Access2'],
    ['User3', 'Access3']
]



auth = dash_auth.PlotlyAuth(
    app,
    APP_NAME,
    'private',
    APP_URL
)

#auth = dash_auth.BasicAuth(
#    app,
#    VALID_USERNAME_PASSWORD_PAIRS
#)


app.layout = html.Div([
html.Div([

html.Div([ 
    html.Span("Iberia Dashboard", className='app-title'),
    
    html.Div(
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/5/5e/Logo_iberia_2013.png',height="100%"),
        style={"float":"right","height":"100%"})
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


def graph_2():

  
    prio=raised_by_month['Priority'].unique()
    
    traces = []

    for i in prio:
        
        incidents =raised_by_month[raised_by_month['Priority']==i].groupby('month').size()
        months=raised_by_month[raised_by_month['Priority']==i]['Month'].unique()
        

        traces.append(go.Bar(
            x=months,
            y=incidents,
            name=i,
            text=incidents,
            textposition='auto',
            marker=go.bar.Marker(
                                opacity=0.6
                                ),

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            
            xaxis={'type':'category', 'title': 'Month'},
            yaxis={'title': 'Number of Incidents'},
            barmode="group",
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            margin=go.layout.Margin(l=60, r=40, t=40, b=100),

        )}

#GENERAL LAYOUT


general_layout = html.Div([


    html.Div([
        html.H6("Indicators of the month:"),

        dcc.Dropdown(
            id='dropdown-1',
            options=[{'label': 'January', 'value': 'January'},{'label': 'February', 'value': 'February'}],
            value='January'
                )

    ],className='row'),
    
    html.Div([
        html.Div([ 
        indicator('blue','Total Number of Incidences Raised','indicator1'),
        ]),

        html.Div([ 
        indicator('blue','Total Number of Incidences in Critical Services','indicator2'),
        ]),
        
        html.Div([ 
        indicator('blue','Total Number of Severity 1','indicator3'),
        ]),


    ], className='row'),

    html.Div([ 

        html.Div([ 



            html.Div([ 
                html.H4('Total Incidents Raised per Severity'),


                dcc.Graph(
                    figure=go.Figure(graph_2()), 
            
                    id='graph1'),

                

            ], className='six columns'),

            html.Div([
                html.H4('Total Incidents Raised per Critical Services'),


                dcc.Graph(
                    figure=go.Figure(
                    data=[
                         go.Bar(
                            x= ['.COM', 'BOOKINGS & INVENTORY SYS', 'CHECK IN SYS',
       'CREW MNGT', 'FLIGHT DISPATCHING',
       'FLIGHT TRACKING & CONTROL', 'LOAD PLAN',
       'MAD-HUB OPERATIONAL MNGT SYS', 'MRO SAP',
       'STATIONS OPERATIONAL MNGT SYS', 'TICKETING SYS'],
                            y= [147, 52, 111, 30, 11, 54, 10, 84, 187, 146, 80],
                            name='January',
                            text=[147, 52, 111, 30, 11, 54, 10, 84, 187, 146, 80],
                            textposition = 'auto',
                            marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                                    )
                     ),
                        go.Bar(
                            x= ['.COM', 'BOOKINGS & INVENTORY SYS', 'CHECK IN SYS',
       'CREW MNGT', 'FLIGHT DISPATCHING',
       'FLIGHT TRACKING & CONTROL', 'LOAD PLAN',
       'MAD-HUB OPERATIONAL MNGT SYS', 'MRO SAP',
       'STATIONS OPERATIONAL MNGT SYS', 'TICKETING SYS'],
                            y= [195, 49, 121, 32, 13, 53, 16, 71, 152, 111, 66],
                            name='February',
                            text=[195, 49, 121, 32, 13, 53, 16, 71, 152, 111, 66],
                            textposition = 'auto',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)',
                                opacity=0.6
                                )
                            )
                            ],
                            layout=go.Layout(
                                title = 'All Severities',
                                showlegend=True,
        
                                legend=go.layout.Legend(
                                    x=1.0,
                                    y=1.0
                                ),
                                margin=go.layout.Margin(l=60, r=40, t=40, b=100)
                            )
                        ),
                       
                        id='graph2'
                    )
                    

            ], className='six columns'),

        ], className='row'),


       html.Div([ 


       html.Div([
                html.H4("Total Incidents per Status"),
           dcc.Graph(
                    figure=go.Figure(
                    data=[
                         go.Bar(
                            x= ['Raised','Closed','Backlog'],
                            y= [10035,9916,1031],
                            name='January',
                            text=[10035,9916,1031],
                            textposition = 'auto',
                            marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                                    )
                     ),
                        go.Bar(
                            x= ['Raised','Closed','Backlog'],
                            y= [8836,8012,1152],
                            name='February',
                            text= [8836,8012,1152],
                            textposition = 'auto',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)',
                                opacity=0.6
                                ),
                            )
                            ],
                            layout=go.Layout(
                                title = 'All Severities',
                                showlegend=True,
                                xaxis={'title':'Status'},
                                yaxis={'title': 'Number of Incidents'},
                               
                                legend=go.layout.Legend(
                                    x=1,
                                    y=1.0
                                ),
                                margin=go.layout.Margin(l=60, r=40, t=40, b=100)
                            )
                        ),
                        style={'height': 500},
                        id='availability_graph'
                    )
               ],
            className='six columns'),




       html.Div([
                html.H4('Password Related Incidents'),
           dcc.Graph(
                    figure=go.Figure(
                    data=[
                         go.Bar(
                            x= ['Password Related','Non-Password Related'],
                            y= [3918,6117],
                            name='January',
                            text=[3918,6117],
                            textposition = 'auto',
                            marker=dict(
                                color='rgb(55, 83, 109)',
                            
                            ),
                            
                     ),
                        go.Bar(
                            x= ['Password Related','Non-Password Related'],
                            y= [3279,5557],
                            name='February',
                            text= [3279,5557],
                            textposition = 'auto',
                            marker=dict(
                                color='rgb(26, 118, 255)',
                            
                            ),
                            opacity=0.6


                           
                            )
                            ],
                            layout=go.Layout(
                            
                                showlegend=True,
                                yaxis={'title': 'Number of Incidents'},
                               
                                legend=go.layout.Legend(
                                    x=1,
                                    y=1.0
                                ),
                                margin=go.layout.Margin(l=60, r=40, t=40, b=100)
                            )
                        ),
                        style={'height': 500},
                        id='Password_graph'
                    )
               ],
            className='six columns'),







            ], className='row') 

],
className= 'twelve columns'
),

])

@app.callback(
    Output("indicator1", "children"), [Input('dropdown-1', 'value')]
)

def total_amount(input):
    print(input)
    if input == "January":
        total_amount = "10'035"
    if input == "February":
        total_amount = "8'836"

    else:
        total_amount = "10'035"
    
    return total_amount


@app.callback(
    Output("indicator2", "children"), [Input('dropdown-1', 'value')]
)

def total_critical(input):
    print(input)
    if input == "January":
        total_amount = '915'
    if input == "February":
        total_amount = '879'

    else:
        total_amount = '915'
    
    return total_amount

@app.callback(
    Output("indicator3", "children"), [Input('dropdown-1', 'value')]
)

def severity1(input):
    print(input)
    if input == "January":
        total_amount = '10'
    if input == "February":
        total_amount = '18'

    else:
        total_amount = '10'
    
    return total_amount




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
            legend={'x': 1, 'y': 1},
            hovermode='closest',
        )}





#PERFORMANCE LAYOUT
performance_layout = html.Div([


                html.Div([
                html.H6("Indicators of the month:"),
                dcc.Dropdown(
                id='dropdown-worst',
                options=[{'label': 'January', 'value': 'January'},{'label': 'February', 'value': 'February'}],
                value='January'
                ),

                html.Div([ 
                indicator('blue','Worst Available Service','indicator11'),
                ]),

                html.Div([ 
                indicator('blue','Worst Reliable Service','indicator22'),
                ]),
                
                html.Div([ 
                indicator('blue','Worst MTTR','indicator33'),
                ]),


            ], className='row'),



            html.Div([ 


            html.Div([
                html.H4('Availability per Critical Services'),
           dcc.Graph(
                    figure=go.Figure(
                    data=[
                         go.Bar(
                            x= servAvail_df['Service'].unique().tolist(),
                            y= servAvail_df['January'].tolist(),
                            name='January',
                            text=servAvail_df['January'].tolist(),
                            textposition = 'auto',
                            marker=go.bar.Marker(
                            color='rgb(29, 104, 57)'
                                    )
                     ),
                        go.Bar(
                            x= servAvail_df['Service'].unique().tolist(),
                            y= servAvail_df['February'].tolist(),
                            name='February',
                            text= servAvail_df['February'].tolist(),
                            textposition = 'auto',
                            marker=go.bar.Marker(
                                color='rgb(50, 171, 96)',
                                opacity=0.6
                                ),
                            )
                            ],
                            layout=go.Layout(
                                title = 'Severity 1 High & Critical',
                                showlegend=True,
                                yaxis={'title': '% Availability'},
                                legend=go.layout.Legend(
                                    x=1,
                                    y=1.0
                                ),
                                margin=go.layout.Margin(l=60, r=40, t=40, b=100)
                            )
                        ),
                        style={'height': 500},
                        id='availability_graph'
                    )
               ],
            className='six columns'),

            

            html.Div([
                html.H4('Reliability per Critical Services'),

                dcc.Graph(
                    figure=go.Figure(
                    data=[
                         go.Bar(
                            x= servRelial_df['January'].tolist(),
                            y= servRelial_df['Service'].unique().tolist(),
                            name='January',
                            text=servRelial_df['January'].tolist(),
                            textposition = 'auto',
                            orientation = 'h',
                            marker=go.bar.Marker(
                            color='rgb(55, 83, 109)',
                            opacity=0.6
                                    )
                     ),
                        go.Bar(
                            y= servRelial_df['Service'].unique().tolist(),
                            x= servRelial_df['February'].tolist(),
                            name='February',
                            text=servRelial_df['February'].tolist(),
                            textposition = 'auto',
                            orientation = 'h',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)',
                                opacity=0.6
                                ),
                            )
                            ],
                            layout=go.Layout(
                                title = 'Severity 1 High & Critical',
                                showlegend=True,
                                xaxis={'title': 'Days between Failures'},
                                legend=go.layout.Legend(
                                    x=1.0,
                                    y=1.0
                                ),
                                margin=go.layout.Margin(l=210, r=40, t=40, b=40)
                            )
                        ),
                        style={'height': 500},
                        id='reliability_graph'
                    )
               ],
            className='six columns'),



            ], className='row'),


         html.Div([
    
               html.Div([
                html.H4('Mean Time to Resolve per Critical Services'),
                dcc.Graph(
                    figure=go.Figure(
                    data=[
                         go.Bar(
                            x= MTTR_df['Service'].unique().tolist(),
                            y= MTTR_df['January'].tolist(),
                            name='January',
                            text=MTTR_df['January'].tolist(),
                            textposition = 'auto',
                            marker=go.bar.Marker(
                            color='orange',
                                    
                                    )
                     ),
                        go.Bar(
                            x= MTTR_df['Service'].unique().tolist(),
                            y= MTTR_df['February'].tolist(),
                            name='February',
                            text=MTTR_df['February'].tolist(),
                            textposition = 'auto',
                            marker=go.bar.Marker(
                                color='orange',
                                opacity=0.60
                                )
                            )
                            ],
                            layout=go.Layout(
                                title = 'Severity High & Critical',
                                showlegend=True,
                                yaxis={'title': 'MTTR in hours'},
                                legend=go.layout.Legend(
                                    x=1.0,
                                    y=1.0
                                ),
                                margin=go.layout.Margin(l=60, r=40, t=40, b=100)
                            )
                        ),
                        style={'height': 500},
                        id='MTTR_graph'
                    )
               ],
            ),

              
       
            ],
            className="row"),

],

)


@app.callback(
    Output("indicator11", "children"), [Input('dropdown-worst', 'value')]
)

def worst_available(input):
    print(input)
    if input == "January":
        worst_service = 'FTC (98.0%)'
    if input == "February":
        worst_service = '.COM (97.96%)'

    else:
        worst_service = 'FTC (98.0%)'
    
    return worst_service


@app.callback(
    Output("indicator22", "children"), [Input('dropdown-worst', 'value')]
)

def worst_reliable(input):
    print(input)
    if input == "January":
        worst_service = 'Stations Ope. (1day, 9h)'
    if input == "February":
        worst_service = 'Stations Ope. (1day, 2h)'

    else:
        worst_service = 'Stations Ope. (1day, 9h)'
    
    return worst_service

@app.callback(
    Output("indicator33", "children"), [Input('dropdown-worst', 'value')]
)

def worst_MTTR(input):
    print(input)
    if input == "January":
        worst_service = 'FTC (1 day,3h)'
    if input == "February":
        worst_service = '.COM (1day,4h)'

    else:
        worst_service = 'FTC (1 day,3h)'
    
    return worst_service



app.scripts.config.serve_locally = True


if __name__ == '__main__':
    app.run_server(debug=True)