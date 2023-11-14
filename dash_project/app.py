import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
            ] , label='Informaçoes do Projeto')
        ]),
        
        
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)