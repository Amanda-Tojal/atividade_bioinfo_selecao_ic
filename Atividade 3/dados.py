import pandas as pd
import streamlit as st
import plotly.express as px

# Configurar a página do Streamlit para largura total
st.set_page_config(layout="wide")

# Carregar os dados
planilha = pd.read_csv('dados.csv', sep=';', low_memory=False, on_bad_lines='skip')

# Extrair a data dos últimos 10 caracteres da coluna seqName
planilha['date'] = planilha['seqName'].str[-10:]

# Converter a coluna de data para o formato datetime
planilha['date'] = pd.to_datetime(planilha['date'], format='%Y-%m-%d', errors='coerce')

# Remover linhas com datas inválidas
planilha = planilha.dropna(subset=['date'])

# Extrair a sigla do estado da coluna seqName
planilha['estado'] = planilha['seqName'].str.extract(r'Brazil/([A-Z]{2})')

# Selecionar as colunas relevantes
data = planilha[['date', 'totalSubstitutions', 'totalDeletions', 'totalInsertions']]

# Ordenar os dados pela data
data = data.sort_values(by='date')

# Verificar se as datas estão ordenadas corretamente
print(data)

# Criar o gráfico de linha
fig = px.line(data, x='date', y=['totalSubstitutions', 'totalDeletions', 'totalInsertions'],
              labels={'value': 'Count', 'variable': 'Metric', 
                      'totalSubstitutions': 'Total Substitutions', 
                      'totalDeletions': 'Total Deletions', 
                      'totalInsertions': 'Total Insertions'},
              title='Evolução ao longo do tempo',
              width=1400, height=700,
              color_discrete_map={
                  'totalSubstitutions': 'blue',
                  'totalDeletions': 'red',
                  'totalInsertions': 'green'
              })

# Ajustar a escala do eixo y para destacar valores entre 0 e 1000 e permitir visualizar valores acima disso
fig.update_yaxes(type="log", range=[0, 4], tickvals=[1, 10, 100, 1000, 10000, 13000])

# Exibir o gráfico de linha no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Contar as ocorrências de cada estado
estado_counts = planilha['estado'].value_counts().reset_index()
estado_counts.columns = ['estado', 'count']

# Criar o gráfico de barras
fig_bar = px.bar(estado_counts, x='estado', y='count', 
                 labels={'estado': 'Estado', 'count': 'Número de Ocorrências'},
                 title='Número de Ocorrências por Região',
                 color='estado',
                 width=1400, height=700)

# Exibir o gráfico de barras no Streamlit
st.plotly_chart(fig_bar, use_container_width=True)
