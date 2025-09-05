import streamlit as st

def calculate_mass_balance(initial_mass, initial_concentration, final_concentration):
    """
    Calcula la masa final y la masa de azúcar a agregar.

    Args:
        initial_mass (float): Masa inicial de la pulpa (M1).
        initial_concentration (float): Concentración inicial de sólidos en % (X1).
        final_concentration (float): Concentración final de sólidos deseada en % (X3).

    Returns:
        tuple: Una tupla conteniendo la masa final (M3) y la masa de azúcar (M2).
               Retorna (None, None) si hay un error en los cálculos.
    """
    # Convertir porcentajes a fracciones decimales
    initial_water_fraction = 1 - (initial_concentration / 100.0)
    final_water_fraction = 1 - (final_concentration / 100.0)

    # Evitar división por cero si la concentración final es 100%
    if final_water_fraction == 0:
        st.error("Error: La concentración final no puede ser 100% porque la pulpa inicial contiene agua.")
        return None, None

    # --- Cálculos basados en el balance de masa ---

    # 1. Balance de componente para el agua (la cantidad de agua es constante)
    # M1 * Y1 = M3 * Y3  =>  M3 = (M1 * Y1) / Y3
    final_mass = (initial_mass * initial_water_fraction) / final_water_fraction

    # 2. Balance de masa general
    # M1 + M2 = M3  =>  M2 = M3 - M1
    sugar_mass_to_add = final_mass - initial_mass

    return final_mass, sugar_mass_to_add

# --- Configuración de la página de Streamlit ---
st.set_page_config(page_title="Balance de Masa", layout="wide")

# --- Interfaz de Usuario de la Aplicación ---
st.title("⚙️ Calculadora de Balance de Masa para Pulpa de Fruta")
st.markdown("---")

# Dividir la pantalla en dos columnas
col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("📋 Datos de Entrada")
    st.write("Introduce los valores del proceso para calcular el azúcar necesario.")
    
    # --- Formularios para la entrada de datos ---
    with st.form(key="input_form"):
        m1_input = st.number_input(
            label="Masa Inicial de Pulpa (M1 en kg)",
            min_value=0.0,
            value=50.0,
            step=0.5,
            help="Cantidad inicial de pulpa que se va a procesar."
        )
        x1_input = st.number_input(
            label="Concentración Inicial de Sólidos (X1 en % o °Brix)",
            min_value=0.0,
            max_value=99.9,
            value=7.0,
            step=0.1,
            help="Porcentaje de sólidos (azúcar) en la pulpa inicial."
        )
        x3_input = st.number_input(
            label="Concentración Final Deseada (X3 en % o °Brix)",
            min_value=0.0,
            max_value=99.9,
            value=10.0,
            step=0.1,
            help="El objetivo de °Brix o porcentaje de sólidos para el producto final."
        )
        
        submit_button = st.form_submit_button(label="Calcular Ahora 🧮")

with col2:
    st.header("📊 Resultados del Cálculo")
    if submit_button:
        if x3_input <= x1_input:
            st.warning("La concentración final deseada debe ser mayor que la concentración inicial para agregar azúcar.")
        else:
            m3_calculada, m2_calculado = calculate_mass_balance(m1_input, x1_input, x3_input)

            if m3_calculada is not None:
                st.success(f"**Resultado:** Se deben agregar **{m2_calculado:.2f} kg** de azúcar.")
                st.markdown("---")
                
                st.subheader("Detalles del Balance:")
                metric1, metric2 = st.columns(2)
                metric1.metric(label="Masa Final de la Pulpa (M3)", value=f"{m3_calculada:.2f} kg")
                metric2.metric(label="Azúcar a Agregar (M2)", value=f"{m2_calculado:.2f} kg")

                with st.expander("Ver las fórmulas y el procedimiento de cálculo ▼"):
                    st.write("El cálculo se basa en dos principios de conservación de masa:")
                    st.markdown("""
                    1.  **Balance General de Masa:** La masa total que entra al sistema es igual a la que sale.
                        $$ M_1 + M_2 = M_3 $$
                    2.  **Balance de Componente (Agua):** La masa de agua se conserva, ya que el azúcar añadido no contiene agua.
                        $$ M_1 \\cdot Y_1 = M_3 \\cdot Y_3 $$
                    """)
                    st.write("**Procedimiento:**")
                    st.markdown(f"""
                    -   **Paso 1: Calcular la masa final (M3)** a partir del balance de agua, donde $Y_1 = 1 - ({x1_input}/100)$ y $Y_3 = 1 - ({x3_input}/100)$.
                        $$ M_3 = \\frac{{M_1 \\cdot Y_1}}{{Y_3}} = \\frac{{{m1_input} \\text{{ kg}} \\cdot {1-(x1_input/100.0):.2f}}}{{{1-(x3_input/100.0):.2f}}} = {m3_calculada:.2f} \\text{{ kg}} $$
                    -   **Paso 2: Calcular la masa de azúcar (M2)** a partir del balance general.
                        $$ M_2 = M_3 - M_1 = {m3_calculada:.2f} \\text{{ kg}} - {m1_input} \\text{{ kg}} = {m2_calculado:.2f} \\text{{ kg}} $$
                    """)
    else:
        st.info("Ingresa los datos en el formulario de la izquierda y presiona 'Calcular' para ver los resultados.")
    
    # Mostrar la imagen del problema como referencia
    st.markdown("---")
    st.image("https://i.imgur.com/gK5L0a4.jpeg", caption="Diagrama de referencia del problema de balance de masa.")
