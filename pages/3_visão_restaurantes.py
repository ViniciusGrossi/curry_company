#Libraries
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from PIL import Image
import plotly.express as px
import folium as folium
import plotly.graph_objects as go

st.set_page_config(page_title='Visão Restaurantes', layout='wide')
#-------------------------------
#Funções
def city_and_type(df1):
            df_aux = (df1.loc[:,['Type_of_order','City', 'Time_taken(min)']]
                    .groupby(['City','Type_of_order'])
                    .agg({'Time_taken(min)':['mean','std']}))
            df_aux.columns = ['avg_time','std_time']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)
def sunburst(df1):
            df_aux = (df1.loc[:,['Road_traffic_density','City', 'Time_taken(min)']]
                    .groupby(['City','Road_traffic_density'])
                    .agg({'Time_taken(min)': ['mean','std']}))
            df_aux.columns = ['avg_time','std_time']
            df_aux = df_aux.reset_index()
            fig = px.sunburst(df_aux, path=['City','Road_traffic_density'], 
                            values='avg_time', 
                            color= 'std_time', 
                            color_continuous_scale= 'RdBu',
                            color_continuous_midpoint=np.average(df_aux['std_time']))
            st.plotly_chart(fig)
def  time_distribution(df1):
        df_aux = df1.loc[:,['Time_taken(min)','City']].groupby('City').agg({'Time_taken(min)': ['mean','std']})
        df_aux.columns = ['avg_time','std_time']
        df_aux = df_aux.reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(name = 'Control',
                        x=df_aux['City'],
                        y=df_aux['avg_time'],
                        error_y = dict(type='data', array=df_aux['std_time'])))
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)
        return fig
def clean_code(df1):
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

  #10. limpando Age
  df1['Delivery_person_Age'] = df1['Delivery_person_Age'] != 0

  return df
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

tab1, tab2 = st.tabs(['Visão Gerencial', '-'])
with tab1:
  with st.container():
    st.markdown("""___""")
    st.title('Overall Metrics')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        delivery_unique = len(df1['Delivery_person_ID'].unique())
        st.metric('Deliverers', delivery_unique)
    with col2:
        df_aux = (df1.loc[:, ['Time_taken(min)','Festival']]
                  .groupby('Festival')
                  .agg({'Time_taken(min)': ['mean','std']}))
        
        df_aux.columns = ['avg_time','std_time']
        df_aux = df_aux.reset_index()
        df_aux  = np.round(df_aux.loc[df_aux['Festival'] == 'Yes ','avg_time'], 2)
        col2.metric('Avg Delivery time at the Festivals', df_aux)

    with col3:
        df_aux = (df1.loc[:, ['Time_taken(min)','Festival']]
                  .groupby('Festival')
                  .agg({'Time_taken(min)': ['mean','std']}))
        
        df_aux.columns = ['avg_time','std_time']
        df_aux = df_aux.reset_index()
        df_aux  = np.round(df_aux.loc[df_aux['Festival'] == 'Yes ','std_time'], 2)
        col3.metric('Std Delivery time at the Festivals', df_aux)
    with col4:
        df_aux = (df1.loc[:, ['Time_taken(min)','Festival']]
                  .groupby('Festival')
                  .agg({'Time_taken(min)': ['mean','std']}))
        
        df_aux.columns = ['avg_time','std_time']
        df_aux = df_aux.reset_index()
        df_aux  = np.round(df_aux.loc[df_aux['Festival'] == 'No ','avg_time'], 2)
        col4.metric('Avg Delivery time without Festivals', df_aux)
    with col5:
        df_aux = (df1.loc[:, ['Time_taken(min)','Festival']]
                  .groupby('Festival')
                  .agg({'Time_taken(min)': ['mean','std']}))
        
        df_aux.columns = ['avg_time','std_time']
        df_aux = df_aux.reset_index()
        df_aux  = np.round(df_aux.loc[df_aux['Festival'] == 'No ','std_time'], 2)
        col5.metric('Std Delivery time at the Festivals', df_aux)     
     
  with st.container():
       #-------------------------------
        st.markdown("""___""")
        st.title('Time distribution')
        time_distribution(df1)

        st.markdown("""___""")
        st.title('SunBurst')
        sunburst(df1)

        st.markdown("""___""")
        st.title('Average and std time by type order and city')
        city_and_type(df1)
        
        
