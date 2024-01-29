#Libraries
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from PIL import Image
import plotly.express as px
import folium as folium

st.set_page_config(page_title='Visão Entregadores', layout='wide')

#-------------------------------
#Funções
#-------------------------------
def top_slowests_deliverers(df1):
        df2 = (df1.loc[:, ['Delivery_person_ID','City','Time_taken(min)']]
            .groupby(['City','Delivery_person_ID'])
            .mean()
            .sort_values(['City','Time_taken(min)'],ascending = False)
            .reset_index())
        df_aux01 = df2.loc[df2['City'] == 'Metropolitian ', :].head(10)
        df_aux02 = df2.loc[df2['City'] == 'Urban ', :].head(10)
        df_aux03 = df2.loc[df2['City'] == 'Semi-Urban ', :].head(10)
        df4 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
        st.dataframe(df4)
        return df4
def top_fastests_deliverers(df1):
      df2 = (df1.loc[:, ['Delivery_person_ID','City','Time_taken(min)']]
            .groupby(['City','Delivery_person_ID'])
            .mean()
            .sort_values(['City','Time_taken(min)'],ascending = True)
            .reset_index())
      df_aux01 = df2.loc[df2['City'] == 'Metropolitian ', :].head(10)
      df_aux02 = df2.loc[df2['City'] == 'Urban ', :].head(10)
      df_aux03 = df2.loc[df2['City'] == 'Semi-Urban ', :].head(10)
      df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
      st.dataframe(df3)
      return df3
def average_rating_per_weather_condition(df1):
      avg_std_weather = (df1.loc[:, ['Delivery_person_Ratings','Weatherconditions']]
                    .groupby('Weatherconditions')
                    .agg({'Delivery_person_Ratings': ['mean','std']}))
      
      avg_std_weather.columns = ['weather_mean', 'weather_std']
      avg_std_weather = avg_std_weather.reset_index()
      st.dataframe(avg_std_weather)
      return avg_std_weather
def avarege_rating_per_road_traffic_density(df1):
      avg_std_traffic = (df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density']]
                    .groupby('Road_traffic_density')
                    .agg({'Delivery_person_Ratings': ['mean','std']}))
      
      avg_std_traffic.columns = ['delivery_mean', 'delivery_std']
      avg_std_traffic = avg_std_traffic.reset_index()
      st.dataframe(avg_std_traffic)
      return avg_std_traffic
def average_rating_per_deliverer(df1):
      avg_deliverer = (df1.loc[:,['Delivery_person_ID', 'Delivery_person_Ratings']]
                      .groupby('Delivery_person_ID')
                      .mean()
                      .reset_index())
      st.dataframe(avg_deliverer)
      return avg_deliverer
def clean_code(df1):
  """ Esta função tem a responsabilidade de limpar o dataframe
    
        Tipo de limpeza:
        1. Remoção dos dados NaN
        2. Mudança de tipo  da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4.Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção de texto da viriável numérica)

        Input: Dataframe
        Output: Dataframe
    """

  df1 = df.copy()
  # 1. convertendo a colun ba Age de texto para numero
  df1['Delivery_person_Age'] = df1['Delivery_person_Age'].replace('NaN ', pd.NA)
  df1['Delivery_person_Age'] = df1['Delivery_person_Age'].fillna(0)
  df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

  #2. convertendo a coluna Ratings de texto para número decimal
  df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].replace('NaN ', pd.NA)
  df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].fillna(0)
  df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

  #3. convertendo a coluna order_date de texto para data
  df1['Order_Date'] = pd.to_datetime( df1['Order_Date'],format='%d-%m-%Y' )

  #4. convertendo multiple_deliveries de texto para numero inteiro
  df1['multiple_deliveries'] = df1['multiple_deliveries'].replace('NaN ', pd.NA)
  df1['multiple_deliveries'] = pd.to_numeric(df1['multiple_deliveries'], errors='coerce').fillna(0).astype(int)

  #5. removendo os espaços dentro de strings/texto/object
  df1 = df1.reset_index (drop=True)
  for i in range( len(df1)):
    df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

  #6. transformando Delivery_location_latitude em numero inteiro
  df1['Delivery_location_latitude'] = pd.to_numeric(df1['Delivery_location_latitude'], errors='coerce')
  df1['Delivery_location_latitude'] = df1['Delivery_location_latitude'].replace('NaN ', pd.NA)
  df1['Delivery_location_latitude'] = df1['Delivery_location_latitude'].fillna(0)
  df1['Delivery_location_latitude'] = df1['Delivery_location_latitude'].astype( int )

  #7. transformando Delivery_location_latitude em numero inteiro
  df1['Delivery_location_longitude'] = pd.to_numeric(df1['Delivery_location_longitude'], errors='coerce')
  df1['Delivery_location_longitude'] = df1['Delivery_location_longitude'].replace('NaN ', pd.NA)
  df1['Delivery_location_longitude'] = df1['Delivery_location_longitude'].fillna(0)
  df1['Delivery_location_longitude'] = df1['Delivery_location_longitude'].astype( int )

  #8. convertendo Time_taken(min) em int
  df1['Time_taken(min)'] = pd.to_numeric(df1['Time_taken(min)'], errors='coerce')
  df1['Time_taken(min)'] = df1['Time_taken(min)'].replace('NaN ', pd.NA)
  df1['Time_taken(min)'] = df1['Time_taken(min)'].fillna(0)
  df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

  #9. limpando latitude e longitude
  df1['Delivery_location_latitude'] = df1['Delivery_location_latitude'].astype(str)
  df1['Delivery_location_latitude'] = df1['Delivery_location_latitude'].str.extract(r'(\d{8})')
  df1 = df1.dropna(subset=['Delivery_location_latitude'])
  df1['Delivery_location_longitude'] = df1['Delivery_location_longitude'].astype(str)
  df1['Delivery_location_longitude'] = df1['Delivery_location_longitude'].str.extract(r'(\d{8})')
  df1 = df1.dropna(subset=['Delivery_location_longitude'])

  #10. limpando Age
  df1 = df1[df1['Delivery_person_Age'] != 0]
  df1.replace('NaN ', np.nan, inplace=True)
  return df1
  # import dataset
