import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import mysql.connector
import pandas as pd

# Conectar ao banco de dados MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    database='DesempenhoVendas',
    password='274962',
    port = 3306
)

# Criar uma instância do aplicativo Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Desempenho de Vendas por Região"),
    
    # Dropdown para selecionar a região
    dcc.Dropdown(
        id='regiao-dropdown',
        options=[
            {'label': 'Todas as Regiões', 'value': 'all'},
            {'label': 'Região Norte', 'value': '1'},
            {'label': 'Região Sul', 'value': '2'},
            {'label': 'Região Oeste', 'value': '3'},
            {'label': 'Região Leste', 'value': '4'},
            {'label': 'Região Centro-Oeste', 'value': '5'},
            {'label': 'Região Nordeste', 'value': '6'}
        ],
        value='all',
        multi=False
    ),

    # Gráfico de barras para exibir as vendas
    dcc.Graph(id='grafico-vendas')
])

# Callback para atualizar o gráfico com base na seleção da região
@app.callback(
    Output('grafico-vendas', 'figure'),
    [Input('regiao-dropdown', 'value')]
)
def update_graph(selected_regiao):
    # Query SQL para obter dados das vendas
    if selected_regiao == 'all':
        query = "SELECT Regioes.nome_regiao, SUM(Vendas.quantidade) as total_vendas FROM Vendas JOIN Regioes ON Vendas.id_regiao = Regioes.id_regiao GROUP BY Regioes.id_regiao"
    else:
        query = f"SELECT Regioes.nome_regiao, SUM(Vendas.quantidade) as total_vendas FROM Vendas JOIN Regioes ON Vendas.id_regiao = Regioes.id_regiao WHERE Vendas.id_regiao = {selected_regiao} GROUP BY Regioes.id_regiao"

    # Executar a query e obter resultados como um DataFrame
    df = pd.read_sql(query, conn)

    # Criar um gráfico de barras
    figure = {
        'data': [
            {'x': df['nome_regiao'], 'y': df['total_vendas'], 'type': 'bar', 'name': 'Vendas'}
        ],
        'layout': {
            'title': f'Desempenho de Vendas por Região ({selected_regiao if selected_regiao != "all" else "Todas as Regiões"})'
        }
    }

    return figure

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)