import streamlit as st
import psycopg2
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import folium_static

# Definir la conexión a la base de datos
def get_db_connection():
    my_database = "chatbot_8n2w"
    my_host = "dpg-cp6qaka0si5c73aigcc0-a.frankfurt-postgres.render.com"
    my_password = "UmxrGACXMb3Y1jaYLwnuS5zQDUBtXWg6"
    my_port = 5432 
    my_user = "chatbot_8n2w_user"
    return psycopg2.connect(
        host=my_host,
        database=my_database,
        user=my_user,
        password=my_password,
        port=my_port
    )

# Función para ejecutar consultas SQL y devolver un DataFrame de Pandas
def sql_query(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Página de inicio
st.markdown('# Inside Beyond Education', unsafe_allow_html=True)
st.image('cropped-Beyond-Education_Horizonatal-color.png', use_column_width=True)

# Menú lateral
option = st.sidebar.selectbox('Navigation', ['Home', 'Preguntas más frecuentes', 
                                             'Desde dónde nos escriben', 
                                             'Destinos de interés',
                                             'Destinos voluntariados', 
                                             'Destinos campamentos'])

# Si selecciona 'Preguntas más frecuentes', mostrar el gráfico
if option == 'Preguntas más frecuentes':
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


# Si selecciona 'Destinos voluntariados', mostrar el mapa de folium.Marker
elif option == 'Destinos voluntariados':
    # Crear un DataFrame con los destinos y sus coordenadas
    data = {
        'destinos': ['Costa Rica', 'Ecuador', 'Panamá', 'Australia', 'Cambodia', 'Fiji', 'Ghana', 'Grecia', 'Hawai', 'Marruecos', 'Perú', 'República Dominicana', 'Tailandia', 'Tanzania', 'Vietnam'],
        'latitud': [9.7489, -1.8312, 8.5380, -25.2744, 12.5657, -17.7134, 7.9465, 39.0742, 19.8968, 31.7917, -9.1899, 18.7357, 15.8700, -6.3690, 14.0583],
        'longitud': [-83.7534, -78.1834, -80.7821, 133.7751, 104.9910, 178.0650, -1.0232, 21.8243, -155.5828, -7.0926, -75.0152, -70.1627, 100.9925, 34.8888, 108.2772]
    }
    df_destinos = pd.DataFrame(data)

    # Crear el mapa con folium.Marker
    mymap = folium.Map(location=[0, 0], zoom_start=2)
    for _, row in df_destinos.iterrows():
        folium.Marker([row['latitud'], row['longitud']], popup=row['destinos']).add_to(mymap)

    # Mostrar el mapa en Streamlit
    folium_static(mymap)

# Si selecciona 'Destinos campamentos', mostrar el mapa con los destinos de campamentos
elif option == 'Destinos campamentos':
    # Crear un DataFrame con los destinos de campamentos y sus coordenadas
    data_campamentos = {
        'destinos': ['West Sussex', 'Crawley', 'Northampton', 'Buckinghamshire', 'Dorset', 'London', 'Manchester', 
                     'Biarritz', 'French Alps', 'Switzerland', 'Swiss Alps', 'Maine', 'New Hampshire', 'Pennsylvania', 
                     'Florida', 'Santander', 'Barcelona', 'Madrid', 'León', 'Berlin', 'Canada', 'Dublin'],
        'latitud': [50.8091, 51.1092, 52.2405, 51.9943, 50.7151, 51.5074, 53.4808, 43.4832, 45.8325, 46.8182, 46.8182, 45.2538, 
                    43.1939, 40.7128, 27.9944, 43.4623, 41.3851, 40.4168, 42.5987, 52.5200, 53.3498, 53.3498],
        'longitud': [-0.7539, -0.1872, -0.9027, -0.7394, -2.4406, -0.1278, -2.2426, -1.5586, 6.6113, 8.2275, 8.2275, -69.4455, 
                     -71.5724, -77.0369, -81.7603, -3.8196, 2.1734, -3.7038, -5.5671, 13.4050, -106.3468, -6.2603]
    }

    df_campamentos = pd.DataFrame(data_campamentos)

    # Crear el mapa con folium.Marker
    mymap_campamentos = folium.Map(location=[0, 0], zoom_start=2)
    for _, row in df_campamentos.iterrows():
        folium.Marker([row['latitud'], row['longitud']], popup=row['destinos']).add_to(mymap_campamentos)

    # Mostrar el mapa en Streamlit
    folium_static(mymap_campamentos)
