import sheets_client
from datetime import datetime
import requests

# Nomes das abas (worksheets) que vamos usar
ABA_PACIENTES = "Pacientes"
ABA_TERAPEUTAS = "Terapeutas"

def get_worksheet(sheet_name):
    """Função genérica para pegar qualquer aba da planilha."""
    # ... (esta função continua igual)
    spreadsheet = sheets_client.get_spreadsheet()
    if spreadsheet:
        try:
            return spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            print(f"❌ ERRO: A aba '{sheet_name}' não foi encontrada na planilha.")
            return None
    return None

def cadastrar_paciente(nome, telefone, cpf, rg, endereco, cep,  nascimento, convenio):
    """Adiciona um novo paciente com a nova estrutura de campos."""
    try:
        worksheet = get_worksheet(ABA_PACIENTENTES) # Garanta que o nome da aba está correto
        if not worksheet:
            return False
        
        timestamp_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # A ordem aqui DEVE ser a mesma das colunas na sua planilha
        nova_linha = [
            nome, telefone, cpf, rg, endereco,cep, 
            nascimento, convenio, 
            timestamp_atual,  # Data do Cadastro
            timestamp_atual   # Ultima Alteração
        ]
        
        worksheet.append_row(nova_linha)
        print(f"✅ Paciente '{nome}' cadastrado com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao cadastrar paciente: {e}")
        return False

# --- Nossas funções antigas que continuam funcionando ---

def consultar_cep(cep):
    """Consulta um CEP na API ViaCEP e retorna os dados do endereço."""
    
    # Limpa o CEP, removendo pontos e traços
    cep_limpo = str(cep).replace("-", "").replace(".", "").strip()
    
    if not cep_limpo.isdigit() or len(cep_limpo) != 8:
        print(f"⚠️ CEP '{cep}' inválido.")
        return None

    try:
        print(f"Consultando CEP {cep_limpo}...")
        # Monta a URL da API
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        
        # Faz a requisição para a API
        response = requests.get(url)
        
        # Se a resposta foi bem-sucedida (código 200)
        if response.status_code == 200:
            dados = response.json()
            # A API ViaCEP retorna um campo "erro" se o CEP não for encontrado
            if dados.get("erro"):
                print(f"CEP {cep_limpo} não encontrado na base de dados.")
                return None
            
            print("✅ Endereço encontrado:", dados)
            return dados
        else:
            print(f"❌ Erro na API do ViaCEP: Status {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão ao consultar CEP: {e}")
        return None

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

def excluir_paciente(nome_paciente):
    """Encontra um paciente pelo nome e exclui a linha correspondente."""
    # ... (esta função continua igual)
    try:
        worksheet = get_worksheet(ABA_PACIENTES)
        if not worksheet: return False
        celula = worksheet.find(nome_paciente)
        if not celula: return False
        worksheet.delete_rows(celula.row)
        print(f"✅ Paciente '{nome_paciente}' excluído com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao excluir paciente: {e}")
        return False