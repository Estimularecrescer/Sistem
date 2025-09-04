import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """
    Autentica com a API do Google Calendar e retorna um objeto 'service'.
    Lida com o fluxo de login OAuth 2.0.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        print("✅ Conexão com o Google Calendar estabelecida.")
        return service
    except HttpError as error:
        print(f"❌ Ocorreu um erro na conexão com a API do Calendar: {error}")
        return None


def criar_evento(service, detalhes_agendamento):
    """Cria um evento na agenda principal do usuário autenticado."""
    
    
    evento = {
      'summary': f'Consulta: {detalhes_agendamento["nome_paciente"]}',
      'location': 'Clínica Estimular & Crescer',
      'description': f'Agendamento com o terapeuta {detalhes_agendamento["nome_terapeuta"]}.',
      'start': {
        'dateTime': detalhes_agendamento["data_hora_inicio"].isoformat(),
        'timeZone': 'America/Sao_Paulo',
      },
      'end': {
        'dateTime': detalhes_agendamento["data_hora_fim"].isoformat(),
        'timeZone': 'America/Sao_Paulo',
      },
      'reminders': { 'useDefault': True },
    }

    try:
        evento_criado = service.events().insert(calendarId='primary', body=evento).execute()
        print(f"✅ Evento criado na Agenda do Google: {evento_criado.get('htmlLink')}")
        return True
    except HttpError as error:
        print(f"❌ Ocorreu um erro ao criar o evento: {error}")
        return False