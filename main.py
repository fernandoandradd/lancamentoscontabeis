import streamlit as st

# Função para carregar uma página
def load_page(page):
    if page == "Ufiscal - Lançamentos Contábeis":
        import lancamentoscontabeis
        lancamentoscontabeis.run()
    elif page == "Ufiscal - Consolidador XLSX":
        import apuracoes_streamlit
        apuracoes_streamlit.run()


# Interface de navegação
st.sidebar.title("Navegação")
page = st.sidebar.selectbox("Selecione uma página", ["Ufiscal - Lançamentos Contábeis", "Ufiscal - Consolidador XLSX"])

# Carregar a página selecionada
load_page(page)
