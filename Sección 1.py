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
    'df_plan_contable'
]
# NUEVO: DataFrames limpios que crearemos
dfs_clean = [
    'df_plan_contable_clean', 'df_caja_clean', 'df_bancos_clean',
    'df_asientos_ventas_clean', 'df_asientos_compras_clean'
]
for df_key in dfs + dfs_clean:
    if df_key not in st.session_state:
        st.session_state[df_key] = None

# --- NUEVAS FUNCIONES DE LIMPIEZA ---
def limpiar_plan_contable():
    """Limpia el DataFrame del Plan Contable Maestro."""
    df = st.session_state.df_plan_contable
    if df is None:
        st.error("Error: El Plan Contable no está cargado para limpiar.")
        return
    
    # Hacemos una copia para no modificar el original
    df_clean = df.copy()
    
    # 1. Renombrar columnas para que sean más fáciles de usar
    df_clean.columns = df_clean.columns.str.strip().str.upper()
    # Asumimos que las columnas se llaman 'CÓDIGO' y 'CUENTAS' o similar
    # Vamos a ser más robustos y tomar las dos primeras columnas
    
    # Renombrar las dos primeras columnas
    if len(df_clean.columns) >= 2:
        df_clean = df_clean.rename(columns={
            df_clean.columns[0]: 'CODIGO',
            df_clean.columns[1]: 'DESCRIPCION'
        })
    else:
        st.error("Error: El Plan Contable no tiene las columnas esperadas.")
        return

    # 2. Quitar filas donde el CODIGO o DESCRIPCION sean NaN (vacías)
    df_clean = df_clean.dropna(subset=['CODIGO', 'DESCRIPCION'])
    
    # 3. Convertir el código a string para cruces seguros
    df_clean['CODIGO'] = df_clean['CODIGO'].astype(str).str.strip()
    
    # 4. Guardar el DataFrame limpio en el session_state
    st.session_state.df_plan_contable_clean = df_clean
    st.success("Función `limpiar_plan_contable` ejecutada.")
    
def limpiar_caja_bancos():
    """Limpia los DF de Caja y Bancos (df_caja, df_bancos)."""
    st.info("Función `limpiar_caja_bancos` (Próximo paso).")
    # Tareas futuras:
    # 1. Filtrar filas vacías.
    # 2. Extraer Nro. Comprobante de la 'DESCRIPCIÓN' (p.ej. "E001-001") a una nueva columna.
    # 3. Extraer el Monto relevante (DEBE o HABER).
    # 4. Guardar en st.session_state.df_caja_clean y df_bancos_clean
    pass

def limpiar_asientos_ventas():
    """Limpia y estructura el DF de Asientos de Ventas (df_asientos_ventas)."""
    st.info("Función `limpiar_asientos_ventas` (Próximo paso).")
    # Tareas futuras:
    # 1. Parsear la tabla para encontrar los asientos de "Cobro".
    # 2. Extraer la Cuenta (ej. 104) y el Monto.
    # 3. Extraer el Nro. de Comprobante.
    # 4. Guardar en st.session_state.df_asientos_ventas_clean
    pass

def limpiar_asientos_compras():
    """Limpia y estructura el DF de Asientos de Compras (df_asientos_compras)."""
    st.info("Función `limpiar_asientos_compras` (Próximo paso).")
    # Tareas futuras:
    # 1. Parsear la tabla para encontrar los asientos de "Pago".
    # 2. Extraer la Cuenta (ej. 101) y el Monto.
    # 3. Extraer el Nro. de Comprobante.
    # 4. Guardar en st.session_state.df_asientos_compras_clean
    pass

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

            # --- Selector para Plan Contable Maestro ---
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
    
    # Mostramos un preview de los datos cargados (los 'sucios' originales)
    st.subheader("Verificación de Datos Cargados (Originales)")
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
        
    show_preview(st.session_state.df_plan_contable, "Plan Contable Maestro (El Diccionario)")

    st.markdown("---")
    
    # --- NUEVO: Sección de Procesamiento (Fase 1) ---
    st.subheader("Fase 1: Limpieza y Corrección de Datos")
    
    # Verificamos que los archivos MÍNIMOS para la corrección estén cargados
    archivos_minimos_cargados = (
        st.session_state.df_plan_contable is not None and
        st.session_state.df_caja is not None and
        st.session_state.df_bancos is not None and
        st.session_state.df_asientos_ventas is not None and
        st.session_state.df_asientos_compras is not None
    )

    if not archivos_minimos_cargados:
        st.warning("Por favor, carga TODOS los archivos (1-5), incluyendo el 'Plan Contable', para activar la corrección.")
    else:
        st.info("¡Todos los archivos necesarios están cargados! Listo para procesar.")
        
        # El botón que dispara toda la lógica de limpieza
        if st.button("🧹 Empezar Limpieza y Corrección"):
            with st.spinner("Procesando... Esto puede tardar un momento..."):
                # Ejecutamos todas las funciones de limpieza en orden
                limpiar_plan_contable()
                limpiar_caja_bancos()
                limpiar_asientos_ventas()
                limpiar_asientos_compras()
            
            st.success("¡Proceso de limpieza terminado!")
            
            # Mostramos un preview de los nuevos DataFrames limpios
            st.subheader("Resultados de la Limpieza (Datos Limpios)")
            
            # Mostraremos el primer DF limpio (Plan Contable)
            show_preview(st.session_state.df_plan_contable_clean, "Plan Contable Maestro (LIMPIO)")
            
            # (Aquí añadiremos los previews de los otros DFs limpios cuando las funciones estén listas)
            st.info("Próximos pasos: Implementar la lógica en las otras funciones de limpieza.")

