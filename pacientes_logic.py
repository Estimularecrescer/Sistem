import sheets_client 


# Nomes das abas (worksheets) que vamos usar
ABA_PACIENTES = "Pacientes"
ABA_TERAPEUTAS = "Terapeutas"

def get_worksheet(sheet_name):
    """Função genérica para pegar qualquer aba da planilha."""
    spreadsheet = sheets_client.get_spreadsheet()
    if spreadsheet:
        try:
            return spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            print(f"❌ ERRO: A aba '{sheet_name}' não foi encontrada na planilha.")
            return None
    return None

def cadastrar_paciente(nome, terapeuta_responsavel, data_nasc, celular, cep, endereco, bairro, cidade, estado, nome_resp=None, cel_resp=None, cpf_resp=None):
    """Adiciona um novo paciente com todos os campos na planilha."""
    try:
        worksheet = get_worksheet(ABA_PACIENTES)
        if not worksheet:
            return False
            
        # A ordem aqui DEVE ser a mesma das colunas na sua planilha
        nova_linha = [
            nome, terapeuta_responsavel, data_nasc, celular, cep, 
            endereco, bairro, cidade, estado,
            nome_resp or "",  # Usa string vazia se o valor for None
            cel_resp or "",
            cpf_resp or ""
        ]
        
        worksheet.append_row(nova_linha)
        print(f"✅ Paciente '{nome}' cadastrado com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao cadastrar paciente: {e}")
        return False

def listar_pacientes():
    """Retorna uma lista de todos os pacientes da planilha."""
    try:
        worksheet = get_worksheet(ABA_PACIENTES)
        if not worksheet:
            return []
        return worksheet.get_all_records()
    except Exception as e:
        print(f"❌ Erro ao listar pacientes: {e}")
        return []

def listar_terapeutas():
    """Retorna uma lista de todos os terapeutas. Será útil para a interface!"""
    try:
        worksheet = get_worksheet(ABA_TERAPEUTAS)
        if not worksheet:
            return []
        # Pega apenas os valores da primeira coluna (nomes dos terapeutas)
        lista_de_terapeutas = worksheet.col_values(1)[1:] # [1:] para pular o cabeçalho
        return lista_de_terapeutas
    except Exception as e:
        print(f"❌ Erro ao listar terapeutas: {e}")
        return []