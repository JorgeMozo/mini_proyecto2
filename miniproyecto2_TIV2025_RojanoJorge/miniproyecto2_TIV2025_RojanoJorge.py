import streamlit as st
import pandas as pd
import datetime as dt
import os 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


class App_Estudiantes:
    def __init__(self):
        try:
            path= os.path.join(os.getcwd(), "estudiantes.csv")
            st.session_state.df = pd.read_csv(path)
            st.session_state.estudiantes =  st.session_state.df.to_dict(orient="records")
            st.success("Estudiantes recuperados exitosamente del Archivo")
        except FileNotFoundError:
            st.session_state.estudiantes = []
            st.session_state.df = pd.DataFrame()  
        st.set_page_config(page_title= "Registro de Estudiantes", page_icon= "✏️")  

    def vista_formulario_de_ingreso(self):
        st.title("Formulario de ingreso")
        with st.form("form_registro"):
            st.write("Por favor, rellene los siguientes campos:")
            colu1, colu2 = st.columns(2)
            with colu1: #todo lo que este identado va en la columna 1
                nombre = st.text_input("Nombre completo", placeholder="Escribe tu nombre...")
                edad = st.number_input("Edad:", min_value=16, max_value=99, step=1)

            with colu2: #todo lo que este identado va en la columna 2
                carrera = st.selectbox("Carreras:", ["Licenciatura en Arquitectura","Ingenieria en Bionanotecnologia",
                                                                     "Ingenieria Mecanica y Electrica","Ingenieria Mecatronica",
                                                                     "Licenciatura en Contaduria y Estrategias Financieras","Licenciatura en Comercio Exterior y Logistica Internacional",
                                                                     "Licenciatura en Psicologia","Licenciatura en Comunicacion"])
                regular = st.checkbox("¿Eres alumno regular? ")

            guardar = st.form_submit_button("Guardar Formulario")
    

        if guardar:
            nuevo_estudiante = {
                "Nombre":nombre, 
                "Edad":edad, 
                "Carrera":carrera, 
                "Regular":regular,
                }
        
            st.session_state.estudiantes.append(nuevo_estudiante)
            st.success(f"Estudiante: {nombre} , registrado correctamente en {carrera}")

            st.session_state.df = pd.DataFrame(st.session_state.estudiantes) #actualizo el dataframe
            path= os.path.join(os.getcwd(), "estudiantes.csv")
            #guardar en la ruta donde se esta trabajando, siendo un concat, y despues le agregas mas ruta o el nombre del archivo
            st.session_state.df.to_csv(path, index=False)

    def vista_visualizacion_de_registros(self):
        st.title("Visualización de registros")
        df=st.session_state.df
        st.dataframe(st.session_state.df)
        carrera = ["Licenciatura en Arquitectura","Ingenieria en Bionanotecnologia",
                                                                     "Ingenieria Mecanica y Electrica","Ingenieria Mecatronica",
                                                                     "Licenciatura en Contaduria y Estrategias Financieras","Licenciatura en Comercio Exterior y Logistica Internacional",
                                                                     "Licenciatura en Psicologia","Licenciatura en Comunicacion"]
        seleccion = st.multiselect("Selecciona los niveles de estudio", carrera, default=carrera)
        condicion = df['Carrera'].isin(seleccion)
        df_filtrado = df[condicion]
        if not st.session_state.df.empty:          

            df_conteo = df_filtrado['Carrera'].value_counts().reset_index()
            df_conteo.columns = ['Carrera', 'Cantidad']

            fig_plotly = px.bar(
                df_conteo,
                x='Carrera',
                y='Cantidad',
                color='Carrera',
                title='Cantidad de alumnos por carrera'
            )


            st.plotly_chart(fig_plotly)

            st.session_state.df = pd.DataFrame(st.session_state.estudiantes) #actualizo el dataframe
            
            path= os.path.join(os.getcwd(), "estudiantes.csv")
            #guardar en la ruta donde se esta trabajando, siendo un concat, y despues le agregas mas ruta o el nombre del archivo
            st.session_state.df.to_csv(path, index=False)




            with st.form("form_exportar"):
                st.write("📝 Especifica el nombre del archivo y la carpeta de destino")

                nombre_archivo = st.text_input("Nombre del archivo (sin extensión)", value="estudiantes")
                carpeta_destino = st.text_input("Ruta de la carpeta", value=os.getcwd())

                exportar = st.form_submit_button("Guardar CSV")

                if exportar:
                    # Asegurarse de que la carpeta exista
                    if not os.path.isdir(carpeta_destino):
                        st.error("❌ La carpeta especificada no existe.")
                    else:
                        ruta_completa = os.path.join(carpeta_destino, f"{nombre_archivo}.csv")
                        st.session_state.df.to_csv(ruta_completa, index=False)
                        st.success(f"✅ Registros guardados en: {ruta_completa}")



        else: 
            st.error("No hay candidatos registrados ⚠️ ☹️ ")
        




    def run_py(self):
        st.sidebar.title("☰ Menú")
        opcion = st.sidebar.radio("Ir a: ", ["Formulario", "Visualizacion"])
        if opcion == "Formulario":
            self.vista_formulario_de_ingreso()
        elif opcion == "Visualizacion":
            self.vista_visualizacion_de_registros()
        else:
            print("ERROR #404")

app = App_Estudiantes()
app.run_py()

