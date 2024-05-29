import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

import os

my_database = os.environ.get('my_database')
my_host = os.environ.get('my_host')
my_password = os.environ.get('my_password')
my_port = os.environ.get('my_port')
my_user = os.environ.get('my_user')

# Configura las variables de conexión
HOST = my_host
DATABASE = my_database
USER = my_user
PASSWORD = my_password
PORT = my_port  # Asegúrate de que este valor sea un entero

# Configura la conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT
    )

# Función para ejecutar consultas SQL y devolver un DataFrame de Pandas
def sql_query(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.set_page_config(page_title="Inside", page_icon="img/cropped-Beyond-Education_Horizonatal-color.png")

# Menú lateral
option = st.sidebar.selectbox('Navigation', ['Home', 'Preguntas más frecuentes', 
                                             'Desde dónde nos escriben', 
                                             'Destinos de interés'])

if option == 'Home':

    # Página de inicio
    
    st.markdown('# Inside Beyond Education', unsafe_allow_html=True)
    st.image('cropped-Beyond-Education_Horizonatal-color.png', use_column_width=True)



# Si selecciona 'Preguntas más frecuentes', mostrar el gráfico
elif option == 'Preguntas más frecuentes':
    # Cargar los datos desde la base de datos
    query = '''
    SELECT * 
    FROM messages
    '''

    df = sql_query(query)

    # Limpiar y procesar los datos
    df['pregunta'] = df['pregunta'].str.translate(str.maketrans('áéíóúÁÉÍÓÚ', 'aeiouAEIOU')).str.lower()

    # Contar las preguntas por categoría
    servicios_count = len(df[df['pregunta'].str.contains("servicios")])
    categories = ['informacion', 'asesoramiento', 'campamento', 'voluntariado', 'universidad', 'orientacion', 
                  'vocacional', 'profesional', 'hijo', 'extranjero', 'verano', 'carrera', 'destino', 'ingles', 
                  'visa', 'beca', 'cv', 'gestion', 'estudiar', 'examen', 'contacto']
    conteos = {category: len(df[df['pregunta'].str.contains(category)]) for category in categories}
    preguntas_df = pd.DataFrame({'categoria': list(conteos.keys()), 'conteo': list(conteos.values())})
    preguntas_df = preguntas_df.sort_values(by='conteo', ascending=False)

    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(preguntas_df, x='categoria', y='conteo', title='Preguntas más frecuentes por los usuarios', labels={'categoria': 'Preguntas', 'conteo': 'Conteo'})

    # Cambiar colores de las barras
    fig.update_traces(marker_color=['#AD66D5']*5 + ['#6C8CD5']*(len(preguntas_df)-5))

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

# Si selecciona 'Desde dónde nos escriben', mostrar el gráfico
elif option == 'Desde dónde nos escriben':
    # Cargar los datos desde la base de datos
    query = '''
    SELECT * 
    FROM messages
    '''

    df = sql_query(query)

    # Filtrar y contar los mensajes por país
    countries = ['de mexico', 'de colombia', 'de españa']
    conteos = {country: len(df[df['pregunta'].str.contains(country, case=False, na=False)]) for country in countries}
    paises_df = pd.DataFrame({'pais': list(conteos.keys()), 'conteo': list(conteos.values())})
    paises_df = paises_df.sort_values(by='conteo', ascending=False)

    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(paises_df, x='pais', y='conteo', title='Mensajes por país', labels={'pais': 'País', 'conteo': 'Conteo'})

    # Cambiar colores de las barras
    fig.update_traces(marker_color=['#AD66D5', '#6C8CD5','#FFE773'])

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)


# Si selecciona 'Destinos de interés', mostrar el gráfico
elif option == 'Destinos de interés':
    # Cargar los datos desde la base de datos
    query = '''
    SELECT * 
    FROM messages
    '''

    df = sql_query(query)

   
    countries = ['holanda', 'estados unidos', 'francia', 'alemania', 'reino unido', 'irlanda', 'portugal', 'españa']
    conteos = {country: len(df[df['pregunta'].str.contains(country, case=False, na=False)]) for country in countries}
    destinos_df = pd.DataFrame({'pais': list(conteos.keys()), 'conteo': list(conteos.values())})
    destinos_df = destinos_df.sort_values(by='conteo', ascending=False)
    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(destinos_df, x='pais', y='conteo', title='Mensajes por destino de interés', labels={'pais': 'País', 'conteo': 'Conteo'})
    
    # Cambiar colores de las barras
    colores = ['#AD66D5']*4 + ['#6C8CD5']*(len(destinos_df)-4)
    fig.update_traces(marker_color=colores)

    st.plotly_chart(fig)


