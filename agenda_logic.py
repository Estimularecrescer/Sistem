import sheets_client
from datetime import datetime

ABA_AGENDAMENTOS = "Agendamentos"

def get_agendamentos_worksheet():
    """Helper para pegar o objeto da aba de agendamentos."""
    spreadsheet = sheets_client.get_spreadsheet()
    if spreadsheet:
        return spreadsheet.worksheet(ABA_AGENDAMENTOS)
    return None

def criar_agendamento(terapeuta, paciente, data, hora_inicio):
    """Adiciona uma nova linha com os dados do agendamento na planilha."""
    try:
        worksheet = get_agendamentos_worksheet()
        if not worksheet:
            return False

        id_agendamento = int(datetime.now().timestamp())

        nova_linha = [
            id_agendamento,
            terapeuta,
            paciente,
            data,
            hora_inicio,
            "Marcado" 
        ]

        worksheet.append_row(nova_linha)
        print(f"✅ Agendamento para '{paciente}' criado com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar agendamento na planilha: {e}")
        return False

def listar_agendamentos_por_dia(data_str):
    """Retorna uma lista de todos os agendamentos de um dia específico."""
    try:
        worksheet = get_agendamentos_worksheet()
        if not worksheet:
            return []

        todos_agendamentos = worksheet.get_all_records()

        agendamentos_do_dia = [
            ag for ag in todos_agendamentos if ag.get("Data") == data_str
        ]

        agendamentos_do_dia.sort(key=lambda x: x.get("Hora_Inicio", ""))

        return agendamentos_do_dia
    except Exception as e:
        print(f"❌ Erro ao listar agendamentos: {e}")
        return []