#--------------------------------------------- Início da Estrutura lógica do código ---------------------------------------------------
#================================
# import dataset
df = pd.read_excel('train.xlsx')
#limpando os dados
df1 = clean_code(df)
#===================================
#Sidebar do Streamlit
#===================================

st.header('Marketplace - Visão Entregadores')

#image_path = 'C:/Users/User/Documents/Data Analysis/DS-Project/logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Selecione uma data limite')
data_inicial = datetime(2022, 4, 13)
date_min = datetime(2022, 2, 11)
date_max = datetime(2022, 4, 6)
date_slider = st.sidebar.slider(
  'Até qual valor?',
  value= data_inicial,
  min_value= date_min,
  max_value= date_max,
  format = 'DD-MM-YYYY'
)
st.header(date_slider)
st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect(
  'Quais as condições do trânsito',
  ['Low ','Medium ','High ','Jam '],
  ['Low ','Medium ','High ','Jam ']
)

weather_options = st.sidebar.multiselect(
  'Quais as condições do clima',
  ['conditions Cloudy','conditions Fog','conditions Sandstorms','conditions Stormy', 'conditions Sunny', 'conditions Windy'],
  ['conditions Cloudy','conditions Fog','conditions Sandstorms','conditions Stormy', 'conditions Sunny', 'conditions Windy'])
st.sidebar.markdown("""___""")
#Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:] 

#Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:] 

#Filtro de clima
linhas_selecionadas = df1['Weatherconditions'].isin(weather_options)
df1 = df1.loc[linhas_selecionadas,:] 

#===================================
#Layout no Streamlit
#===================================

tab1, tab2 = st.tabs(['Visão Gerencial', '-'])
with tab1: 
  with st.container():

  #Overall Metrics
     
    st.markdown('# Overall Metrics')
    col1, col2, col3, col4 = st.columns(4, gap='large')
    with col1:
      maior_idade=df1.loc[:,'Delivery_person_Age'].max()
      col1.metric('Biggest age', maior_idade)
    with col2:
      menor_idade=df1.loc[:,'Delivery_person_Age'].min()
      col2.metric('Lowest age', menor_idade)
    with col3:
      melhor_condicao = df1.loc[:,'Vehicle_condition'].max()
      col3.metric('Better car condition', melhor_condicao)
    with col4:
      pior_condicao = df1.loc[:,'Vehicle_condition'].min()
      col4.metric('Worst car condition', pior_condicao)

      #Ratings

with st.container():
  st.markdown("""___""")
  st.title('Ratings')

  col1, col2= st.columns(2)
  with col1:
    st.markdown('##### Avarege Rating per deliverer')
    average_rating_per_deliverer(df1)
  with col2:
    st.markdown('##### Avarege Rating per road traffic density')
    avarege_rating_per_road_traffic_density(df1)
    st.markdown('##### Average Rating per weather condition')
    average_rating_per_weather_condition(df1)

    #Delivery Speed

with st.container():
  st.markdown("""___""")
  st.title('Delivery Speed')  

  col1, col2= st.columns(2)

  with col1:
    st.subheader('Top Fastests deliverers')
    top_fastests_deliverers(df1)
  with col2:
    st.subheader('Top Slowests deliverers')
    top_slowests_deliverers(df1)
    
