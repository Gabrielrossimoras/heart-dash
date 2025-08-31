from ucimlrepo import fetch_ucirepo
import plotly.express as px
from dash import dcc, html
import dash_bootstrap_components as dbc

heart_disease = fetch_ucirepo(id=45)
dados = heart_disease.data.features
dados['doenca'] = 1 * (heart_disease.data.targets > 0)

fig_hist = px.histogram(dados, x='age', nbins=30, color='doenca',
                        title='Distribuição Etária (Plotly)')
fig_box = px.box(dados, x='doenca', y='age', color='doenca',
                 title='Distribuição Etária por Doença')

layout = html.Div([
    html.H1('Gráficos - Heart Disease'),
    dbc.Container([
        dbc.Row([
            dbc.Col([dcc.Graph(figure=fig_hist)], md=7),
            dbc.Col([dcc.Graph(figure=fig_box)], md=5)
        ])
    ])
])
