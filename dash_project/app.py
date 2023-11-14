import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import Dash
from dash import Input
from dash import Output
from dash import callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np

dados = pd.read_csv('censo_estadual_2007_a_2022.csv', encoding='latin-1', sep=',', low_memory=False)
dados.drop(columns='Unnamed: 0', inplace=True)
frequencia = pd.crosstab(dados['NU_ANO_CENSO'], dados['CO_ORGAO_REGIONAL'])

frequencia.rename(columns={
    1:'1a. GRE',
    2:'2a. GRE',
    3:'3a. GRE',
    4:'4a. GRE',
    5:'5a. GRE',
    6:'6a. GRE',
    7:'7a. GRE',
    8:'8a. GRE',
    9:'9a. GRE',
    10:'10a. GRE',
    11:'11a. GRE',
    12:'12a. GRE',
    13:'13a. GRE',
    14:'14a. GRE',
}, inplace=True)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.H1(
            children='Estudo do Censo',
            style={
                'color': 'blue',
                'fontsize': '40px'
            }
        ),
        html.H2('INEP - CENSO ESCOLAR - MICRODADOS'),
        html.P('Dados interessantes'),
        dbc.Tabs([
            dbc.Tab([
                html.Ul([
                    html.Li('Número de escolas estaduais em 2022'),
                    html.Li('Período de tempo abordado: 2007 a 2022'),
                    html.Li('Frequência que é realizado o censo: ANUAL'),
                    html.Li('Último censo realizado: 2022'),
                    html.Li([
                        'Fonte dos dados: ',
                        html.A('Censo Escolar - Microdados do Censo Escolar da Educacação Básica', 
                        href='https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar'
                        )
            ])
            
        ])
            ] , label='Informaçoes do Projeto'),
            dbc.Tab([
                html.Div(
                    dcc.Graph(id='gerencias')
                )
            ] )
        ]),
    ]
)

@callback(
    Output('gerencias', 'figure'),
    Input('gerencias', 'value')
)
def plotar_quantidade_escolas_por_regional(ano):    
    title = 'Main Source for News'
    labels = ['1a. GRE', '2a. GRE', '3a. GRE', '4a. GRE']
    colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    mode_size = [8, 8, 12, 8]
    line_size = [2, 2, 4, 2]

    x_data = np.vstack((np.arange(2007, 2023),)*4)

    y_data = np.array([
        frequencia['1a. GRE'],
        frequencia['2a. GRE'],
        frequencia['3a. GRE'],
        frequencia['4a. GRE'],
    ])

    fig = go.Figure()

    for i in range(4):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))

        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
    # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                    xanchor='right', yanchor='middle',
                                    text=label + ' {}'.format(y_trace[0]),
                                    font=dict(family='Arial',
                                                size=16),
                                    showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[11],
                                    xanchor='left', yanchor='middle',
                                    text='{}'.format(y_trace[-1]),
                                    font=dict(family='Arial',
                                                size=16),
                                    showarrow=False))
    # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                xanchor='left', yanchor='bottom',
                                text='Decréscimo de Escolas Por Gerência Regional',
                                font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                showarrow=False))
    # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                xanchor='center', yanchor='top',
                                text='Source: PewResearch Center & ' +
                                    'Storytelling with data',
                                font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                showarrow=False))

    fig.update_layout(
        annotations=annotations,           
        autosize=True,
        width=1200,
        height=800,
    )


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)