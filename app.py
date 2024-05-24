import streamlit as st
import psycopg2


def generar_graficos(df):
    """
    Función para iterar sobre un DataFrame y generar gráficos Plotly.

    Args:
        df (pandas.DataFrame): El DataFrame a procesar.

    Returns:
        None: No se devuelve ningún valor.
    """

    # Recorre las columnas del DataFrame
    for columna in df.columns:
        # Crea un gráfico de dispersión para cada columna
        fig = px.scatter(df, x=columna, y='otra_columna')  # Reemplaza 'otra_columna' con la variable Y deseada

        # Muestra el gráfico en Streamlit
        st.plotly_chart(fig)
