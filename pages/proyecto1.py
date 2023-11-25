import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
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

        # Clasificar las varaibles del dataset
        categoricas=[]
        continuas=[]
        discretas=[]
        fechas=[]
        numericas=[]

        # Ciclo para obtener clasificación de varaibles, según los tipos de datos
        for colName in dataset.columns:

            if(pd.api.types.is_datetime64_any_dtype(dataset[colName])):
                fechas.append(colName)
            #if((dataset[colName].dtype=='datetime64') or (dataset[colName].dtype=='datetime.date') ):
            #    fechas.append(colName)

            elif((dataset[colName].dtype=='object') or (dataset[colName].dtype=='string')):
                categoricas.append(colName)
            else:
                if((dataset[colName].dtype=='int64')or (dataset[colName].dtype=='float64')or (dataset[colName].dtype=='uint8')):
                    if (len(dataset[colName].unique())<=30):
                        discretas.append(colName)
                        numericas.append(colName)
                    else:
                        continuas.append(colName)
                        numericas.append(colName)

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
        var_continua=st.selectbox("Variable: ",continuas)

        # Grafica de densidad para la variable elegida
        fig1=plt.figure(figsize=(10,4))
        sns.histplot(dataset[var_continua],kde=True,color="skyblue")

        plt.axvline(np.mean(dataset[var_continua]),color='red',linestyle='dashed',label="Media")
        plt.axvline(np.median(dataset[var_continua]),color='green',linestyle='dashed',label="Mediana")
        plt.axvline(np.std(dataset[var_continua]),color='blue',linestyle='dashed',label="Desv")
        plt.axvline(np.var(dataset[var_continua]),color='orange',linestyle='dashed',label="Var.")
        plt.legend()

        plt.title(f"Densidad de {var_continua} ")
        st.pyplot(fig1, clear_figure=True)

        # Seleccionar variable discreta
        st.write("Selecciona la variable **discreta** que deseas graficar")
        var_discreta=st.selectbox("Variable: ",discretas) 

        # Obtener la moda
        moda_result=stats.mode(dataset[var_discreta])
        moda=moda_result.mode

        # Grafica de histograma para la variable elegida
        fig2=plt.figure(figsize=(10,4))
        sns.histplot(dataset[var_discreta],color="skyblue")

        plt.axvline(np.mean(dataset[var_discreta]),color='red',linestyle='dashed',label="Media")
        plt.axvline(np.median(dataset[var_discreta]),color='green',linestyle='dashed',label="Mediana")
        plt.axvline(moda,color='black',linestyle='dashed',label="Moda")
        plt.axvline(np.std(dataset[var_discreta]),color='blue',linestyle='dashed',label="Desv")
        plt.axvline(np.var(dataset[var_discreta]),color='orange',linestyle='dashed',label="Var.")
        plt.legend()
        
        plt.title(f"Histograma de {var_discreta} ")
        st.pyplot(fig2, clear_figure=True) 

        # Seleccionar variable categorica
        st.write("Selecciona la variable **categórica** que deseas graficar")
        var_categorica=st.selectbox("Variable: ",categoricas)   

        # Conteo de categorias
        count_data=dataset[var_categorica].value_counts().reset_index()
        count_data.columns = ['Categoría', 'Conteo'] 

        # Grafica de barras para la variable elegida
        fig3=plt.figure(figsize=(10,4))
        sns.barplot(x='Categoría',y='Conteo',data=count_data)

        plt.title(f"Barras de {var_categorica} ")
        st.pyplot(fig3, clear_figure=True)
        
        st.markdown('<hr>', unsafe_allow_html=True)

        # Graficas Combinadas
        st.subheader('Graficas de variables combinadas')
        
        # Se definen las combinaciones de variables a graficar
        tipos_var = ["Categóricas", "Contínuas", "Discretas","Temporales"]
        tipos_var_2 = ['Categóricas', 'Contínuas']
        tipos_var_3 = ['Contínuas', 'Discretas']
        
        # Se selecciona la variable independiente
        var_seleccion_x = st.selectbox("Seleccione el tipo de variable a visualizar en X", tipos_var)

        #Se elaboran las selecciones según combinación
        if var_seleccion_x == "Categóricas":
            var_seleccion_y = st.selectbox("Seleccione el tipo de variable a visualizar en Y", tipos_var_2)
        elif (var_seleccion_x == "Contínuas") or (var_seleccion_x == "Discretas") or (var_seleccion_x == "Temporales"):
            var_seleccion_y = st.selectbox("Seleccione el tipo de variable a visualizar en Y", tipos_var_3)
        
        if (var_seleccion_x == "Categóricas"):
            var_x = st.selectbox("Seleccione la variable independiente X:", categoricas)

            if var_seleccion_y =="Contínuas": 
                var_y = st.selectbox("Seleccione la variable independiente Y:", continuas)
                plot_cont=sns.boxplot(data=dataset, x=dataset[var_x], y=dataset[var_y])
                plot_cont.set_xlabel(var_x)
                plot_cont.set_ylabel(var_y)
                plot_cont.set_title(f"Gráfico de distribución {var_x} vs {var_y}")
                st.pyplot(plot_cont.figure, clear_figure=True)
            
            if var_seleccion_y =="Categóricas": 
                var_y = st.selectbox("Seleccione la variable independiente Y:", categoricas)
                fig, ax = plt.subplots()
                #Se crea la tabla de contingencia
                cuentas = pd.crosstab(dataset[var_x],dataset[var_y])
                cuentas.plot(kind='bar', stacked=True, ax=ax, width =1)
                ax.set_xlabel('Variables')
                ax.set_ylabel('Frecuencia')
                ax.set_title('Gráfico de Mosaico')
                st.pyplot(plt, clear_figure=True)

                # Gráfico de mosaico
                st.set_option('deprecation.showPyplotGlobalUse', False)
                mosaic(cuentas.stack())

                st.pyplot( clear_figure=True)

                #Se calcula el coeficiente de contingencia de Cramer
                chi2, p, _, _ = stats.chi2_contingency(cuentas)
                n = cuentas.sum().sum()
                k = min(cuentas.shape)
                cramer_v = round((chi2 / (n * (k - 1)))**0.5,5)

                #Se expone el coeficiente:
                st.write(f'El coeficiente de contingencia de Cramer es: {cramer_v}')
        
        elif var_seleccion_x == "Contínuas":
            var_x_cont = st.selectbox("Seleccione la variable independiente X:", continuas)
