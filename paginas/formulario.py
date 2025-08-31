# formulario.py
# -*- coding: utf-8 -*-
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import pandas as pd
import numpy as np
from app import app

# Carrega o modelo e as medianas
modelo = joblib.load('modelo_xgboost.pkl')
medianas = joblib.load('medianas.pkl')

# Formulário
formulario = dbc.Container([
    html.P("Preencha os dados e clique em 'Prever'", 
           className='text-center mb-4 custom-subtitle'),
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Label('Idade'),
                dbc.Input(id='idade', type='number', placeholder='Digite a idade')
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Sexo biológico'),
                dbc.Select(id='sexo', options=[
                    {'label': 'Masculino', 'value': '1'},
                    {'label': 'Feminino', 'value': '0'}
                ])
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Tipo de dor no peito'),
                dbc.Select(id='cp', options=[
                    {'label': 'Angina típica', 'value': '1'},
                    {'label': 'Angina atípica', 'value': '2'},
                    {'label': 'Dor não cardíaca', 'value': '3'},
                    {'label': 'Assintomático', 'value': '4'}
                ])
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Pressão arterial em repouso'),
                dbc.Input(id='trestbps', type='number',
                          placeholder='Digite a pressão arterial em repouso')
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Colesterol sérico'),
                dbc.Input(id='chol', type='number',
                          placeholder='Digite o colesterol sérico')
            ], className='mb-3'),
        ]),

        dbc.Col([
            dbc.CardGroup([
                dbc.Label('Frequência cardíaca máxima atingida'),
                dbc.Input(id='thalach', type='number',
                          placeholder='Digite a frequência máxima atingida')
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Angina induzida por exercício'),
                dbc.Select(id='exang', options=[
                    {'label': 'Não', 'value': '0'},
                    {'label': 'Sim', 'value': '1'}
                ])
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Depressão do segmento ST'),
                dbc.Input(id='oldpeak', type='number',
                          placeholder='Digite o valor do ST')
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Inclinação do segmento ST'),
                dbc.Select(id='slope', options=[
                    {'label': 'Ascendente', 'value': '1'},
                    {'label': 'Plana', 'value': '2'},
                    {'label': 'Descendente', 'value': '3'}
                ])
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Button('Prever', id='botao-prever', color='primary', n_clicks=0)
            ], className='mb-3')
        ])
    ])
])

# Layout da página
layout = html.Div([
    html.H1('Previsão de Doença Cardíaca', className='text-center mt-4 custom-title'),
    formulario,
    html.Div(id='previsao')
])

# Callback para previsão
@app.callback(
    Output('previsao', 'children'),
    [Input('botao-prever', 'n_clicks')],
    [State('idade', 'value'),
     State('sexo', 'value'),
     State('cp', 'value'),
     State('trestbps', 'value'),
     State('chol', 'value'),
     State('thalach', 'value'),
     State('exang', 'value'),
     State('oldpeak', 'value'),
     State('slope', 'value')]
)
def prever_doenca(n_clicks, idade, sexo, cp, trestbps, chol, thalach, exang, oldpeak, slope):
    if n_clicks == 0:
        return ''

    entradas_usuario = pd.DataFrame(
        data=[[idade, sexo, cp, trestbps, chol, thalach, exang, oldpeak, slope]],
        columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'thalach', 'exang', 'oldpeak', 'slope']
    )

    # Preenche valores em branco
    entradas_usuario.fillna(medianas, inplace=True)

    # Ajusta tipos
    entradas_usuario['oldpeak'] = entradas_usuario['oldpeak'].astype(np.float64)
    for col in entradas_usuario.columns:
        if col != 'oldpeak':
            entradas_usuario[col] = entradas_usuario[col].astype(int)

    previsao = modelo.predict(entradas_usuario)[0]
    if previsao == 1:
        return dbc.Alert("⚠️ Você tem risco de doença cardíaca!", color='danger', className='mt-3')
    else:
        return dbc.Alert("✅ Você NÃO tem risco de doença cardíaca!", color='success', className='mt-3')
