def intro():
    import streamlit as st

    st.write("# Proyecto 1: Product development")
    st.sidebar.success("Seleccionar una acción")

    st.markdown(
        """
        El proyecto consta de 2 fases, la carga de datos y la generación y elaboración del análisis. 

        **👈 Seleccionar la fase de carga de datos de la lista de la izquierda para comenzar.** Seguido, seleccionar la fase "2. Analizar Datos"

        ### Want to learn more?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )

intro()