import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
from csv import writer

dicionario_e110 = dict()
dicionario_e520 = dict()
dicionario_h005 = dict()

#registro 0000

DT_INI_0000 = str
DT_FIN_0000 = str
CNPJ_0000 = str

# registro e110

REG_E100 = str
VL_TOT_DEBITOS = float
VL_AJ_DEBITOS = float
VL_TOT_AJ_DEBITOS = float
VL_ESTORNOS_CRED = float
VL_TOT_CREDITOS = float
VL_AJ_CREDITOSS = float
VL_TOT_AJ_CREDITOS = float
VL_ESTORNOS_DEB = float
VL_SLD_CREDOR_ANT = float
VL_SLD_APURADO = float
VL_TOT_DED = float
VL_ICMS_RECOLHER = float
VL_SLD_CREDOR_TRANSPORTAR = float
DEB_ESP = float

# registro E520

REG_E520 = str
VL_SD_ANT_IPI_E520 = float
VL_DEB_IPI_E520 = float
VL_CRED_IPI_E520 = float
VL_OD_IPI_E520 = float
VL_OC_IPI_E520 = float
VL_SC_IPI_E520 = float
VL_SD_IPI_E520 = float

# registro E005

REG_H005 = str
DT_INV_H005 = str
VL_INV_H005 = str
MOT_INV_H005 = str

