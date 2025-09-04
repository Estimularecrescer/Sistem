import google_calendar_client
from datetime import datetime, timedelta

def main():
    print("--- INICIANDO TESTE DE INTEGRAÇÃO COM GOOGLE CALENDAR ---")

    service = google_calendar_client.get_calendar_service()

    if service:
        agora = datetime.now().astimezone() 
        inicio = agora + timedelta(hours=1)
        fim = inicio + timedelta(minutes=45)

        detalhes_exemplo = {
            "nome_paciente": "Paciente Teste",
            "nome_terapeuta": "Dra. Ana",
            "data_hora_inicio": inicio,
            "data_hora_fim": fim
        }

        print(f"\nTentando criar evento para '{detalhes_exemplo['nome_paciente']}' às {inicio.strftime('%H:%M')}...")

        google_calendar_client.criar_evento(service, detalhes_exemplo)
    else:
        print("\nNão foi possível obter o serviço da agenda. Teste falhou.")

    print("\n--- TESTE FINALIZADO ---")

if __name__ == "__main__":
    main()