import dash
import dash_core_components as dcc
import dash_html_components as html
import subprocess
import json
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State, Event
from collections import deque
import re

app = dash.Dash(__name__,static_folder='assets')
app.css.config.serve_locally=True
color = {'background':'#111111','text':'#FFFFFF','button':'111111','border':'#FFFFFF','tab':'#111111','buttontext':'#FFFFFF'}
server = app.server
app.layout=html.Div(id = 'bg',children=[
    html.Link(href='/assets/stylesheet.css',rel='stylesheet'),
    html.Br(),
    html.Div([
    html.H3('Network Performance Analysis',style = {'color':color['text'],'margin':'auto'}),
    html.Br(),
    html.Div([
    html.Div([
        html.P('BWCTL Client',style = {'color':color['text']}),
        html.Div([dcc.Input(id='input_client', type='text')],style = {'width':300})],style = {'float':'left'}),
        html.Div([
            html.P('BWCTL Remote Server',style = {'color':color['text']}),
            html.Div([dcc.Dropdown(
                id='input_server',
                options=[
                    {'label':'150.100.209.131','value':'150.100.209.131'},
                    {'label':'192.12.19.99','value':'192.12.19.99'},
                    {'label':'192.124.227.22','value':'192.124.227.22'},
                    {'label':'acb-perfsonar.usc.edu ','value':'68.181.200.67'},
                    {'label':'ampas-perfsonar.mgmt.usc.edu','value':' 10.6.1.14'},
                    {'label':'ari-perfsonar-10g.usc.edu','value':'128.125.88.91'},
                    {'label':'ari-perfsonar-1g.usc.edu ','value':'128.125.88.90'},
                    {'label':'ari-perfsonar-fortinet-10g.mgmt.usc.edu','value':'10.2.18.69'},
                    {'label':'ari-perfsonar-gw.usc.edu ','value':'128.125.88.89'},
                    {'label':'cal-perfsonar-10g.usc.edu','value':'128.125.88.69'},
                    {'label':'cal-perfsonar-1g.usc.edu','value':'128.125.88.68'},
                    {'label':'cal-perfsonar-gw.usc.edu','value':'128.125.88.65'},
                    {'label':'deter-perfsonar.usc.edu','value':'68.181.200.71'},
                    {'label':'dr-perfsonar.usc.edu','value':'128.125.251.186'},
                    {'label':'hpc-perfsonar.hpcc.usc.edu ','value':'10.125.0.20'},
                    {'label':'hpc-perfsonar.usc.edu','value':'128.125.214.141'},
                    {'label':'hsv-perfsonar-10g.usc.edu   ','value':'128.125.88.83'},
                    {'label':'hsv-perfsonar-1g.usc.edu','value':'128.125.88.82'},
                    {'label':'hsv-perfsonar-gw.usc.edu','value':'128.125.88.81'},
                    {'label':'mcc-perfsonar-10g.usc.edu ','value':'128.125.88.75'},
                    {'label':'mcc-perfsonar-1g.usc.edu  ','value':'128.125.88.74'},
                    {'label':'mcc-perfsonar-gw.usc.edu','value':'128.125.88.73'},
                    {'label':'phe-perfsonar.usc.edu ','value':'68.181.200.72'},
                    {'label':'raharu.usc.edu','value':'128.125.88.662'},
                    {'label':'rri-perfsonar.usc.edu ','value':'68.181.200.68'},
                    {'label':'scb-perfsonar.usc.edu','value':'68.181.200.66'},
                    {'label':'ten2-perfsonar-gw.usc.edu','value':'68.181.200.65'},
                    {'label':'vhe-perfsonar.usc.edu  ','value':'68.181.200.69'},
                    {'label':'zni-perfsonar-1g.usc.edu','value':'68.181.163.152'},
                    {'label':'zni-perfsonar.usc.edu','value':'68.181.200.70'}
                    ])],style = {'width':300})],style = {'float':'left'}),

        html.P('Test Duration',style = {'color':color['text']}),
        html.Div(dcc.Input(id='input_time', type='text',style = {'width':50})),
    ],style={'width':400,'margin':'auto'}),
    html.Br(),
    ],style={'textAlign':'center'}),
    html.Button(children='Start', type='submit', id='button',style = {'color':color['buttontext'],'borderColor':color['border'],'backgroundColor':color['button'],'marginLeft':20}),
    html.Br(),
    html.Div(id = 'output-graph')

],style = {'height':'200vh','backgroundColor':color['background']})

