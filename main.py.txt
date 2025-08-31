# main.py
# -*- coding: utf-8 -*-
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import paginas
from app import app

# Barra de navegação
navegacao = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Gráficos", href="/graficos")),
        dbc.NavItem(dbc.NavLink("Formulário", href="/formulario")),
    ],
    brand="Dashboard - Unoesc",
    brand_href="/",
    color="primary",
    dark=True
)

# Layout principal
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navegacao,
    html.Div(id="conteudo")
])

# Callback de navegação
@app.callback(
    Output("conteudo", "children"),
    [Input("url", "pathname")]
)
def mostrar_pagina(pathname):
    if pathname == "/formulario":
        return paginas.formulario.layout
    elif pathname == "/graficos":
        return paginas.graficos.layout
    else:
        return html.H2("Bem-vindo ao Dashboard de Doenças Cardíacas!", className="text-center mt-4")

# Executa o app
if __name__ == "__main__":
    # Cloud Run escuta na porta 8080 e host 0.0.0.0
    app.run(debug=False, port=8080, host="0.0.0.0")
