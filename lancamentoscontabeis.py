import streamlit as st
import pandas as pd
from io import StringIO

def process_excel(file):
    df = pd.read_excel(file)
    return df

def process_text_input(text_input):
    # Verifica se a primeira linha contém cabeçalhos
    if "Data" in text_input.split("\n")[0]:
        data = StringIO(text_input)
        df = pd.read_csv(data, sep="\t")
    else:
        data = StringIO(text_input)
        df = pd.read_csv(data, sep="\t", header=None, names=["Data", "Debito", "Credito", "Valor", "Historico"])
    return df

def generate_output_file(df, cnpj, usuario):
    output = ""
    output += "|0000|" + cnpj + "|\n"
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)  # Usa dayfirst=True para formato DD/MM/YYYY
    for index, row in df.iterrows():
        output += "|6000|X||||\n"
        output += "|6100|" + row['Data'].strftime('%d/%m/%Y') + "|" + str(row['Debito']) + "|" + str(row['Credito']) + "|" + str(row['Valor']) + "||" + row['Historico'] + "|" + usuario + "||\n"
    return output




def run ():

    st.title('Ufiscal: Lançamentos Contábeis')

    cnpj = st.text_input('Digite CNPJ da empresa')
    usuario = st.text_input('Digite o Usuário Domínio Sistemas')
    uploaded_file = st.file_uploader("Anexe uma planilha do Excel ou cole aqui sua tabela de lançamentos contábeis")
    text_input = st.text_area("Ou cole os dados da planilha aqui (separados por tabulação)")

    if st.button('Carregar'):
        if uploaded_file is not None:
            df = process_excel(uploaded_file)
            st.write(df)
        elif text_input:
            df = process_text_input(text_input)
            st.write(df)

    if st.button('Exportar'):
        if uploaded_file is not None:
            df = process_excel(uploaded_file)
            output = generate_output_file(df, cnpj, usuario)
            st.download_button(label="Download Arquivo TXT", data=output, file_name="lancamentos.txt")
        elif text_input:
            df = process_text_input(text_input)
            output = generate_output_file(df, cnpj, usuario)
            st.download_button(label="Download Arquivo TXT", data=output, file_name="lancamentos.txt")
