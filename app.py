import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from plotly import graph_objects as go  # Adiciona esta linha de importação
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar os dados
@st.cache_data
def load_data():
    data = pd.read_csv('lego.csv', sep=';')
    return data

# Lê os dados
data = load_data()

# Título do Dashboard
st.title('Dashboard LEGO - Análise de Conjuntos')

# Sidebar com opções
st.sidebar.title('Opções')
menu = st.sidebar.selectbox('Selecione uma opção:', ('home','Visão Geral','Consulta por Filtros', 'Rating de Temas', 'Rating de Subtemas', 
                                                     'Média de Peças por Tema', 'Gráfico de Pizza', 'Trendline de Lançamentos por Ano',
                                                      'Análise de Correlação', 'Análise por Ano', 'Análise por Tema', 
                                                     'Análise por Categoria', 'Análise de Disponibilidade', 'Análise de Peças', 
                                                     'Análise de Minifiguras', 'Análise de Propriedade'))


if menu == 'home':
    gif_url = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExajU0c2s3dGZmamk2cjhqdG1zNjk5dGc2em5zY3o5aWs2ajQ0MXlrMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7zMkk1aiQVonuZQKi6/giphy.gif"
    st.markdown(f'<img src="{gif_url}" alt="GIF" width="600">', unsafe_allow_html=True)

    st.title("DATABASE BRINQUEDOS LEGO")

    # Introdução
    st.markdown("""
    A tabela de banco de dados em questão armazena informações relacionadas a conjuntos de brinquedos, pertencentes às linhas de produtos da empresa LEGO, como os conjuntos de blocos de construção.
    """)

    # Processo de Construção da Tabela
    st.write("""
A tabela de banco de dados em questão armazena informações relacionadas a conjuntos de brinquedos,
pertencentes às linhas de produtos da empresa LEGO, como os conjuntos de blocos de construção.

**Processo de Construção da Tabela:**
A tabela foi criada com a utilização de filtros específicos, visando facilitar a análise dos conjuntos de brinquedos LEGO.
Os filtros utilizados foram:
- **Ano (Year):** Limitando os dados aos conjuntos lançados dentro do intervalo de 1983 a 2023.
- **Grupo de Tema (Theme_Group):** Agrupando os conjuntos com base em categorias mais amplas.
- **Grupo (Subtheme):** Detalhando os conjuntos ainda mais através de subtemas específicos.

**Limpeza de Dados:**
Antes de prosseguir com as análises, foi realizada uma etapa de limpeza de dados para
remover informações inconsistentes, faltantes ou duplicadas. Isso assegura a integridade
e confiabilidade dos dados a serem analisados.

**Gráficos utilizados:**
1. Rating por Tema dos Legos
2. Rating por Subtema dos Legos
3. Média da Quantidade de Peças por Tema
4. Gráfico de Pizza: Mostrando o total de conjuntos 'Owned' por tema, proporcionando uma visão percentual
da coleção do usuário. Além disso, uma contagem de categorias pode ser exibida em um gráfico de pizza
separado.

**Especificações:**
Link da base original sem a filtragem: [LEGO Sets and...](https://www.kaggle.com/datasets/willianoliveiragibin/lego-sets-and)
Tamanho: 376kb
Colunas: 12 (base filtradas) com 3 colunas utilizadas; Linhas: 14795 (base filtrada);
""")



# Visão Geral dos Dados
elif menu == 'Visão Geral':
    st.header('Visão Geral dos Conjuntos LEGO')
    st.write(data.head())

    st.subheader('Informações Gerais')
    descricao_estatisticas = data.describe().rename(index={
        'count': 'Contagem',
        'mean': 'Média',
        'std': 'Desvio Padrão',
        'min': 'Mínimo',
        '25%': '25º Percentil',
        '50%': 'Mediana',
        '75%': '75º Percentil',
        'max': 'Máximo'
    })

    st.write("A tabela abaixo apresenta estatísticas descritivas sobre os conjuntos LEGO.")
    st.write(descricao_estatisticas)

# Consulta por Filtros
elif menu == 'Consulta por Filtros':
    st.header('Consulta por Filtros')

    # Filtros
    selected_year = st.selectbox('Selecione o Ano:', data['Year'].unique())
    selected_theme = st.selectbox('Selecione o Tema:', data['Theme'].unique())
    selected_theme_group = st.selectbox('Selecione o Grupo Temático:', data['Theme_Group'].unique())

    # Aplicar filtros
    filtered_data = data[(data['Year'] == selected_year) & (data['Theme'] == selected_theme) & (data['Theme_Group'] == selected_theme_group)]

    st.subheader('Resultados da Consulta')
    st.write(filtered_data)

# Contagem de Temas
elif menu == 'Rating de Temas':
    st.header('Rating de Temas')

    # Contar a ocorrência de cada tema
    theme_counts = data['Theme'].value_counts().reset_index()
    theme_counts.columns = ['Theme', 'Count']

    st.subheader('Contagem de Temas')
    fig_theme_counts = px.bar(theme_counts, x='Theme', y='Count', labels={'x': 'Tema', 'y': 'Contagem'})
    st.plotly_chart(fig_theme_counts)

# Contagem de Subtemas
elif menu == 'Rating de Subtemas':
    st.header('Rating de Subtemas')

    # Contar a ocorrência de cada subtema
    subtheme_counts = data['Subtheme'].value_counts().reset_index()
    subtheme_counts.columns = ['Subtheme', 'Count']

    st.subheader('Contagem de Subtemas')
    fig_subtheme_counts = px.bar(subtheme_counts, x='Subtheme', y='Count', labels={'x': 'Subtema', 'y': 'Contagem'})
    st.plotly_chart(fig_subtheme_counts)

