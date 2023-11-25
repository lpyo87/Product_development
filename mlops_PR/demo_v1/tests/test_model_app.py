import streamlit as st
import pandas as pd

from pycaret.regression import load_model
from pycaret.regression import predict_model

data_path = 'data/raw/data_traffic_v1.csv'
dataset = pd.read_csv(data_path)
model=load_model('models/model_v1')


def main():
    st.title("Traffic Prediction Model")
    
    temp = st.slider("Temp", min_value=dataset['temp'].min(), max_value=dataset['temp'].max())
    rain_1h = st.slider("rain_1h", min_value=dataset['rain_1h'].min(), max_value=dataset['rain_1h'].max())
    snow_1h = st.slider("snow_1h", min_value=dataset['snow_1h'].min(), max_value=dataset['snow_1h'].max())
   
    clouds_all = st.slider("clouds all", min_value=dataset['clouds_all'].min(), max_value=dataset['clouds_all'].max())
    Rush_hour = st.select_slider("Rush_Hour", options=list(dataset['Rush Hour'].unique()))
    
    holiday = st.selectbox("Holiday", options=list(dataset['holiday'].unique()))
    weather_main = st.selectbox("weather_main?", options=list(dataset['weather_main'].unique()))

    get_pred = st.button("Predecir")

    if(get_pred):
        data_to_predict = pd.DataFrame({'temp':[temp],
                                      'rain_1h': [rain_1h],
                                      'snow_1h': [snow_1h],
                                      'clouds_all': [clouds_all],
                                      'Rush Hour': [Rush_hour],
                                      'holiday':[holiday],
                                      'weather_main':[weather_main]})
        predicciones = predict_model(model, data = data_to_predict)
        #predicciones = predict_model(model, data= data_test)
        print(data_to_predict)
        valor_predicho = round(list(predicciones['prediction_label'])[0],4)
        st.success(f"Valor Predicho: {valor_predicho}")


    st.title("Prueba")

if (__name__=='__main__'):
    main()