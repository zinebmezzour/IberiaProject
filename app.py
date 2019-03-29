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
c_df=pd.read_sql_query('select * from "critic";', conn)
jf_df=pd.read_sql_query('select * from "janfebraised";', conn)
servAvail_df=pd.read_sql_query('select * from "ServAvailJF";', conn)
servRelial_df=pd.read_sql_query('select * from "ServReliabilityJF";', conn)



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
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
        
    )


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
    
    html.Div([
        html.Div([ 
        indicator('blue','my first indicator','indicator1'),
        ]),

        html.Div([ 
        indicator('blue','my second indicator','indicator2'),
        ]),
        
        html.Div([ 
        indicator('blue','my third indicator','indicator3'),
        ]),


    ], className='row'),

    html.Div([ 

        html.Div([ 

            html.Div([
                dcc.Dropdown(
                id='dropdown-1',
                options=[{'label': i, 'value': i} for i in dff['year'].unique()],
                value=2018
                )
            ]),


            dcc.Graph(id='graph1'),
        ], className='six columns'),

        html.Div([ 


            html.Div([
                dcc.Dropdown(
                id='dropdown-2',
                options=[{'label': i, 'value': i} for i in dff['year'].unique()],
                value=2018
                )
            ]),

            dcc.Graph(id='graph2'),

        ], className='six columns'),

    ], className='row'),


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
className= 'twelve columns'
)


   
@app.callback(
    Output("indicator1", "children"), [Input('dropdown-3', 'value')]
)
def middle_leads_indicator_callback(domain):
    print(domain)
    #df = pd.read_json(df, orient="split")
    if domain == "All_Domains":
        open_leads = len(
        dff[
            (dff["Priority"] == "Critical")
        ].index
    )
    else:
        open_leads = len(
        dff[
            (dff["Domain"] == domain)
        ].index
    )
    
    return open_leads


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


#PERFORMANCE LAYOUT
performance_layout = html.Div([
        html.H2("Performance"),

            html.Div([
    
                html.Div([ 
                    
                    
                    html.Div([
                        dcc.Dropdown(
                        id='dropdown-11',
                        options=[{'label': i, 'value': i} for i in dff['year'].unique()],
                        value=2018
                        )
                    ], className='twelve columns'),


                html.Div([ 

                    html.Div([
                        html.H4('Graph1'),
                        dcc.Graph(id='graph11')
                    ], className='six columns'),

                    html.Div([
                        html.H4('Graph2'),
                        dcc.Graph(id='graph22'),
                        
                    ], className="six columns")

                ],className='row')


                        ],
                    className='twelve columns'),    
       
            ],
            className="row"),



            html.Div([ 


            html.Div([
                html.H4('Availability of Critical Services per Month'),
           dcc.Graph(
                    figure=go.Figure(
                    data=[
                         go.Bar(
                            x= servAvail_df['Service'].unique().tolist(),
                            y= servAvail_df['January'].tolist(),
                            name='January',
                            marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                                    )
                     ),
                        go.Bar(
                            x= servAvail_df['Service'].unique().tolist(),
                            y= servAvail_df['February'].tolist(),
                            name='February',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)'
                                )
                            )
                            ],
                            layout=go.Layout(
                                
                                showlegend=True,
                                yaxis={'title': '% Availability'},
                                legend=go.layout.Legend(
                                    x=0,
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
                html.H4('Reliability of Critical Services per Month'),

                dcc.Graph(
                    figure=go.Figure(
                    data=[
                         go.Bar(
                            x= servRelial_df['Service'].unique().tolist(),
                            y= servRelial_df['January'].tolist(),
                            name='January',
                            marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                                    )
                     ),
                        go.Bar(
                            x= servRelial_df['Service'].unique().tolist(),
                            y= servRelial_df['February'].tolist(),
                            name='February',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)'
                                )
                            )
                            ],
                            layout=go.Layout(
                                
                                showlegend=True,
                                yaxis={'title': 'Hours between Failures'},
                                legend=go.layout.Legend(
                                    x=0,
                                    y=1.0
                                ),
                                margin=go.layout.Margin(l=60, r=100, t=0, b=100)
                            )
                        ),
                        style={'height': 500},
                        id='reliability_graph'
                    )
               ],
            className='six columns'),



            ], className='twelve columns')

],

)

@app.callback(
    Output('graph44', 'figure'),
    [Input('dropdown-55', 'value') 
    ])


def graph_44():
    print(input)

    filtered_df = servAvail_df[input].tolist()
    
    #filtered_df1 = servAvail_df['February'].tolist()

    critical_services_options= servAvail_df['Service'].unique().tolist()

 #   availability=[]

 #   for i in critical_services_options :
 #       p=filtered_df[i].unique()
 #       p=p.tolist()
  #      p=p[0]
  #      availability.append(p)

       
    return ({
        'data': [{'x':critical_services_options, 'y':filtered_df,'type':'scatter', 'name':input}
    
        ],
        'layout': go.Layout(
            xaxis={'type':'category', 'title': 'Services'},
            yaxis={'title': '% Availability'},
            barmode="group",
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            title="Availability for Critical Services in {}".format(input)
            )
        }
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
    [Input('dropdown-11', 'value') 
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