import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración inicial de la página
st.set_page_config(page_title="Sistema de Agenda", layout="wide")

# Título de la aplicación
st.title("📅 Sistema de Agendamiento de Citas")

# Inicializar el archivo CSV si no existe
def init_data():
    try:
        return pd.read_csv('citas.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['fecha', 'hora', 'nombre', 'email', 'asunto'])
        df.to_csv('citas.csv', index=False)
        return df

# Cargar datos
df = init_data()

# Crear el formulario de agenda
with st.form("formulario_cita"):
    st.subheader("Agendar Nueva Cita")
    
    # Campos del formulario
    nombre = st.text_input("Nombre completo")
    email = st.text_input("Correo electrónico")
    
    # Selector de fecha
    fecha = st.date_input(
        "Seleccione la fecha",
        min_value=datetime.today(),
        max_value=datetime.today() + timedelta(days=30)
    )
    
    # Selector de hora
    horas_disponibles = [
        f"{h:02d}:00" for h in range(9, 18)
        if f"{fecha} {h:02d}:00" not in df['fecha'].astype(str) + " " + df['hora'].astype(str)
    ]
    
    hora = st.selectbox("Seleccione la hora disponible", horas_disponibles)
    
    asunto = st.text_area("Asunto de la cita")
    
    submitted = st.form_submit_button("Agendar Cita")
    
    if submitted:
        # Validar que todos los campos estén llenos
        if nombre and email and fecha and hora and asunto:
            # Agregar nueva cita
            nueva_cita = pd.DataFrame([{
                'fecha': fecha,
                'hora': hora,
                'nombre': nombre,
                'email': email,
                'asunto': asunto
            }])
            
            df = pd.concat([df, nueva_cita], ignore_index=True)
            df.to_csv('citas.csv', index=False)
            st.success("¡Cita agendada exitosamente!")
        else:
            st.error("Por favor complete todos los campos")

# Mostrar citas existentes
st.subheader("Citas Agendadas")
if not df.empty:
    st.dataframe(
        df.sort_values(['fecha', 'hora']),
        hide_index=True,
        column_config={
            "fecha": "Fecha",
            "hora": "Hora",
            "nombre": "Nombre",
            "email": "Email",
            "asunto": "Asunto"
        }
    )
else:
    st.info("No hay citas agendadas")

# Agregar información de pie de página
st.markdown("---")
st.markdown("### 📝 Información")
st.markdown("""
- Las citas están disponibles de lunes a viernes de 9:00 a 17:00
- Puede agendar citas hasta 30 días en adelanto
- Las citas tienen una duración de 1 hora
""")