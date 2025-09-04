from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCalendarWidget, 
    QListWidget, QPushButton, QLabel
)
from PySide6.QtCore import QDate
import agenda_logic
from agendamento_dialog import JanelaNovoAgendamento

class TelaAgenda(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        calendario_layout = QVBoxLayout()
        self.calendario = QCalendarWidget()
        self.calendario.setSelectedDate(QDate.currentDate())
        self.btn_novo_agendamento = QPushButton("➕ Novo Agendamento")
        calendario_layout.addWidget(QLabel("Selecione uma data:"))
        calendario_layout.addWidget(self.calendario)
        calendario_layout.addWidget(self.btn_novo_agendamento)

        lista_layout = QVBoxLayout()
        self.lista_agendamentos = QListWidget()
        lista_layout.addWidget(QLabel("Agendamentos para o dia selecionado:"))
        lista_layout.addWidget(self.lista_agendamentos)

        layout.addLayout(calendario_layout, 1)
        layout.addLayout(lista_layout, 2)   

        self.calendario.selectionChanged.connect(self.carregar_agendamentos_do_dia)
        self.btn_novo_agendamento.clicked.connect(self.abrir_janela_novo_agendamento)

        self.carregar_agendamentos_do_dia()

    def carregar_agendamentos_do_dia(self):
        self.lista_agendamentos.clear()
        data_selecionada = self.calendario.selectedDate().toString("dd/MM/yyyy")

        agendamentos = agenda_logic.listar_agendamentos_por_dia(data_selecionada)

        if agendamentos:
            for ag in agendamentos:
                texto = f"{ag.get('Hora_Inicio')} - {ag.get('Paciente')} com {ag.get('Terapeuta')}"
                self.lista_agendamentos.addItem(texto)
        else:
            self.lista_agendamentos.addItem("Nenhum agendamento para este dia.")

    def abrir_janela_novo_agendamento(self):
        data_selecionada = self.calendario.selectedDate().toString("dd/MM/yyyy")
        dialog = JanelaNovoAgendamento(data_selecionada, self)

        if dialog.exec():
            self.carregar_agendamentos_do_dia()