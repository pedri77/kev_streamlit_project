import requests
import pandas as pd
import datetime
import io
import streamlit as st
import plotly.express as px

st.title("Catálogo KEV: Vulnerabilidades Explotadas (Última Semana)")

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv"
response = requests.get(KEV_URL)
df = pd.read_csv(io.StringIO(response.text))

hoy = datetime.datetime.utcnow()
df['dateAdded'] = pd.to_datetime(df['dateAdded'], errors='coerce')
una_semana = hoy - datetime.timedelta(days=7)
df_recent = df[df['dateAdded'] >= una_semana]

st.subheader("Tabla de vulnerabilidades recientes")
st.dataframe(df_recent[['cveID', 'vendorProject', 'product', 'vulnerabilityName', 'dateAdded']])

st.subheader("Vulnerabilidades recientes por proveedor")
fig1 = px.bar(df_recent['vendorProject'].value_counts().reset_index(),
              x='index', y='vendorProject',
              labels={'index': 'Proveedor', 'vendorProject': 'Cantidad'},
              title='Proveedores afectados')
st.plotly_chart(fig1)

st.subheader("Distribución por fecha de inclusión")
fig2 = px.histogram(df_recent, x='dateAdded', nbins=7,
                    title='Vulnerabilidades por fecha',
                    labels={'dateAdded': 'Fecha'})
st.plotly_chart(fig2)

st.subheader("Descargar Excel")
nombre_archivo = f"kev_ultimos_7_dias_{hoy.strftime('%Y%m%d')}.xlsx"
buffer = io.BytesIO()
df_recent.to_excel(buffer, index=False)
buffer.seek(0)
st.download_button(label="Descargar archivo Excel", data=buffer, file_name=nombre_archivo, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
