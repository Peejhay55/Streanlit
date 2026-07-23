
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# Configuración
# -----------------------------
st.set_page_config(
    page_title="Análisis de Accidentes de Tránsito",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Simulador y Analizador de Accidentes de Tránsito")
st.markdown(
    """
Este sistema genera datos simulados de accidentes de tránsito y presenta
análisis cuantitativos, cualitativos y gráficos de manera interactiva.
"""
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Configuración")

n = st.sidebar.slider(
    "Cantidad de accidentes",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

seed = st.sidebar.number_input(
    "Semilla aleatoria",
    value=42,
    step=1
)

np.random.seed(seed)

# -----------------------------
# Simulación
# -----------------------------
vehiculos = ["Carro", "Moto"]

climas = [
    "Soleado",
    "Lluvia",
    "Nublado"
]

gravedad = [
    "Leve",
    "Moderado",
    "Grave"
]

causas = [
    "Exceso de velocidad",
    "Distracción",
    "Alcohol",
    "Falla mecánica",
    "Condiciones de la vía"
]

ciudades = [
    "Bogotá",
    "Medellín",
    "Cali",
    "Barranquilla",
    "Bucaramanga"
]

df = pd.DataFrame({
    "Vehículo": np.random.choice(vehiculos, n, p=[0.55, 0.45]),
    "Ciudad": np.random.choice(ciudades, n),
    "Clima": np.random.choice(climas, n, p=[0.5,0.3,0.2]),
    "Gravedad": np.random.choice(gravedad, n, p=[0.6,0.3,0.1]),
    "Causa": np.random.choice(causas, n),
    "Edad conductor": np.random.randint(18,70,n),
    "Hora": np.random.randint(0,24,n)
})

# -----------------------------
# Datos
# -----------------------------
st.header("Datos simulados")
st.dataframe(df, use_container_width=True)

# -----------------------------
# Indicadores
# -----------------------------
st.header("Análisis Cuantitativo")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total accidentes", len(df))
c2.metric("Carros", (df["Vehículo"]=="Carro").sum())
c3.metric("Motos", (df["Vehículo"]=="Moto").sum())
c4.metric("Edad promedio", round(df["Edad conductor"].mean(),1))

# -----------------------------
# Análisis cualitativo
# -----------------------------
st.header("Análisis Cualitativo")

tipo = df["Vehículo"].value_counts().idxmax()
causa = df["Causa"].value_counts().idxmax()
gravedad_pred = df["Gravedad"].value_counts().idxmax()

st.write(f"• El vehículo con mayor número de accidentes fue **{tipo}**.")
st.write(f"• La causa más frecuente fue **{causa}**.")
st.write(f"• La gravedad predominante fue **{gravedad_pred}**.")

# -----------------------------
# Filtros
# -----------------------------
st.header("Interacción Dinámica")

vehiculo = st.selectbox(
    "Filtrar por vehículo",
    ["Todos"] + vehiculos
)

ciudad = st.selectbox(
    "Filtrar por ciudad",
    ["Todas"] + ciudades
)

filtro = df.copy()

if vehiculo != "Todos":
    filtro = filtro[filtro["Vehículo"] == vehiculo]

if ciudad != "Todas":
    filtro = filtro[filtro["Ciudad"] == ciudad]

st.write(f"Registros encontrados: **{len(filtro)}**")

# -----------------------------
# Gráficos
# -----------------------------
st.header("Análisis Gráfico")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        filtro,
        x="Vehículo",
        color="Vehículo",
        title="Accidentes por tipo de vehículo"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        filtro,
        names="Gravedad",
        title="Distribución por gravedad"
    )
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig = px.bar(
        filtro["Causa"].value_counts().reset_index(),
        x="index",
        y="Causa",
        labels={
            "index":"Causa",
            "Causa":"Cantidad"
        },
        title="Accidentes por causa"
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.histogram(
        filtro,
        x="Hora",
        nbins=24,
        title="Accidentes por hora"
    )
    st.plotly_chart(fig, use_container_width=True)

st.header("Datos filtrados")
st.dataframe(filtro, use_container_width=True)