# Opción variable Y contínuas
            if var_seleccion_y == "Contínuas":
                var_y_cont = st.selectbox("Seleccione la variable independiente Y:", continuas)
                plot_cont=sns.scatterplot(data=dataset, x=dataset[var_x_cont], y=dataset[var_y_cont])
                plot_cont.set_xlabel(var_x_cont)
                plot_cont.set_ylabel(var_y_cont)
                plot_cont.set_title(f"Gráfico de dispersión {var_x_cont} vs {var_y_cont}")
                st.pyplot(plot_cont.figure, clear_figure=True)

                # Calcular la correlación entre las variables seleccionadas
                if var_x_cont == var_y_cont:
                    valor_correlacion = 1
                else:
                    correlacion = dataset[[var_x_cont, var_y_cont]].corr()
                    valor_correlacion = round(correlacion.loc[var_x_cont, var_y_cont],5)

                # Mostrar la correlación en Streamlit
                st.write(f"Correlación entre las variables seleccionadas: {valor_correlacion}")

            elif var_seleccion_y == "Discretas":
                var_y_disc = st.selectbox("Seleccione la variable independiente Y:", discretas)
                plot_disc=sns.scatterplot(data=dataset, x=dataset[var_x_cont], y=dataset[var_y_disc])
                plot_disc.set_xlabel(var_x_cont)
                plot_disc.set_ylabel(var_y_disc)
                plot_disc.set_title(f"Gráfico de dispersión {var_x_cont} vs {var_y_disc}")
                st.pyplot(plot_disc.figure, clear_figure=True)

                # Calcular la correlación entre las variables seleccionadas
                if var_x_cont == var_y_disc:
                    valor_correlacion = 1
                else:
                    correlacion = dataset[[var_x_cont, var_y_disc]].corr()
                    valor_correlacion = round(correlacion.loc[var_x_cont, var_y_disc],5)

                # Mostrar la correlación en Streamlit
                st.write(f"Correlación entre las variables seleccionadas: {valor_correlacion}")
        
        elif var_seleccion_x == "Discretas":
            var_x_disc = st.selectbox("Seleccione la variable independiente X:", discretas)
            # Opción variable Y contínuas
            if var_seleccion_y == "Contínuas":
                var_y_disc = st.selectbox("Seleccione la variable independiente Y:", continuas)
                plot_disc=sns.scatterplot(data=dataset, x=dataset[var_x_disc], y=dataset[var_y_disc])
                plot_disc.set_xlabel(var_x_disc)
                plot_disc.set_ylabel(var_y_disc)
                plot_disc.set_title(f"Gráfico de dispersión {var_x_disc} vs {var_y_disc}")
                st.pyplot(plot_disc.figure, clear_figure=True)

                # Calcular la correlación entre las variables seleccionadas
                if var_x_disc == var_y_disc:
                    valor_correlacion = 1
                else:
                    correlacion = dataset[[var_x_disc, var_y_disc]].corr()
                    valor_correlacion = round(correlacion.loc[var_x_disc, var_y_disc],5)

                # Mostrar la correlación en Streamlit
                st.write(f"Correlación entre las variables seleccionadas: {valor_correlacion}")

            else:
                var_y_disc = st.selectbox("Seleccione la variable independiente Y:", discretas)
                plot_disc=sns.scatterplot(data=dataset, x=dataset[var_x_disc], y=dataset[var_y_disc])
                plot_disc.set_xlabel(var_x_disc)
                plot_disc.set_ylabel(var_y_disc)
                plot_disc.set_title(f"Gráfico de dispersión {var_x_disc} vs {var_y_disc}")
                st.pyplot(plot_disc.figure, clear_figure=True)

                # Calcular la correlación entre las variables seleccionadas
                if var_x_disc == var_y_disc:
                    valor_correlacion = 1
                else:
                    correlacion = dataset[[var_x_disc, var_y_disc]].corr()
                    valor_correlacion = round(correlacion.loc[var_x_disc, var_y_disc],5)

                # Mostrar la correlación en Streamlit
                st.write(f"Correlación entre las variables seleccionadas: {valor_correlacion}")
        
        elif var_seleccion_x == "Temporales":
            if fechas == []:
                var_y_temp = []
            else:    
                var_x_temp = st.selectbox("Seleccione la variable independiente X:", fechas)
                if var_seleccion_y == "Contínuas":
                    var_y_temp = st.selectbox("Seleccione la variable independiente Y:", continuas)
                    plot_temp=sns.scatterplot(data=dataset, x=dataset[var_x_temp], y=dataset[var_y_temp])
                    plot_temp.set_xlabel(var_x_temp)
                    plot_temp.set_ylabel(var_y_temp)
                    plot_temp.set_title(f"Gráfico de dispersión {var_x_temp} vs {var_y_temp}")
                    st.pyplot(plot_temp.figure, clear_figure=True)

                    # Calcular la correlación entre las variables seleccionadas
                    if var_x_temp == var_y_temp:
                        valor_correlacion = 1
                    else:
                        correlacion = dataset[[var_x_temp, var_y_temp]].corr()
                        valor_correlacion = round(correlacion.loc[var_x_temp, var_y_temp],5)

                    # Mostrar la correlación en Streamlit
                    st.write(f"Correlación entre las variables seleccionadas: {valor_correlacion}")

                else:
                    var_y_temp = st.selectbox("Seleccione la variable independiente Y:", discretas)
                    plot_temp=sns.scatterplot(data=dataset, x=dataset[var_x_temp], y=dataset[var_y_temp])
                    plot_temp.set_xlabel(var_x_temp)
                    plot_temp.set_ylabel(var_y_temp)
                    plot_temp.set_title(f"Gráfico de dispersión {var_x_temp} vs {var_y_temp}")
                    st.pyplot(plot_temp.figure, clear_figure=True)

                    # Calcular la correlación entre las variables seleccionadas
                    if var_x_temp == var_y_temp:
                        valor_correlacion = 1
                    else:
                        correlacion = dataset[[var_x_temp, var_y_temp]].corr()
                        valor_correlacion = round(correlacion.loc[var_x_temp, var_y_temp],5)

                    # Mostrar la correlación en Streamlit
                    st.write(f"Correlación entre las variables seleccionadas: {valor_correlacion}")



if(__name__=='__main__'):
    main()