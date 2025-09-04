# Em pacientes_logic.py
import sheets_client
from datetime import datetime
import gspread

# ... (código do cache e get_worksheet continua igual) ...
ABA_PACIENTES = "Pacientes"
_cache_pacientes = None

def get_worksheet(sheet_name):
    spreadsheet = sheets_client.get_spreadsheet()
    if spreadsheet:
        try: return spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound: return None
    return None

def invalidar_cache():
    global _cache_pacientes
    _cache_pacientes = None

def listar_pacientes():
    global _cache_pacientes
    if _cache_pacientes is not None: return _cache_pacientes
    worksheet = get_worksheet(ABA_PACIENTES)
    if not worksheet: return []
    _cache_pacientes = worksheet.get_all_records()
    return _cache_pacientes

def get_paciente_por_nome(nome_paciente):
    lista_pacientes = listar_pacientes()
    for paciente in lista_pacientes:
        if paciente.get("Nome") == nome_paciente:
            return paciente
    return None

def cadastrar_paciente(dados_paciente):
    try:
        worksheet = get_worksheet(ABA_PACIENTES)
        if not worksheet: return False
        
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # A ordem aqui DEVE corresponder à nova estrutura da planilha
        nova_linha = [
            dados_paciente['nome'], dados_paciente['telefone'], dados_paciente['cpf'],
            dados_paciente['rg'], dados_paciente['cep'], dados_paciente['endereco'],
            dados_paciente['bairro'], dados_paciente['cidade'], dados_paciente['estado'],
            dados_paciente['nascimento'], dados_paciente['convenio'],
            timestamp, timestamp
        ]
        worksheet.append_row(nova_linha)
        invalidar_cache()
        return True
    except Exception as e:
        print(f"❌ Erro ao cadastrar paciente: {e}")
        return False

def editar_paciente(nome_original, novos_dados):
    try:
        worksheet = get_worksheet(ABA_PACIENTES)
        if not worksheet: return False

        celula = worksheet.find(nome_original)
        if not celula: return False

        dados_antigos = worksheet.row_values(celula.row)
        data_cadastro = dados_antigos[11] if len(dados_antigos) > 11 else ""
        
        timestamp_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # CORREÇÃO: Monta a linha com TODOS os campos na ordem correta
        linha_atualizada = [
            novos_dados['nome'], novos_dados['telefone'], novos_dados['cpf'],
            novos_dados['rg'], novos_dados['cep'], novos_dados['endereco'],
            novos_dados['bairro'], novos_dados['cidade'], novos_dados['estado'],
            novos_dados['nascimento'], novos_dados['convenio'],
            data_cadastro, timestamp_atual
        ]
        
        # Atualiza a linha inteira (A até M são 13 colunas)
        worksheet.update(f'A{celula.row}:M{celula.row}', [linha_atualizada])
        invalidar_cache()
        return True
    except Exception as e:
        print(f"❌ Erro ao editar paciente: {e}")
        return False

def excluir_paciente(nome_paciente):
    # ... (esta função não precisa de mudanças, mas é bom confirmar que ela chama invalidar_cache()) ...
    sucesso = False
    try:
        worksheet = get_worksheet(ABA_PACIENTES)
        if worksheet:
            celula = worksheet.find(nome_paciente)
            if celula:
                worksheet.delete_rows(celula.row)
                sucesso = True
    except Exception as e:
        print(f"❌ Erro ao excluir paciente: {e}")
    if sucesso:
        invalidar_cache()
    return sucesso
    
def listar_terapeutas():
    # ... (esta função não precisa de mudanças) ...
    worksheet = get_worksheet("Terapeutas")
    if not worksheet: return []
    return worksheet.col_values(1)[1:]