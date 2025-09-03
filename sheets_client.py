import gspread

CREDENTIALS_FILE = 'credentials.json'

SPREADSHEET_NAME = 'BancoDeDados_Clinica'

def get_spreadsheet():
    """Autentica e retorna o objeto da planilha principal."""
    try:
        gc = gspread.service_account(filename=CREDENTIALS_FILE)
        spreadsheet = gc.open(SPREADSHEET_NAME)
        print("Conexão com a planilha estabelecida.")
        return spreadsheet
    except FileNotFoundError:
        print(f"ERRO: Arquivo de credenciais '{CREDENTIALS_FILE}' não encontrado.")
        return None
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"ERRO: Planilha '{SPREADSHEET_NAME}' não encontrada.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado na conexão: {e}")
        return None