# Média de Peças por Tema
elif menu == 'Média de Peças por Tema':
    st.header('Média de Peças por Tema')

    # Calcular a média de peças por tema
    avg_pieces_by_theme = data.groupby('Theme')['Pieces'].mean().reset_index()

    st.subheader('Média de Peças por Tema')
    fig_avg_pieces_theme = px.bar(avg_pieces_by_theme, x='Theme', y='Pieces', labels={'x': 'Tema', 'y': 'Média de Peças'})
    st.plotly_chart(fig_avg_pieces_theme)

# Gráfico de Pizza
elif menu == 'Gráfico de Pizza':
    st.header('Gráfico de Pizza')

    # Total de conjuntos "owned" por tema
    owned_by_theme = data.groupby('Theme')['Owned'].sum().reset_index()

    st.subheader('Total de Owned por Tema')
    fig_owned_by_theme = px.pie(owned_by_theme, names='Theme', values='Owned', title='Total de Owned por Tema')
    st.plotly_chart(fig_owned_by_theme)

    # Contagem de categorias
    category_counts = data['Category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']

    st.subheader('Contagem de Categorias')
    fig_category_counts = px.pie(category_counts, names='Category', values='Count', title='Contagem de Categorias')
    st.plotly_chart(fig_category_counts)

# Trendline de Lançamentos por Ano (usando as colunas Name e Year)
elif menu == 'Trendline de Lançamentos por Ano':
    st.header('Trendline de Lançamentos por Ano')

    # Calcular a média de lançamentos por ano
    avg_releases_by_year = data.groupby('Year').size().reset_index(name='Count')

    # Adicionar uma constante para a regressão linear
    avg_releases_by_year['constant'] = 1

    # Ajustar o modelo de regressão linear
    model = sm.OLS(avg_releases_by_year['Count'], avg_releases_by_year[['Year', 'constant']])
    results = model.fit()

    # Adicionar a trendline aos dados
    avg_releases_by_year['trendline'] = results.predict(avg_releases_by_year[['Year', 'constant']])

    # Criar trace para a trendline
    trace_trendline = go.Scatter(x=avg_releases_by_year['Year'], y=avg_releases_by_year['trendline'],
                                 mode='lines', name='Trendline', line=dict(color='red'))

    # Criar o gráfico
    fig_avg_releases_by_year = px.scatter(avg_releases_by_year, x='Year', y='Count',
                                          labels={'x': 'Ano de Lançamento', 'y': 'Média de Lançamentos'},
                                          title='Trendline de Lançamentos por Ano')

    # Adicionar a trendline ao gráfico
    fig_avg_releases_by_year.add_trace(trace_trendline)

    # Mostrar o gráfico
    st.plotly_chart(fig_avg_releases_by_year)

# Análise de Correlação entre Year e Theme
elif menu == 'Análise de Correlação':
    st.header('Análise de Correlação entre Year e Theme')

    # Converter a coluna 'Theme' para uma representação numérica
    data['Theme_numeric'] = data['Theme'].astype('category').cat.codes

    # Calcular a matriz de correlação
    correlation_matrix = data[['Year', 'Theme_numeric']].corr()

    # Plotar o heatmap com seaborn
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5, ax=ax)
    st.pyplot(fig)

    st.subheader('Observação:')
    st.write("O valor de correlação pode ser interpretado, mas é importante ter em mente que a correlação não necessariamente indica causalidade.")

# Análise por Ano
elif menu == 'Análise por Ano':
    st.header('Análise por Ano')

    st.subheader('Distribuição de Conjuntos por Ano')
    fig_year = px.histogram(data, x='Year', nbins=20, labels={'x': 'Ano de Lançamento'})
    st.plotly_chart(fig_year)

# Análise por Tema
elif menu == 'Análise por Tema':
    st.header('Análise por Tema')

    st.subheader('Top 10 Temas Mais Recorrentes')
    top_10_theme = data['Theme'].value_counts().nlargest(10)
    st.bar_chart(top_10_theme)

# Análise por Categoria
elif menu == 'Análise por Categoria':
    st.header('Análise por Categoria')

    st.subheader('Distribuição de Conjuntos por Categoria')
    fig_category = px.histogram(data, x='Category', labels={'x': 'Categoria'})
    st.plotly_chart(fig_category)

# Análise de Disponibilidade
elif menu == 'Análise de Disponibilidade':
    st.header('Análise de Disponibilidade')

    st.subheader('Distribuição de Conjuntos por Disponibilidade')
    fig_availability = px.histogram(data, x='Availability', labels={'x': 'Disponibilidade'})
    st.plotly_chart(fig_availability)

# Análise de Peças
elif menu == 'Análise de Peças':
    st.header('Análise de Peças')

    st.subheader('Distribuição de Peças por Conjunto')
    fig_pieces = px.histogram(data, x='Pieces', labels={'x': 'Número de Peças'})
    st.plotly_chart(fig_pieces)

# Análise de Minifiguras
elif menu == 'Análise de Minifiguras':
    st.header('Análise de Minifiguras')

    st.subheader('Distribuição de Minifiguras por Conjunto')
    fig_minifigures = px.histogram(data, x='Minifigures', labels={'x': 'Número de Minifiguras'})
    st.plotly_chart(fig_minifigures)

# Análise de Propriedade
elif menu == 'Análise de Propriedade':
    st.header('Análise de Propriedade')

    st.subheader('Distribuição de Conjuntos por Propriedade')
    fig_owned = px.histogram(data, x='Owned', labels={'x': 'Propriedade'})
    st.plotly_chart(fig_owned)

# Créditos
st.sidebar.text("Desenvolvido por: Victória Thaisa")
