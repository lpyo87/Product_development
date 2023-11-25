import streamlit as st
import pandas as pd
import utils
import re
from googletrans import Translator
dataset = pd.read_csv("BankChurners.csv")
dataset = dataset.iloc[0:100,:]
numericas, categoricas = utils.get_features_domain(dataset)

def main():
    st.header("Exploración de Datos")
    #st.dataframe(dataset.style.highlight_max(axis=0))
    st.dataframe(dataset)
    #st.table(dataset) Realiza una tabla con los datos pero es a través de código HTML (Más tardado)
    #colores = "Verde"
    select_columna = st.selectbox("Seleccionar columna", numericas)
    colores = st.radio("Colores: ", ("Verde", "Rojo", "Amarillo"))
    boton_promedio = st.button("Promedio")

    if(boton_promedio):
        promedio = round(dataset[select_columna].mean(),2)
        strOut = f"Promedio de {select_columna}: {promedio}"
        if(colores == "Verde"):
            st.success(strOut)
        elif(colores == 'Rojo'):
            st.error(strOut)
        else:
            st.warning(strOut)
    else:
        st.text("NOOOOO")
    
    #Slider contínuo
    valor = st.slider("Edad: ", 10,90)
    st.text(f"Valor: {valor}")

    #Slider discreto
    select_value = st.select_slider("Nivel", options = ['Bajo','Medio', 'Alto'])
    st.text(f"Valor Seleccionado: {select_value}")

    #Multi select
    multi_valor = st.multiselect("Idioma: ", ("Inglés", "Español", "Frances", "Aleman"), default="Inglés")
    st.text(multi_valor)

    #Entrada de Texto:
    patron = r"[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.(com|net|edu)"
    correo = st.text_input("Ingrese su Correo", max_chars=30)
    if(re.match(patron, correo)):
        st.success(f"El correo: {correo}, es válido.")
    else:
        st.error(f"El correo: {correo} NO es válido.")

    src_lang  = st.selectbox("Idioma Fuente: ", ["Español", "Inglés", "Francés"])
    dest_lang = st.selectbox("Idioma Destino: ", ["Español", "Inglés", "Francés"])
    texto = st.text_area("Ingrese sus preguntas:","", 25)
    traducir = st.button("Traducir")
    if(traducir):
        if(src_lang == "Español"): src_lang = "es"
        elif(src_lang == "Inglés"): src_lang = 'en'
        else: src_lang = 'fr'
        
        if(dest_lang == "Español"): dest_lang = "es"
        elif(dest_lang == "Inglés"): dest_lang = 'en'
        else: dest_lang = 'fr'
        translator = Translator()
        translation = translator.translate(texto, src = src_lang, dest = dest_lang)
        st.text(translation.text)
if(__name__=='__main__'):
    main()