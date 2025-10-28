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
# Inicializamos todos los DataFrames que necesitamos
dfs = [
    'df_caja', 'df_bancos', 'df_asientos_ventas', 'df_registro_ventas',
    'df_asientos_compras', 'df_registro_compras', 'df_planilla',
    'df_libro_diario', 'df_balance_general', 'df_eri_funcion',
    'df_plan_contable'  # <-- NUEVO: Añadimos el Plan de Cuentas Maestro
]
for df in dfs:
    if df not in st.session_state:
        st.session_state[df] = None

# --- Función para limpiar y mostrar preview (CORREGIDA) ---
def show_preview(df, title):
    """Muestra un expander con el preview de un DataFrame."""
    with st.expander(f"Ver Preview: {title}", expanded=False):
        if df is not None:
            st.dataframe(df.head())
        else:
            st.info("Hoja no cargada o aún no seleccionada.")

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    st.title("Cargador de Libros Contables")
    st.write("Sube los archivos Excel de tu hermana aquí.")
    st.info("Selecciona la hoja correcta para cada formato.")

    # --- UPLOADER 1: LIBRO CAJA Y BANCOS ---
    st.header("1. Libro Caja y Bancos (.xls)")
    file_caja_bancos = st.file_uploader("Cargar `FORMATOS...xls`", type=["xls", "xlsx"], key="file_caja")

    if file_caja_bancos:
        try:
            file_bytes = file_caja_bancos.getvalue()
            xls_buffer = io.BytesIO(file_bytes)
            xls_caja = pd.ExcelFile(xls_buffer, engine='xlrd')
            sheet_names_caja = xls_caja.sheet_names
            
            # Selector para L.CAJA01 (Efectivo)
            sheet_caja = st.selectbox(
                "Selecciona hoja 'L.CAJA01' (Efectivo)", 
                sheet_names_caja, 
                index=None, 
                placeholder="Elige la hoja de Caja...",
                key="cb_caja"
            )
            if sheet_caja:
                st.session_state.df_caja = pd.read_excel(xls_caja, sheet_name=sheet_caja, header=8)
                st.success(f"Hoja '{sheet_caja}' cargada (Caja).")

            # Selector para L.CAJA02 (Bancos)
            sheet_bancos = st.selectbox(
                "Selecciona hoja 'L.CAJA02' (Bancos)", 
                sheet_names_caja, 
                index=None, 
                placeholder="Elige la hoja de Bancos...",
                key="cb_bancos"
            )
            if sheet_bancos:
                st.session_state.df_bancos = pd.read_excel(xls_caja, sheet_name=sheet_bancos, header=8)
                st.success(f"Hoja '{sheet_bancos}' cargada (Bancos).")
                
        except Exception as e:
            st.error(f"Error al leer Caja/Bancos: {e}")

    # --- UPLOADER 2: LIBRO VENTAS ---
    st.header("2. Libro de Ventas (.xlsx)")
    file_ventas = st.file_uploader("Cargar `Libro de ventas.xlsx`", type=["xls", "xlsx"], key="file_ventas")

    if file_ventas:
        try:
            file_bytes = file_ventas.getvalue()
            xls_buffer = io.BytesIO(file_bytes)
            xls_ventas = pd.ExcelFile(xls_buffer, engine='openpyxl')
            sheet_names_ventas = xls_ventas.sheet_names

            # Selector para Asientos de Ventas (A.C.)
            sheet_asientos_ventas = st.selectbox(
                "Selecciona hoja 'A.C.' (Asientos Venta)", 
                sheet_names_ventas, 
                index=None, 
                placeholder="Elige la hoja de Asientos...",
                key="cb_asientos_ventas"
            )
            if sheet_asientos_ventas:
                st.session_state.df_asientos_ventas = pd.read_excel(xls_ventas, sheet_name=sheet_asientos_ventas, header=8)
                st.success(f"Hoja '{sheet_asientos_ventas}' cargada (Asientos Venta).")
            
            # Selector para Registro de Ventas (Formato 14.1)
            sheet_reg_ventas = st.selectbox(
                "Selecciona hoja 'Hoja1' (Registro Venta)", 
                sheet_names_ventas, 
                index=None, 
                placeholder="Elige la hoja de Registro...",
                key="cb_reg_ventas"
            )
            if sheet_reg_ventas:
                st.session_state.df_registro_ventas = pd.read_excel(xls_ventas, sheet_name=sheet_reg_ventas, header=8)
                st.success(f"Hoja '{sheet_reg_ventas}' cargada (Registro Venta).")

        except Exception as e:
            st.error(f"Error al leer Ventas: {e}")

    # --- UPLOADER 3: LIBRO COMPRAS ---
    st.header("3. Libro de Compras (.xlsx)")
    file_compras = st.file_uploader("Cargar `Libro de compras.xlsx`", type=["xls", "xlsx"], key="file_compras")

    if file_compras:
        try:
            file_bytes = file_compras.getvalue()
            xls_buffer = io.BytesIO(file_bytes)
            xls_compras = pd.ExcelFile(xls_buffer, engine='openpyxl')
            sheet_names_compras = xls_compras.sheet_names

            # Selector para Asientos de Compras (Hoja3)
            sheet_asientos_compras = st.selectbox(
                "Selecciona hoja 'Hoja3' (Asientos Compra)", 
                sheet_names_compras, 
                index=None, 
                placeholder="Elige la hoja de Asientos...",
                key="cb_asientos_compras"
            )
            if sheet_asientos_compras:
                st.session_state.df_asientos_compras = pd.read_excel(xls_compras, sheet_name=sheet_asientos_compras, header=5)
                st.success(f"Hoja '{sheet_asientos_compras}' cargada (Asientos Compra).")

            # Selector para Registro de Compras (Formato 8.1)
            sheet_reg_compras = st.selectbox(
                "Selecciona hoja 'Hoja1' (Registro Compra)", 
                sheet_names_compras, 
                index=None, 
                placeholder="Elige la hoja de Registro...",
                key="cb_reg_compras"
            )
            if sheet_reg_compras:
                st.session_state.df_registro_compras = pd.read_excel(xls_compras, sheet_name=sheet_reg_compras, header=8)
                st.success(f"Hoja '{sheet_reg_compras}' cargada (Registro Compra).")

        except Exception as e:
            st.error(f"Error al leer Compras: {e}")

    # --- UPLOADER 4: PLANILLA ---
    st.header("4. Planilla de Trabajadores (.xlsx)")
    file_planilla = st.file_uploader("Cargar `Planilla...xlsx`", type=["xls", "xlsx"], key="file_planilla")

    if file_planilla:
        try:
            file_bytes = file_planilla.getvalue()
            xls_buffer = io.BytesIO(file_bytes)
            xls_planilla = pd.ExcelFile(xls_buffer, engine='openpyxl')
            sheet_names_planilla = xls_planilla.sheet_names
            
            sheet_planilla = st.selectbox(
                "Selecciona la hoja de 'Planilla'", 
                sheet_names_planilla, 
                index=None, 
                placeholder="Elige la hoja de Planilla...",
                key="cb_planilla"
            )
            if sheet_planilla:
                st.session_state.df_planilla = pd.read_excel(xls_planilla, sheet_name=sheet_planilla, header=10)
                st.success(f"Hoja '{sheet_planilla}' cargada (Planilla).")
        except Exception as e:
            st.error(f"Error al leer Planilla: {e}")

    # --- UPLOADER 5: DESARROLLO CASO PRÁCTICO ---
    st.header("5. Caso Práctico (Reportes Finales)")
    file_dev = st.file_uploader("Cargar `Desarrollo caso práctico...xlsx`", type=["xls", "xlsx"], key="file_dev")

    if file_dev:
        try:
            file_bytes = file_dev.getvalue()
            xls_buffer = io.BytesIO(file_bytes)
            xls_dev = pd.ExcelFile(xls_buffer, engine='openpyxl')
            sheet_names_dev = xls_dev.sheet_names

            # --- NUEVO: Selector para Plan Contable Maestro ---
            sheet_plan_contable = st.selectbox(
                "Selecciona hoja 'Plan Contable'", 
                sheet_names_dev, 
                index=None, 
                placeholder="Elige la hoja del Plan de Cuentas...",
                key="cb_plan"
            )
            if sheet_plan_contable:
                # header=2 (fila 3)
                st.session_state.df_plan_contable = pd.read_excel(xls_dev, sheet_name=sheet_plan_contable, header=2)
                st.success(f"Hoja '{sheet_plan_contable}' cargada (Plan Contable Maestro).")

            # Selector para Libro Diario (F5.1)
            sheet_diario = st.selectbox(
                "Selecciona hoja 'F5.1 Libro Diario'", 
                sheet_names_dev, 
                index=None, 
                placeholder="Elige la hoja de Libro Diario...",
                key="cb_diario"
            )
            if sheet_diario:
                st.session_state.df_libro_diario = pd.read_excel(xls_dev, sheet_name=sheet_diario, header=10)
                st.success(f"Hoja '{sheet_diario}' cargada (Libro Diario).")

            # Selector para Balance General
            sheet_balance = st.selectbox(
                "Selecciona hoja 'Balance General'", 
                sheet_names_dev, 
                index=None, 
                placeholder="Elige la hoja de Balance...",
                key="cb_balance"
            )
            if sheet_balance:
                st.session_state.df_balance_general = pd.read_excel(xls_dev, sheet_name=sheet_balance, header=8)
                st.success(f"Hoja '{sheet_balance}' cargada (Balance General).")

            # Selector para ERI Función
            sheet_eri = st.selectbox(
                "Selecciona hoja 'ERI_Función'", 
                sheet_names_dev, 
                index=None, 
                placeholder="Elige la hoja de ERI...",
                key="cb_eri"
            )
            if sheet_eri:
                st.session_state.df_eri_funcion = pd.read_excel(xls_dev, sheet_name=sheet_eri, header=5)
                st.success(f"Hoja '{sheet_eri}' cargada (ERI Función).")

        except Exception as e:
            st.error(f"Error al leer Desarrollo Práctico: {e}")

