# Universidad Galileo
# Maestría Inteligencia de Negocios y Análisis de Datos
# Curso: Product Development
# Sección L
# Jose Manuel Lara Rodas
# Luis Pedro Pérez Gutiérrez
# Leonel Eduardo Contreras González


import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
from dateutil.parser import parse
from statsmodels.graphics.mosaicplot import mosaic

def main():

    # Definir la variable de estado del dataset para poder utilizarlo en los diferentes menú
    if 'dataset' not in st.session_state:
        st.session_state.dataset = None

    # Mensaje de Bienvenida 
    st.title("Bienvenidos a la aplicación:")
    st.header("ExploreData")
    
    # Definir el Menú con select box al costado de la pantalla
    menu = st.sidebar.selectbox("Menú:", ["Opciones","1. Cargar Archivo", "2. Analizar Datos"])


    # Valor default del select box
    if menu=="Opciones":

        st.subheader('👈 Selecciona tu opción en el panel de Menú')

    # Valor seleccionable del menú para cargar archivo tipo CSV o Excel
    if menu == "1. Cargar Archivo":

        st.title('Carga tu dataset: csv o Excel 👇')

        carga_archivo=st.file_uploader("Cargar un archivo CSV o Excel", type=["csv","xlsx"]) # Comando para cargar el archivo

        # Si ya se cargo el archivo validar que tipo es
        if carga_archivo is not None:

            # Validación si el archivo es CSV o Excel
            try:
                if carga_archivo.name.endswith('.csv'):
                    dataset= pd.read_csv(carga_archivo)
                    st.session_state.dataset = dataset # Actualizar la variable de estado del dataset para utilizarlo posterior
                elif carga_archivo.name.endswith('.xlsx'):
                    dataset= pd.read_excel(carga_archivo,engine='openpyxl')
                    st.session_state.dataset = dataset # Actualizar la variable de estado del dataset para utilizarlo posterior
                
                st.success("Archivo cargado con éxito")
                st.success("Ve al Menú y elige: Analizar Datos")
            # Error si el archivo no es CSV o Excel
            except Exception as e:

                st.error("Error al cargar el archivo. Asegúrate de que sea un archivo CSV o Excel válido.")

    # Valor seleccionable del menú para analizar los datos cargados en la opcion anterior, se utiliza la variable de estado
    if menu== "2. Analizar Datos":

        st.title('Análisis y exploración de datos')
 

        dataset=st.session_state.dataset # Definir el dataset como el valor que trae la variable de estado en el menú anterior

        # Información General del dataset
        st.subheader('Dataset:')
        st.dataframe(dataset)
        st.subheader('Dimensión del Dataset:')
        st.write(dataset.shape)
        st.subheader('Tipos de Datos:')

        # Clasificar las variables del dataset
        categoricas = []
        continuas = []
        discretas = []
        fechas = []
        numericas = []



        # Obtener clasificación de variables
        for colName in dataset.columns:
                if np.issubdtype(dataset[colName].dtype, np.number):
                    if len(dataset[colName].unique()) <= 30:
                        discretas.append(colName)
                        numericas.append(colName)
                    else:
                        continuas.append(colName)
                        numericas.append(colName)
                else:
                    try:
                        if dataset[colName].apply(lambda x: isinstance(parse(x), (datetime.datetime, datetime.date, datetime.time))).all():
                            fechas.append(colName)
                    except Exception as e:
                        categoricas.append(colName)


        # Desplegar tipos de Variables
        st.write("Variables Categóricas")
        st.dataframe({"Variables":categoricas})
        st.write("Variables Numéricas Continuas")
        st.dataframe({"Variables":continuas})
        st.write("Variables Numéricas Discretas")
        st.dataframe({"Variables":discretas})
        st.write("Variables Tipo Temporales")
        st.dataframe({"Variables":fechas})

        st.markdown('<hr>', unsafe_allow_html=True)
        
        # Desplegar información de variables númericas
        st.subheader('Información estadística de las variables')
        st.markdown("Selecciona la variable")
        variable=st.selectbox("Variable: ",numericas) # Seleccionar que variable se quiere obtener info.
        st.write(f'El valor mínimo de la variable {variable} es : {dataset[variable].min()}')
        st.write(f'El valor máximo de la variable {variable} es : {dataset[variable].max()}')
        st.write(f'El promedio de la variable {variable} es : {round(dataset[variable].mean(),2)}')
        st.write(f'La desviación estándar de la variable {variable} es : {round(dataset[variable].std(),2)}')
        
        st.markdown('<hr>', unsafe_allow_html=True)

        # Graficas Individuales
        st.subheader('Graficas de variables individuales')

        # Seleccionar variable continua
        st.markdown("Selecciona la variable **continua** que deseas graficar")
        var_continua=st.selectbox("Variable (Continua):", continuas, key="var_continua")

        # Grafica de densidad para la variable elegida
        fig1 = plt.figure(figsize=(10, 4))
        sns.histplot(dataset[var_continua], kde=True, color="skyblue")

        plt.axvline(np.mean(dataset[var_continua]), color='red', linestyle='dashed', label="Media")
        plt.axvline(np.median(dataset[var_continua]), color='green', linestyle='dashed', label="Mediana")
        plt.axvline(np.std(dataset[var_continua]), color='blue', linestyle='dashed', label="Desv")
        plt.axvline(np.var(dataset[var_continua]), color='orange', linestyle='dashed', label="Var.")
        plt.legend()

        plt.title(f"Densidad de {var_continua}")
        st.pyplot(fig1, clear_figure=True)

        st.markdown('<hr>', unsafe_allow_html=True)

        # Seleccionar variable discreta
        st.write("Selecciona la variable **discreta** que deseas graficar")
        var_discreta=st.selectbox("Variable: ", discretas)

        if var_discreta:
            # Obtener la moda
            moda_result = stats.mode(dataset[var_discreta])
            moda = moda_result.mode

            # Grafica de histograma para la variable elegida
            fig2 = plt.figure(figsize=(10, 4))
            sns.histplot(dataset[var_discreta], color="skyblue")

            plt.axvline(np.mean(dataset[var_discreta]), color='red', linestyle='dashed', label="Media")
            plt.axvline(np.median(dataset[var_discreta]), color='green', linestyle='dashed', label="Mediana")
            plt.axvline(moda, color='black', linestyle='dashed', label="Moda")
            plt.axvline(np.std(dataset[var_discreta]), color='blue', linestyle='dashed', label="Desv")
            plt.axvline(np.var(dataset[var_discreta]), color='orange', linestyle='dashed', label="Var.")
            plt.legend()

            plt.title(f"Histograma de {var_discreta} ")
            st.pyplot(fig2, clear_figure=True)
        else:   
            st.warning("No hay variables discretas en el conjunto de datos.")

        st.markdown('<hr>', unsafe_allow_html=True)

        # Seleccionar variables categoricas
        st.write("Selecciona la variable **categórica** que deseas graficar")
        var_categorica = st.selectbox("Variable categórica:", categoricas, key="selectbox_var_categorica")

        # Verificar si el usuario ha seleccionado una variable categórica
        if var_categorica:
            # Conteo de categorias
            count_data = dataset[var_categorica].value_counts().reset_index()
            count_data.columns = ['Categoría', 'Conteo'] 

            # Grafica de barras para la variable elegida
            fig3 = plt.figure(figsize=(10, 4))
            sns.barplot(x='Categoría', y='Conteo', data=count_data)

            plt.title(f"Barras de {var_categorica}")
            st.pyplot(fig3, clear_figure=True)
        else:
            st.warning("No hay variables categóricas en el conjunto de datos.")

        st.markdown('<hr>', unsafe_allow_html=True)
        
        # Gráfica de Correlación
        st.subheader('Gráfica de Correlación')

        # Verificar si existen variables discretas
        if not discretas:
            st.warning("No hay variables discretas en el conjunto de datos.")
        else:
            var_x_corr = st.selectbox("Seleccione una variable continua:", continuas)
            var_y_corr = st.selectbox("Seleccione una variable discreta:", discretas)

        # Inicializar las variables var_x_corr y var_y_corr con valores predeterminados
            if var_x_corr is None:
                var_x_corr = continuas[0] if continuas else None
            if var_y_corr is None:
                var_y_corr = discretas[0] if discretas else None

            if var_x_corr and var_y_corr:
            # Verificar que ambas variables sean válidas
                if var_x_corr in dataset.columns and var_y_corr in dataset.columns:
                    plot_corr = sns.scatterplot(data=dataset, x=dataset[var_x_corr], y=dataset[var_y_corr])
                    plot_corr.set_xlabel(var_x_corr)
                    plot_corr.set_ylabel(var_y_corr)
                    plot_corr.set_title(f"Gráfico de dispersión {var_x_corr} vs {var_y_corr}")
                    st.pyplot(plot_corr.figure, clear_figure=True)

                    if var_x_corr == var_y_corr:
                        valor_correlacion = 1
                    else:
                        correlacion = dataset[[var_x_corr, var_y_corr]].corr()
                        valor_correlacion = round(correlacion.loc[var_x_corr, var_y_corr],5)                
                
                    # Mostrar la correlación en Streamlit
                    st.write(f"Correlación entre las variables seleccionadas: {valor_correlacion}")
                else:
                    st.warning("Por favor, seleccione variables válidas.")

        st.markdown('<hr>', unsafe_allow_html=True)            

        # Gráfica de Variable Categórica y Variable Continua
        st.subheader('Gráfica de Variable Categórica y Variable Continua')
        var_x_cat_cont = st.selectbox("Seleccione la variable categórica X:", categoricas)
        var_y_cat_cont = st.selectbox("Seleccione la variable continua Y:", continuas)

        if var_x_cat_cont and var_y_cat_cont:
            plot_box = sns.boxplot(data=dataset, x=var_x_cat_cont, y=var_y_cat_cont)
            plot_box.set_xlabel(var_x_cat_cont)
            plot_box.set_ylabel(var_y_cat_cont)
            plot_box.set_title(f"Gráfico de distribución {var_x_cat_cont} vs {var_y_cat_cont}")
            st.pyplot(plot_box.figure, clear_figure=True)
        else:
            st.warning("Por favor, seleccione variables válidas.")

        st.markdown('<hr>', unsafe_allow_html=True)
        # Gráfica de Variable Categórica y Serie Temporal

        st.subheader('Gráfica de Variable Categórica y Serie Temporal')
        if fechas:
            var_x_cat_temp = st.selectbox("Seleccione la variable categórica X:", categoricas, key="var_x_cat_temp")
            if var_x_cat_temp:
                var_y_cat_temp = st.selectbox("Seleccione la serie temporal Y:", fechas, key="var_y_cat_temp")
                if var_y_cat_temp:
                    line_plot = sns.lineplot(data=dataset, x=var_y_cat_temp, y=var_x_cat_temp)
                    line_plot.set_xlabel(var_y_cat_temp)
                    line_plot.set_ylabel(var_x_cat_temp)
                    line_plot.set_title(f"Gráfico de línea {var_x_cat_temp} vs {var_y_cat_temp}")
                    st.pyplot(line_plot.figure, clear_figure=True)
                else:
                    st.warning("Por favor, seleccione una variable de serie temporal.")
            else:
                st.warning("Por favor, seleccione una variable categórica.")
        else:       
            st.warning("No hay variables suficientes en el conjunto de datos.")
        
        st.markdown('<hr>', unsafe_allow_html=True)

        # Gráfica de Variable Categórica y Variable Categórica (Gráfico de Mosaico)
        st.subheader('Gráfica de Variable Categórica y Variable Categórica (Gráfico de Mosaico)')
        var_x_cat3 = st.selectbox("Seleccione la variable categórica X:", categoricas, key="var_x_cat3")
        var_y_cat3 = st.selectbox("Seleccione la variable categórica Y:", categoricas, key="var_y_cat3")

        if not categoricas:
            st.warning("No hay variables categóricas en el conjunto de datos.")
        else:
            fig, ax = plt.subplots()
            cuentas = pd.crosstab(dataset[var_x_cat3], dataset[var_y_cat3])
            cuentas.plot(kind='bar', stacked=True, ax=ax, width=1)
            ax.set_xlabel(var_x_cat3)
            ax.set_ylabel('Frecuencia')
            ax.set_title('Gráfico de Mosaico')
            st.pyplot(fig, clear_figure=True)

            mosaic(cuentas.stack())
            st.pyplot(clear_figure=True)

            chi2, p, _, _ = stats.chi2_contingency(cuentas)
            n = cuentas.sum().sum()
            k = min(cuentas.shape)
            cramer_v = round((chi2 / (n * (k - 1)))**0.5, 5)
            st.write(f'El coeficiente de contingencia de Cramer es: {cramer_v}')

if __name__ == '__main__':
    main()