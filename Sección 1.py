import streamlit as st
import pandas as pd
import io

# --- Configuración de la Página ---
st.set_page_config(
    page_title="App Contable (Mi Hermana)",
    page_icon="🧾",
    layout="wide"
)

# --- Estado de la Sesión (Session State) ---
# Usamos st.session_state para guardar los DataFrames cargados
if 'df_caja' not in st.session_state:
    st.session_state.df_caja = None
if 'df_bancos' not in st.session_state:
    st.session_state.df_bancos = None
if 'df_asientos_ventas' not in st.session_state:
    st.session_state.df_asientos_ventas = None
if 'df_asientos_compras' not in st.session_state:
    st.session_state.df_asientos_compras = None

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    st.title("Cargador de Libros Contables")
    st.write("Sube los archivos Excel de tu hermana aquí.")
    st.info("La app espera los archivos `.xls` o `.xlsx` originales.")

    # --- UPLOADER 1: LIBRO CAJA Y BANCOS ---
    st.header("1. Libro Caja y Bancos (.xls)")
    st.write("Sube `FORMATOS DE LIBROS CAJA Y BANCOS.xls`")
    file_caja_bancos = st.file_uploader("Cargar .xls Caja y Bancos", type=["xls", "xlsx"], key="file_caja")

    if file_caja_bancos:
        try:
            # Leemos las hojas relevantes (Formato 1.1 y 1.2)
            # Basado en el análisis de los CSV, los headers están en filas específicas
            st.session_state.df_caja = pd.read_excel(file_caja_bancos, sheet_name="L.CAJA01", header=8)
            st.session_state.df_bancos = pd.read_excel(file_caja_bancos, sheet_name="L.CAJA02", header=9)
            st.success("¡Caja y Bancos cargados!")
        except Exception as e:
            st.error(f"Error al leer Caja/Bancos: {e}")
            st.warning("Asegúrate de que las hojas se llamen 'L.CAJA01' y 'L.CAJA02'.")

    # --- UPLOADER 2: LIBRO VENTAS ---
    st.header("2. Libro de Ventas (.xlsx)")
    st.write("Sube `Libro de ventas.xlsx`")
    file_ventas = st.file_uploader("Cargar .xlsx Ventas", type=["xls", "xlsx"], key="file_ventas")

    if file_ventas:
        try:
            # Asientos de Ventas: Hoja "A.C."
            st.session_state.df_asientos_ventas = pd.read_excel(file_ventas, sheet_name="A.C.", header=9)
            st.success("¡Asientos de Ventas cargados!")
        except Exception as e:
            st.error(f"Error al leer Asientos de Ventas: {e}")
            st.warning("Asegúrate de que la hoja se llame 'A.C.'.")

    # --- UPLOADER 3: LIBRO COMPRAS ---
    st.header("3. Libro de Compras (.xlsx)")
    st.write("Sube `Libro de compras.xlsx`")
    file_compras = st.file_uploader("Cargar .xlsx Compras", type=["xls", "xlsx"], key="file_compras")

    if file_compras:
        try:
            # Asientos de Compras: Usaremos "Hoja3" que está más estructurada
            st.session_state.df_asientos_compras = pd.read_excel(file_compras, sheet_name="Hoja3", header=5)
            st.success("¡Asientos de Compras cargados!")
        except Exception as e:
            st.error(f"Error al leer Asientos de Compras: {e}")
            st.warning("Asegúrate de que la hoja se llame 'Hoja3'.")

# --- Página Principal ---
st.title("Validador de Libros Contables 🧾")
st.write("Esta aplicación implementa la lógica de corrección definida por tu hermana (basada en `plan_de_app.md`).")
st.markdown("---")

# --- Lógica de la App ---
# 1. Verificar si todos los archivos están cargados
archivos_cargados = (
    st.session_state.df_caja is not None and
    st.session_state.df_bancos is not None and
    st.session_state.df_asientos_ventas is not None and
    st.session_state.df_asientos_compras is not None
)

if not archivos_cargados:
    st.warning("Por favor, carga los 3 archivos Excel en la barra lateral izquierda para comenzar.")
    # 
    st.image("https://i.imgur.com/gYvD31Y.png", caption="Sube los archivos en la barra lateral", width=300)
else:
    st.success("¡Todos los archivos han sido cargados con éxito!")
    st.info("Aquí es donde implementaremos la lógica de corrección (Parte 2 del Plan).")

    # Mostramos un preview de los datos cargados
    st.subheader("Verificación de Datos Cargados")

    with st.expander("Ver Formato 1.1: Libro Caja (Efectivo)"):
        st.dataframe(st.session_state.df_caja.head())

    with st.expander("Ver Formato 1.2: Libro Bancos (Cuenta Corriente)"):
        st.dataframe(st.session_state.df_bancos.head())

    with st.expander("Ver Asientos de Ventas (A.C.)"):
        st.dataframe(st.session_state.df_asientos_ventas.head())

    with st.expander("Ver Asientos de Compras (Hoja3)"):
        st.dataframe(st.session_state.df_asientos_compras.head())

    # --- Placeholder para la Lógica de Corrección ---
    st.subheader("Próximo Paso: Aplicar Lógica de Corrección")
    st.write("El siguiente paso será tomar los asientos de ventas y compras y cruzarlos con la información de caja y bancos para encontrar y corregir las inconsistencias.")

    st.code("""
# Lógica a implementar (pseudo-código):

# 1. Limpiar datos (quitar NaNs, convertir montos, estandarizar descripciones)
# ...

# 2. Iterar sobre Asientos de Ventas
# para cada asiento_venta in df_asientos_ventas:
#   if es_asiento_de_cobro:
#     monto = asiento_venta['Monto_Cobrado']
#     comprobante = asiento_venta['Nro_Comprobante']
#
#     # Buscar en CAJA (Formato 1.1)
#     if comprobante in df_caja['Descripción']:
#       asiento_venta['Cuenta_Corregida'] = 101 # Caja
#
#     # Buscar en BANCOS (Formato 1.2)
#     elif comprobante in df_bancos['Descripción']:
#       asiento_venta['Cuenta_Corregida'] = 104 # Bancos
#
#     else:
#       asiento_venta['Cuenta_Corregida'] = "ERROR: No Encontrado"
#
# # 3. Repetir lógica para Asientos de Compras
# ...

# 4. Mostrar tabla de asientos corregidos
# st.dataframe(df_asientos_ventas_corregido)
    """, language="python")
