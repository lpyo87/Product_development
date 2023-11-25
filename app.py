import streamlit as st

a = 5 + 6


def main():
    st.title("Hola Mundo")

    #texto
    st.title("Mi primera Aplicación de Streamlit")
    st.text(f"El resultado es: {a}")
    st.text("Esto es otra linea")

    #headers
    st.header("Esto es un Header")
    st.subheader("Esto es un subheader")

    #Markdown
    st.markdown("### Header Markdown")

    #Mensajes de bootstrap
    st.success("Success")
    st.error("Error!")
    st.warning("Warning")
    st.info("Info")
    st.exception("Exception")

    #Evaluación de código directo
    st.write("Esto es un print")
    st.write(6+5)
    productos = dict(Gasolina = 35.35, Diesel = 30.12, VPower = 37.89)
    st.write(productos)
    


main()
#if(__name__=='___main___'):
#    main()