# --- Página Principal ---
st.title("Validador de Libros Contables 🧾")
st.write("Esta aplicación implementa la lógica de corrección definida por tu hermana (basada en `plan_de_app.md`).")
st.markdown("---")

# 1. Verificar si CUALQUIER archivo está cargado
archivos_cargados = any(st.session_state[df] is not None for df in dfs)

if not archivos_cargados:
    st.warning("Por favor, carga los archivos Excel en la barra lateral izquierda para comenzar.")
    st.image("https://i.imgur.com/gYvD31Y.png", caption="Sube los archivos en la barra lateral", width=300)
else:
    st.success("¡Archivos cargados! Revisa los previews de los datos.")
    st.info("Aquí es donde implementaremos la lógica de corrección (Parte 2 del Plan).")

    # Mostramos un preview de los datos cargados
    st.subheader("Verificación de Datos Cargados")

    col1, col2 = st.columns(2)
    
    with col1:
        show_preview(st.session_state.df_caja, "Formato 1.1: Libro Caja (Efectivo)")
        show_preview(st.session_state.df_asientos_ventas, "Asientos de Ventas (A.C.)")
        show_preview(st.session_state.df_asientos_compras, "Asientos de Compras (Hoja3)")
        show_preview(st.session_state.df_planilla, "Planilla de Trabajadores")
        show_preview(st.session_state.df_balance_general, "Balance General (Reporte Final)")

    with col2:
        show_preview(st.session_state.df_bancos, "Formato 1.2: Libro Bancos (Cta Cte)")
        show_preview(st.session_state.df_registro_ventas, "Registro de Ventas (Formato 14.1)")
        show_preview(st.session_state.df_registro_compras, "Registro de Compras (Formato 8.1)")
        show_preview(st.session_state.df_libro_diario, "Libro Diario (Reporte Final)")
        show_preview(st.session_state.df_eri_funcion, "ERI por Función (Reporte Final)")
        
    # --- NUEVO: Preview del Plan Contable Maestro ---
    show_preview(st.session_state.df_plan_contable, "Plan Contable Maestro (El Diccionario)")


    # --- Placeholder para la Lógica de Corrección ---
    st.subheader("Próximo Paso: Aplicar Lógica de Corrección")
    
    # NUEVO: Verificamos si el Plan Contable está cargado
    if st.session_state.df_plan_contable is not None:
        st.success("¡Plan Contable Maestro cargado! Ya podemos empezar a limpiar y corregir.")
    else:
        st.warning("Por favor, carga el 'Plan Contable' (del Uploader 5) para continuar.")

    st.code("""
# Lógica a implementar (pseudo-código):

# 0. USAR EL PLAN MAESTRO
#    plan_maestro = st.session_state.df_plan_contable
#    (Esto nos servirá como diccionario)

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
#       asiento_venta['Cuenta_Corregida'] = 101 # (Buscar 'Caja' en plan_maestro)
#
#     # Buscar en BANCOS (Formato 1.2)
#     elif comprobante in df_bancos['Descripción']:
#       asiento_venta['Cuenta_Corregida'] = 104 # (Buscar 'Bancos' en plan_maestro)
#
#     else:
#       asiento_venta['Cuenta_Corregida'] = "ERROR: No Encontrado"
#
# # 3. Repetir lógica para Asientos de Compras
# ...

# 4. Mostrar tabla de asientos corregidos
# st.dataframe(df_asientos_ventas_corregido)
    """, language="python")

