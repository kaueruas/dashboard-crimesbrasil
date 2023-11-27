import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('Crimes_brasil_uf.csv')

st.set_page_config(
    page_title="Crimes Dashboards",
    layout="wide"
)



st.title('Ocorrências de crimes no Brasil (2014-2022)')
st.markdown('''---''')


uf=st.sidebar.multiselect (
     key=1,
     label="Estados",
     options=df['Uf'].unique(),
     default=df['Uf'].unique()
 )
tc=st.sidebar.multiselect (
     key=2,
     label="Tipo de crime",
     options=df['Tipo_crime'].unique(),
     default=df['Tipo_crime'].unique()
 )

df = df.query('Uf == @uf and Tipo_crime == @tc')

left_column, right_column = st.columns(2)
with left_column:
    st.header('DataFrame:')
    st.dataframe(df)


media_ocorrencias = df.groupby('Tipo_crime')['Ocorrencias'].mean().sort_values(ascending=False).reset_index()

with right_column:
    fig1 = px.bar(media_ocorrencias, x='Ocorrencias', y='Tipo_crime', orientation='h',
                 title='Média de Ocorrências por Tipo de Crime',
                 labels={'Ocorrencias': 'Média de Ocorrências', 'Tipo_crime': 'Tipo de Crime'},
                 height=520)
    st.plotly_chart(fig1)

agrupar_data = df.groupby("Data")["Ocorrencias"].mean().reset_index()
fig2=px.line(agrupar_data, x="Data", y="Ocorrencias" , labels={"Ocorrencias":"Ocorrências"},title="Ocorrências de crimes ao longo dos anos (2014-2022)" )
col1, col2, col3 = st.columns([1, 3, 1])  
with col2:
    st.plotly_chart(fig2, use_container_width=True)


st.markdown('''---''')

dados_crimes = pd.DataFrame(df)
dados_sp = dados_crimes.copy()
dados_sp['Data'] = pd.to_datetime(dados_sp['Data'])
dados_sp.loc[:,'ano'] = dados_sp['Data'].dt.year
crimes_por_ano = dados_sp.groupby(['ano', 'Tipo_crime'])['Ocorrencias'].mean().reset_index()
fig3 = px.line(crimes_por_ano, x='ano', y='Ocorrencias', color='Tipo_crime', title='Evolução dos Crimes no Brasil (2014-2022)',labels={'Ocorrencias': 'Ocorrências', 'ano': 'Ano', 'Tipo_crime': 'Tipo de Crime'}, width=1200)
st.plotly_chart(fig3)

media_por_estado = df.groupby('Uf')['Ocorrencias'].mean().reset_index()
media_por_estado = media_por_estado.sort_values(by='Ocorrencias', ascending=False)
fig4 = px.bar(media_por_estado, x='Ocorrencias', y='Uf',orientation="h", title='Média de Ocorrências por Estado', height=960,width=1000,
              labels={'Uf': 'Estado', 'Ocorrencias': 'Média de Ocorrências'})

st.plotly_chart(fig4)


    