def run():

    st.title('Processamento de Arquivos EFD ICMS IPI')

    uploaded_files = st.file_uploader("Importe os Arquivos TXT da EFD ICMS IPI", type="txt", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            dados = uploaded_file.read().decode('ANSI').splitlines()

            for registro in dados:

                if registro[:6] == '|0000|':

                    registros0000 = list(registro.split('|'))

                    DT_INI_0000 = datetime.strptime(registros0000[4], '%d%m%Y').date()
                    DT_FIN_0000 = datetime.strptime(registros0000[5], '%d%m%Y').date()
                    CNPJ_0000 = registros0000[7]

                if registro[:6] == '|E110|':

                    registrosE100 = list(registro.split('|'))

                    VL_TOT_DEBITOS = registrosE100[2]
                    VL_AJ_DEBITOS = registrosE100[3]
                    VL_TOT_AJ_DEBITOS = registrosE100[4]
                    VL_ESTORNOS_CRED = registrosE100[5]
                    VL_TOT_CREDITOS = registrosE100[6]
                    VL_AJ_CREDITOSS = registrosE100[7]
                    VL_TOT_AJ_CREDITOS = registrosE100[8]
                    VL_ESTORNOS_DEB = registrosE100[9]
                    VL_SLD_CREDOR_ANT = registrosE100[10]
                    VL_SLD_APURADO = registrosE100[11]
                    VL_TOT_DED = registrosE100[12]
                    VL_ICMS_RECOLHER = registrosE100[13]
                    VL_SLD_CREDOR_TRANSPORTAR = registrosE100[14]
                    DEB_ESP = registrosE100[15]

                    dicionario_e110[CNPJ_0000 + str(DT_INI_0000)] = (
                        CNPJ_0000, DT_INI_0000, DT_FIN_0000, VL_TOT_DEBITOS, VL_AJ_DEBITOS, VL_TOT_AJ_DEBITOS, VL_ESTORNOS_CRED,
                        VL_TOT_CREDITOS, VL_AJ_CREDITOSS, VL_TOT_AJ_CREDITOS, VL_ESTORNOS_DEB, VL_SLD_CREDOR_ANT, VL_SLD_APURADO,
                        VL_TOT_DED, VL_ICMS_RECOLHER, VL_SLD_CREDOR_TRANSPORTAR, DEB_ESP)

                if registro[:6] == '|E520|':

                    registrosE520 = list(registro.split('|'))

                    REG_E520 = registrosE520[1]
                    VL_SD_ANT_IPI_E520 = registrosE520[2]
                    VL_DEB_IPI_E520 = registrosE520[3]
                    VL_CRED_IPI_E520 = registrosE520[4]
                    VL_OD_IPI_E520 = registrosE520[5]
                    VL_OC_IPI_E520 = registrosE520[6]
                    VL_SC_IPI_E520 = registrosE520[7]
                    VL_SD_IPI_E520 = registrosE520[8]

                    dicionario_e520[CNPJ_0000 + str(DT_INI_0000)] = (
                        CNPJ_0000, DT_INI_0000, DT_FIN_0000, REG_E520, VL_SD_ANT_IPI_E520, VL_DEB_IPI_E520, VL_CRED_IPI_E520,
                        VL_OD_IPI_E520, VL_OC_IPI_E520, VL_SC_IPI_E520, VL_SD_IPI_E520)

                if registro[:6] == '|H005|':

                    registrosH005 = list(registro.split('|'))

                    REG_H005 = registrosH005[1]
                    DT_INV_H005 = registrosH005[2]
                    VL_INV_H005 = registrosH005[3]
                    MOT_INV_H005 = registrosH005[4]

                    if MOT_INV_H005 == "01":
                        MOT_INV_H005 = "01 - No final no período"
                    elif MOT_INV_H005 == "02":
                        MOT_INV_H005 = "02 - Na mudança de forma de tributação da mercadoria (ICMS)"
                    elif MOT_INV_H005 == "03":
                        MOT_INV_H005 = "03 - Na solicitação da baixa cadastral, paralisação temporária e outras situações"
                    elif MOT_INV_H005 == "04":
                        MOT_INV_H005 = "04 - Na alteração de regime de pagamento - condição do contribuinte"
                    elif MOT_INV_H005 == "05":
                        MOT_INV_H005 = "05 - Por determinação dos fiscos"
                    elif MOT_INV_H005 == "06":
                        MOT_INV_H005 = "06 - Para controle das mercadorias sujeitas ao regime de substituição tributária - restituição/ ressarcimento/ complementação"

                    dicionario_h005[CNPJ_0000 + str(DT_INI_0000) + str(VL_SD_IPI_E520)] = (
                        CNPJ_0000, DT_INI_0000, DT_FIN_0000, REG_H005, DT_INV_H005, VL_INV_H005, MOT_INV_H005)

    st.write("Dados do Registro E110:")
    st.write(pd.DataFrame.from_dict(dicionario_e110, orient='index', columns=[
        'CNPJ', 'Data Inicio', 'Data Final', 'Débito(Saidas e Prestações)', 'Valor total dos ajustes a débito decorrentes do documento fiscal.',
        'Valor total de "Ajustes a débito".', 'Valor total de Ajustes "Estornos de créditos"', 'Valor total dos créditos por "Entradas e aquisições com crédito do imposto".',
        'Valor total dos ajustes a crédito decorrentes do documento fiscal."', 'Valor total de "Ajustes a crédito".', 'Valor total de Ajustes "Estornos de Débitos".',
        'Valor total de "Saldo credor do período anterior".', 'Valor do saldo devedor apurado.', 'Valor total de "Deduções".', 'Valor total de "ICMS a recolher" (11-12).',
        'Valor total de "Saldo credor a transportar para o período seguinte".', 'Valores recolhidos ou a recolher, extra-apuração.'
    ]))

    st.write("Dados do Registro E520:")
    st.write(pd.DataFrame.from_dict(dicionario_e520, orient='index', columns=[
        'CNPJ', 'Data Inicio', 'Data Final', "REG_E520", "Saldo credor do IPI transferido do período anterior.",
        "Valor total dos débitos por 'Saídas com débito do imposto'", "Valor total dos créditos por 'Entradas e aquisições com crédito do imposto'",
        "Valor de 'Outros débitos' do IPI (inclusive estornos de crédito)", "Valor de 'Outros créditos' do IPI (inclusive estornos de débitos).",
        "Valor do saldo credor do IPI a transportar para o período seguinte.", "Valor do saldo devedor do IPI a recolher"
    ]))

    st.write("Dados do Registro H005:")
    st.write(pd.DataFrame.from_dict(dicionario_h005, orient='index', columns=[
        'CNPJ', 'Data Inicio', 'Data Final', "REG_H005", "Data do inventário.", "Valor total do estoque", "Informe o motivo do Inventário"
    ]))

    def save_to_csv(data_dict, file_name, header):
        caminho_salvar = st.text_input(f'Informe o caminho para salvar o {file_name}', f'{file_name}.csv')
        if caminho_salvar:
            with open(caminho_salvar, 'w', newline='') as arquivo:
                escritor_csv = writer(arquivo, delimiter=';', quotechar=';')
                escritor_csv.writerow(header)
                escritor_csv.writerows(data_dict.values())
            st.success(f'Arquivo {file_name} salvo com sucesso!')

    if st.button('Salvar Registro E110'):
        save_to_csv(dicionario_e110, "Registro E110", [
            'CNPJ', 'Data Inicio', 'Data Final', 'Débito(Saidas e Prestações)', 'Valor total dos ajustes a débito decorrentes do documento fiscal.',
            'Valor total de "Ajustes a débito".', 'Valor total de Ajustes "Estornos de créditos"', 'Valor total dos créditos por "Entradas e aquisições com crédito do imposto".',
            'Valor total dos ajustes a crédito decorrentes do documento fiscal."', 'Valor total de "Ajustes a crédito".', 'Valor total de Ajustes "Estornos de Débitos".',
            'Valor total de "Saldo credor do período anterior".', 'Valor do saldo devedor apurado.', 'Valor total de "Deduções".', 'Valor total de "ICMS a recolher" (11-12).',
            'Valor total de "Saldo credor a transportar para o período seguinte".', 'Valores recolhidos ou a recolher, extra-apuração.'
        ])

    if st.button('Salvar Registro E520'):
        save_to_csv(dicionario_e520, "Registro E520", [
            'CNPJ', 'Data Inicio', 'Data Final', "REG_E520", "Saldo credor do IPI transferido do período anterior.",
            "Valor total dos débitos por 'Saídas com débito do imposto'", "Valor total dos créditos por 'Entradas e aquisições com crédito do imposto'",
            "Valor de 'Outros débitos' do IPI (inclusive estornos de crédito)", "Valor de 'Outros créditos' do IPI (inclusive estornos de débitos).",
            "Valor do saldo credor do IPI a transportar para o período seguinte.", "Valor do saldo devedor do IPI a recolher"
        ])

    if st.button('Salvar Registro H005'):
        save_to_csv(dicionario_h005, "Registro H005", [
            'CNPJ', 'Data Inicio', 'Data Final', "REG_H005", "Data do inventário.", "Valor total do estoque", "Informe o motivo do Inventário"
        ])

    if st.button('Salvar Todos os Registros'):
        save_to_csv(dicionario_e110, "Registro E110", [
            'CNPJ', 'Data Inicio', 'Data Final', 'Débito(Saidas e Prestações)', 'Valor total dos ajustes a débito decorrentes do documento fiscal.',
            'Valor total de "Ajustes a débito".', 'Valor total de Ajustes "Estornos de créditos"', 'Valor total dos créditos por "Entradas e aquisições com crédito do imposto".',
            'Valor total dos ajustes a crédito decorrentes do documento fiscal."', 'Valor total de "Ajustes a crédito".', 'Valor total de Ajustes "Estornos de Débitos".',
            'Valor total de "Saldo credor do período anterior".', 'Valor do saldo devedor apurado.', 'Valor total de "Deduções".', 'Valor total de "ICMS a recolher" (11-12).',
            'Valor total de "Saldo credor a transportar para o período seguinte".', 'Valores recolhidos ou a recolher, extra-apuração.'
        ])
        save_to_csv(dicionario_e520, "Registro E520", [
            'CNPJ', 'Data Inicio', 'Data Final', "REG_E520", "Saldo credor do IPI transferido do período anterior.",
            "Valor total dos débitos por 'Saídas com débito do imposto'", "Valor total dos créditos por 'Entradas e aquisições com crédito do imposto'",
            "Valor de 'Outros débitos' do IPI (inclusive estornos de crédito)", "Valor de 'Outros créditos' do IPI (inclusive estornos de débitos).",
            "Valor do saldo credor do IPI a transportar para o período seguinte.", "Valor do saldo devedor do IPI a recolher"
        ])
        save_to_csv(dicionario_h005, "Registro H005", [
            'CNPJ', 'Data Inicio', 'Data Final', "REG_H005", "Data do inventário.", "Valor total do estoque", "Informe o motivo do Inventário"
        ])
