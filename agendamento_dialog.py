from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QFormLayout, QVBoxLayout, 
    QMessageBox, QComboBox, QTimeEdit
)
from PySide6.QtCore import QTime
import pacientes_logic
import agenda_logic
import google_calendar_client
from datetime import datetime

class JanelaNovoAgendamento(QDialog):
    def __init__(self, data_selecionada, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Agendamento")
        self.data_selecionada = data_selecionada 
        layout = QFormLayout(self)

        self.combo_pacientes = QComboBox()
        self.combo_terapeutas = QComboBox()
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(9, 0)) 

        self.carregar_dados_dropdown()

        layout.addRow(QLabel(f"Data: {self.data_selecionada}"), None)
        layout.addRow(QLabel("Paciente:"), self.combo_pacientes)
        layout.addRow(QLabel("Terapeuta:"), self.combo_terapeutas)
        layout.addRow(QLabel("Horário:"), self.time_edit)

        self.btn_salvar = QPushButton("Salvar Agendamento")
        layout.addWidget(self.btn_salvar)

        self.btn_salvar.clicked.connect(self.salvar_agendamento)

    def carregar_dados_dropdown(self):
        pacientes = pacientes_logic.listar_pacientes()
        for paciente in pacientes:
            self.combo_pacientes.addItem(paciente.get("Nome"))

        terapeutas = pacientes_logic.listar_terapeutas()
        for terapeuta in terapeutas:
            self.combo_terapeutas.addItem(terapeuta)

    def salvar_agendamento(self):
        paciente = self.combo_pacientes.currentText()
        terapeuta = self.combo_terapeutas.currentText()
        hora_inicio = self.time_edit.time().toString("HH:mm")

        sucesso_sheets = agenda_logic.criar_agendamento(
            terapeuta, paciente, self.data_selecionada, hora_inicio
        )

        if sucesso_sheets:
            QMessageBox.information(self, "Sucesso", "Agendamento salvo na planilha com sucesso!")

            try:
                service = google_calendar_client.get_calendar_service()
                if service:
                    data_hora_inicio_str = f"{self.data_selecionada} {hora_inicio}"
                    inicio_dt = datetime.strptime(data_hora_inicio_str, "%d/%m/%Y %H:%M")
                    fim_dt = inicio_dt + timedelta(hours=1) 

                    detalhes_evento = {
                        "nome_paciente": paciente,
                        "nome_terapeuta": terapeuta,
                        "data_hora_inicio": inicio_dt,
                        "data_hora_fim": fim_dt
                    }
                    google_calendar_client.criar_evento(service, detalhes_evento)
            except Exception as e:
                QMessageBox.warning(self, "Aviso", f"Agendamento salvo na planilha, mas falhou ao sincronizar com Google Calendar: {e}")

            self.accept() # Fecha a janela
        else:
            QMessageBox.critical(self, "Erro", "Não foi possível salvar o agendamento na planilha.")