@app.callback(
    Output('output-graph','children'),  [Input('button', 'n_clicks')],[State('input_client','value'),State('input_server','value'), State('input_time', 'value')])
def update_graph(n_clicks,client_ip,server_ip,time_in_secs):

    f = subprocess.check_output(['pscheduler','task','--format','json','throughput','--source',str(client_ip),'--dest',str(server_ip), '--duration', 'PT'+str(time_in_secs)+'S'])
    a,b = f.split('"intervals":')
    a1,b1 = a.split('connecting_to')
    a2,b2 = a1.split('timestamp')
    a3,b3 = b2.split('GMT')
    a4,b4 = a3.split(',')
    c = '{"intervals":'+ b
    d,e = c.split("No further runs scheduled")
    data = json.loads(d)
    X = deque(maxlen = 50)
    Y1 = deque(maxlen = 50)
    Y2 = deque(maxlen = 50)

    for i in range(len(data['intervals'])):
        X.append(data['intervals'][i]['streams'][0]['end'])
        Y1.append(data['intervals'][i]['streams'][0]['throughput-bits'])
        Y2.append(data['intervals'][i]['streams'][0]['retransmits'])


    return [
        html.Br(),
        html.Br(),
            html.Div([
                html.Table([
                    html.Tr([html.Td('Server IP'),html.Td(str(server_ip))],style = {'color':color['text']}),
                    html.Tr([html.Td('Current Status'),html.Td(['OK'],style = {'color':'#00FF00'})],style = {'color':color['text']}),
                    html.Tr([html.Td('Time'),html.Td(b4)],style = {'color':color['text']}),
                    html.Tr([html.Td('Average Throughput'),html.Td(data['summary']['summary']['throughput-bytes'])],style = {'color':color['text']}),
                    html.Tr([html.Td('Total Retransmits'),html.Td(data['summary']['summary']['retransmits'])],style = {'color':color['text']})

            ])
            ],style = {'margin':'auto','width':250}),
        html.Br(),
        html.Br(),
        html.Div([dcc.Tabs(id='tabs',children=[
            dcc.Tab(label='Bar',style={'backgroundColor':color['tab'],'margin':'auto','color':'#FFFFFF','borderColor':color['border']},children=[
                html.Div(children =[dcc.Graph(
                id = 'example1',
                figure = {
                    'data': [
                                {'x':list(X),'y':list(Y1),'type':'bar'},
                            ],
                    'layout':go.Layout(
                            xaxis={ 'title': 'Time in seconds'},
                            yaxis={'title': 'Throughput-bits'},
                            hovermode='closest',
                            title=b4
                            )
                }
            ),
            html.Br(),
            html.Br(),
            dcc.Graph(
                id = 'example2',
                figure = {
                    'data': [
                                {'x':list(X),'y':list(Y2),'type':'bar'}
                            ],
                    'layout':go.Layout(
                            xaxis={ 'title': 'Time in seconds'},
                            yaxis={'title': 'retransmits'},
                            hovermode='closest',
                            title=b4
                            )

                }
            )],style={'width':'700','margin':'auto'})
            ]),

            dcc.Tab(label='Line',style={'textAlign':'center','margin':'auto','backgroundColor':color['tab'],'color':'#FFFFFF','borderColor':'#7FDBFF'},children=[
                html.Div(children =[dcc.Graph(
                id = 'example1',
                figure = {
                    'data': [
                                {'x':list(X),'y':list(Y1),'type':'line'},
                            ],
                    'layout':go.Layout(
                            xaxis={ 'title': 'Time in seconds'},
                            yaxis={'title': 'Throughput-bits'},
                            hovermode='closest',
                            title=b4
                            )

                }
            ),
            html.Br(),
            html.Br(),
            dcc.Graph(
                id = 'example2',
                figure = {
                    'data': [
                                {'x':list(X),'y':list(Y2),'type':'line','name':'retransmits'}
                            ],
                    'layout':go.Layout(
                            xaxis={ 'title': 'Time in seconds'},
                            yaxis={'title': 'retransmits'},
                            hovermode='closest',
                            title=b4
                            )

                }
            )],style={'width':'700','margin':'auto'})
            ]),
        ],style = {'margin':'auto'})]),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
