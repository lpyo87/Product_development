import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

dataset = pd.read_csv("BankChurners.csv")


def main():
    st.title("Modelo de Regresión")
    st.dataframe(dataset)
    
    variable = st.selectbox("Variable", ["Customer_Age","Credit_Limit"])

    #Mínimo y máximo de la variable
    min = dataset[variable].min()
    max = dataset[variable].max()

    kde = stats.gaussian_kde(dataset[variable])
    rangos = st.slider(f"Valor de {variable}", min, max, (min, max))
    r_min = rangos[0]
    r_max = rangos[1]

    fig, ax = plt.subplots(figsize=(10,4))
    # Con Seaborn
    sns.kdeplot(dataset[variable], color = 'green')
    # Líneas verticales de intervalo
    # Mínimo
    kde_value_min = kde.evaluate(r_min)
    ax.vlines(x = r_min, ymin=0, ymax=kde_value_min)
    # Máximo
    kde_value_max = kde.evaluate(r_max)
    ax.vlines(x = r_max, ymin=0, ymax=kde_value_max)
    # Con Matplot lib
    # dataset[variable].plot.density(color = 'blue')
    # Sombrear el área entre r_min y r_max bajo la curva KDE
    x = np.linspace(r_min, r_max, 1000)  # 1000 puntos entre r_min y r_max
    y = kde.evaluate(x)
    ax.fill_between(x, y, color="orange", alpha=0.5)  # alpha es para la transparencia
    plt.title(f"Densidad de {variable}")
    st.pyplot(fig)

    st.text(f"Probabilidad: {np.round(np.sum(y), 4)/100}")

    fig2 = plt.figure(figsize=(10,4))
    categoricas =[]
    for col in dataset.columns:
        if((dataset[col].dtype == 'object') or (dataset[col].dtype == 'string')):
            categoricas.append(col)

    continuas =[]
    for col in dataset.columns:
        if((dataset[col].dtype == 'float64') or (dataset[col].dtype == 'int64')):
            continuas.append(col)
    variableA = st.selectbox("Variable Continua", continuas)
    variableB = st.selectbox("Variable Discreta", categoricas)

    sns.boxplot(dataset, x=variableB, y=variableA)
    st.pyplot(fig2)


if (__name__ == '__main__'):
    main()