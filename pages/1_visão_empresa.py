#Libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import folium as folium
import plotly.graph_objects as go

from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Empresa', layout='wide')
#-------------------------------
#Funções
#-------------------------------
def country_maps(df1):
    data = {
        'City': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Jaipur', 'Ahmedabad', 'Pune', 'Lucknow'],
        'Latitude': [19.0760, 28.6139, 12.9716, 17.3850, 13.0827, 22.5726, 26.9124, 23.0225, 18.5204, 26.8467],
        'Longitude': [72.8777, 77.2090, 77.5946, 78.4867, 80.2707, 88.3639, 75.7873, 72.5714, 73.8567, 80.9462]
    }
    df_coordinates = pd.DataFrame(data)
    #map
    map = folium.Map()
    for index, location_info in df_coordinates.iterrows():
        folium.Marker( [location_info['Latitude'],
                    location_info['Longitude']],
                    popup=location_info['Latitude']).add_to(map)
    folium_static(map,width=1024,height=600)
    return index
def orders_share_by_week(df1):
        df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
        df_aux1 = (df1.loc[:,['ID','week_of_year']]
                   .groupby('week_of_year')
                   .count()
                   .reset_index())
        df_aux2 = (df1.loc[:,['Delivery_person_ID', 'week_of_year']]
                   .groupby('week_of_year')
                   .nunique()
                   .reset_index())
        df_aux = pd.merge( df_aux1, df_aux2, how = 'inner')
        df_aux['order_by_deliverer'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        fig = px.line(df_aux, x = 'week_of_year', y= 'order_by_deliverer')
        return fig
def order_by_week(df1):        
        df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
        df_aux = (df1.loc[:,['ID','week_of_year']]
                  .groupby('week_of_year')
                  .count()
                  .reset_index())
        fig = px.line(df_aux, x='week_of_year', y='ID')
        return fig
def traffic_order_city(df1): 
                columns = ['ID','City', 'Road_traffic_density']
                df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].replace('NaN ', pd.NA)
                df_aux = (df1.loc[:, columns]
                          .groupby(['City','Road_traffic_density'])
                          .count()
                          .reset_index())
                fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
                return fig
def traffic_order_share(df1):
    columns = ['ID','Road_traffic_density']
    df_aux = (df1.loc[:, columns]
              .groupby('Road_traffic_density')
              .count()
              .reset_index())
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN',:]
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
    return fig
def order_metric(df1):
        #Order Metrics
            columns = ['ID', 'Order_Date']
            df_aux = df1.loc[:,columns].groupby('Order_Date').count().reset_index()
            #Plotly
            fig = px.bar(df_aux, x='Order_Date', y='ID' )

            return fig
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
    df1.replace('NaN ', np.nan, inplace=True)
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

    return df1
#--------------------------------------------- Início da Estrutura lógica do código ---------------------------------------------------
#================================
# import dataset
df = pd.read_excel('dataset/train.xlsx')
#limpando os dados
df1 = clean_code(df)

#Sidebar do Streamlit
st.header('Marketplace - Visão Cliente')

#image_path = 'C:/Users/User/Documents/Data Analysis/logo.png'
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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática','Visão Geográfica'])
with tab1: 
  with st.container():
    fig = order_metric(df1)
    st.markdown('# Orders by day')
    st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
          fig = traffic_order_share(df1)
          st.header('Traffic Order Share')
          st.plotly_chart(fig, use_container_width=True)
     
        with col2:
          fig = traffic_order_city(df1)
          st.header('Traffic Order City')
          st.plotly_chart(fig, use_container_width=True)
            
with tab2: 
  with st.container():
    fig = order_by_week(df1)
    st.header ('Orders by Week')
    st.plotly_chart(fig, use_container_width=True)
  with st.container():
    fig = orders_share_by_week(df1)
    st.header('Orders Share by week')
    st.plotly_chart(fig, use_container_width=True)
with tab3:
  st.markdown('# Country Maps')
  country_maps(df1)
  
#===================================
#Carga
#===================================
  
